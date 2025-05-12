from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews
import google.generativeai as genai
import json, os
import requests
from dotenv import load_dotenv

load_dotenv()

# 創建MCP伺服器
mcp = FastMCP("Google News Search")

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

@mcp.tool()
def search_news(keyword: str, language: str = "zh-TW", period: str = "2d", max_results: int = 4) -> str:
    """
    先用 Gemini API 產生 2 個與關鍵詞相關的詞彙，再用這些詞彙進行 Google 新聞搜尋，彙整前 max_results 筆新聞並摘要。

    Args:
        keyword (str): 搜尋關鍵詞。
        language (str, optional): 語言代碼，預設為 "zh-TW"（繁體中文）。
        period (str, optional): 時間範圍，預設為 "2d"（2天內新聞）。
        max_results (int, optional): 回傳新聞數量，預設為 4。

    Returns:
        str: 前 max_results 筆新聞的 JSON 字串，包含 Gemini 產生的摘要。
    """
    GEMINI_API_KEY = "" # 個人API key
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

    def get_related_keywords(keyword):
        headers = {"Content-Type": "application/json"}
        prompt = f"請給我2個和『{keyword}』相關的繁體中文詞彙，只回傳JSON陣列，不要有其他說明。"
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        try:
            resp = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=10)
            if resp.status_code == 200:
                import json as pyjson, re
                text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                match = re.search(r'\[.*\]', text, re.DOTALL)
                if match:
                    return pyjson.loads(match.group(0))
                else:
                    return [keyword]
            else:
                return [keyword]
        except Exception as e:
            return [keyword]

    def get_insight(title, desc):
        try:
            prompt = f"請用繁體中文針對新聞標題：「{title}」，與內文片段：「{desc}」，提供一百字內的洞察"
            response = model.generate_content(prompt)
            print('[Gemini Debug] response:', response.text.encode('cp950', errors='replace').decode('cp950'))
            return response.text.strip()
        except Exception as e:
            return f"洞察錯誤: {str(e)}"

    try:
        keywords = [keyword] + get_related_keywords(keyword)
        seen = set()
        all_news = []
        gn = GoogleNews(lang=language, period=period)
        for kw in keywords:
            gn.clear()
            gn.search(kw)
            for article in gn.results():
                unique_id = article.get("title", "") + article.get("link", "")
                if unique_id not in seen:
                    seen.add(unique_id)
                    all_news.append(article)
        # 取前max_results筆
        formatted_results = []
        for article in all_news[:max_results]:
            title = article.get("title", "")
            desc = article.get("desc", "")
            insight = get_insight(title, desc) if title and desc else "無標題或內文可洞察"
            formatted_results.append({
                "標題": title,
                "連結": article.get("link", "").split('?')[0],
                "發佈時間": article.get("date", ""),
                "描述": desc,
                "洞察": insight
            })
        import json as pyjson
        return pyjson.dumps(formatted_results, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"搜尋時發生錯誤: {str(e)}"

if __name__ == "__main__":
    mcp.run() 
