from flask import Flask, redirect, flash, url_for, request, session, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from qna_extractor import extract_qna
from info_extractor import extract_info
import configparser

config = configparser.ConfigParser()
config.read(r'app-config.ini')
host = config['SERVER_CONFIGURATIONS']['host']
port = config['SERVER_CONFIGURATIONS']['port']
upload_folder = config['SERVER_CONFIGURATIONS']['upload_folder']
secret_key = config['SERVER_CONFIGURATIONS']['secret_key']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = secret_key

@app.route('/qnaExtractor/')
def show_qna_main_page():
    results_qna = session.pop('results_qna', [])
    return render_template('qna_home.html', results = results_qna)

@app.route('/regexExtractor/')
def show_regex_main_page():
    results_regex = session.pop('results_regex', [])
    return render_template('regex_home.html', results = results_regex)

def __allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/uploadPDFqna/', methods = ['POST'])
def upload_pdf_qna():
    input_file = request.files['input_pdf']
    if input_file and __allowed_file(input_file.filename, ['pdf']):
        filename = secure_filename(input_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        input_file.save(pdf_path)
        print("pdf_path: " + pdf_path)
        flash(filename + ' successfully uploaded and executed.')
        return extract_qna_from_pdf(pdf_path)
    else:
        flash('Invalid File Format. Upload PDF file only.')
    return redirect(url_for('show_qna_main_page'))

@app.route('/uploadExcel/', methods = ['POST'])
def upload_excel():
    input_file = request.files['input_excel']
    if input_file and __allowed_file(input_file.filename, ['xls', 'xlsx']):
        filename = secure_filename(input_file.filename)
        print("excel filename: " + filename)
        input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "questions.xlsx"))
        #return redirect(url_for('uploaded_file', filename=filename))
        flash('Question File successfully uploaded.')
    else:
        flash('Invalid Question File Format. Upload Excel file only.')
    return redirect(url_for('show_qna_main_page'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def extract_qna_from_pdf(pdf_path):
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], "questions.xlsx")
    results_qna = extract_qna(pdf_path=pdf_path, quesion_excel_path=excel_path)
    session['results_qna'] = results_qna
    return redirect(url_for('show_qna_main_page'))

@app.route('/uploadPDFregex/', methods = ['POST'])
def upload_pdf_regex():
    input_file = request.files['input_pdf']
    if input_file and __allowed_file(input_file.filename, ['pdf']):
        filename = secure_filename(input_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        input_file.save(pdf_path)
        print("pdf_path: " + pdf_path)
        flash(filename + ' successfully uploaded and executed.')
        return extract_info_from_pdf(pdf_path)
    else:
        flash('Invalid File Format. Upload PDF file only.')
    return redirect(url_for('show_regex_main_page'))

@app.route('/uploadJSON/', methods = ['POST'])
def upload_json():
    input_file = request.files['config_json']
    if input_file and __allowed_file(input_file.filename, ['json']):
        filename = secure_filename(input_file.filename)
        print("excel filename: " + filename)
        input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "info_extractor.json"))
        #return redirect(url_for('uploaded_file', filename=filename))
        flash('JSON successfully uploaded.')
    else:
        flash('Invalid file format. Upload JSON file only.')
    return redirect(url_for('show_regex_main_page'))

def extract_info_from_pdf(pdf_path):
    excel_path = "dummy.xlsx"
    config_json_path = os.path.join(app.config['UPLOAD_FOLDER'], "info_extractor.json")
    results_regex = extract_info(pdf_path=pdf_path, excel_path=excel_path, json_rules_path=config_json_path)
    session['results_regex'] = results_regex
    return redirect(url_for('show_regex_main_page'))

if __name__ == '__main__':
   app.run(host=host, port=port)