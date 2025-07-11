from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 配置上传文件夹和允许的文件类型
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'tar.gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 16MB 上传限制

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 检查文件扩展名是否允许
def allowed_file(filename):
    for ext in ALLOWED_EXTENSIONS:
        if filename.lower().endswith(ext):
            return True
    return False

# 首页路由 - 显示文件上传表单
@app.route('/', methods=['GET', 'POST'])
def index():
    success_message = None
    if request.method == 'POST':
        # 检查请求中是否有文件
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空文件
        if file.filename == '':
            return redirect(request.url)
        
        # 检查文件是否有效且扩展名允许
        if file and allowed_file(file.filename):
            # 确保文件名安全
            filename = secure_filename(file.filename)
            # 保存文件到上传文件夹
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success_message = f"文件 {filename} 上传成功！"
        else:
            return "不允许的文件类型"
    return render_template('index.html', success_message=success_message)

# 处理文件上传的路由
@app.route('/', methods=['POST'])
def upload_file():
    # 检查请求中是否有文件
    if 'file' not in request.files:
        return "未选择文件", 400
    
    file = request.files['file']
    
    # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空文件
    if file.filename == '':
        return "未选择文件", 400
    
    # 检查文件是否有效且扩展名允许
    if file and allowed_file(file.filename):
        # 确保文件名安全
        filename = secure_filename(file.filename)
        # 保存文件到上传文件夹
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "上传成功", 200
    else:
        return "不允许的文件类型", 400

# 显示上传的文件
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)    