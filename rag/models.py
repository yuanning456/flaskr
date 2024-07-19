from models import db

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