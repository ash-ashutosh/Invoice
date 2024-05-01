from streamlit_chat import message
import streamlit as st

from langchain import FAISS, LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import easyocr

# initialize reader
reader = easyocr.Reader(['en'], gpu=False)

openai_api_key = os.getenv("OPENAI_API_KEY")

# Create the embeddings object
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# *********************** Utils ***********************
def create_db_from_text(file):
    text = reader.readtext(file, detail=0)
    description = ' '.join([str(elem) for elem in text])

    document = Document(page_content=description)
    documents = [document]

    db = FAISS.from_documents(documents, embeddings)

    return db

def get_response_from_query(db, query, openai_api_key):
    documents = db.similarity_search(query, k=1)
    content = " ".join([d.page_content for d in documents])

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9, openai_api_key=openai_api_key)

    prompt_template = """
        You are a helpful assistant that that can answer questions about invoices based on the ocr extracted text based on easyocr: {documents}

        When you are answering respect the following rules:
        - Only use the factual information from the description to answer the question.
        - Do not use any information that is not in the text.
        - Do not use your own knowledge to answer the question.
        - If you feel like you don't have enough information to answer the question do not elaborate and directly say "I don't know",  but keep answering with language that the customer used in the question.
        - always answer short and precise
        - dont mention currencies 
        """

    system_message_prompt = SystemMessagePromptTemplate.from_template(prompt_template)

    user_template = "Answer the following question: {question}"
    user_message_prompt = HumanMessagePromptTemplate.from_template(user_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, user_message_prompt])

    chain = LLMChain(llm=llm, prompt=chat_prompt)

    resp = chain.run(question=query, documents=content)
    resp = resp.replace("\n", "")

    return resp

def generate_response(query, db, openai_api_key):
    res = get_response_from_query(db, query, openai_api_key)
    return res


# *********************** Streamlit App ***********************
st.title("Welcome to Invoice Assistant Created By Ashutosh")

uploaded_file = st.file_uploader("Choose an invoice...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    invoice = uploaded_file.read()
    db = create_db_from_text(invoice)
    st.image(invoice, width=300, caption='Uploaded Invoice')

    if 'question' not in st.session_state:
        st.session_state['question'] = []

    if 'answer' not in st.session_state:
        st.session_state['answer'] = []

    question = st.text_input("Enter a question : ")

    if st.button("Clear chat"):
        question = ""
        st.session_state['question'] = []
        st.session_state['answer'] = []

    if question:
        response = generate_response(question, db=db, openai_api_key=openai_api_key)

        st.session_state['question'].append(question)
        st.session_state['answer'].append(response)

    if st.session_state['answer']:
        for i in range(len(st.session_state['answer'])):
            message(st.session_state['question'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["answer"][i], key=str(i))
