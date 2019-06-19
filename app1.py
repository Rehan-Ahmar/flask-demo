from flask import Flask, redirect, url_for, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = r"D:\Demos\sample-web-project\uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/main/')
def show_main_page():
    return 'This is main page'
    
@app.route("/start")
def start():
    return render_template("demo_start.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('hello_name',user = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('hello_name',user = user))

@app.route('/success/<user>')
def hello_name(user):
    dict = {'phy':50,'che':60,'maths':70}
    return render_template('demo_result.html', name = user, marks=51, result = dict)    




def __allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadStart')
def upload():
   return render_template('upload.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        input_file = request.files['input_file']
        if input_file and __allowed_file(input_file.filename):
            filename = secure_filename(input_file.filename)
            print("filename: " + filename)
            print("upload folder: " + app.config['UPLOAD_FOLDER'])
            input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            return 'Invalid File Format'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
   app.run()
   #app.run(debug = True)