# google_serper_search.py

from langchain_community.utilities import GoogleSerperAPIWrapper
from engine.utils import format_news_results
#,rewrite_query_for_law, LAW_DOMAINS


# Khởi tạo công cụ Google Serper với loại tìm kiếm "news"
search = GoogleSerperAPIWrapper(type="news", num_results=5)

# Gọi Google Serper và lấy kết quả tin tức
def get_google_serper_results(query: str) -> str:
    results = search.results(query)
    return format_news_results(results)

# def get_google_serper_results(query: str) -> str:
#     # Rewrite query để filter các trang luật chính thống khi cần
#     q2 = rewrite_query_for_law(query, LAW_DOMAINS)
#     results = search.results(q2)
#     return format_news_results(results)