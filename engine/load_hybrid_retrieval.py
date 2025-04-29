import os
from dotenv import load_dotenv
from typing import Dict
from langchain_elasticsearch import ElasticsearchRetriever
from elasticsearch import Elasticsearch
from engine.load_llms_emb import embd ,llm
from engine.load_vectostore import get_vector_store


# Load biến môi trường
load_dotenv()

index_name = "laws"
text_field = "text"
es_url     = "http://localhost:9200" 

# --- Định nghĩa hàm hybrid_query ---
def hybrid_query(search_query: str) -> Dict:
    # Sử dụng embed_query để tạo vector cho truy vấn
    query_vector = embd.embed_query(search_query)
    return {
        "retriever": {
            "rrf": {  # Rank Reciprocal Fusion: kết hợp hai truy vấn theo kiểu "should"
                "retrievers": [
                    {  # Thành phần full text search: dùng match query trên trường "text"
                        "standard": {
                            "query": {
                                "match": {
                                    text_field: search_query
                                }
                            }
                        }
                    },
                    {  # Thành phần vector search: dùng knn query trên trường "embedding_field"
                        "knn": {
                            "field": "embedding_field",  # Điều chỉnh nếu mapping của bạn dùng tên khác
                            "query_vector": query_vector,
                            "k": 5,
                            "num_candidates": 10
                        }
                    }
                ]
            }
        }
    }


# 4. Khởi tạo retriever dùng client
hybrid_retriever = ElasticsearchRetriever.from_es_params(
    index_name=index_name,
    body_func=hybrid_query,
    content_field=text_field,
    url=es_url
)

# Hàm trả về retriever
def get_hybrid_retriever():
    return hybrid_retriever
