from fetchAWS import OPENAI_API_KEY
#from fetchLocal import OPENAI_API_KEY  # use this if importing from a local .env file
from svmmodel import predict_input
import time
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

#same path and collection name used to make the DB
persist_directory = 'chroma_db'
collection_name="my_collection"

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#establish db 
vectordb = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory=persist_directory
)

# set up retriever
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# set up prompt template

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert in linux resource management. you will recive inputs from the system and give great insights into what is going on
    as all as educate the use on what should be done if there is any need for concern.
    Context:
    {context}
    
    Question: 
    {question}
    
    Answer:"""
)

# to avoid the model rephrasing the question in its reponse
no_rephrase_prompt = PromptTemplate.from_template("{question}")

# set up conversational retrieval chain

llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])

conversation = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": custom_prompt},
    condense_question_prompt=no_rephrase_prompt
)

# start the conversation
while True:
    start_time = time.time()
    question = "system data: "
    
    for response in predict_input(interval=5):
        question += str(response) + "\n"  # add the response
        if time.time() - start_time >= 180:  # 3 minutes
            break
    
    answer = conversation.invoke({"question": question})
    #print(answer)
    print() 