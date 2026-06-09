# dashboard/app.py
# Road Safety Bénin — Dashboard Dash + Plotly

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# --- Layout ---
app.layout = html.Div([
    html.H1("Sécurité Routière au Bénin (2010–2022)",
            style={"textAlign": "center"}),
    # Les composants seront ajoutés ici
])

if __name__ == "__main__":
    app.run(debug=True)