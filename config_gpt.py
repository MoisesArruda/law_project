#%%
import os
import glob
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory,FileChatMessageHistory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

###### Configurar LLM_Chat e Embeddings ######

class GPTConfig:

    """
    Classe para configurar os objetos do AzureChatOpenAI e OpenAIEmbeddings para serem utilizados.
    
    Attributes:
        openai_api_base (str): A URL base da API do OpenAI.
        openai_api_version (str): A versão da API do OpenAI.
        openai_api_key (str): A chave da API do OpenAI.
        openai_api_type (str): O tipo da API do OpenAI.
        deployment_name (str): O nome do deployment da API do OpenAI.
        temperature (float): O valor da temperatura para determinar o comportamento da resposta, por padrão é 0.0.
        chunk_size (int): O tamanho do chunk para o OpenAIEmbeddings.
    """
    def __init__(self):
        self.openai_api_base = os.getenv("OPENAI_API_BASE")
        self.openai_api_version = os.getenv("OPENAI_API_VERSION")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api_type = os.getenv("OPENAI_API_TYPE")
        self.deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.deployment = os.getenv("EMBEDDING_DEPLOYMENT_NAME")

    def create_chat(self,t=0.1):
        """
        Configura os objetos do AzureChatOpenAI para serem utilizados.

        Returns:
            AzureChatOpenAI: O objeto de AzureChatOpenAi configurado.
        """
        return AzureChatOpenAI(
            openai_api_base=self.openai_api_base,
                openai_api_version=self.openai_api_version,
                openai_api_key=self.openai_api_key,
                openai_api_type=self.openai_api_type,
                deployment_name=self.deployment_name,
                temperature=t,
        )
    
    def create_embeddings(self,chunk_size=1):
        """
        Configura os objetos do OpenAIEmbeddings para serem utilizados.

        Returns:
            OpenAIEmbeddings: O objeto de OpenAIEmbeddings configurado.
        """
        return OpenAIEmbeddings(
            deployment=self.deployment,
            chunk_size=chunk_size
            )



###### Prompt e leitura arquivo ######
    
class Prompt:
    """
    Classe para configurar o prompt e em sequência realizar o armazenamento
    do documento que será utilizado para realizar a busca.
    """
    def __init__(self):
        
        self.prompt=None

    def create_prompt(self):
        
        """Cria o prompt a partir do template."""  
        template = """Responda sempre em português. Você ira receber um texto de um processo judicial.\n
                Sua funcao é auxiliar o advogado e melhorar ou modificar adequadamente o texto respeitando o contexto judicial da ocasião .
        Chat_history = {chat_history}
        Human: {query}
        Answer:"""

        prompt = PromptTemplate(template=template,input_variables=['chat_history','query'])
        self.prompt=prompt
        return self.prompt
    

class Memory():

    def __init__(self):

        self.memory = None


    def input_memory(self,query):

        self.memory = ConversationBufferMemory(
            #chat_memory = FileChatMessageHistory(file_path="historic_json/messages.json"),
            memory_key="chat_history",
            input_key="query",
            return_messages=True
        )

        return self.memory