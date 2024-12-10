from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# Vektör tabanı oluşturma
def create_vector_store(chunks):
    """
    Metin parçalarını vektör tabanına ekler.
    """
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

# Vektör tabanını sorgulama
def query_vector_store(vector_store, question):
    """
    Vektör tabanını sorgular ve bir yanıt döner.
    """
    llm = OpenAI(model="gpt-4")  # OpenAI GPT modelini kullan
    retriever = vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(question)
