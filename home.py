from scrap import data_collection
import os
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.document_loaders import TextLoader




#this call the function from scrap module which helps to scrap data using selenium 
meta_data=data_collection()

#The data is then stored inside a text file 
with open('meta.txt', 'w') as file:
    file.write(meta_data)



#Defining all the required api keys
os.environ['HUGGINGFACEHUB_API_TOKEN']="123456"
groq_api_key="123456"

#defining the Embedding model
huggingface_embeddings = HuggingFaceHubEmbeddings(
    model="BAAI/bge-small-en-v1.5"
)

#Loading the llm model from groq which help to achive faster response
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

#Setting the prompt template
prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

#defining the embeding variable
embeddings=huggingface_embeddings

#loading the contents of the meta txt file that we have created
loader = TextLoader("meta.txt")
docs=loader.load()

text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=200) ## Chunk Creation
final_documents=text_splitter.split_documents(docs) #splitting
vectors=FAISS.from_documents(final_documents,embeddings) #vector embeddings

#initializing the prompt1 variable
prompt1=""
while(prompt1!='byebye'):
    prompt1=input("Enter Your Question From Doduments : ")
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response=retrieval_chain.invoke({'input':prompt1})
    print("Response : ",response['answer'])
print("Thank You ")
