#!/usr/bin/env python3
#
# Academic History PDF Parser (Final Correct Version)
#
# This script extracts course data from a Brazilian university's academic history PDF,
# processes it, and saves the output to a CSV file inside a 'data' directory.
#
# Requirements: pypdf
# Usage: python extract-data.py <path_to_your_pdf_file.pdf>
#

import sys
import re
import csv
import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """Reads a PDF file and extracts the text from all its pages."""
    full_text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
        return full_text
    except FileNotFoundError:
        print(f"Error: PDF file not found at '{pdf_path}'.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None

def parse_academic_history(history_text):
    """Parses the raw text from an academic history document and organizes it by semester."""
    semesters_data = {}
    semester_count = 0

    semester_regex = re.compile(
        r"(\d{4}\s*(?:1º|2º|1°)\.?\s*(?:Semestre|Anual))([\s\S]*?)"
        r"(?=\d{4}\s*(?:1º|2º|1°)\.?\s*(?:Semestre|Anual)|Créditos obtidos|_____________________________________________________________________________)"
    )

    for semester_match in semester_regex.finditer(history_text):
        original_semester_string = semester_match.group(1).strip()
        semester_block = semester_match.group(2)
        
        is_anual = "Anual" in original_semester_string
        if not is_anual:
            semester_count += 1

        year, anual_semester = "N/A", "N/A"
        year_semester_match = re.match(r"(\d{4})\s*(.*)", original_semester_string)
        if year_semester_match:
            year, anual_semester = year_semester_match.groups()
            anual_semester = anual_semester.replace("°.", "º").replace("º.", "º").strip()
            if "Anual" in anual_semester:
                anual_semester = "Anual"
        
        semester_courses = []

        for line in semester_block.split('\n'):
            line = line.strip()
            if not (line and re.match(r'^[A-Z]*\d+', line)):
                continue

            parts = line.split()
            course_code = parts[0]
            
            try:
                # --- FINAL, ROBUST PARSING LOGIC ---
                
                # Isolate the grade/status from the end of the line
                grade = parts[-2] if len(parts) > 1 and parts[-1] == 'A' else parts[-1]
                
                # Isolate the main data block (everything between code and grade)
                end_index_for_data = -2 if len(parts) > 1 and parts[-1] == 'A' else -1
                data_tokens = parts[1:end_index_for_data]

                # Find where the course name ends and numbers begin
                name_tokens = []
                number_tokens = []
                found_first_number = False
                for token in data_tokens:
                    # Strip parentheses for checking if it's a digit
                    cleaned_token = token.strip('()')
                    if cleaned_token.isdigit():
                        found_first_number = True
                    
                    if found_first_number:
                        number_tokens.append(cleaned_token)
                    else:
                        name_tokens.append(token)
                
                course_name = " ".join(name_tokens)

                # The first number found is ALWAYS Lecture Credits (AU)
                lecture_credits = int(number_tokens[0]) if len(number_tokens) > 0 else 0
                work_credits = 0

                # The second number is Work Credits (TR) ONLY IF it's a single digit.
                # This correctly distinguishes it from multi-digit CH values.
                if len(number_tokens) > 1 and len(number_tokens[1]) == 1:
                     work_credits = int(number_tokens[1])

            except (ValueError, IndexError):
                # Fallback for simple lines like TCC
                if len(parts) >= 4 and parts[-1].isalpha():
                    course_name = " ".join(parts[1:-2])
                    lecture_credits = int(parts[-2])
                    work_credits = 0
                    grade = parts[-1]
                else:
                    continue
            
            unit_match = re.match(r'([A-Z]+|^\d{3})', course_code)
            unit = unit_match.group(1) if unit_match else "N/A"
            
            if not course_name:
                continue

            course_data = {
                "semester": "N/A" if is_anual else semester_count, "unit": unit, "year": year, 
                "anual_semester": anual_semester, "course_name": course_name.strip(), 
                "total_credits": lecture_credits + work_credits, "lecture_credits": lecture_credits, 
                "work_credits": work_credits, "grade": grade.strip(),
            }
            semester_courses.append(course_data)
        
        if semester_courses:
            semesters_data[original_semester_string] = semester_courses

    return semesters_data

def write_data_to_csv(data, output_filepath):
    headers = ["SEMESTER", "UNIT", "YEAR", "ANUAL SEMESTER", "COURSE NAME", "TOTAL CREDITS", "LECTURE CREDITS", "WORK CREDITS", "GRADE"]
    try:
        with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            all_courses = sorted([course for courses_list in data.values() for course in courses_list], 
                                 key=lambda x: (isinstance(x['semester'], int), x['semester']))
            for course in all_courses:
                writer.writerow([
                    course["semester"], course["unit"], course["year"], course["anual_semester"],
                    course["course_name"], course["total_credits"], course["lecture_credits"],
                    course["work_credits"], course["grade"]
                ])
        print(f"Successfully created CSV file: {output_filepath}")
    except Exception as e:
        print(f"An error occurred while writing the CSV file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract-data.py <path_to_pdf_file>")
        sys.exit(1)
    pdf_filepath = sys.argv[1]
    print(f"Reading data from '{pdf_filepath}'...")
    raw_text = extract_text_from_pdf(pdf_filepath)
    if raw_text:
        print("Parsing academic data...")
        parsed_data = parse_academic_history(raw_text)
        if parsed_data:
            output_dir = "data"
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.basename(pdf_filepath).rsplit('.', 1)[0]
            output_filename = f"{base_name}_data.csv"
            full_output_path = os.path.join(output_dir, output_filename)
            print(f"Writing data to '{full_output_path}'...")
            write_data_to_csv(parsed_data, full_output_path)
        else:
            print("Could not parse any academic data from the PDF.")
    else:
        print("Script finished due to PDF reading error.")