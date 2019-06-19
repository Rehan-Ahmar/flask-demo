import pdfbox
import re
import os
import string
import json
from xlrd import open_workbook

def __get_output_file_path(pdf_path, filename_suffix):
    basename = os.path.basename(pdf_path)
    dirname = os.path.dirname(pdf_path)
    filename = os.path.splitext(basename)[0] + filename_suffix
    return os.path.join(dirname, filename)
    
def __writeFile(filepath, text):
    file = open(filepath,"wb")
    file.write(text.encode("utf-8"))
    
def __writeJsonFile(filepath, obj):
    with open(filepath, 'w') as outfile:
        json.dump(obj, outfile, indent=2)

def get_pdf_text(pdf_path):
    p = pdfbox.PDFBox()
    text = p.extract_text(pdf_path, sort=True)
    text = re.sub(r'[^\x00-\x7F]+','', text)
    #print("*********** Extracted Text *********\n" + text)
    #__writeFile(__get_output_file_path(pdf_path, "_unprocessed_text.txt"), text)
    return text;
    
def __process_line(line):
    processed_line = re.sub(r'[^A-Za-z\d]', ' ', line)
    processed_line = re.sub(r'\s+',' ', processed_line).strip()
    return processed_line
    
def __process_lines(lines):
    result = []
    for line in lines:
        processed_line = __process_line(line)
        if processed_line:
            result.append(processed_line)
    return result
    
def get_all_processed_lines_from_pdf(pdf_path):
    text = get_pdf_text(pdf_path)
    lines = text.splitlines()
    #__writeFile(__get_output_file_path(pdf_path, "_lines.txt"), "\r\n".join(lines))
    processed_lines = __process_lines(lines)
    #__writeFile(__get_output_file_path(pdf_path, "_processed_lines.txt"), "\r\n".join(processed_lines))
    return processed_lines
    
def read_excel(excel_path):
    wb = open_workbook(excel_path)
    questions = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        for row in range(1, number_of_rows):
            question_no = (sheet.cell(row,0).value)
            question = (sheet.cell(row,1).value)
            entry = {}
            entry["question_no"] = question_no
            entry["question"] = question
            entry["processed_question"] = __process_line(question)
            questions.append(entry)
    return questions
    
def check_if_complete_question_present(question, lines, line_index):
    for i in range(line_index, len(lines)):
        searchResult = re.search(final_regex, qtext, re.I|re.S)
    
    
def extract_qna(pdf_path, quesion_excel_path):
    lines = get_all_processed_lines_from_pdf(pdf_path)
    questions = read_excel(quesion_excel_path)
    results = []
    q_index = 0
    line_index = 0
    values= ""
    #__writeJsonFile(__get_output_file_path(pdf_path, "_questions.txt"), questions)

    for question_dict in questions:
        qnum = question_dict["question_no"]
        qtext = question_dict["processed_question"]
        print("********* qtext: ******" + qtext)

        question_match_in_progress = False
        remaining_question = ""
        match_start_index = -1
        value = "";
        
        while line_index < len(lines):
            line = lines[line_index]
            print("**** line: " + line)
            final_regex = line
            if question_match_in_progress:
                print("   question_match_in_progress")
                searchText = remaining_question
            else:
                print(" match not in progress.")
                final_regex = final_regex.lstrip("0123456789.- ")
                searchText = qtext
            print("Final regex: " + final_regex)
            print("Search text: " + searchText)
            searchResult = re.search(final_regex, searchText, re.I|re.S)
            
            if searchResult:
                print("       Matched ")
                remaining_question = re.sub(final_regex, '', searchText, re.I|re.S).strip()
                print("remaining_question: " + remaining_question)
                if not remaining_question:
                    value = lines[line_index + 1]
                    print("value: " + value)
                    line_index += 1
                    break;
                if not question_match_in_progress:
                    match_start_index = line_index;
                    question_match_in_progress = True
            else:
                print("     No  Match ")
                if question_match_in_progress:
                    question_match_in_progress = False
                    qtext = question_dict["processed_question"]
                    line_index = match_start_index
            line_index += 1
            
        if (line_index == len(lines)):
            line_index = 0
        
        print("value: " + value)
        if value:
            entry = {}
            entry["question_no"] = question_dict["question_no"]
            entry["question"] = question_dict["question"]
            entry["response"] = value
            results.append(entry)
    #__writeJsonFile(__get_output_file_path(pdf_path, "_responses.txt"), results)
    return results

if __name__ == "__main__":
    quesion_excel_path = r"D:\Demos\goldman-demo\CodeBase\Demo\questions.xlsx"
    pdf_path = r"D:\Demos\goldman-demo\CodeBase\Demo\EmploymentApplication.pdf"
    extract_qna(pdf_path=pdf_path, quesion_excel_path=quesion_excel_path)
