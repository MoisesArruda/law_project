import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
import json
import os

## Bedrock Clients

def bedrock_llm():#llm_model):

    bedrock=boto3.client(service_name="bedrock-runtime",region_name='us-east-1')

    llm = Bedrock(verbose=True, client=bedrock)#,model_id=llm_model)

    return llm

def bedrock_embeddings(embedding_llm):

    bedrock=boto3.client(service_name="bedrock-runtime",region_name='us-east-1')
    
    bedrock_embeddings=BedrockEmbeddings(model_id=embedding_llm,client=bedrock)

    return bedrock_embeddings


def create_prompt_classificacao():

    """Cria o prompt a partir do template."""  
    template = """Responda SEMPRE em português. Faca uma resposta objetiva, Voce vai receber uma texto de defesa de um advogado para seu cliente.\n  
        Sua funcao é apenas CLASSIFICAR o conteudo do texto de acordo com as seguintes opçoes e retornar APENAS um dos seguintes: \n    
                'Pensão Alimenticia'\n        'Guarda Compartilhada'\n        'Guarda Unilateral'\n  'Regulamentação de visitar'\n
    Não é necessário retornar uma explicação, um resumo ou algo relacionado, apenas a classificação"
    Chat_history = {history}
    Human: {query}
    Answer:"""

    prompt = PromptTemplate(template=template,input_variables=['history','query'])
    return prompt



def create_prompt_summarizacao():

    """Cria o prompt a partir do template."""  
    template = """RResponda sempre em português. Sua função é summarizar este texto de forma que os principais pontos sejam abordados e o entendimento seja claro
    Chat_history = {history}
    Human: {query}
    Answer:"""

    prompt = PromptTemplate(template=template,input_variables=['history','query'])
    return prompt


def Memory():

    memory = ConversationBufferMemory(
            #chat_memory = FileChatMessageHistory(file_path="data/messages.json"),
            memory_key="history",
            return_messages=True
        )
    
    return memory

if __name__ == "__main__":
  
    bedrock=boto3.client(
                    service_name="bedrock-runtime", 
                    region_name='us-east-1',
                    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
                                )
    # conversation= ConversationChain(
    # llm=llm, verbose=False, memory=ConversationBufferMemory()) #memory_chain)

    template = """Responda sempre em português. Sua função é summarizar este texto de forma que os principais pontos sejam abordados e o entendimento seja claro
    Chat_history = {history}
    Human: {query}
    Answer:"""

    prompt = PromptTemplate(template=template,input_variables=['history','query'])


    body = {"prompt": template,"temperature": 0.0}
    model_id= "mistral.mistral-7b-instruct-v0:2"

    response = bedrock.invoke_model(modelId=model_id, body=json.dumps(body))
    response_body = json.loads(response.get('body').read())
    form =  response_body['outputs'][0]['text']
    print(form)




