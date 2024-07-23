import openai
import psycopg2
from psycopg2.extras import DictCursor

GPT_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_COMPLETIONS_MODEL = "text-davinci-003"
MAX_TOKENS = 1024

# OpenAI的API Key
openai.api_key = '<Secret API Key>'

prompt = '如何创建一个RDS PostgreSQL实例'

prompt_response = openai.Embedding.create(
    model=EMBEDDING_MODEL,
    input=prompt,
)
prompt_embedding = prompt_response['data'][0]['embedding']

# 连接RDS PostgreSQL数据库
conn = psycopg2.connect(database="<数据库名>",
                        host="<RDS实例连接地址>",
                        user="<用户名>",
                        password="<密码>",
                        port="<数据库端口>")
conn.autocommit = True


def answer(prompt_doc, prompt):
    improved_prompt = f"""
    按下面提供的文档和步骤来回答接下来的问题：
    (1) 首先，分析文档中的内容，看是否与问题相关
    (2) 其次，只能用文档中的内容进行回复,越详细越好，并且以markdown格式输出
    (3) 最后，如果问题与RDS PostgreSQL不相关，请回复"我对RDS PostgreSQL以外的知识不是很了解"

    文档:
    \"\"\"
    {prompt_doc}
    \"\"\"

    问题: {prompt}
    """

    response = openai.Completion.create(
        model=GPT_COMPLETIONS_MODEL,
        prompt=improved_prompt,
        temperature=0.2,
        max_tokens=MAX_TOKENS
    )

    print(f"{response['choices'][0]['text']}\n")


similarity_threshold = 0.78
max_matched_doc_counts = 8

# 通过pgvector过滤出相似度大于一定阈值的文档块
similarity_search_sql = f'''
SELECT doc_chunk, token_size, 1 - (embedding <=> '{prompt_embedding}') AS similarity 
FROM rds_pg_help_docs WHERE 1 - (embedding <=> '{prompt_embedding}') > {similarity_threshold} ORDER BY id LIMIT {max_matched_doc_counts};
'''

cur = conn.cursor(cursor_factory=DictCursor)
cur.execute(similarity_search_sql)
matched_docs = cur.fetchall()

total_tokens = 0
prompt_doc = ''
print('Answer: \n')
for matched_doc in matched_docs:
    if total_tokens + matched_doc['token_size'] <= 1000:
        prompt_doc += f"\n---\n{matched_doc['doc_chunk']}"
        total_tokens += matched_doc['token_size']
        continue

    answer(prompt_doc,prompt)

    total_tokens = 0
    prompt_doc = ''

answer(prompt_doc,prompt)