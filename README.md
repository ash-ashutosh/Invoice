# Invoice
This is project based on LLM
### 1. Introduction
The goal of this project was to develop an interactive Invoice Assistant using Streamlit, Langchain, and easyOCR technologies. This assistant allows users to upload an invoice image containing text and ask questions related to the invoice content. The system utilizes Langchain's capabilities in language modeling and information retrieval, integrated with easyOCR for text extraction from images, to generate responses to user queries about invoices.

### 2. Implementation Details
The project involved several key components and functionalities:

Text Extraction: The easyocr library was employed to extract text from uploaded invoice images. The extracted text was then processed to create a document database (db) using Langchain's FAISS module.
Question Answering with Language Models: Langchain's ChatOpenAI module, utilizing the GPT-3.5-turbo model from OpenAI, was used for question answering. The system generates responses based on the extracted text from the invoice image and user queries.
Interactive User Interface: Streamlit was utilized to create an intuitive user interface. Users can upload an invoice image, input questions related to the invoice content, and receive real-time responses from the Invoice Assistant.

### 3. Workflow
Upon uploading an invoice image, the system performs text extraction using easyocr. The extracted text is used to create a document database (db) for information retrieval. Users can then input questions about the invoice content via a text input field.

The system processes user questions using the Langchain-based question-answering pipeline (generate_response function). The response is generated based on the content extracted from the invoice image and the query posed by the user.

### 4. Features of the Streamlit App

File Uploader: Users can upload invoice images in common formats (e.g., png, jpg, jpeg).
Question Input: Users can enter questions related to the invoice content.
Interactive Chat Display: The app displays a chat-like interface showing user questions and corresponding answers in real-time.
Session Management: The app utilizes Streamlit's session state to maintain a history of user interactions (questions asked and responses received) during the session.
Clear Chat Button: Users can clear the chat history (i.e., reset questions and answers) with the click of a button.

### 5. Conclusion
In conclusion, the Invoice Assistant project successfully demonstrates the integration of image processing, natural language understanding, and interactive user interface technologies. The use of Langchain for language modeling and Streamlit for web-based application development enables a seamless and user-friendly experience for interacting with invoice content through textual queries. This project showcases the potential of combining advanced AI models with accessible web frameworks to build practical and efficient information retrieval systems.








