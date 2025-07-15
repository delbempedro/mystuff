#!/usr/bin/env python3
#
# Academic History PDF Parser (Version 7 - Uppercase headers, split year/semester)
#
# This script extracts course data from a Brazilian university's academic history PDF,
# processes it, and saves the output to a CSV file inside a 'data' directory.
#
# Requirements: pypdf
# Usage: python parser.py <path_to_your_pdf_file.pdf>
#

import sys
import re
import csv
import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Reads a PDF file and extracts the text from all its pages.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The concatenated text content from all pages of the PDF, or None on error.
    """
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
    """
    Parses the raw text from an academic history document and organizes it by semester.

    Args:
        history_text (str): The full text content from the PDF.

    Returns:
        dict: A dictionary with the original semester name as keys and a list of course dictionaries as values.
    """
    semesters_data = {}
    semester_count = 0  # Counter for the sequential semester number

    semester_regex = re.compile(
        r"(\d{4}\s*(?:1º|2º|1°)\.?\s*(?:Semestre|Anual))([\s\S]*?)"
        r"(?=\d{4}\s*(?:1º|2º|1°)\.?\s*(?:Semestre|Anual)|Créditos obtidos|_____________________________________________________________________________)"
    )

    for semester_match in semester_regex.finditer(history_text):
        semester_count += 1
        original_semester_string = semester_match.group(1).strip()
        semester_block = semester_match.group(2)
        
        # --- NEW LOGIC TO SPLIT YEAR AND ANUAL SEMESTER ---
        year, anual_semester = "N/A", "N/A"
        year_semester_match = re.match(r"(\d{4})\s*(.*)", original_semester_string)
        if year_semester_match:
            year = year_semester_match.group(1)
            anual_semester = year_semester_match.group(2).replace("°.", "º").replace("º.", "º").strip()
        # --- END OF NEW LOGIC ---

        semester_courses = []

        course_regex = re.compile(
            r"^((?:[A-Z]{2,3})?\d{4,})\s+"
            r"(.+?)\s+"
            r"(\d+)"
            r"(?:\s+(\d+))?"
            r".*?"
            r"(\d+\.\d+|[A-Z]{2,})"
        )

        for line in semester_block.split('\n'):
            course_match = re.search(course_regex, line.strip())
            if course_match:
                course_code = course_match.group(1)
                
                unit_match = re.match(r'([A-Z]+|^\d{3})', course_code)
                unit = unit_match.group(1) if unit_match else "N/A"
                
                course_name = course_match.group(2).strip()
                lecture_credits = int(course_match.group(3))
                work_credits = int(course_match.group(4)) if course_match.group(4) else 0
                grade = course_match.group(5).strip()

                course_data = {
                    "semester": semester_count,
                    "unit": unit,
                    "year": year,
                    "annual_semester": anual_semester,
                    "course_name": course_name,
                    "total_credits": lecture_credits + work_credits,
                    "lecture_credits": lecture_credits,
                    "work_credits": work_credits,
                    "grade": grade,
                }
                semester_courses.append(course_data)
        
        if semester_courses:
            semesters_data[original_semester_string] = semester_courses

    return semesters_data

def write_data_to_csv(data, output_filepath):
    """
    Writes the parsed academic data to a CSV file.

    Args:
        data (dict): The dictionary of parsed data from parse_academic_history.
        output_filepath (str): The full path for the output CSV file.
    """
    # Define headers in all uppercase
    headers = ["SEMESTER", "UNIT", "YEAR", "ANNUAL SEMESTER", "COURSE NAME", "TOTAL CREDITS", "LECTURE CREDITS", "WORK CREDITS", "GRADE"]
    
    try:
        with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            all_courses = [course for courses_list in data.values() for course in courses_list]
            for course in all_courses:
                writer.writerow([
                    course["semester"],
                    course["unit"],
                    course["year"],
                    course["annual_semester"],
                    course["course_name"],
                    course["total_credits"],
                    course["lecture_credits"],
                    course["work_credits"],
                    course["grade"]
                ])
        print(f"Successfully created CSV file: {output_filepath}")
    except Exception as e:
        print(f"An error occurred while writing the CSV file: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <path_to_pdf_file>")
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
            
            base_name = pdf_filepath.split('/')[-1].rsplit('.', 1)[0]
            output_filename = f"{base_name}_data.csv"
            full_output_path = os.path.join(output_dir, output_filename)

            print(f"Writing data to '{full_output_path}'...")
            write_data_to_csv(parsed_data, full_output_path)
        else:
            print("Could not parse any academic data from the PDF. The PDF format might be significantly different.")
    else:
        print("Script finished due to PDF reading error.")