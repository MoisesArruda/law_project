
from dotenv import load_dotenv
import os
import json
from langchain.chains import LLMChain
from config_gpt import GPTConfig,Prompt,Memory
import boto3
load_dotenv()


def gpt_response(query=None):
     
    llm_chat = GPTConfig().create_chat()
    prompt = Prompt().create_prompt()
    memory = Memory().input_memory(query)
    llm_chain = LLMChain(llm=llm_chat,prompt=prompt,memory=memory,verbose=True)
    response = llm_chain.run(query=query,memory=memory)

    return response


def bedrock_summarizacao(userInput):
    
    bedrock=boto3.client(
                    service_name="bedrock-runtime", 
                    region_name='us-east-1',
                    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
                                )
    
    template = """Responda sempre em português. Sua função é summarizar este texto de forma que os principais pontos sejam abordados e o entendimento seja claro    
    Texto: {Texto}"""
    prompt_final = template.replace("{Texto}",userInput)

    body = {"prompt": prompt_final,"temperature": 0.0,"max_tokens":3000}
    model_id= "mistral.mistral-7b-instruct-v0:2"

    response = bedrock.invoke_model(modelId=model_id, body=json.dumps(body))
    response_body = json.loads(response.get('body').read())
    resp =  response_body['outputs'][0]['text']

    return resp

def bedrock_classificacao(userInput):

    bedrock=boto3.client(
                    service_name="bedrock-runtime", 
                    region_name='us-east-1',
                    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
                                )
    
    template = """Responda em português. Faca uma resposta objetiva, Voce vai receber uma texto de defesa de um advogado para seu cliente.\n    Sua funcao é apenas CLASSIFICAR o conteudo do texto de acordo com as seguintes opçoes e retornar APENAS um dos seguintes: \n        'Pensão Alimenticia'\n        'Guarda Compartilhada'\n        'Guarda Unilateral'\n  'Regulamentação de visitar'\n
Não é necessário retornar uma explicação, um resumo ou algo relacionado, apenas a classificação"""

    body = {"prompt": template,"temperature": 0.0}
    model_id= "mistral.mistral-7b-instruct-v0:2"

    response = bedrock.invoke_model(modelId=model_id, body=json.dumps(body))
    response_body = json.loads(response.get('body').read())
    form =  response_body['outputs'][0]['text']
    
    return form

if __name__ == "__main__":

    llm = bedrock_classificacao("A Requerente, em observância ao art. 319, VII do Código de processo civil, opta pelarealização da audiência de conciliação uma vez que se trata de matéria envolvendomenor, razão pela qual se faz necessário empreender todos os esforços possíveis amanter o melhor interesse da criança.II – DOS FATOSA Requerente é avó materna de MIGUEL VERNIZZI ARRUDA, menor impúbere, 08 (oito)anos de idade, nascido em 29/09/2015, e sempre cuidou da criança, juntamente comsua filha Barbara Beatriz que é a genitora do menor.Insta frisar que a Requerente possui sentimento de mãe pela criança, vez que sempreacompanhou a filha nos exames de pré-natal/ultrassonografia, tanto é que a Autora foia primeira pessoa a pegar o menor no colo quando este nasceu.Além do mais, modificou todo seu apartamento para receber a criança e dar todosuporte que esta necessitaria, posteriormente mudou de casa para que a criança tivessemais espaço para crescer e se desenvolver.Para conferir o original, acesse o site https://esaj.tjsp.jus.br/pastadigital/pg/abrirConferenciaDocumento.do, informe o processo 1018834-71.2023.8.26.0020 e código ynyO6Xal.Este documento é cópia do original, assinado digital")
    print(llm)
#db = gpt_input()
#print(gpt_anwser("O que é o Docker?",db))