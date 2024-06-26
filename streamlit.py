# Documentação completa pode ser encontrada aqui: https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/intermediate/bedrock-rag-chatbot

import streamlit as st
from front.vars import *
from response_chat import gpt_response,bedrock_summarizacao,bedrock_classificacao
from config_gpt import GPTConfig,Prompt,Memory
from aws.conn_bedrock import *
from langchain.chains import LLMChain

def configure_page_init():

    st.set_page_config(page_title="LexAssist.IA.",  page_icon="📋") #HTML title
    #variavel do plano de fundo da tela principal
    st.markdown(page_bg_img,unsafe_allow_html=True) 
    #variavel do plano de fundo da aba ajuda
    st.markdown(page_mk_bg_img,unsafe_allow_html=True) 
    # Definindo a cor de fundo e borda para st.session_state.messages
    st.markdown(page_pgt,unsafe_allow_html=True)
    #setando o fundo da aba ajuda e da página principal
    path = "data/logo-default-143x27.png"
    st.image(path,width=900)#, use_column_width=True)

    with st.sidebar:
        st.title('Informações e dicas de uso') #page title
        st.markdown("""<h2 style='font-size:15px;'>Eu sou a LexAssist.AI, a inteligência artificial treinada para responder perguntas e conferir informações sobre processos judiciais e ajudar advogados em suas tarefas.</h2>""", unsafe_allow_html=True)

        st.write('Created by [Moisés Arruda](https://www.linkedin.com/in/dataengineer-moisesarruda/) and [Leonardo Caldeira](https://www.linkedin.com/in/leonardo-caldeira-6033a1144/)')
        st.sidebar.divider() 
    st.title("LexAssist.IA ")

def glossary():

    with st.sidebar.expander("Manual de uso"):
        
        st.caption(":gray[ 1- Seja especifíco nas perguntas.]" )     
        st.caption(":gray[ 2- Evite perguntas fora de contexto.]" )    

    with st.sidebar.expander("Sugestões de perguntas"):
        st.caption(":gray[ 1-  Qual a classificação deste processo?]")
        st.caption(":gray[ 2- Faça um resumo desta petição!]")
        st.caption(":gray[ 3- Melhore este texto!]")
        st.caption(":gray[ 4- Quem são os individuos envolvidos neste processo?]")

    with st.sidebar.expander("Glossario"):    
        st.subheader("Link oficial para o glossario da setur:")
        st.caption(":gray[[Glossario](https://www.each.usp.br/turismo/livros/glossario_do_turismo_MTUR.pdf) 📝]")


def chat_history():

    if "messages" not in st.session_state.keys(): # Verifique de o histórico de mensagens ainda não foi criado.
        st.session_state.messages=[ # Inicie o histórico de mensagem.
            {"role":"assistant","content": "Olá! Como posso te ajudar?"}
    ]
        print(st.session_state.messages,": Inicio")

    for message in st.session_state.messages: # Loop pelo histórico de bate-papo
        with st.chat_message(message["role"]): # Renderiza uma linha de chat para a função determinada, contendo tudo no bloco with
                print(st.session_state.messages,": role")
                st.write(message["content"]) # Exibir o conteúdo do bate-papo


    user_prompt = st.chat_input() # Exiba uma caixa de pergunta

    if user_prompt is not None:
        st.session_state.messages.append( # Adicione a última mensagem para o histórico
            {"role":"user","content":user_prompt})
        print(st.session_state.messages,": user_prompt")
        with st.chat_message("user"): # Exiba uma mensagem de bate-papo do usuário
            st.write(user_prompt) # Mostre a última mensagem do usuário

    if st.session_state.messages[-1]["role"] != "assistant":
        print(st.session_state.messages,": -1")
        with st.chat_message("assistant"): # Mostre uma nova mensagem do bot
            with st.spinner("Loading..."):

                opcoes = ["formulacao","summarizacao","classificacao"]
                if user_prompt in opcoes[0]:

                    # st.write("Opcao formulação")
                    ai_response = gpt_response(query=user_prompt)
                    st.write(ai_response)
                    # st.session_state.messages.append({"role":"assistant","content":ai_response)
                    # return ai_response


                elif user_prompt in opcoes[1]:
                
                    # st.write("Opção summarizacão")
                    ai_response = bedrock_summarizacao(user_prompt)
                    st.write(ai_response)
                    # st.session_state.messages.append(ai_response)
                    # return ai_response
            
                elif user_prompt in opcoes[2]:  

                    #st.write("Opção classificacao")
                    ai_response = bedrock_classificacao(user_prompt)
                    st.write(ai_response)
                    # st.session_state.messages.append(ai_response)
                    # return ai_response



            # else:
            #     st.write("Sua opção não está correta, tente novamente!")

         

        new_ai_message = {"role":"assistant","content":ai_response}
        st.session_state.messages.append(new_ai_message)
        print(st.session_state.messages,": final")

if __name__ == "__main__":

    configure_page_init()
    glossary()
    chat_history()