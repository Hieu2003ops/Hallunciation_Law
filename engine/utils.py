from typing import List
import re

def format_tavily_result(raw_result: List[dict]) -> str:
    formatted = "📚 **Kết quả từ Tavily:**\n\n"
    seen_urls = set()
    idx_counter = 1  # Để đánh số thứ tự cho các mục duy nhất
    
    for item in raw_result:
        url = item.get("url", "Không có URL")
        # Nếu URL đã xuất hiện, bỏ qua mục này
        if url in seen_urls:
            continue    
        seen_urls.add(url)
        
        content = item.get("content", "Không có nội dung").strip()
        source_type = (
            "official"
            if any(domain in url for domain in ["phapluat", "hethongphapluat", "lawnet", "moj.gov", "quochoi.vn"])
            else "news"
        )
        # Làm sạch content – ngắt dòng dài
        content = content.replace(". ", ".\n").replace("? ", "?\n").replace("! ", "!\n")
        
        # Format mỗi mục đẹp
        formatted += f"### {idx_counter}.{url}\n"
        formatted += f"🔗 **Loại nguồn:** `{source_type}`\n"
        formatted += f"**Tóm tắt nội dung:**\n{content}\n"
        formatted += "-" * 10 + "\n"
        idx_counter += 1
    
    return formatted




def format_news_results(results: dict) -> str:
    if not results or "news" not in results:
        return "Không tìm thấy kết quả tin tức nào."

    formatted = "Kết quả Tìm kiếm Tin tức:\n\n"
    for idx, item in enumerate(results["news"], start=1):
        title = item.get("title", "Không có tiêu đề")
        snippet = item.get("snippet", "Không có mô tả")
        link = item.get("link", "Không có link")
        date = item.get("date", "Không có ngày")
        source = item.get("source", "Không có nguồn")
        formatted += f"{idx}. {title}\n"
        formatted += f"   - Nguồn: {source} | Ngày: {date}\n"
        formatted += f"   - Mô tả: {snippet}\n"
        formatted += f"   - Link: {link}\n\n"
    return formatted