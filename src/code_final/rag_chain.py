import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.document_loaders import DataFrameLoader
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from uuid import uuid4

load_dotenv()

OPENAI_API_KEY = "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"


class create_rag_chain:

    def __init__(self,
                 db_path,
                 openai_key,
                 top_k=10,
                 embedding_model="text-embedding-ada-002"):

        self.df_docs = pd.read_parquet(db_path)
        self.client = OpenAI(api_key=openai_key)
        self.embedding_model = embedding_model
        self.top_k = top_k

        self.llm = ChatOpenAI(model="gpt-4o-mini",
                              temperature=0.05,
                              api_key=OPENAI_API_KEY)

        system_prompt = """
                    You are a highly trained virtual assistant specialized in providing accurate, professional support for banking-related queries.
                    Use only the information provided in the context to answer questions. Do not reference or infer details from external sources.
                    If the necessary information is absent from the context, politely inform the user that you do not know or that the information is unavailable.
                    Keep responses concise and relevant, ensuring clarity in a maximum of five sentences.
                    Always maintain a polite, professional, and helpful tone, focusing on delivering precise, clear, and customer-centric answers.
                    If the inquiry relates to banking services such as account management, transactions, loans, fees, or policies, refer only to the context, avoiding general financial advice unless it is explicitly supported by the context provided.
                    For questions involving specific terms, phrases, or data in Latin, convert them into Cyrillic and interpret them using the context to provide the most accurate response.
                    Respond in the same language as the user's inquiry to ensure a seamless communication experience.
                    When the user greets you (e.g., "hi," "hello," "сайн уу," "сайн байна уу"), respond appropriately with a polite greeting, using the same language.
                
                    Always list the sources exactly as they appear in the context provided.
                    
                    Context: {context}
                    Question: {question}
                
                    Answer: [Provide your concise answer here based on the context.]
                    Sources: [List only the sources from the context used for your answer.]

               """

        self.prompt = ChatPromptTemplate.from_template(system_prompt)

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        emb = self.client.embeddings.create(input=[text],
                                            model=self.embedding_model).data[0].embedding

        return emb

    def get_topk_context(self, query):
        emb = self.get_embedding(query)
        self.df_docs['similarity'] = self.df_docs['embeds'].apply(lambda x:
                                                                  cosine_similarity([x],
                                                                                    [emb])[0][0])

        top_k = self.df_docs.loc[self.df_docs['similarity'] > 0.0].nlargest(self.top_k, 'similarity')

        return top_k[["text", "title", "source"]]

    @staticmethod
    def format_docs(docs):
        formatted_docs = [
            f"Content: {doc.page_content}\nSource: {doc.metadata['source']}"
            for doc in docs
        ]
        return "\n\n".join(formatted_docs)

    def get_response(self, query):

        top_k = self.get_topk_context(query)
        relevant_docs = [
            Document(page_content=row['text'], metadata={'source': row['source']})
            for _, row in top_k.iterrows()
        ]

        if relevant_docs:
            formatted_context = self.format_docs(relevant_docs)
            messages = self.prompt.format_messages(context=formatted_context,
                                                   question=query)

            response = self.llm.invoke(messages)
            return response.content
        else:
            return "I'm sorry, I couldn't find any relevant documents for your query."

    def handle_query(self, query):
        """Main function to process a query and return the chatbot's response."""
        try:
            return self.get_response(query)
        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"
