

from pathlib import Path
from flask import current_app
from openai import OpenAI
import requests
from .models import FileInfo, db, QnA
import os
from .bert import bert_embedding, text_to_embedding, get_most_similar_embedding
from .moonshot import chat
#文件上传 api POST https://api.moonshot.cn/v1/files

def get_client(url: str):
    client = OpenAI(
    api_key = "{os.getenv('MOONSHOT_SECRET_KEY')}",
    base_url = url,
)
    return client
def file_to_moonshot(filepath):
    client = OpenAI(
    api_key = "{os.getenv('MOONSHOT_SECRET_KEY')}",
    base_url = "https://api.moonshot.cn/v1",
)
    file_object = client.files.create(file=Path(filepath), purpose="file-extract")
    try:
        current_app.logger.error(file_object.json())
        id = file_object.id
        new_file = FileInfo(moonshot_id=id)
        db.session.add(new_file)
        db.session.commit()

    except UnicodeDecodeError as e:
        current_app.logger.error("Error decoding message: %s", str(e))
   
  
    return file_object


def file_list():
    headers = {
    "Authorization": f"Bearer {os.getenv('MOONSHOT_SECRET_KEY')}",
    "Content-Type": "application/json"
    }
    response = requests.get('https://api.moonshot.cn/v1/files', headers=headers)
    if response.status_code == 200:
        files_info = response.json()
        current_app.logger.error(files_info)
        return files_info
    else:
        print(f"Failed to get files. Status code: {response.status_code}, Response: {response.text}")
        return None

def get_info(file_id:str):
    headers = {
    "Authorization": f"Bearer {os.getenv('MOONSHOT_SECRET_KEY')}",
    "Content-Type": "application/json"
    }
    response = requests.get( "https://api.moonshot.cn/v1/files/" + file_id , headers=headers)
    if response.status_code == 200:
        files_info = response.json()
        current_app.logger.error(files_info)
        return files_info
    else:
        print(f"Failed to get files. Status code: {response.status_code}, Response: {response.text}")
        return None
   
def get_info_content(file_id:str):
    
    headers = {
    "Authorization": f'Bearer {os.getenv('MOONSHOT_SECRET_KEY')}',
    "Content-Type": "application/json"
    }
    response = requests.get( "https://api.moonshot.cn/v1/files/" + file_id + '/content' , headers=headers)
    if response.status_code == 200:
        files_info = response.json()
        current_app.logger.error(files_info)
        fileinfo = FileInfo.query.filter_by(moonshot_id=file_id).first()
        current_app.logger.error(fileinfo)
        

        fileinfo.file_content = files_info.get('content', None)
        fileinfo.file_type = files_info.get('file_type', None)
        fileinfo.filename = files_info.get('filename', None)
        fileinfo.title = files_info.get('titleget', None)
        fileinfo.type = files_info.get('type', None)
        db.session.commit()

        return files_info
    else:
        print(f"Failed to get files. Status code: {response.status_code}, Response: {response.text}")
        return None
   

def ask(question:str):
    if question == '':
        return {"message": "请输入问题"}
    question_embedding = text_to_embedding(question)

    text = "三年级一班有同学：小明、小红、大壮、小李、小刚，小红是学习委员、小明是班长，大壮是体育委员和数学课代表。 小红带了红领巾，今天天气小雨，35度，特斯拉卖35万一辆。"
    embedding = text_to_embedding(question)
    answer = chat(question, text)
    qnA_entry = QnA(question=question, embedding=question_embedding.tobytes(), answer=answer)
    db.session.add(qnA_entry)
    db.session.commit()
    
    return answer


def get_message_b():
    
    return {"message": "This is endpoint b"}

def process_message_c():
    # 这里可以加入复杂的业务逻辑处理
    return {"message": "This is endpoint c"}