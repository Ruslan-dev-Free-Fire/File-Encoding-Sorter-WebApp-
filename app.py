from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)

# Указываем папку для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Максимальный размер загружаемых файлов (в байтах)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Например, 16 MB

# Секретный ключ для безопасности (для flash-сообщений)
app.secret_key = 'your_secret_key_here'


# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'


@app.route('/sort_files', methods=['POST'])
def sort_files():
    try:
        subprocess.run(['python', 'file_sorter.py'], check=True)
        return 'Sorting completed successfully.'
    except subprocess.CalledProcessError as e:
        return f'Error during sorting: {e}'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start_script')
def start_script():
    subprocess.call(['python', 'your_script.py'])
    return 'Script started'


@app.route('/file_encoding_sorter', methods=['GET', 'POST'])
def file_encoding_sorter():
    if request.method == 'POST':
        # Проверка, был ли выбран файл
        if 'file' not in request.files:
            flash('File not selected', 'error')
            return redirect(request.url)

        file = request.files['file']

        # Если пользователь не выбрал файл, браузер отправит пустое поле без имени файла
        if file.filename == '':
            flash('File not selected', 'error')
            return redirect(request.url)

        # Проверка разрешенных расширений файла
        if not allowed_file(file.filename):
            flash('Only files with the extension .txt are allowed', 'error')
            return redirect(request.url)

        # Если файл прошел все проверки, сохраняем его
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
            # Здесь вы можете провести дополнительную обработку файла, если это необходимо

    return render_template('file_encoding_sorter.html')


if __name__ == '__main__':
    app.run(debug=True)