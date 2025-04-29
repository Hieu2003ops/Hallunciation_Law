from engine.load_hybrid_retrieval import get_hybrid_retriever
from engine.load_llms_emb import llm, embd
from engine.prompting import prompt_law
from engine.tavily_search import get_tavily_results
from engine.google_serper_search import get_google_serper_results

def run_full_pipeline(query: str) -> str:
    # --- PHẦN I: RAG Pipeline ---
    # Sử dụng hybrid_retriever để lấy tài liệu liên quan
    retriever = get_hybrid_retriever()
    retrieved_docs = retriever.invoke(query)
    retrieved_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # # Sử dụng prompt template và LLM để lấy câu trả lời từ văn bản pháp luật
    # final_prompt = prompt_law.format(retrieved_context=retrieved_context, query=query)
    # response = llm.invoke(final_prompt)
    # raw = response.content

    # Chạy LLMChain, sẽ chỉ trả về output (thường là phần assistant.content)
    raw = prompt_law.run(
        retrieved_context=retrieved_context,
        query=query
    )

    # --- Post-process: tách chỉ phần trả lời ---
    marker = "### 📝 Trả lời:"
    if marker in raw:
        rag_answer = raw.split(marker, 1)[1].strip()
    else:
        rag_answer = raw.strip()

    # --- Chèn greeting vào đầu ---
    greeting = (
        f"Chào bạn,\n"
        f"Tôi là trợ lý pháp lý chuyên về Luật Kinh tế Việt Nam.\n\n"
        f"Sau đây mình sẽ trả lời câu hỏi: \"{query}\"\n\n"
    )
    rag_answer = greeting + rag_answer
    rag_answer = rag_answer.replace("\nđ)", "\ne)")

    # --- PHẦN II: Công cụ tìm kiếm bổ sung ---
    # Lấy kết quả từ Tavily Search (đã định dạng trong module tavily_search)
    # tavily_output = get_tavily_results(query)
    
    # Lấy kết quả từ Google Serper Search (đã định dạng trong module google_serper_search)
    serper_output = get_google_serper_results(query)

    # Tổng hợp output cuối cùng theo định dạng yêu cầu
    full_output = f"""
==============================
🎯 **PHẦN I: Phân tích từ văn bản pháp luật (RAG pipeline):**

{rag_answer}

==============================
🧭 **PHẦN II: Các nguồn thông tin bổ sung từ công cụ tìm kiếm:**

--- Tavily # tavily_output ---


--- Google Serper (Tin tức) ---
{serper_output}

==============================
""".strip()
    return full_output
