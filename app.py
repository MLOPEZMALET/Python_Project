# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import io
import re
import operator

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
        ]) for i in range(min(len(df_freq), 10))]
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
                                            html.P("L'analyseur est une application qui vous permet d'obtenir des informations sur votre corpus. Les résultats d'une analyse informatique peuvent ainsi lancer ou enrichir vos pistes de réflexion."),
                                            html.P("Comment faire? C'est très simple: vous choisissez ce que vous voulez obtenir comme résultats dans l'onglet configuration puis vous déposez votre corpus (en format .txt) dans l'onglet Data."),
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
                                            dcc.Checklist(
                                                options=[
                                                    {
                                                        "label": "Mots les plus fréquents (sans mots grammaticaux)",
                                                        "value": "FREQ",
                                                    },
                                                    {
                                                        "label": "Mots les plus fréquents (parmi tous)",
                                                        "value": "FREQSTOP",
                                                    },
                                                    {
                                                        "label": "Structures syntaxiques les plus fréquentes",
                                                        "value": "STX",
                                                    },
                                                    {
                                                        "label": "Étendue du vocabulaire",
                                                        "value": "VOC",
                                                    },
                                                    {
                                                        "label": "Analyse de la ponctuation",
                                                        "value": "PONCT",
                                                    },
                                                    {
                                                        "label": "Analyse de sentiments",
                                                        "value": "SENT",
                                                    },
                                                ],
                                                value=["FREQ", "FREQSTOP", "STX", "VOC", "PONCT" "SENT"],
                                                style={
                                                    "textAlign": "center",
                                                },
                                            ),
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
            children=[
                html.Div(id="output-apercu"),
                html.Div(id="output-tableau-freq")
                ]
            )

    ],
)

# DYNAMISME DE L'APPLICATION_________________________________________________


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


@app.callback(
    Output("output-tableau-freq", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
)
def update_df(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            generate_table(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children


if __name__ == "__main__":
    app.run_server(debug=True)
