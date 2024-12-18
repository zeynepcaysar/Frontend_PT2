from flask import Flask, render_template
import json
import matplotlib.pyplot as plt
import numpy as np

from requestss import get_skills_by_domain
from requestss import get_popular_skills_by_domain
from requestss import get_ict_skills
from requestss import get_language_skills
from requestss import get_skills_from_language
from requestss import get_transversal_skills

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('accueil.html')

if __name__ == '__main__':
    app.run(debug=True)





