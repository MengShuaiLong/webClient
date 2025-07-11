from flask import Flask, request, jsonify, render_template
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 配置上传文件夹和允许的文件类型
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip', 'rar', 'tar.gz'}
# 限制文件大小为 10MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查文件扩展名是否允许
def allowed_file(filename):
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        # 处理 tar.gz 特殊情况
        if ext == 'gz' and filename.endswith('.tar.gz'):
            return True
        return ext in ALLOWED_EXTENSIONS
    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            # 获取上传的文件
            file = request.files.get('file')
            # 获取 IMEI 号
            imei = request.form.get('imei')

            if not file or not imei:
                return jsonify({"message": "文件或 IMEI 号缺失"}), 400

            # 检查文件名是否有效
            if file.filename == '':
                return jsonify({"message": "未选择有效文件"}), 400

            # 检查文件类型是否允许
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # 生成带 IMEI 号的文件名
                new_filename = f"{imei}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                return jsonify({"message": "文件上传成功"}), 200
            else:
                return jsonify({"message": "不允许的文件类型，允许的类型: " + ', '.join(ALLOWED_EXTENSIONS)}), 400

        except Exception as e:
            return jsonify({"message": f"文件上传失败: {str(e)}"}), 500

    try:
        # 尝试渲染指定模板
        return render_template('ota_parm.html')
    except TemplateNotFound:
        # 若模板文件不存在，返回 JSON 错误响应
        error_msg = "未找到 'ota_parm.html' 模板文件，请检查文件是否存在。"
        print(error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)    