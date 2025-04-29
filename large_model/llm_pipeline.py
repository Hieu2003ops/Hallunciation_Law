import os
from dotenv import load_dotenv

# Gemini (Google GenAI) imports
import google.generativeai as genai

# Together AI imports
from together import Together

# --- Load environment ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY not set in .env")

# --- Gemini setup (using genai directly) ---
genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_PROMPT = """
Bạn là một trợ lý pháp lý chuyên gia về Luật Kinh tế Việt Nam, hoạt động như một agent tư vấn pháp lý.
Nhiệm vụ của bạn là:
1. Phân tích cẩn thận câu hỏi dựa trên các văn bản pháp lý, điều khoản cụ thể và các dẫn chứng hiện hành.
4. Đưa ra các ví dụ minh họa cụ thể khi cần thiết.
5. Tổng hợp và tóm tắt các thông tin, sau đó trả lời câu hỏi một cách rõ ràng, logic và chi tiết.
6. Nếu cần, hãy chỉ ra những điểm mâu thuẫn hoặc các vấn đề còn tồn tại trong quy định.
7. Trình bày câu trả lời của bạn theo cấu trúc rõ ràng, chia thành các đoạn với tiêu đề phụ, dẫn chứng cụ thể và giải thích chi tiết.

Câu hỏi: {query}

Trước khi trả lời, hãy suy nghĩ kỹ và phân tích các khía cạnh của câu hỏi.
Trả lời:
"""

def run_gemini_only(query: str) -> str:
    prompt = GEMINI_PROMPT.format(query=query)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text

# --- Meta-Llama (Together AI) setup ---
together = Together(api_key=TOGETHER_API_KEY)
LLAMA_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

def run_llama_only(query: str) -> str:
    # Chỉ gửi trực tiếp câu hỏi đến LLaMA mà không sử dụng prompt template
    completion = together.chat.completions.create(
        model=LLAMA_MODEL,
        messages=[{"role": "user", "content": query}],
        stream=False
    )
    return completion.choices[0].message.content

# if __name__ == "__main__":
#     test_query = "Theo luật trọng tài thương mại, trọng tài nước ngoài là gì?"
    
#     print("=== Kết quả GEMINI: ===")
#     print(run_gemini_only(test_query))
    
#     print("\n=== Kết quả LLaMA: ===")
#     print(run_llama_only(test_query))