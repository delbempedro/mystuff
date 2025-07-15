#!/usr/bin/env python3
#
# Academic History PDF Parser
#
# This script extracts course data from a Brazilian university's academic history PDF,
# processes it, and saves the output to a CSV file.
#
# Requirements: pypdf (install via pip or your system's package manager)
# Usage: python parser.py <path_to_your_pdf_file.pdf>
#
import sys
import re
import csv
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
                # Add a newline character to help separate content from different pages
                full_text += page.extract_text() + "\n"
        return full_text
    except FileNotFoundError:
        print(f"Error: PDF file not found at '{pdf_path}'. Please check the path.")
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
        dict: A dictionary with semesters as keys and a list of course dictionaries as values.
              Returns an empty dictionary if no data can be parsed.
    """
    # This dictionary will store all the structured data.
    # Format: {"Semester Name": [{"course_name": "...", "grade": "..."}]}
    semesters_data = {}

    # Regex to find each semester block. It looks for a year followed by semester info.
    # It captures until it finds the next semester block or the end of the records.
    semester_regex = re.compile(r"(\d{4}\s(?:1º|2º|1º\.|2°)\.\s(?:Semestre|Anual))([\s\S]*?)(?=\d{4}\s(?:1º|2º|1º\.|2°)\.\s(?:Semestre|Anual)|Créditos obtidos)")

    for semester_match in semester_regex.finditer(history_text):
        # Clean up the semester name for consistency
        semester_name = semester_match.group(1).replace("°.", "º").replace("º.", "º").strip()
        semester_block = semester_match.group(2)
        
        semester_courses = []

        # Regex to find course details within a semester block.
        # It looks for a course code, name, credits, and grade.
        # Groups: 1-Code, 2-Name, 3-LectureCredits, 4-WorkCredits, 5-Frequency, 6-Grade
        course_regex = re.compile(r"([A-Z]{2,3}\d{4,5})\s+(.*?)\s+(\d+)\s+(?:(\d+)\s+)?\d+.*?\s+(?:\d{1,3})\s+([\d\.]+|MA)\s+A?")

        for course_match in re.finditer(course_regex, semester_block):
            # Extract data using regex groups
            course_name = course_match.group(2).strip()
            lecture_credits_str = course_match.group(3)
            work_credits_str = course_match.group(4)
            grade_str = course_match.group(6)

            # Convert credit strings to integers, defaulting to 0 if not found
            lecture_credits = int(lecture_credits_str) if lecture_credits_str else 0
            work_credits = int(work_credits_str) if work_credits_str else 0
            
            # Create a dictionary for the current course
            course_data = {
                "course_name": course_name,
                "total_credits": lecture_credits + work_credits,
                "lecture_credits": lecture_credits,
                "work_credits": work_credits,
                "grade": grade_str, # Keep grade as string to handle 'MA' (Enrolled)
            }
            semester_courses.append(course_data)
        
        if semester_courses:
            semesters_data[semester_name] = semester_courses

    return semesters_data

def write_data_to_csv(data, output_filename):
    """
    Writes the parsed academic data to a CSV file.

    Args:
        data (dict): The dictionary of parsed data from parse_academic_history.
        output_filename (str): The name for the output CSV file.
    """
    # Define the headers for the CSV file
    headers = ["Semester", "Course Name", "Total Credits", "Lecture Credits", "Work Credits", "Grade"]
    
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the header row
            writer.writerow(headers)
            
            # Iterate through the data and write each course as a row
            for semester, courses in data.items():
                for course in courses:
                    writer.writerow([
                        semester,
                        course["course_name"],
                        course["total_credits"],
                        course["lecture_credits"],
                        course["work_credits"],
                        course["grade"]
                    ])
        print(f"Successfully created CSV file: {output_filename}")
    except Exception as e:
        print(f"An error occurred while writing the CSV file: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    # Check if a command-line argument (the filename) was provided
    if len(sys.argv) < 2:
        print("Usage: python parser.py <path_to_pdf_file>")
        sys.exit(1) # Exit the script if no file is provided

    pdf_filepath = sys.argv[1]
    
    # Step 1: Extract text from the provided PDF file
    print(f"Reading data from '{pdf_filepath}'...")
    raw_text = extract_text_from_pdf(pdf_filepath)
    
    if raw_text:
        # Step 2: Parse the extracted text to get structured data
        print("Parsing academic data...")
        parsed_data = parse_academic_history(raw_text)
        
        if parsed_data:
            # Step 3: Write the structured data to a CSV file
            output_csv_filename = pdf_filepath.replace('.pdf', '_data.csv')
            print(f"Writing data to '{output_csv_filename}'...")
            write_data_to_csv(parsed_data, output_csv_filename)
        else:
            print("Could not parse any academic data from the PDF.")