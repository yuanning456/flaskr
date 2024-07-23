from flask import current_app
from openai import OpenAI
import os
#文件上传 api POST https://api.moonshot.cn/v1/files



def chat(ask, bg:str):
   
    client = OpenAI(
    api_key = os.getenv('MOONSHOT_SECRET_KEY'),
    base_url = "https://api.moonshot.cn/v1",
    )
    current_app.logger.error(ask)
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "system", "content": bg},
            {"role": "user", "content": ask}
        ],
        temperature = 0.3,
    )
    current_app.logger.error(completion)
    return completion.choices[0].message.content