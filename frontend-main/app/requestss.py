import pprint
import webbrowser
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import FOAF, RDF, RDFS

from rdflib import Graph, URIRef, Literal

g = Graph()

ex = Namespace("http://example.org/")  # utiliser ça quand c'est nous qui avons créé le type

rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

g.parse("RDF_final.ttl", format="turtle")


# LISTE DE TOUS LES JOBS
def get_all_jobs():
    list_jobs = []

    requete = g.query(
        """SELECT ?label
           WHERE {{
             ?job rdf:type ns1:Job . 
             ?job rdfs:label ?label .
           }}  
        """
    )

    for i in requete:
        list_jobs.append(i[0])
        print(i[0])


# LISTE DE TOUS LES SKILLS

def get_all_skills():
    list_skills = []

    requete = g.query(
        """SELECT ?label
           WHERE {{
             ?skill rdf:type ns1:Skill . 
             ?skill rdfs:label ?label .
           }}  
        """
    )

    for i in requete:
        list_skills.append(i[0])
        print(i[0])


# LITSE DE TOUTES LES COMPANY
def get_all_company():
    list_company = []

    requete = g.query(
        """SELECT ?label
           WHERE {{
             ?company rdf:type ns1:Company . 
             ?company rdfs:label ?label .
           }}  
        """
    )

    for i in requete:
        list_company.append(i[0])
        print(i[0])


# LISTE DE TOUS LES PAYS
def get_all_countries():
    list_countries = []

    requete = g.query(
        """SELECT ?label
           WHERE {{
             ?country rdf:type ns1:Country . 
             ?country rdfs:label ?label .
           }}  
        """
    )

    for i in requete:
        list_countries.append(i[0])
        print(i[0])


# LISTE DE TOUTES LES INFOS SUR UN JOB, METTRE EN ENTREE DE LA FONCTION UN MOT CLE POUR TROUVER
# TOUS LES JOBS CORRESPONDANTS

def get_all_info_for_a_job(input_job):
    requete = g.query(
        """SELECT ?label ?description ?location ?company ?country ?url (GROUP_CONCAT(DISTINCT ?skill; separator=" ; ") AS ?skills) (GROUP_CONCAT(DISTINCT ?type; separator=" ; ") AS ?types)
           WHERE {{
             ?job rdf:type ns1:Job .
             ?job rdfs:label ?label .
             ?job ns1:hasDescription ?description .
             ?job ns1:atLocation ?location .
             ?job ns1:forCompany ?company_url .
             ?company_url rdfs:label ?company .
             ?job ns1:atCountry ?country_url .
             ?country_url rdfs:label ?country .
             ?job ns1:hasType ?type .
             ?job ns1:hasURL ?url .
             ?job ns1:hasSkill ?skill .
             
             FILTER(CONTAINS(?label, "{}"))
             
           }}  GROUP BY ?job
        """.format(input_job)
    )

    # i correspond à chaque job trouvé, on itère sur ce i (le job) pour avoir toutes les infos (skill, country, etc...)

    for i in requete:
        job = i[0]
        print(job)

        description = i[1]
        print(description)

        location = i[2]
        print(location)

        company = i[3]
        print(company)

        country = i[4]
        print(country)

        url = i[5]
        print(url)

        list_skills = i[6]
        print(list_skills)

        list_type = i[7]
        print(list_type)


# added search results to return to the function display search
def get_all_info_for_a_jobb(input_job):
    requete = g.query(
        """SELECT ?label ?description ?location ?company ?country ?url (GROUP_CONCAT(DISTINCT ?skill; separator=" ; ") AS ?skills) (GROUP_CONCAT(DISTINCT ?type; separator=" ; ") AS ?types)
                   WHERE {{
                     ?job rdf:type ns1:Job .
                     ?job rdfs:label ?label .
                     ?job ns1:hasDescription ?description .
                     ?job ns1:atLocation ?location .
                     ?job ns1:forCompany ?company_url .
                     ?company_url rdfs:label ?company .
                     ?job ns1:atCountry ?country_url .
                     ?country_url rdfs:label ?country .
                     ?job ns1:hasType ?type .
                     ?job ns1:hasURL ?url .
                     ?job ns1:hasSkill ?skill .

                     FILTER(CONTAINS(?label, "{}"))

                   }}  GROUP BY ?job
                """.format(input_job)
    )

    search_results = []  # Initialize an empty list to hold the job details

    for i in requete:
        # Create a dictionary for each job and add it to the search_results list
        job_details = {
            'job': i[0],
            'description': i[1],
            'location': i[2],
            'company': i[3],
            'country': i[4],
            'url': i[5],
            'skills': i[6],
            'types': i[7]
        }
        search_results.append(job_details)

    return search_results


# get all info for all jobs
def get_all_info_for_all_jobs():
    jobs_info = []  # List to hold information for all jobs

    requete = g.query(
        """
        
        SELECT ?label ?description ?location ?company ?country ?url (GROUP_CONCAT(DISTINCT ?skill; separator=" ; ") AS ?skills)
        WHERE {
            ?job rdf:type ns1:Job .
            ?job rdfs:label ?label .
            ?job ns1:hasDescription ?description .
            ?job ns1:atLocation ?location .
            ?job ns1:forCompany ?company_url .
            ?company_url rdfs:label ?company .
            ?job ns1:atCountry ?country_url .
            ?country_url rdfs:label ?country .
            ?job ns1:hasURL ?url .
            ?job ns1:hasSkill ?skill .
        }
        GROUP BY ?job
        """
    )

    for i in requete:
        skills_list = [skill.split('/')[-1] for skill in i['skills'].split(" ; ")] if i['skills'] else []
        job_info = {
            'positionName': i['label'].split('/')[-1],
            'description': i['description'],
            'location': i['location'].split('/')[-1],
            'company': i['company'].split('/')[-1],
            'country': i['country'].split('/')[-1],
            'full_url': i['url'],  # Keep the full URL for linking purposes
            'esco_skills': skills_list
        }
        jobs_info.append(job_info)

    return jobs_info


# get 3 jobs
def get_top_3_job_names():
    job_names = []  # List to hold the names of the top 3 jobs

    requete = g.query(
        """
        
        SELECT ?label
        WHERE {
            ?job rdf:type ns1:Job .
            ?job rdfs:label ?label .
        }
        LIMIT 3
        """
    )

    for row in requete:
        job_names.append(str(row.label))

    return job_names


# POPULARITE DE TOUS LES SKILLS
def get_count_of_skills():
    requete = g.query(
        """SELECT ?skill (COUNT(?job) as ?count)
           WHERE {{
             ?job rdf:type ns1:Job .
             ?job rdfs:label ?label .
             ?job ns1:hasSkill ?skill .

           }}  GROUP BY ?skill
        """
    )

    for i in requete:
        skill = i[0]
        popularite = i[1]

        print(f"Skill : {skill} Popularite : {popularite} ")


def get_count_of_skillstop3():
    requete = g.query(
        """SELECT ?skill (COUNT(?job) AS ?count)
           WHERE {
             ?job rdf:type ns1:Job .
             ?job rdfs:label ?label .
             ?job ns1:hasSkill ?skill .
           }
           GROUP BY ?skill
           ORDER BY DESC(?count)
           LIMIT 3
        """
    )

    top_skills = []
    for row in requete:
        skill_uri = str(row[0])
        skill_name = skill_uri.split('/')[-1]
        skill_name = skill_name.replace('_', ' ')
        skill_name = skill_name.title()
        top_skills.append(skill_name)

    return top_skills


# Pour faire marcher la fonction get_all_info_for_a_job(input_job) :
'''input_job = str(input("Entrer un mot-clé pour trouver un job correspondant : "))
get_all_info_for_a_job(input_job)'''


# POPULARITE DE TOUS LES SKILLS
def get_count_of_skills():
    list_skill = []
    list_pop = []

    g.parse("RDF_final.ttl", format="turtle")
    requete = g.query(
        """SELECT ?skill_label (COUNT(?job) as ?count)
           WHERE {{
             ?job rdf:type ns1:Job .
             ?job rdfs:label ?label .
             ?job ns1:hasSkill ?skill .
             ?skill rdfs:label ?skill_label .

           }}  GROUP BY ?skill
           ORDER BY DESC(COUNT(?job))
        """
    )

    for i in requete:
        list_skill.append(i[0])
        list_pop.append(i[1])

    return list_skill, list_pop

    # skill = i[0]
    # popularite = i[1]
    # print(f"Skill : {skill} Popularite : {popularite} ")


'''def get_popular_skills_by_domain():

    g.parse("RDF_skills_with_categories.ttl", format="turtle")

    popularity = get_count_of_skills()

    for i in popularity:

        skill = i[0]
        popularite = i[1]

        print(f"Skill : {skill} Popularite : {popularite} ")'''

# Pour faire marcher la fonction get_all_info_for_a_job(input_job) :
'''input_job = str(input("Entrer un mot-clé pour trouver un job correspondant : "))
get_all_info_for_a_job(input_job)'''


# res_pop = get_count_of_skills()

# list_skill, list_pop = res_pop

# compteur_skill = 0

# for i in list_skill:
# print(f"Skill : {i} Popularite : {list_pop[compteur_skill]} ")

# compteur_skill += 1


def get_skills_by_domain(domain_name):
    g = Graph()

    # list_domain = get_all_domains()
    list_skills = []

    g.parse("RDF_skills_with_categories.ttl", format="turtle")

    requete = g.query(
        """SELECT ?skill_label 
           WHERE {{
                    ?skill ns1:category ?domain .
                    ?domain rdfs:label "{}" .
                    ?skill rdfs:label ?skill_label . 
                 }}
        """.format(domain_name)
    )

    for i in requete:
        label = i['skill_label'].value

        list_skills.append(label)

    g.close()

    return list_skills


def get_all_skills():
    g = Graph()
    g.parse("RDF_final.ttl", format="turtle")
    list_skills = []

    requete = g.query(
        """SELECT ?label
           WHERE {{
             ?skill rdf:type ns1:Skill . 
             ?skill rdfs:label ?label .
           }}  
        """
    )

    for i in requete:
        label = i['label'].value

        list_skills.append(label)
        # print(i[0])

    g.close()
    return list_skills


def get_popular_skills_by_domain(domain_name):
    skills_of_domain = get_skills_by_domain(
        domain_name)  # retourne une liste de skills du domaine

    all_jobs_skills = get_all_skills()

    skill_matching = []

    for i in skills_of_domain:

        for j in all_jobs_skills:

            if i in j:
                # print(f"Correspondance trouvée pour {j}")

                skill_matching.append(j)

    g = Graph()

    g.parse("RDF_final.ttl", format="turtle")

    resultats_skills = []

    for k in skill_matching:

        requete = g.query(
            """SELECT (COUNT(?job) as ?count)
               WHERE {{
                        ?job rdf:type ns1:Job .
                        ?job rdfs:label ?label .
                        ?job ns1:hasSkill ?skill .
                        ?skill rdfs:label "{}" .
                     }}
                    GROUP BY ?res
                    ORDER BY DESC(COUNT(?job))
            """.format(k)
        )

        for result in requete:
            count_value = result['count'].value
            # print(f"Skill: {k}, Popularité: {count_value}")
            resultats_skills.append({"Skill": k, "Popularité": int(count_value)})

    g.close()

    resultats_skills = sorted(resultats_skills, key=lambda x: x["Popularité"], reverse=True)

    # Afficher les résultats triés
    # for result in resultats_skills:
    # print(f"Skill: {result['Skill']}, Popularité: {result['Popularité']}")

    return resultats_skills


def get_ict_skills():
    g = Graph()

    g.parse("RDF_ICT_skills.ttl", format="turtle")

    list_skills = []

    requete = g.query(
        """SELECT ?skill_label
           WHERE {{
                    ?skill rdf:type ns1:ICTSkill .
                    ?skill rdfs:label ?skill_label .
                 }}
                GROUP BY ?skill_label 
        """
    )

    for i in requete:
        label = i['skill_label'].value

        list_skills.append(label)

    g.close()

    return list_skills


'''def get_popularity_ICT_skills():

    all_jobs_skills = get_all_skills()

    ict_skills = get_ict_skills()

    skill_matching = []

    for i in ict_skills:

        for j in all_jobs_skills:

            if i in j:

                print(f"Correspondance trouvée pour {j}")

                skill_matching.append(j)

    g = Graph()

    g.parse("RDF_final.ttl", format="turtle")

    resultats_skills = []

    for k in skill_matching:

        requete = g.query(
            """SELECT (COUNT(?job) as ?count)
               WHERE {{
                        ?job rdf:type ns1:Job .
                        ?job rdfs:label ?label .
                        ?job ns1:hasSkill ?skill .
                        ?skill rdfs:label "{}" .
                     }}
                    GROUP BY ?res
                    ORDER BY DESC(COUNT(?job))
            """.format(k)
        )

        for result in requete:
            count_value = result['count'].value
            # print(f"Skill: {k}, Popularité: {count_value}")
            resultats_skills.append({"Skill": k, "Popularité": int(count_value)})

    g.close()

    resultats_skills = sorted(resultats_skills, key=lambda x: x["Popularité"], reverse=True)

    # Afficher les résultats triés
    for result in resultats_skills:
        print(f"Skill: {result['Skill']}, Popularité: {result['Popularité']}")

    return resultats_skills'''


def get_language_skills():
    g = Graph()

    g.parse("RDF_language_skills.ttl", format="turtle")

    list_skills = []

    requete = g.query(
        """SELECT ?skill
           WHERE {{
                    ?skill rdf:type ns1:LanguageSkill .

                 }}
                GROUP BY ?skill
        """
    )

    for i in requete:
        segments = str(i).split('/')

        # Obtenez le dernier segment en utilisant le dernier élément de la liste
        dernier_segment = segments[-1]

        nouveau_mot = dernier_segment[:-4]

        # label = i['skill'].value

        list_skills.append(nouveau_mot)

    g.close()

    return list_skills


# POPULARITE DE TOUS LES SKILLS DEMANDES POUR LES JOBS, copy from requetes de backend
def get_popularity_of_skills():
    g = Graph()

    list_skill = []
    list_pop = []

    g.parse("RDF_final.ttl", format="turtle")
    requete = g.query(
        """SELECT ?skill_label (COUNT(?job) as ?count)
           WHERE {{
             ?job rdf:type ns1:Job .
             ?job rdfs:label ?label .
             ?job ns1:hasSkill ?skill .
             ?skill rdfs:label ?skill_label .

           }}  GROUP BY ?skill
           ORDER BY DESC(COUNT(?job))
        """
    )

    for i in requete:
        list_skill.append(i[0])
        list_pop.append(i[1])
    g.close()

    return list_skill, list_pop


def get_skills_from_language(language):
    g = Graph()

    g.parse("RDF_language_skills.ttl", format="turtle")

    list_skills = []

    requete = g.query(
        """SELECT ?skill_label
           WHERE {{

                    ?skill rdf:type ns1:{} .
                    ?skill rdfs:label ?skill_label .

                 }}
                GROUP BY ?skill_label
        """.format(language)
    )

    for i in requete:
        label = i['skill_label'].value

        list_skills.append(label)

    g.close()

    return list_skills


def get_transversal_skills():
    g = Graph()

    g.parse("RDF_transversal_skills.ttl", format="turtle")

    list_skills = []

    requete = g.query(
        """SELECT ?skill_label
           WHERE {{
                    ?skill rdf:type ns1:TransversalSkill .
                    ?skill rdfs:label ?skill_label .
                 }}
                GROUP BY ?skill_label 
        """
    )

    for i in requete:
        label = i['skill_label'].value

        list_skills.append(label)

    g.close()

    return list_skills


# Pour faire marcher la fonction get_all_info_for_a_job(input_job) :
'''input_job = str(input("Entrer un mot-clé pour trouver un job correspondant : "))
get_all_info_for_a_job(input_job)'''

# accéder aux popularités

'''res_pop = get_count_of_skills()

list_skill, list_pop = res_pop

compteur_skill = 0

for i in list_skill:

    print(f"Skill : {i} Popularite : {list_pop[compteur_skill]} ")

    compteur_skill+=1'''

# accéder aux skills en fonction d'un domaine précis

'''res = get_skills_by_domain("agriculture, forestry, fisheries and veterinary")
print(res)'''

# print(get_skills_by_domain("business, administration and law"))
# print(get_popular_skills_by_domain("business, administration and law"))


# get_popular_skills_by_domain("business, administration and law")


'''for i in get_transversal_skills():
    print(i)'''

# get_popularity_ICT_skills()

'''for i in get_skills_from_language("French"):
    print(i)'''
