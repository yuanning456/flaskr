from models import db
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import LargeBinary

class FileInfo(db.Model):
    __tablename__ = 'file_info'
    id = db.Column(db.Integer, primary_key=True)
    moonshot_id = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255))
    file_type = db.Column(db.String(255))
    title = db.Column(db.Text)
    file_content = db.Column(db.Text)
class embeddings(db.Model):
    __tablename__ = 'embeddings'
    id = db.Column(db.Integer, primary_key=True)
    embedding = db.Column(db.Text)
    def __repr__(self):
        return f"<Embedding(id={self.id}, embedding={self.embedding})>"
    

class QnA(db.Model):
    __tablename__ = 'qna'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    embedding = db.Column(LargeBinary, nullable=False)  # 使用 LargeBinary 存储嵌入向量
    answer = db.Column(db.Text, nullable=True)
    