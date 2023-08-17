import csv

def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        all_questions = [(row[0], row[1], row[2]) for row in reader]
    return all_questions

