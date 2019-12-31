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

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# df = pd.read_fwf("vero.txt", sep="\t")
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    # text = io.StringIO(decoded.decode('utf-8'))
    text = decoded.decode("utf-8")
    return html.Div(
        [
            html.H4("Aperçu du texte contenu dans: " + filename),
            html.H6(text[:300]),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            # html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #    'whiteSpace': 'pre-wrap',
            #    'wordBreak': 'break-all'
            # })
        ]
    )


def stats():
    phrases = len(list(text.split("\n")))
    return phrases


def count_freq(text):
    pass

# COMPOSANTES DE L'APPLICATION_________________________________________________

app.layout = html.Div(
    id="alignment-body",
    className="app-body",
    children=[
        html.H1(children="Analyseur de texte"),
        html.Div(children="""Une interface pour une première analyse de corpus"""),
        html.Div(
            [
                html.Div(
                    id="alignment-control-tabs",
                    className="control-tabs",
                    children=[
                        dcc.Tabs(
                            id="alignment-tabs",
                            value="what-is",
                            children=[
                                dcc.Tab(
                                    label="Explication",
                                    value="what-is",
                                    children=html.Div(
                                        className="control-tab",
                                        children=[
                                            html.H4(
                                                className="what-is",
                                                children="Qu'est-ce qu'un analyseur de texte?",
                                                style={
                                                    "width": "100%",
                                                    "height": "60px",
                                                    "textAlign": "center",
                                                    "margin": "10px",
                                                },
                                            ),
                                            html.P("L'analyseur est une application qui vous permet d'obtenir des informations sur votre corpus. Les résultats d'une analyse informatique peuvent ainsi lancer ou enrichir vos pistes de réflexion. C'est très simple:"),
                                            html.P("Comment faire? C'est très simple:vous choisissez ce que vous voulez obtenir comme résultats dans l'onglet configuration puis vous déposez votre corpus dans l'onglet Data. Voilà tout!")
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
                                            html.P("bliblabla"),
                                            html.Label(
                                                className="config",
                                                children="Checkboxes1",
                                                style={
                                                    "width": "100%",
                                                    "height": "60px",
                                                    "lineHeight": "60px",
                                                    "textAlign": "left",
                                                    "margin": "10px"
                                                    }
                                                ),
                                            dcc.Checklist(
                                                options=[
                                                    {
                                                        "label": "New York City",
                                                        "value": "NYC",
                                                    },
                                                    {
                                                        "label": u"Montréal",
                                                        "value": "MTL",
                                                    },
                                                    {
                                                        "label": "San Francisco",
                                                        "value": "SF",
                                                    },
                                                ],
                                                value=["NYC", "MTL", "SF"],
                                                style={
                                                    "textAlign": "left",
                                                },
                                            ),
                                            html.Label(
                                                className="config",
                                                children="Checkboxes2",
                                                style={
                                                    "width": "100%",
                                                    "height": "60px",
                                                    "lineHeight": "60px",
                                                    "textAlign": "center",
                                                    "margin": "10px"
                                                    }
                                                ),
                                            dcc.Checklist(
                                                options=[
                                                    {
                                                        "label": "New York City",
                                                        "value": "NYC",
                                                    },
                                                    {
                                                        "label": u"Montréal",
                                                        "value": "MTL",
                                                    },
                                                    {
                                                        "label": "San Francisco",
                                                        "value": "SF",
                                                    },
                                                ],
                                                value=["NYC", "MTL", "SF"],
                                                style={
                                                    "textAlign": "center",
                                                },
                                            ),
                                            html.Label(
                                                className="config",
                                                children="Checkboxes3",
                                                style={
                                                    "width": "100%",
                                                    "height": "60px",
                                                    "lineHeight": "60px",
                                                    "textAlign": "right",
                                                    "margin": "15px"
                                                    }
                                                ),
                                            dcc.Checklist(
                                                options=[
                                                    {
                                                        "label": "New York City",
                                                        "value": "NYC",
                                                    },
                                                    {
                                                        "label": u"Montréal",
                                                        "value": "MTL",
                                                    },
                                                    {
                                                        "label": "San Francisco",
                                                        "value": "SF",
                                                    },
                                                ],
                                                value=["NYC", "MTL", "SF"],
                                                style={
                                                    "textAlign": "right"
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
                                                        children="Select preloaded dataset",
                                                    ),
                                                    dcc.Upload(
                                                        id="upload-data",
                                                        children=html.Div(
                                                            [
                                                                "Déposez votre fichier ici ou",
                                                                html.A(
                                                                    " sélectionnez-le"
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
        html.Div(id="output-data-upload"),
        dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=[
                            1995,
                            1996,
                            1997,
                            1998,
                            1999,
                            2000,
                            2001,
                            2002,
                            2003,
                            2004,
                            2005,
                            2006,
                            2007,
                            2008,
                            2009,
                            2010,
                            2011,
                            2012,
                        ],
                        y=[
                            219,
                            146,
                            112,
                            127,
                            124,
                            180,
                            236,
                            207,
                            236,
                            263,
                            350,
                            430,
                            474,
                            526,
                            488,
                            537,
                            500,
                            439,
                        ],
                        name="Rest of world",
                        marker=dict(color="rgb(55, 83, 109)"),
                    ),
                    dict(
                        x=[
                            1995,
                            1996,
                            1997,
                            1998,
                            1999,
                            2000,
                            2001,
                            2002,
                            2003,
                            2004,
                            2005,
                            2006,
                            2007,
                            2008,
                            2009,
                            2010,
                            2011,
                            2012,
                        ],
                        y=[
                            16,
                            13,
                            10,
                            11,
                            28,
                            37,
                            43,
                            55,
                            56,
                            88,
                            105,
                            156,
                            270,
                            299,
                            340,
                            403,
                            549,
                            499,
                        ],
                        name="China",
                        marker=dict(color="rgb(26, 118, 255)"),
                    ),
                ],
                layout=dict(
                    title="US Export of Plastic Scrap",
                    showlegend=True,
                    legend=dict(x=0, y=1.0),
                    margin=dict(l=40, r=0, t=40, b=30),
                ),
            ),
            style={"height": 300},
            id="my-graph",
        )
        # html.H4("phrases"+str(stats(text)))
    ],
    style={'columnCount':1})

# DYNAMISME DE L'APPLICATION_________________________________________________

@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children


if __name__ == "__main__":
    app.run_server(debug=True)
