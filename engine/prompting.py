
# engine/prompting.py

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from engine.load_llms_emb import llm

# 1. System prompt: định nghĩa vai trò, phạm vi chuyên môn
system_template = """
Bạn là một chuyên gia pháp lý hàng đầu, giảng viên Luật Kinh tế Việt Nam với nhiều năm kinh nghiệm.
Bạn am hiểu sâu về các bộ luật: Thương mại, Doanh nghiệp, Lao động, Thuế, Ngân hàng, Thương mại điện tử, Đầu tư…
Luôn đưa ra phân tích chính xác, dẫn chứng nguyên văn, và trình bày logic rõ ràng.
Bạn sẽ **suy nghĩ nội bộ** (ẩn chain-of-thought), và **không** xuất bất kỳ bước nào.  
Chỉ bắt đầu xuất **kết quả** từ phần “### 📝 Trả lời:”.
"""

# 2. Human prompt: chèn retrieved_context + câu hỏi + hướng dẫn thực thi
human_template = """

**🔔 BẮT BUỘC TUÂN THEO ĐỊNH DẠNG DƯỚI ĐÂY**  

### 📚 Thông tin pháp lý được truy xuất từ văn bản:
(Chỉ sử dụng phần này, tuyệt đối không suy diễn ngoài `retrieved_context`)
------------------------------------------------
{retrieved_context}

🔍 _LƯU Ý_: retrieved_context có thể là:
- Hoàn toàn đoạn văn (paragraph)
- Hoàn toàn bullet-list (dấu “-” hoặc “a), b), c)…)
- Hỗn hợp paragraph và bullet

**Bước 0 – Chuẩn hoá nội dung**  
- Tóm tắt paragraph dài thành bullet ngắn (1–2 câu).  
- Giữ nguyên bullet gốc.  
- Kết quả: bullet-list chuẩn Latin `a)`, `b)`, `c)`.  


------------------------------------------------

❓ **Câu hỏi pháp lý**:  
“{query}”

## 🛠️ Hướng dẫn 4 bước – PHẢI THỰC HIỆN ĐẦY ĐỦ:

**Bước 1 – Trích dẫn nguồn luật (tự động chia nhỏ bullet nếu trích dài)**  
- Liệt kê bullet Latin `a)`, `b)`, `c)…`, mỗi bullet gồm:
  - **Theo Điều X, Khoản Y**:  
    “<Nguyên văn Điều/Khoản>”  
    • Nếu nguyên văn chứa nhiều mục (a), b), …), hãy **tách xuống** thành bullet con:  
      - a) …  
      - b) …  

**Bước 2 – Giải thích học thuật & thực tiễn** n/n
2.1 **Giải thích học thuật**  
- Trình bày khái niệm, thuật ngữ, và cơ sở pháp lý một cách chuyên sâu cho **sinh viên luật** (2–3 câu).  

2.2 **Giải thích thực tiễn & Ví dụ**  n/n
- Nhấn mạnh **rủi ro** và **cơ hội** cho **doanh nghiệp** (1–2 câu).  
- Cho **1 ví dụ thực tiễn** cụ thể (2–3 câu).

**Bước 3 – Góc nhìn đối lập (tuỳ chọn):**n/n 
- Nếu có >1 phương án, nêu ưu/nhược điểm mỗi phương án, dùng bullet a), b)…  
- Nếu chỉ có 1, ghi “Không có góc nhìn đối lập.”

**Bước 4 – Tổng hợp kết luận:** n/n
- Dùng bullet Latin để liệt kê:  
  - **Kết luận cuối cùng**: …  
  - **Đề xuất/Khuyến nghị**: …  
  - **Lưu ý quan trọng**: …

🔔 **LƯU Ý**: _Không in lại hướng dẫn, chỉ xuất **answer** từ “### 📝 Trả lời:”_

### 📝 Trả lời:
"""

# 3. Kết hợp vào ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template),
])

# 4. Tạo chain
prompt_law = LLMChain(llm=llm, prompt=chat_prompt)






