from typing import List
import re

def format_tavily_result(raw_result: List[dict]) -> str:
    formatted = "📚 **KẾT QUẢ TÌM KIẾM:**\n\n"
    seen_urls = set()
    idx_counter = 1
    
    for item in raw_result:
        url = item.get("url", "Không có URL")
        # Bỏ qua mục trùng lặp
        if url in seen_urls:
            continue    
        seen_urls.add(url)
        
        content = item.get("content", "Không có nội dung").strip()
        
        # Xác định loại nguồn
        source_type = (
            "Nguồn chính thức"
            if any(domain in url for domain in ["phapluat", "hethongphapluat", "lawnet", "moj.gov", "quochoi.vn"])
            else "Báo chí/Tin tức"
        )
        
        # Xử lý nội dung để hiển thị đẹp hơn
        # Xóa khoảng trắng thừa
        content = re.sub(r'\s+', ' ', content)
        
        # Phân tách các điều khoản để dễ đọc
        content = re.sub(r'(Điều \d+\.)', r'\n\n\1', content)
        content = re.sub(r'(\d+\.)', r'\n\1', content)
        
        # Đảm bảo có dấu cách sau dấu chấm, phẩy
        content = re.sub(r'\.([A-Z])', r'. \1', content)
        content = re.sub(r'\,([A-Z])', r', \1', content)
        
        # Định dạng các đoạn văn bản
        paragraphs = re.split(r'\n{2,}', content)
        formatted_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                # Mỗi đoạn văn không quá dài
                if len(para) > 150:
                    sentences = re.split(r'(?<=[.!?])\s+', para)
                    current_paragraph = ""
                    
                    for sentence in sentences:
                        if len(current_paragraph) + len(sentence) <= 150:
                            current_paragraph += sentence + " "
                        else:
                            formatted_paragraphs.append(current_paragraph.strip())
                            current_paragraph = sentence + " "
                    
                    if current_paragraph.strip():
                        formatted_paragraphs.append(current_paragraph.strip())
                else:
                    formatted_paragraphs.append(para.strip())
        
        # Tạo nội dung đã định dạng
        formatted_content = "\n\n".join(formatted_paragraphs)
        
        # Giới hạn độ dài nếu quá dài
        if len(formatted_content) > 600:
            formatted_content = formatted_content[:600] + "..."
        
        # Tạo card hiển thị kết quả
        formatted += f"## {idx_counter}. {url.split('//')[1].split('/')[0]}\n\n"
        formatted += f"**Phân loại:** {source_type} 📑\n\n"
        formatted += f"**Liên kết:** [Xem nguồn gốc]({url}) 🔗\n\n"
        formatted += "**Trích dẫn nội dung:**\n\n"
        formatted += f"```\n{formatted_content}\n```\n\n"
        formatted += "---\n\n"  # Đường phân cách giữa các kết quả
        
        idx_counter += 1
    
    return formatted
