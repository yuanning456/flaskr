from flask import jsonify, request
from . import bp
from .service import get_message_b, process_message_c, file_to_moonshot, file_list, get_info, get_info_content
from flask import render_template
from flask import current_app
from flask import Blueprint
import os

# current_app.register_blueprint(bp, url_prefix='/rag')
# bp = Blueprint('rag', __name__)


@bp.route('/b', methods=['GET'])
def b():
    response = get_message_b()
    return jsonify(response)

@bp.route('/c', methods=['POST'])
def c():
    response = process_message_c()
    return render_template('c.html', title='Endpoint C', message=response['message'])

@bp.route('/upload_file', methods=['POST', 'GET'])

def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            file_to_moonshot(upload_path)
            return {"message": f"File {filename} uploaded successfully"}
        else:
            return {"message": "No file uploaded"}
    else:
        return render_template('upload_file.html', title='文件上传')
   
@bp.route('/get_file_list', methods=['GET'])
def get_file_list():
    list = file_list()
    return jsonify(list)


@bp.route('/get_file_info', methods=['GET'])
def get_file_info():# cq897s2tnn0t8799pip0
    file_id = request.args.get('file_id')
    info = get_info(file_id)
    return jsonify(info)


@bp.route('/get_file_content', methods=['GET'])
def get_file_content():# cq897s2tnn0t8799pip0
    file_id = request.args.get('file_id')
    info = get_info_content(file_id)
    return jsonify(info)







