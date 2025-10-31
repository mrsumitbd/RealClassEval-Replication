from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pinecone import Pinecone, ServerlessSpec
from uuid import uuid4
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import Docx2txtLoader

class LegalDocumentsVectorStore:

    def __init__(self, legal_documents, embeddings, index_name='legal-documents-index'):
        self.embeddings = embeddings
        self.index_name = index_name
        self.full_legal_documents = {}
        self.legal_documents = self.get_splitted_legal_documents(legal_documents)
        self.vector_store = self.initialize_vector_store()

    def get_splitted_legal_documents(self, legal_documents):
        docs = []
        for path_legal_document in legal_documents:
            loader = Docx2txtLoader(path_legal_document)
            text = loader.load()
            self.full_legal_documents[path_legal_document] = text
            doc = RecursiveCharacterTextSplitter(separators=['\n\n'], chunk_size=700, chunk_overlap=50).split_documents(text)
            docs.extend(doc)
        return docs

    def initialize_vector_store(self):
        pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
        try:
            pc.create_index(name=self.index_name, metric='cosine', dimension=768, spec=ServerlessSpec(cloud='aws', region='us-east-1'))
        except Exception as e:
            print(f'Index already exists.')
        index = pc.Index(self.index_name)
        return PineconeVectorStore(index=index, embedding=self.embeddings)

    def get_vector_store(self):
        return self.vector_store

    def add_documents(self):
        self.uuids = [str(uuid4()) for _ in range(len(self.legal_documents))]
        self.vector_store.add_documents(documents=self.legal_documents, ids=self.uuids)

    def delete_documents(self):
        self.vector_store.delete(ids=self.uuids)

    def get_document_text(self, path):
        return self.full_legal_documents[path]

    def get_all_documents(self):
        return self.full_legal_documents