from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

import os
import dotenv 
import google.generativeai as genai 
dotenv.load_dotenv(override=True)


# GLOBAL VARIABLES
genai.configure(api_key=os.getenv('LLM_API_KEY'))
os.environ['GOOGLE_API_KEY'] = os.getenv('LLM_API_KEY')
DATA_PATH = 'data/raw/'

# CLASS
class LLM:
    def __init__(self):
        pass 

    def connect(self, filepath):
        self.load_model()
        self.load_docs(filepath)

    def load_model(self, model_name: str = 'gemini-pro'):
        print('Load models...')
        self.model = ChatGoogleGenerativeAI(model = model_name)
    
    def load_docs(self, filepath: str):
        print('Load documents...')
        loader = CSVLoader(DATA_PATH + filepath)
        self.documents = loader.load()

    def ask(self, questions: str):
        # Buat template
        template = """
        Anda adalah seorang project manager. Dari data berikut {docs},
        """
        template += questions 

        # Buat prompt 
        prompt = ChatPromptTemplate.from_template(template)

        # Buat chain
        output_parser = StrOutputParser()
        chain = prompt | self.model | output_parser

        # Keluarkan answer
        answer = chain.invoke({
            'docs': self.documents
        })

        return answer
