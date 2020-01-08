# CODE TABLE GENERATION

def generate_table_postags(contents, filename):
    """creates a table with the syntaxic statistics"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    doc = nlp(text)
    dict_postags = freq_postags(doc)
    df_postags = pd.DataFrame(dict_postags, columns=["Partie du discours de " + filename, "Fréquence"])

    return html.Div([
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_postags.columns])] +
            # Body
            [html.Tr([html.Td(df_postags.iloc[i][col]) for col in df_postags.columns]) for i in range(min(len(df_postags), 14))],
            style={
                "borderStyle": "none",
                "width": "200px",
                "margin": "auto",
                "margin-bottom": "30px",
                "padding": "20px"
                },
            ),
    ])


def generate_table_sentences(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    dict_sentences = count_sentences(text)
    df_sentences = pd.DataFrame(dict_sentences, columns=["Longueur des phrases de " + filename, "Fréquence"])

    return html.Div(children=[
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_sentences.columns])] +
            # Body
            [html.Tr([html.Td(df_sentences.iloc[i][col]) for col in df_sentences.columns]) for i in range(min(len(df_sentences), 19))],
            style={
                "borderStyle": "none",
                "width": "200px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                },
            ),
    ])



def generate_table_long_mots(contents, filename):
    """creates a table with the word length statistics"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    text = decoded.decode("utf-8")
    doc = nlp(text)
    dict_long = long_mots(doc)
    df_long = pd.DataFrame(dict_long, columns=["Longueur des mots de " + filename, "Fréquence"])

    return html.Div(children=[
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_long.columns])] +
            # Body
            [html.Tr([html.Td(df_long.iloc[i][col]) for col in df_long.columns]) for i in range(min(len(df_long), 19))],
            style={
                "borderStyle": "none",
                "width": "200px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                },
            ),
    ])


def generate_table_stopinfreq(contents, filename):
    """creates a table with term frequency values (with stopwords)"""
    mots = tokenizer(contents)
    dict_freq = count_freq(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots dans " + filename, "Fréquence"])
    df_freq = df_freq[:20]

    return html.Div(children=[
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_freq.columns])] +
            # Body
            [html.Tr([
                html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
            ]) for i in range(min(len(df_freq), 20))],
            style={
                "borderStyle": "none",
                "width": "200px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                })
    ])


def generate_table_freq(contents, filename):
    """creates a table with term frequency values (no stopwords)"""
    mots = tokenizer(contents)
    dict_freq = count_freq_sans_mot_vides(mots)
    df_freq = pd.DataFrame(dict_freq, columns=["Mots dans " + filename, "Fréquence"])
    df_freq = df_freq[:20]

    return html.Div(children=[
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_freq.columns])] +

            # Body
            [html.Tr([
                html.Td(df_freq.iloc[i][col]) for col in df_freq.columns
            ]) for i in range(min(len(df_freq), 20))],
            style={
                "borderStyle": "none",
                "width": "200px",
                "margin": "auto",
                "margin-bottom": "20px",
                "padding": "20px"
                })
    ])

# CODE CALLBACKS

# ___________tableau fréquence sans mots vides


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

# ____________longueur des phrases


@app.callback(
    Output("output-tableau-longueur-phrases", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("long_phrase", "value")],
    )
def update_df_longueur_phrases(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_sentences(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children

# ____________longueur des mots


@app.callback(
    Output("output-tableau-longueur-mots", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("long_mot", "value")],
    )
def update_df_longueur_mots(list_of_contents, list_of_names, value):
    if list_of_contents is not None and value == "O":
        children = [
            generate_table_long_mots(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children
