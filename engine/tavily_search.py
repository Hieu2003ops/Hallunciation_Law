# tavily_search.py

from langchain_community.tools import TavilySearchResults
from pydantic import BaseModel, Field
from typing import List
from engine.utils import format_tavily_result
#,rewrite_query_for_law, LAW_DOMAINS


# Định nghĩa model cho một mục kết quả
# class SearchResultItem(BaseModel):
#     url: str = Field(..., description="Link của bài viết")
#     content: str = Field(..., description="Nội dung tóm tắt hoặc câu trả lời")

# # Định nghĩa model cho output của tool
# class TavilySearchOutput(BaseModel):
#     results: List[SearchResultItem] = Field(..., description="Danh sách kết quả tìm kiếm")


tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    name="TavilyVietnamLawSearch",
    description=(
        "Tìm kiếm pháp luật Việt Nam từ thuvienphapluat.vn, luatvietnam.vn, quochoi.vn, vietnamlaw.net"
    ),
)

# Gọi công cụ Tavily với truy vấn tiếng Việt
def get_tavily_results(query: str) -> str:
    raw_result = tool.invoke({"query": query})
    return format_tavily_result(raw_result)

# def get_tavily_results(query: str) -> str:
#     # Rewrite query để giới hạn domain pháp luật
#     q2 = rewrite_query_for_law(query, LAW_DOMAINS)
#     raw_result = tool.invoke({"query": q2})
#     return format_tavily_result(raw_result)
