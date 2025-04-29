
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
"""

# 2. Human prompt: chèn retrieved_context + câu hỏi + hướng dẫn thực thi
human_template = """
### 📚 Thông tin pháp lý được truy xuất từ văn bản:
(Chỉ sử dụng phần này, tuyệt đối không suy diễn ngoài `retrieved_context`)
------------------------------------------------
{retrieved_context}

🔍 _LƯU Ý_: retrieved_context có thể là:
- Hoàn toàn đoạn văn (paragraph)
- Hoàn toàn bullet-list (dấu “-” hoặc “a), b), c)…)
- Hỗn hợp paragraph và bullet

**Bước 0 – Chuẩn hoá nội dung**  
- Tách riêng từng paragraph; nếu paragraph dài, **tóm tắt** mỗi đoạn thành một bullet ngắn (1–2 câu).  
- Giữ nguyên những dòng đã là bullet (dấu “-” hay “a), b), c)…”).  
- Kết quả thu được phải là một **bullet-list** (a), b), c)…).


------------------------------------------------

❓ **Câu hỏi pháp lý**:  
“{query}”

## 🛠️ Hướng dẫn 5 bước – PHẢI THỰC HIỆN ĐẦY ĐỦ:

**Bước 1 – Liệt kê vấn đề pháp lý (bullet a), b), c)…):**  
- Quét toàn bộ `retrieved_context` để xác định **tối thiểu 3** luận điểm chính.  
- Luôn dùng ký tự Latin: `a)`, `b)`, `c)`… (không sử dụng “đ)”, “ê)”, v.v.).  
- Với mỗi bullet, viết **ít nhất 2 câu** mô tả tại sao đó là vấn đề pháp lý quan trọng.

**Bước 2 – Trích dẫn NGUYÊN VĂN & GIẢI THÍCH:**  
- Dưới từng bullet, trích **nguyên văn** Điều/Khoản/Bộ luật từ `retrieved_context`.  
- Sau mỗi trích dẫn, viết **1 câu** giải thích ý nghĩa và phạm vi áp dụng của điều khoản đó.

**Bước 3 – Phân tích & ví dụ minh họa:**  
- Phân tích mục đích, ý nghĩa và tác động pháp lý (nhấn mạnh rủi ro & cơ hội cho doanh nghiệp).  
- Cho **1 ví dụ thực tiễn** cụ thể (câu ngắn 2–3 câu).

**Bước 4 – Góc nhìn đối lập (tuỳ chọn):**  
- Nếu có >1 phương án, nêu ưu/nhược điểm mỗi phương án, dùng bullet a), b)…  
- Nếu chỉ có 1, ghi “Không có góc nhìn đối lập.”

**Bước 5 – Tổng hợp kết luận:**  
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






