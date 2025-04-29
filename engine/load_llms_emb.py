import os
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load biến môi trường từ file .env
load_dotenv()

# Lấy các key từ file .env
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY not found in .env!")

# Khởi tạo LLM (ChatTogether)
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo",                  
                top_p=1.0,                   
                seed=42,   
                verbose= False)

#meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo


# Khởi tạo embedding model
embd = HuggingFaceEmbeddings(model_name="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
