import os
from dotenv import load_dotenv
from langchain.vectorstores import ElasticsearchStore
from engine.load_llms_emb import embd  # Import embedding model từ file load_llms_embedding.py

# Nạp biến môi trường
load_dotenv()

# Bắt buộc phải có ELASTICSEARCH_URL và ES_INDEX trong .env
# es_url = os.getenv("ELASTICSEARCH_URL")

# index_name = os.getenv("ES_INDEX")


index_name = "laws"
text_field = "text"
es_url     = "http://localhost:9200" 

# 2. Khởi tạo vector store (dùng trực tiếp URL)
vector_store = ElasticsearchStore(
    es_url=es_url,
    index_name=index_name,
    embedding=embd,
)

# count = vector_store.client.count(index=index_name)["count"]
# print(f"Số lượng tài liệu trong vector store: {count}")

def get_vector_store():
    return vector_store