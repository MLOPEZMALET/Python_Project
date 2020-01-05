# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import stopwords
import io
import instruments
import re
import operator
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
from spacy.lang.fr import French

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
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    # text = io.StringIO(decoded.decode('utf-8'))
    text = decoded.decode("utf-8")
    return html.Div(
        [
            html.H6("Aperçu du texte contenu dans: " + filename),
            html.H6(text[:300])

            # horizontal line
            # For debugging, display the raw contents provided by the web browser
            # html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #    'whiteSpace': 'pre-wrap',
            #    'wordBreak': 'break-all'
            # })
        ]
    )


def tokenizer(contents):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    new = re.sub(r'[^\w\s]', '', text)
    liste = new.split()
    return liste



def count_freq(liste):
    liste_of_frequence = [liste.count(w) for w in liste]
    dictionary = dict(zip(liste, liste_of_frequence))
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict


def count_freq_sans_mot_vides(liste):
    dicvide = stopwords.motsvides
    liste = [e for e in liste if e not in dicvide]
    liste_of_frequence = [liste.count(w) for w in liste]
    dictionary = dict(zip(liste, liste_of_frequence))
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dict, instruments.wordcl(dictionary)
def ponctuation(liste):
    cptinterog=0
    for e in liste:
        if '?' in e:
            cptinterog+=1
#combien de phrases exclamatives?
    cptex=0
    for e in liste:
        if '!' in e:
            cptex+=1
    #combien de phrases avec ...?
    cptpts=0
    for e in liste:
        if '...' in e:
            cptpts+=1
    return [['!',cptex],['?',cptinterog],['...',cptpts]]
    
def generate_table_ponctuation(contents, filename):
    mots = tokenizer(contents)
    ponct= ponctuation(mots)
    df_ponct = pd.DataFrame(dict_ponct, columns=["Signe de ponctuation", "Fréquence"])

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_ponct.columns])] +

        # Body
        [html.Tr([
            html.Td(df_ponct.iloc[i][col]) for col in df_ponct.columns
        ]) for i in range(3)],
        style={
            "borderStyle": "double",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"

        }
    )

def generate_table(contents, filename):
    mots = tokenizer(contents)
    dict_freq = count_freq(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots", "Fréquence"])

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_freq.columns])] +

        # Body
        [html.Tr([
            html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
        ]) for i in range(min(len(df_freq), 10))],
        style={
            "borderStyle": "double",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"

        }
    )


def generate_table_2(contents, filename):
    mots = tokenizer(contents)
    dict_freq, wordcloud = count_freq_sans_mot_vides(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots", "Fréquence"])

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_freq.columns])] +

        # Body
        [html.Tr([
            html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
        ]) for i in range(min(len(df_freq), 10))],
        style={
            "borderStyle": "double",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"
        },
    )


def generate_table_voc(contents, filename):
    mots = nlp_fr(contents)
    lemmes = [token.lemma_ for token in mots]
    print(lemmes)
    nb_mots = len(lemmes)
    print(nb_mots)
    mots_uniques = len(set(lemmes))
    print(mots_uniques)
    stat = {
        "nb": ["Nombre de mots uniques dans le document: ", mots_uniques],
        "nb2": ["Nombre de mots total du document: ", nb_mots],
        "nb3": ["Richesse du vocabulaire: ", round(mots_uniques/nb_mots, 3)]
         }
    print(stat)
    df_freq = pd.DataFrame.from_dict(stat, orient="index", columns=["Mesure", "Valeur"])

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_freq.columns])] +

        # Body
        [html.Tr([
            html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
        ]) for i in range(min(len(df_freq), 10))],
        style={
            "borderStyle": "double",
            "width": "100px",
            "margin": "auto",
            "margin-bottom": "20px",
            "padding": "20px"
        },
    )

# COMPOSANTES DE L'APPLICATION_________________________________________________


app.layout = html.Div(
    id="alignment-body",
    className="app-body",
    style={
        'backgroundColor': colors["background"],
        'columnCount': 1
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
                "color": colors["text"]
                },
            ),
        html.Div(
            style={
                'backgroundColor': colors["background"],
                'columnCount': 1,
                "margin-bottom": "50px",
                },
            children=[
                html.Div(
                    id="alignment-control-tabs",
                    className="control-tabs",
                    style={
                        "width": "100%",
                        "height": "100px",
                        "lineHeight": "20px",
                        "textAlign": "center",
                        "margin": "10px",
                        "padding": "10px"
                    },
                    children=[
                        dcc.Tabs(
                            id="alignment-tabs",
                            value="what-is",
                            style={
                                "width": "100%",
                                "height": "60px",
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
                                            "height": "60px",
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
                                                    "height": "60px",
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
                                            html.Label(
                                                className="config",
                                                children="Sélectionnez les informations souhaitées",
                                                style={
                                                    "width": "100%",
                                                    "height": "30px",
                                                    "lineHeight": "30px",
                                                    "textAlign": "center",
                                                    "margin": "10px"
                                                    }
                                                ),
                                            html.Label('Mots les plus fréquents (sans mots grammaticaux)'),
                                                dcc.RadioItems(
                                                    id="freq",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
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
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.Label("Analyse de sentiments"),
                                                dcc.RadioItems(
                                                    id="sentiment",
                                                    options=[
                                                        {'label': 'OUI', 'value': 'O'},
                                                        {'label': 'NON', 'value': 'N'},
                                                        ],
                                                    value='O',
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
                                                    labelStyle={'display': 'inline-block'}
                                                    ),
                                            html.P(" "),
                                            html.Button(id='submit-button', n_clicks=0, children='Valider'),
                                            html.P(" "),
                                            html.P(id="display-selected-values"),
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
            id="outputs",
            style={"columnCount": 3},
            children=[
                html.Div(id="output-apercu", style={}),
                html.Div(
                    id="output-tableau-freq",
                    style={
                        "width": "100%"
                        },
                    ),
                html.Div(
                    id="output-tableau-freq-sansmotsvides",
                    style={"width": "100%"}
                )
            ]
        ),
        html.Div(
            id="outputs2",
            style={"columnCount": 3},
            children=[
                html.Div(
                    id="output-tableau-voc",
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
     State("sentiment", "value"),
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
def update_df2(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_2(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________tableau fréquence avec mots vides


@app.callback(
    Output("output-tableau-freq", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("stop_in_freq", "value")],
)
def update_df(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table(c, n) for c, n in zip(list_of_contents, list_of_names)
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

# ___________ TODO: graphique fréquence

# ___________ TODO: éventuellement, si temps, fréquence d'un mot en particulier précisé par l'utilisateur

# ___________ TODO: étendue du vocabulaire

@app.callback(
    Output("output-tableau-voc", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("voc", "value")],
)
def update_df(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_voc(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children
# ____________tableau fréquence de ponctuation


#@app.callback(
    #Output("output-tableau-freq", "children"),
    #[Input("upload-data", "contents")],
    #[State("upload-data", "filename"), State("stop_in_freq", "value")],
#)
#def update_df(list_of_contents, list_of_names, value):
   # if list_of_contents is not None and value == "O":
       # children = [
           # generate_table_ponctuation(c, n) for c, n in zip(list_of_contents, list_of_names)
       # ]
      #  return children

# ___________ TODO: analyse de ponctuation



# ___________ TODO: analyse de sentiments



# ___________ TODO: mot donné dans contexte



if __name__ == "__main__":
    app.run_server(debug=True)
