from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_models import BedrockChat
from langchain.chains import ConversationalRetrievalChain

from langchain_community.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def get_llm():
        
    model_kwargs = { #anthropic
        "max_tokens": 512,
        "temperature": 0, 
        "top_k": 250, 
        "top_p": 1, 
        "stop_sequences": ["\n\nHuman:"] 
    }
    
    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0", #set the foundation model
        model_kwargs=model_kwargs) #configure the inference parameters
    
    return llm


def get_index(): 
    # Cria e retorna um armazenamento de vetores na memória para ser usado na aplicação
    
    embeddings = BedrockEmbeddings() # Cria um cliente de Embeddings Titan
    
    pdf_path = "data/Docker_para_desenvolvedores.pdf" 

    loader = PyPDFLoader(file_path=pdf_path) 
    
    text_splitter = RecursiveCharacterTextSplitter( 
        # Cria um divisor de texto
        separators=["\n\n", "\n", ".", " "], 
        # Divide os chunks em (1) parágrafo, (2) linha, (3) sentença ou (4) palavra, nesta ordem
        chunk_size=1000, 
        # Divide em chunks de 1000 caracteres usando os separadores acima
        chunk_overlap=100 
        # Número de caracteres que podem se sobrepor com o chunk anterior
    )
    
    index_creator = VectorstoreIndexCreator( 
        # Cria uma fábrica de armazenamento de vetores
        vectorstore_cls=FAISS, 
        # Usa um armazenamento de vetores na memória para fins de demonstração
        embedding=embeddings, #use Titan embeddings
        text_splitter=text_splitter,  # Usa o divisor de texto recursivo
    )
    
    index_from_loader = index_creator.from_loaders([loader]) # Cria um índice de armazenamento de vetores a partir do PDF carregado
    
    return index_from_loader  # Retorna o índice para ser armazenado em cache pela aplicação cliente


def get_memory(): #create memory for this chat session
    
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True) #Maintains a history of previous messages
    
    return memory


def get_rag_chat_response(input_text, memory, index):
    
    llm = get_llm()
    
    conversation_with_retrieval = ConversationalRetrievalChain.from_llm(llm, index.vectorstore.as_retriever(), memory=memory, verbose=True)
    
    chat_response = conversation_with_retrieval.invoke({"question": input_text}) # Passa a mensagem do usuário e o resumo para o modelo
    
    return chat_response['answer']

