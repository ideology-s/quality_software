from openai import OpenAI
from app.config import settings

def chat_with_ai(message: str):
    if not settings.OPENAI_API_KEY:
        return {
            "id": 1,
            "role": "assistant",
            "content": "AI 服务尚未配置 API Key，请在 .env 文件中设置 OPENAI_API_KEY。",
            "thinking": "",
        }

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个校园小摊经营助手，帮助摊主分析出摊日志、日程安排、商品经营和排队订单数据，给出经营建议。回答简洁实用。",
                },
                {"role": "user", "content": message},
            ],
        )
        content = response.choices[0].message.content or ""
        return {
            "id": response.id if hasattr(response, 'id') else 1,
            "role": "assistant",
            "content": content,
            "thinking": f"已思考（用时 {response.usage.total_tokens if hasattr(response, 'usage') and response.usage else '--'} tokens）",
        }
    except Exception as e:
        return {
            "id": 1,
            "role": "assistant",
            "content": f"AI 服务暂时不可用：{str(e)}。请稍后再试。",
            "thinking": "",
        }
