# main.py (FastAPI)
from fastapi import FastAPI
from pydantic import BaseModel
from engine.pipeline import run_full_pipeline  # Import hàm chạy pipeline
from large_model.llm_pipeline import run_llama_only,run_gemini_only
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# Khởi tạo FastAPI app
app = FastAPI()

# Cho phép CORS từ localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # hoặc ["*"] nếu bạn muốn mở rộng
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Định nghĩa schema cho request input
class QueryRequest(BaseModel):
    query: str  # Câu hỏi từ người dùng

# Endpoint nhận câu hỏi và trả lời qua pipeline
@app.post("/rag")
async def ask_query(request: QueryRequest):
    query = request.query
    print(f"Received query: {query}")  # Add debug statement here
    result = run_full_pipeline(query)
    print(f"Pipeline result: {result}")  # Debug result here
    return {"result": result}

@app.post("/gemini")
async def gemini_query(request: QueryRequest):
    query = request.query
    print(f"Received query: {query}")  # Add debug statement here
    result = run_gemini_only(query)
    print(f"Pipeline result: {result}")  # Debug result here
    return {"result": result}

@app.post("/meta_llama")
async def meta_llama_query(request: QueryRequest):
    query = request.query
    print(f"Received query: {query}")  # Add debug statement here
    result = run_llama_only(query)
    print(f"Pipeline result: {result}")  # Debug result here
    return {"result": result}


if __name__ == "__main__":
    # Chạy Uvicorn ngay trong file main.py
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)
