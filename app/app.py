from flask import Flask, render_template, render_template_string, make_response, request, redirect, url_for

import json
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
import plotly

import cufflinks as cf

from pymongo import MongoClient

import numpy as np
import pandas as pd
import pickle as pk

app = Flask(__name__)
app.debug = True

# mongoDB connection
client = MongoClient()
db = client.petitions_db
coll = db.petitions

# load information to generate plotly & recs
prob_win = pd.read_pickle('prob_win.pkl')
tfidf_topics_df = pd.read_pickle('tfidf_topics_df.pkl')
with open('id_title_map.pkl', 'rb') as f:
    id_title_map = pk.load(f)
with open('dists10k.pkl', 'rb') as f:
    dists10k = pk.load(f)

petitions = list(tfidf_topics_df.index[:10000])
dists = pd.DataFrame(dists10k.toarray(), index=petitions, columns=petitions)
 
@app.route('/')
def my_form():
    graphs = [{'data': [{'marker': {'color': ['#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574',
     '#E06574'],
    'line': {'width': 1.3},
    'size': [88,
     34,
     64,
     112,
     52,
     24,
     24,
     20,
     16,
     53,
     34,
     32,
     46,
     18,
     12,
     49,
     12,
     29,
     17,
     21,
     52,
     19,
     15,
     77,
     16,
     22,
     16,
     25,
     17,
     36],
    'symbol': 'dot'},
   'mode': 'markers',
   'text': ['Animal Cruelty<br>Probability of Success: 0.14<br>Open Petitions: 1944<br>Lifetime supporters: 8184741<br>Themes: animals, dogs, shelter, abuse',
    'Children and Family<br>Probability of Success: 0.10<br>Open Petitions: 1401<br>Lifetime supporters: 2523596<br>Themes: child, parent, abuse, custody',
    'Community Issues<br>Probability of Success: 0.13<br>Open Petitions: 4311<br>Lifetime supporters: 5610054<br>Themes: community, public, board, development',
    'Criminal Justice<br>Probability of Success: 0.12<br>Open Petitions: 2964<br>Lifetime supporters: 10610531<br>Themes: family, life, prison, sentence',
    'Education - School Administration<br>Probability of Success: 0.12<br>Open Petitions: 1799<br>Lifetime supporters: 4354700<br>Themes: school, district, teachers, principal',
    'Education - Teaching<br>Probability of Success: 0.09<br>Open Petitions: 1977<br>Lifetime supporters: 1443199<br>Themes: students, education, teachers, test',
    'Education - University<br>Probability of Success: 0.11<br>Open Petitions: 1012<br>Lifetime supporters: 1459634<br>Themes: university, campus, faculty, tuition',
    'Environmental<br>Probability of Success: 0.08<br>Open Petitions: 830<br>Lifetime supporters: 1077167<br>Themes: water, fluoride, plastic, toxic',
    'First World Problems<br>Probability of Success: 0.05<br>Open Petitions: 1036<br>Lifetime supporters: 622455<br>Themes: want, play, love, rid',
    'Food, Farming and Livestock<br>Probability of Success: 0.17<br>Open Petitions: 892<br>Lifetime supporters: 4472739<br>Themes: eggs, farms, aramark, chickens',
    'Games<br>Probability of Success: 0.07<br>Open Petitions: 1871<br>Lifetime supporters: 2522997<br>Themes: games, football, xbox, pokemon',
    'Government - City<br>Probability of Success: 0.11<br>Open Petitions: 1205<br>Lifetime supporters: 2302354<br>Themes: city, council, mayor, ordinance',
    'Government - Federal and Foreign Policy<br>Probability of Success: 0.08<br>Open Petitions: 2372<br>Lifetime supporters: 3764349<br>Themes: obama, congress, america, syria',
    'Government - State<br>Probability of Success: 0.11<br>Open Petitions: 712<br>Lifetime supporters: 819523<br>Themes: county, commissioners, board, sheriff',
    'Harambe<br>Probability of Success: 0.06<br>Open Petitions: 337<br>Lifetime supporters: 213520<br>Themes: harambe, gorilla, death, memorial',
    'Healthcare<br>Probability of Success: 0.10<br>Open Petitions: 1532<br>Lifetime supporters: 4035964<br>Themes: marijuana, health, patients, cancer',
    'Income Inequality<br>Probability of Success: 0.09<br>Open Petitions: 234<br>Lifetime supporters: 171570<br>Themes: inquality, wealthiest, economic, extreme',
    'Legislature<br>Probability of Success: 0.12<br>Open Petitions: 1287<br>Lifetime supporters: 1966418<br>Themes: state, bill, law, governor',
    'Music<br>Probability of Success: 0.08<br>Open Petitions: 842<br>Lifetime supporters: 702830<br>Themes: music, band, album, artists',
    'Personal Issues<br>Probability of Success: 0.07<br>Open Petitions: 1334<br>Lifetime supporters: 1170414<br>Themes: please, help, support, share',
    'Police Brutality<br>Probability of Success: 0.08<br>Open Petitions: 1042<br>Lifetime supporters: 4368101<br>Themes: police, black, enforcement, brutality',
    'Politics - Democratic Party<br>Probability of Success: 0.04<br>Open Petitions: 1590<br>Lifetime supporters: 990971<br>Themes: sanders, clinton, vote, democratic',
    'Politics - Republican Party<br>Probability of Success: 0.04<br>Open Petitions: 831<br>Lifetime supporters: 492012<br>Themes: trump, republican, candidate, gop',
    'Power of the Crowd<br>Probability of Success: 0.07<br>Open Petitions: 6413<br>Lifetime supporters: 7024810<br>Themes: people, change, think, world',
    'Public Spaces and Infrastructure<br>Probability of Success: 0.08<br>Open Petitions: 739<br>Lifetime supporters: 593733<br>Themes: park, space, residents, recreation',
    'Safety<br>Probability of Success: 0.09<br>Open Petitions: 1495<br>Lifetime supporters: 1261798<br>Themes: traffic, intersection, speed, safety',
    'Tech and the Internet<br>Probability of Success: 0.08<br>Open Petitions: 701<br>Lifetime supporters: 614546<br>Themes: youtube, content, google, facebook',
    'Television<br>Probability of Success: 0.06<br>Open Petitions: 2122<br>Lifetime supporters: 1611652<br>Themes: fans, season, netflix, movie',
    'Weapons and Violence<br>Probability of Success: 0.08<br>Open Petitions: 594<br>Lifetime supporters: 728561<br>Themes: gun, violence, firearms, nra',
    "Women's Rights<br>Probability of Success: 0.13<br>Open Petitions: 1167<br>Lifetime supporters: 2756410<br>Themes: sexual, rape, transgender, women"],
   'type': 'scatter',
   'x': [0.1436123348017621,
    0.10307298335467349,
    0.1308467741935484,
    0.1254057244024786,
    0.12372138334145154,
    0.09890610756608934,
    0.11769834350479512,
    0.08690869086908691,
    0.053881278538812784,
    0.1725417439703154,
    0.07650542941757157,
    0.11592076302274394,
    0.08310784692694241,
    0.1133250311332503,
    0.06388888888888888,
    0.10356933879461673,
    0.09302325581395349,
    0.12627291242362526,
    0.08078602620087336,
    0.07489597780859916,
    0.08516242317822652,
    0.04504504504504504,
    0.04041570438799076,
    0.0746031746031746,
    0.08877928483353884,
    0.09007912355447352,
    0.08842652795838751,
    0.0618921308576481,
    0.0847457627118644,
    0.13104988830975428],
   'y': [1944,
    1401,
    4311,
    2964,
    1799,
    1977,
    1012,
    830,
    1036,
    892,
    1871,
    1205,
    2372,
    712,
    337,
    1532,
    234,
    1287,
    842,
    1334,
    1042,
    1590,
    831,
    6413,
    739,
    1495,
    701,
    2122,
    594,
    1167]}],
 'layout': {'legend': {'bgcolor': '#FFFFFF', 'font': {'color': '#4D5663'}},
  'paper_bgcolor': '#FFFFFF',
  'plot_bgcolor': '#FFFFFF',
  'title': 'Petition Topics by Frequency and Rate of Success',
  'titlefont': {'color': '#4D5663'},
  'xaxis1': {'gridcolor': '#E1E5ED',
   'showgrid': False,
   'tickfont': {'color': '#4D5663'},
   'title': 'Probability of Success',
   'titlefont': {'color': '#4D5663'},
   'zerolinecolor': '#E1E5ED'},
  'yaxis1': {'gridcolor': '#E1E5ED',
   'showgrid': False,
   'tickfont': {'color': '#4D5663'},
   'title': 'Number of Petitions Open',
   'titlefont': {'color': '#4D5663'},
   'zerolinecolor': '#E1E5ED'}}}]
    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',
                            ids=ids,
                            graphJSON=graphJSON)

@app.route('/', methods=['POST'])
def my_form_post():
    petition_id = request.form['text']
    return redirect(url_for('dashboard_maker', a=petition_id), code=302)

@app.route('/<a>/')
def dashboard_maker(a):
    # enter petition id
    # find petition name
    # show plotly
    # show recommendations with links to URLs
    petition_title = id_title_map[str(a)]
    df = pd.DataFrame(tfidf_topics_df.ix[petition_title])
    df.columns = ['Importance']
    df = df.reset_index().sort_values(by='index', ascending=True)

    figure = df.iplot(kind = 'bar', x = 'index', y = 'Importance', title=petition_title, 
              yTitle='Topic Importance', margin = (50,50,200,50), color='red', theme='white',
              asFigure=True)

    graphs = [figure]
    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    petition_group = [petition_title]
    petitions_summed = dists[petition_group].apply(lambda row: np.sum(row), axis=1)
    petitions_summed = petitions_summed.sort_values(ascending=False)
    ranked_petitions = petitions_summed.index[petitions_summed.index.isin(petition_group)==False]
    ranked_petitions = ranked_petitions.tolist()
    similar = ranked_petitions[:10]

    return render_template('graphs.html',
                           ids=ids,
                           graphJSON=graphJSON,
                           similar=similar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)