# Documentação completa pode ser encontrada aqui: https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/intermediate/bedrock-rag-chatbot

import streamlit as st

from front.vars import *
from response_chat import gpt_response,bedrock_summarizacao,bedrock_classificacao
from config_gpt import GPTConfig,Prompt,Memory
from aws.conn_bedrock import *
from langchain.chains import LLMChain
import rag_chatbot_lib as glib #reference to local lib script

def configure_page_init():

    st.set_page_config(page_title="LexAssist.AI",  page_icon="📋") #HTML title
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
    st.title("LexAssist.AI ")

def glossary():

    with st.sidebar.expander("Manual de uso"):
        
        st.caption(":gray[ 1- Seja especifíco nas perguntas.]" )     
        st.caption(":gray[ 2- Evite perguntas fora de contexto.]" )    

    with st.sidebar.expander("Sugestões de perguntas"):
        st.caption(":gray[ 1-  Qual a classificação deste processo?]")
        st.caption(":gray[ 2- Faça um resumo desta petição!]")
        st.caption(":gray[ 3- Melhore este texto!]")
        st.caption(":gray[ 4- Quem são os individuos envolvidos neste processo?]")

    # with st.sidebar.expander("Glossario"):    
    #     st.subheader("Link oficial para o glossario da setur:")
    #     st.caption(":gray[[Glossario](https://www.each.usp.br/turismo/livros/glossario_do_turismo_MTUR.pdf) 📝]")


def chat_history():

    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True) #Maintains a history of previous messages

    if "messages" not in st.session_state: # Verifique de o histórico de mensagens ainda não foi criado.
        st.session_state.messages=[ # Inicie o histórico de mensagem.
            {"role":"assistant","content": """Olá! \n Escolha sua opção: \n
1 - Formulação \n
2 - Summarização \n
3 - Classificação"""}
    ]
        print(st.session_state.messages,": Inicio")

    if "llm_choice" not in st.session_state:
        st.session_state.llm_choice = None

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

        # Se a escolha do LLM ainda não foi feita, determine qual LLM usar
        if st.session_state.llm_choice is None:
            opcoes = ["Formulação","Summarização","Classificação"]
            if user_prompt in opcoes:
                st.session_state.llm_choice = user_prompt
                ai_response = f"Você optou pela opção de {user_prompt}, por favor, forneça seu texto."
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                with st.chat_message("assistant"):
                    st.write(ai_response)

            else:
                ai_response = "Opção inválida. Por favor, escolha entre: Formulação, Summarização, Classificação."
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                with st.chat_message("assistant"):
                    st.write(ai_response)
        else:
            # Chame a função de resposta apropriada com base na escolha do LLM
            if st.session_state.llm_choice == "Formulação":
                ai_response = gpt_response(user_prompt)
            elif st.session_state.llm_choice == "Summarização":
                ai_response = bedrock_summarizacao(user_prompt)
            elif st.session_state.llm_choice == "Classificação":
                ai_response = bedrock_classificacao(user_prompt)

            # Garantindo a imagem de robo
            with st.chat_message("assistant"):
                # Enviando a resposta para o front
                st.write(ai_response)
                # Armazenando a resposta no histórico
            st.session_state.messages.append({"role": "assistant", "content": ai_response})


if __name__ == "__main__":

    configure_page_init()
    glossary()
    chat_history()