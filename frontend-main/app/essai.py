import json

from frontend.app.requestss import get_count_of_skills, get_count_of_skillstop3


def import_jobs_data(file_path):
    try:
        with open(file_path, 'r') as file:
            jobs_data = json.load(file)
        return jobs_data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return None

file_path = '/backend/PT2/resources/indeed_jobs.json'
jobs = import_jobs_data(file_path)

if jobs is not None:
    # Process the 'jobs' data as needed
    print(jobs)

te = get_count_of_skillstop3();
for i in te:
    print(f"Skill : {i} ")