from flask import Flask, render_template, request
import json
import matplotlib.pyplot as plt
import numpy as np

from requestss import get_count_of_skills
from requestss import get_count_of_skillstop3
from requestss import get_popular_skills_by_domain
from requestss import get_ict_skills
from requestss import get_language_skills
from requestss import get_skills_from_language
from requestss import get_transversal_skills
from requestss import get_all_info_for_all_jobs
from requestss import get_skills_by_domain
from requestss import get_top_3_job_names
from requestss import get_popularity_of_skills
from requestss import get_all_info_for_a_jobb
from requestss import get_jobs_with_skill
from requestss import get_jobs_with_skill_and_description

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


def pop_skill():
    sk = get_count_of_skills()

    skillpopularity, skillpopularity2 = sk

    skills_dict = {}
    compteur_skill = 0
    skkkk = []
    pkkkk = []

    for i in range(len(skillpopularity)):
        if compteur_skill <= 10:
            skill_name = skillpopularity[i]
            skkkk.append(skill_name)
            popularity = skillpopularity2[i]
            pkkkk.append(popularity)
            skills_dict[skill_name] = popularity
            compteur_skill += 1

    y = np.array(pkkkk)
    mylabels = skkkk
    plt.pie(y, labels=mylabels)
    plt.savefig('static/images/my_plot.png')
    return skills_dict


def pop_skill_dom(dom: str):
    sk = get_popular_skills_by_domain(dom)

    # print(sk)

    # for result in resultats_skills:
    # print(f"Skill: {result['Skill']}, Popularité: {result['Popularité']}")

    skills_dictdom = {}
    compteur_skill = 0
    skkkk = []
    pkkkk = []

    for i in sk:
        if compteur_skill <= 10:
            skill_name = i['Skill']
            skkkk.append(skill_name)
            popularity = i['Popularité']
            pkkkk.append(popularity)
            skills_dictdom[skill_name] = popularity
            compteur_skill += 1

    y = np.array(pkkkk)
    mylabels = skkkk
    plt.pie(y, labels=mylabels)
    plt.savefig('static/images/my_plot_dom.png')
    return skills_dictdom


app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'


@app.route('/', methods=['GET', 'POST'])
def accueil():
    top_skills = get_count_of_skillstop3()
    jobs_data = get_top_3_job_names()
    skills, popularity = get_popularity_of_skills()

    return render_template('accueil.html', top_skills=top_skills, jobs_data=jobs_data, skills=skills,
                           popularity=popularity)


@app.route('/jobs', methods=['GET', 'POST'])
def display_jobs():
    jobs_data = get_all_info_for_all_jobs()
    length_of_jobs = len(jobs_data) if jobs_data else 0

    return render_template('jobsss.html', jobs_data=jobs_data, length=length_of_jobs)


@app.route('/skills', methods=['GET', 'POST'])
def display_skills():
    skills_dict = pop_skill()

    skills_dom = pop_skill_dom("business, administration and law")

    return render_template('skills.html', skills_dict=skills_dict, skills_dom=skills_dom)


@app.route('/search', methods=['GET', 'POST'])
def display_search():
    search_results = []
    domain_skills = []
    language_skills = []
    technique_skills = []

    if request.method == 'POST':
        # Process keyword search if present
        keyword = request.form.get('keyword')
        if keyword:
            search_results = get_all_info_for_a_jobb(keyword)

        selected_domains = request.form.getlist('domaine')
        for domain in selected_domains:
            skills = get_skills_by_domain(domain)
            for skill in skills:
                domain_skills.append({"Skill": skill})

        selected_languages = request.form.getlist('langue')
        for language in selected_languages:
            skills = get_skills_from_language(language)
            language_skills.extend(skills)

            #   selected_languages = request.form.getlist('langue')
            #  for language in selected_languages:
             #  skills = get_jobs_with_skill_and_description(language)
            #   language_skills.extend(skills)


            selected_techniques = request.form.getlist('technique')
            for technique in selected_techniques:
                skills = get_jobs_with_skill(technique)
                technique_skills.extend(skills)

    return render_template('search.html', search_results=search_results, domain_skills=domain_skills, language_skills=language_skills,technique_skills=technique_skills)


if __name__ == '__main__':
    app.run(debug=True)