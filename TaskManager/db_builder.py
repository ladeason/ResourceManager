from fetchAWS import OPENAI_API_KEY
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyMuPDFLoader  
import os

"""
sources used:
https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=03bf1bc2593fb000afeb8ecb48e7ece574504fb0
https://listengine.tuxfamily.org/lists.tuxfamily.org/cllfst/2009/09/pdfZ6yp2ADu48.pdf
https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=ab979c0d464975facbf97d10c920096f027bc164

"""

#gathering content from websites
loader = PyMuPDFLoader() #url would go into the webbase loader
docs = loader.load()

#Split content into chunks
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = text_splitter.split_documents(docs)

#establishing vector database
persist_directory = 'chroma_db'

embedding  = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding, collection_name="my_collection")

vectordb.add_documents(split_docs)
vectordb.persist()

print("Web content loaded, split, and stored in Chroma.")





