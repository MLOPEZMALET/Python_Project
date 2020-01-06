# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import spacy
import stopwords
import io
import instruments
import re

import operator
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import spacy
from spacy.lang.fr import French
nlp = spacy.load('fr_core_news_sm')

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# df = pd.read_fwf("vero.txt", sep="\t")
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# STYLE_____________________________________________

colors = {
    "background": "#F5F5DC",
    "tabsBackground": "#FFFFFF",
    "text": "#191970"
}

# FONCTIONS SUR LE CONTENU_____________________________________________________

nlp_fr = French()


def parse_contents(contents, filename):
    """decodes text files and shows an overview of their content"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    # text = io.StringIO(decoded.decode('utf-8'))
    text = decoded.decode("utf-8")
    return html.Div(
        [
            html.H6("Aperçu du texte contenu dans: " + filename, style={"textAlign": "center"}),
            html.I(text[:350]),
            html.Hr()
        ]
    )


def tokenizer(contents):
    """splits text into tokens and returns them in a list"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    new = re.sub(r'[^\w\s]', '', text)
    liste = new.lower().split()
    return liste
    
def freq_postags(doc):
    t=[ word.pos_ for word in doc]
    liste_of_frequence= [t.count(e) for e in t]
    #les valeurs seront les nombres d'occurences dans le deuxieme liste(liste_of_frequence)
    dictionary = dict(zip(t,liste_of_frequence))
    #list_key_value = [ [k,v] for v, k in dictionary.items() ]
    #freqplot(dictionary)
    #for w in sorted(dictionary, key=dictionary.get, reverse=True):
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict
    
def generate_table_postags(contents, filename):
    """creates a table with the punctuation statistics"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    doc = nlp(text)
    dict_postags = freq_postags(doc)
    df_postags = pd.DataFrame(dict_postags, columns=["Partie de discours", "Fréquence"])

    return html.Div([
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_postags.columns])] +
            # Body
            [html.Tr([html.Td(df_postags.iloc[i][col]) for col in df_postags.columns]) for i in range(min(len(df_postags), 14))],
            style={
                "borderStyle": "none",
                "width": "100px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                },
            ),
    ])
    
def count_freq(liste):
    """counts the occurrencies of each word and returns a sorted dictionary"""
    liste_of_frequence = [liste.count(w) for w in liste]
    dictionary = dict(zip(liste, liste_of_frequence))
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict


def count_freq_sans_mot_vides(liste):
    """same as count_freq but doesn't take into account the stopwords"""
    dicvide = stopwords.motsvides
    liste = [e for e in liste if e not in dicvide]
    liste_of_frequence = [liste.count(w) for w in liste]
    dictionary = dict(zip(liste, liste_of_frequence))
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict


def ponctuation(liste):
    """counts the occurrencies of each punctuation sign"""
    cptinterog = 0
    for e in liste:
        if '?' in e:
            cptinterog += 1
# combien de phrases exclamatives?
    cptex = 0
    for e in liste:
        if '!' in e:
            cptex += 1
    # combien de phrases avec ...?
    cptpts = 0
    for e in liste:
        if '...' in e:
            cptpts += 1
    # phrases déclaratives
    cpt = 0
    for e in liste:
        if '.' in e:
            cpt += 1
    # deux points
    cdeuxpts = 0
    for e in liste:
        if ':' in e:
            cdeuxpts += 1
    # point virgule
    cptvirg = 0
    for e in liste:
        if ';' in e:
            cptvirg += 1
    # virgule
    cvirg = 0
    for e in liste:
        if ',' in e:
            cvirg += 1
    # TODO: ajouter guillemets? tirets longs? et autres?
    return [['!', cptex], ['?', cptinterog], ['...', cptpts], ['.', cpt], [':', cdeuxpts], [';', cptvirg], [',', cvirg]]


def generate_table_ponctuation(contents, filename):
    """creates a table with the punctuation statistics"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    doc_fr = nlp_fr(text)
    ponct = [str(token) for token in doc_fr if token.is_punct]
    dict_ponct = ponctuation(ponct)
    df_ponct = pd.DataFrame(dict_ponct, columns=["Signe de ponctuation", "Fréquence"])

    return html.Div([
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_ponct.columns])] +
            # Body
            [html.Tr([html.Td(df_ponct.iloc[i][col]) for col in df_ponct.columns]) for i in range(7)],
            style={
                "borderStyle": "none",
                "width": "100px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                },
            ),
    ])
def long_mots(doc):
    l1=[]
    l2=[]
    l3=[]
    l4=[]
    for token in doc:
        l1.append(len(token.text))
        l2.append(token.text)
    for e in l1:
        l3.append((l1.count(e),e))
    for e in sorted(l3):
        if e not in l4:
            l4.append(e)
    l5=dict(l4)
    l6=[]
    l7=[]
    for e in l4:
        if e[0]==1:
            l6.append(e[0])
            l7.append(e[1])
        else:
            l6.append(e[0])
            l7.append(e[1])
    dictionary = dict(zip(l7, l6))
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict

def generate_table_long_mots(contents, filename):
    """creates a table with the punctuation statistics"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    doc = nlp(text)
    dict_long = long_mots(doc)
    df_long = pd.DataFrame(dict_long, columns=["Longueur du mot", "Fréquence"])

    return html.Div([
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_long.columns])] +
            # Body
            [html.Tr([html.Td(df_long.iloc[i][col]) for col in df_long.columns]) for i in range(min(len(df_long), 20))],
            style={
                "borderStyle": "none",
                "width": "100px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                },
            ),
    ])

def generate_table_stopinfreq(contents, filename):
    """creates a table with term frequency values (with stopwords)"""
    mots = tokenizer(contents)
    dict_freq = count_freq_sans_mot_vides(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots", "Fréquence"])
    df_freq = df_freq[:20]

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_freq.columns])] +
        # Body
        [html.Tr([
            html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
        ]) for i in range(min(len(df_freq), 20))],
        style={
            "borderStyle": "none",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"

        }
    )


def generate_table_freq(contents, filename):
    """creates a table with term frequency values (no stopwords)"""
    mots = tokenizer(contents)
    dict_freq = count_freq(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots", "Fréquence"])
    df_freq = df_freq[:20]

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_freq.columns])] +

        # Body
        [html.Tr([
            html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
        ]) for i in range(min(len(df_freq), 20))],
        style={
            "borderStyle": "none",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"
        },
    )


def generate_table_voc(contents, filename):
    """creates a table with vocabulary variety statistics"""
    mots = nlp_fr(contents)
    lemmes = [token.lemma_ for token in mots]
    nb_mots = len(lemmes)
    mots_uniques = len(set(lemmes))
    stat = {
        "nb": ["Nombre de mots uniques dans le document: ", mots_uniques],
        "nb2": ["Nombre de mots total du document: ", nb_mots],
        "nb3": ["Richesse du vocabulaire: ", round(mots_uniques/nb_mots, 3)]
         }
    df_freq = pd.DataFrame.from_dict(stat, orient="index", columns=["Mesure", "Valeur"])

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_freq.columns])] +

        # Body
        [html.Tr([
            html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
        ]) for i in range(min(len(df_freq), 20))],
        style={
            "borderStyle": "none",
            "height": "auto",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"
        },
    )


def plot_freq(contents, filename):
    """plots the most frequent terms into a sorted bar chart"""
    mots = tokenizer(contents)
    dict_freq = count_freq(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots", "Fréquence"])
    df_freq = df_freq[:20]
    plot_freq = {
        "data": [
            {
                "y": df_freq["Mots"],
                "x": df_freq["Fréquence"],
                "type": "bar",
                "name": "frquence des mots",
                "orientation": "h",
                }
        ],
        "layout": {"height": "550", "margin": "10px"}
    }
    return dcc.Graph(figure=plot_freq)


    def plot_stopinfreq(contents, filename):
        """plots the most frequent terms into a sorted bar chart"""
        mots = tokenizer(contents)
        dict_freq = count_freq(mots)
        df_freq = pd.DataFrame(dict_freq, columns=["Mots", "Fréquence"])
        df_freq = df_freq[:20]
        plot_freq = {
            "data": [
                {
                    "y": df_freq["Mots"],
                    "x": df_freq["Fréquence"],
                    "type": "bar",
                    "name": "frquence des mots",
                    "orientation": "h",
                    }
            ],
            "layout": {"height": "550", "margin": "10px"}
        }
        return dcc.Graph(figure=plot_freq)


# COMPOSANTES DE L'APPLICATION_________________________________________________


app.layout = html.Div(
    id="alignment-body",
    className="app-body",
    style={
        'backgroundColor': colors["tabsBackground"],
        'columnCount': 1,
        'position': 'static'
        },
    children=[
        html.H1(
            children="Analyseur de texte",
            style={
                "textAlign": "center",
                "color": colors["text"]
                }
            ),
        html.Div(
            children="""Une interface pour une première analyse de corpus""",
            style={
                "textAlign": "center",
                "color": colors["text"],
                "margin-bottom": "15px"
                },
            ),
        html.Div(
            style={
                'backgroundColor': colors["tabsBackground"],
                'columnCount': 1,
                "margin-bottom": "50px",
                },
            children=[
                html.Div(
                    id="alignment-control-tabs",
                    className="control-tabs",
                    style={
                        "width": "100%",
                        "lineHeight": "20px",
                        "textAlign": "center",
                        "margin": "auto",
                        "padding": "10px"
                    },
                    children=[
                        dcc.Tabs(
                            id="alignment-tabs",
                            value="what-is",
                            style={
                                "width": "100%",
                                "lineHeight": "20px",
                                "textAlign": "center",
                                "margin": "10px",
                                "color": colors["text"]
                            },
                            children=[
                                dcc.Tab(
                                    label="Explication",
                                    value="what-is",
                                    children=html.Div(
                                        className="control-tab",
                                        style={
                                            "width": "100%",
                                            "lineHeight": "20px",
                                            "textAlign": "center",
                                            "margin": "10px",
                                        },
                                        children=[
                                            html.H4(
                                                className="what-is",
                                                children="Qu'est-ce qu'un analyseur de texte?",
                                                style={
                                                    "width": "100%",
                                                    "textAlign": "center",
                                                    "margin": "10px"
                                                },
                                            ),
                                            html.P(
                                                """L'analyseur est une application qui vous permet d'obtenir des informations sur votre corpus.
                                                Les résultats d'une analyse informatique peuvent ainsi lancer ou enrichir vos pistes de réflexion.
                                                En effet, le numérique permet de calculer rapidement des indicateurs et des statistiques précieuses pour un travail d'analyse textuelle.""",
                                                style={"margin-bottom": "20px"}
                                                ),
                                            html.P(
                                                "Comment faire?",
                                                style={"textAlign": "center", "margin-bottom": "2Opx"}
                                                ),
                                            html.P(
                                                """C'est très simple: vous choisissez ce que vous voulez obtenir comme résultats dans l'onglet configuration
                                                puis vous déposez votre corpus (en format .txt) dans l'onglet Data.""",
                                                style={"margin-bottom": "20px"}
                                            ),
                                            html.P(
                                                "Est-ce que je peux analyser deux documents pour les comparer?",
                                                style={"textAlign": "center", "margin-bottom": "2Opx"}
                                            ),
                                            html.P(
                                            "Oui, il suffit de les déposer à la fois, surtout pas l'un après l'autre. D'ailleurs, cela vous permettra de calculer les termes les plus spécifiques, entre autres"
                                            ),
                                            html.P("Voilà tout!"),
                                        ],
                                    ),
                                ),
                                dcc.Tab(
                                    label="Configuration",
                                    value="config",
                                    children=html.Div(
                                        className="control-tab",
                                        children=[
                                            html.H4(
                                                className="config",
                                                children="De quoi avez-vous besoin?",
                                                style={
                                                    "width": "100%",
                                                    "height": "60px",
                                                    "lineHeight": "60px",
                                                    "textAlign": "center",
                                                    "margin": "10px",
                                                },
                                            ),
                                            html.B(
                                                className="config",
                                                children="Sélectionnez les informations souhaitées",
                                                style={
                                                    "width": "100%",
                                                    "height": "30px",
                                                    "lineHeight": "30px",
                                                    "textAlign": "center",
                                                    "margin-bottom": "20px"
                                                    }
                                                ),
                                            html.Label('Voulez-vous comparer deux documents?(duplique les éléments sélectionnés + ajoute TF-IDF et mesure de spécificité)'),
                                                dcc.RadioItems(
                                                    id="multiple",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Label('Mots les plus fréquents (sans mots grammaticaux)'),
                                                dcc.RadioItems(
                                                    id="freq",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Label('Mots les plus fréquents (avec mots grammaticaux)'),
                                                dcc.RadioItems(
                                                    id="stop_in_freq",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Label("Structures syntaxiques les plus fréquentes"),
                                                dcc.RadioItems(
                                                    id="stx",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                                    html.Label("Longueur des mots"),
                                                dcc.RadioItems(
                                                    id="long",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),

                                            html.Label("Etendue du vocabulaire"),
                                                dcc.RadioItems(
                                                    id="voc",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Label("Analyse de la ponctuation"),
                                                dcc.RadioItems(
                                                    id="ponct",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Label("Contexte d'un terme donné"),
                                                dcc.RadioItems(
                                                    id="ctxt",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
                                                    style={"margin-bottom": "10px"},
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Button(id='submit-button', n_clicks=0, children='Valider'),
                                            html.P(" "),
                                            html.B(id="display-selected-values"),
                                            html.Hr(),
                                        ],
                                    ),
                                ),
                                dcc.Tab(
                                    label="Data",
                                    value="alignment-tab-select",
                                    children=html.Div(
                                        className="control-tab",
                                        children=[
                                            html.Div(
                                                className="app-controls-block",
                                                children=[
                                                    html.Div(
                                                        className="fullwidth-app-controls-name",
                                                    ),
                                                    dcc.Upload(
                                                        id="upload-data",
                                                        children=html.Div(
                                                            [
                                                                "Déposez votre fichier .txt ici ou ",
                                                                html.A(
                                                                    "sélectionnez-le"
                                                                ),
                                                            ]
                                                        ),
                                                        style={
                                                            "width": "100%",
                                                            "height": "60px",
                                                            "lineHeight": "60px",
                                                            "borderWidth": "1px",
                                                            "borderStyle": "dashed",
                                                            "borderRadius": "5px",
                                                            "textAlign": "center",
                                                            "margin": "10px",
                                                        },
                                                        # Allow multiple files to be uploaded
                                                        multiple=True,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),
        html.Div(
            id="output-apercu",
            style={"margin": "20px"}
            ),
        html.Div(
            id="outputs",
            style={
                "columnCount": 2,
                "margin": "10px"
            },
            children=[
                html.Div(
                    id="output-tableau-freq",
                    style={
                        "width": "auto"
                        },
                    ),
                html.Div(id="stopinfrequency_figure", style={"width": "auto"}),
                html.Div(
                    id="output-tableau-freq-sansmotsvides",
                    style={"width": "auto"}
                ),
                html.Div(id="frequency_figure", style={"width": "auto"})
            ]
        ),
        html.Div(
            id="outputs2",
            style={
                "columnCount": 3,
                "margin": "20px"
                },
            children=[
                html.Div(
                    id="output-tableau-voc",
                    style={"width": "100%"}
                ),
                html.Div(
                    id="output-tableau-ponct",
                    style={"width": "100%"}
                ),
                html.Div(
                    id="output-tableau-postags",
                    style={"width": "100%"}
                ),
                html.Div(
                    id="output-tableau-longueur",
                    style={"width": "100%"}
                ),
            ]
        )
    ]
)

# DYNAMISME DE L'APPLICATION_________________________________________________


# ____________aperçu du texte


@app.callback(
    Output("output-apercu", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________checkboxes


@app.callback(
    Output("display-selected-values", "children"),
    [Input('submit-button', 'n_clicks')],
    [State("freq", "value"),
     State("stop_in_freq", "value"),
     State("stx", "value"),
     State("ctxt", "value"),
     State("voc", "value"),
     State("ponct", "value")
     ]
 )
def update_output(n_clicks, *value):
    if n_clicks == 0:
        return "Veuillez enregistrer vos préférences"
    else:
        return "Vos préférences ont bien été enregistrées, à présent, déposez votre corpus dans l'onglet Data"

# ____________tableau fréquence sans mots vides


@app.callback(
    Output("output-tableau-freq-sansmotsvides", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("freq", "value")],
)
def update_df_freq(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_freq(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________tableau fréquence avec mots vides


@app.callback(
    Output("output-tableau-freq", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("stop_in_freq", "value")],
)
def update_df_stopinfreq(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_stopinfreq(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ___________ TODO: wordcloud

"""INTERESTING CODE FROM THE INTERNET (https://community.plot.ly/t/wordcloud-in-dash/11407/3)

words = dir(go)[:30]
colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
weights = [random.randint(15, 35) for i in range(30)]



data = go.Scatter(x=[random.random() for i in range(30)],
                 y=[random.random() for i in range(30)],
                 mode='text',
                 text=words,
                 marker={'opacity': 0.3},
                 textfont={'size': weights,
                           'color': colors})
layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
fig = go.Figure(data=[data], layout=layout)

plot(fig)
"""

# ___________graphique fréquence sans mots vides


@app.callback(
    Output("frequency_figure", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("freq", "value")]
)
def update_plot(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            plot_freq(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________graphique frequence avec mots motsvides

@app.callback(
    Output("stopinfrequency_figure", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("stop_in_freq", "value")]
)
def update_plot(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            plot_freq(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children


# ___________ TODO: éventuellement, si temps, fréquence d'un mot en particulier précisé par l'utilisateur

# ___________ TODO: étendue du vocabulaire VALEURS PAS VRAISEMBLABLES


@app.callback(
    Output("output-tableau-voc", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("voc", "value")],
)
def update_df_voc(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_voc(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________tableau fréquence de ponctuation


@app.callback(
    Output("output-tableau-ponct", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("ponct", "value")],
)
def update_df_ponct(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_ponctuation(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children


# ___________ TODO: mot donné dans contexte

# ____________TODO: POS Tags
@app.callback(
    Output("output-tableau-postags", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("stx", "value")],
)
def update_df_postags(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_postags(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children
# ____________TODO: longueur des mots
@app.callback(
    Output("output-tableau-longueur", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("long", "value")],
)
def update_df_postags(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_long_mots(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________TODO: tfidf

# ____________TODO: spécificité


if __name__ == "__main__":
    app.run_server(debug=True)
