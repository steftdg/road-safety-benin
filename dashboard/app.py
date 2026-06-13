# -*- coding: utf-8 -*-
import os
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path

# --- Donnees ----------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
df_nat  = pd.read_csv(BASE / "data" / "processed" / "accidents_national.csv")
df_dept = pd.read_csv(BASE / "data" / "processed" / "accidents_departements.csv")

YEARS = sorted(df_nat["annee"].unique())
DEPTS = sorted(df_dept["departement"].unique())

last       = df_nat[df_nat["annee"] == 2022].iloc[0]
prev       = df_nat[df_nat["annee"] == 2019].iloc[0]
delta_tues = int(last["tues"] - prev["tues"])
delta_tx   = round(last["taux_mortalite"] - prev["taux_mortalite"], 1)
worst      = df_dept[df_dept["annee"] == 2022].sort_values("taux_mortalite", ascending=False).iloc[0]

# --- Palette ----------------------------------------------------------------
BG       = "#0f172a"
CARD     = "#1e293b"
BORDER   = "#334155"
RED      = "#ef4444"
ORANGE   = "#f97316"
BLUE     = "#38bdf8"
MUTED    = "#94a3b8"
WHITE    = "#f1f5f9"
FONT     = "Inter, system-ui, sans-serif"

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT, color=WHITE, size=12),
    margin=dict(t=50, b=40, l=60, r=20),
)

AXIS_STYLE = dict(gridcolor=BORDER, zerolinecolor=BORDER, color=WHITE, linecolor=BORDER)

def card_style(extra=None):
    s = {"background": CARD, "borderRadius": "12px", "padding": "20px",
         "marginBottom": "20px", "border": f"1px solid {BORDER}"}
    if extra:
        s.update(extra)
    return s

def kpi_block(value, label, color, sub=None):
    children = [
        html.Div(value, style={"fontSize": "2rem", "fontWeight": "800",
                               "color": color, "lineHeight": "1.1"}),
        html.Div(label, style={"fontSize": "0.75rem", "color": MUTED,
                               "marginTop": "4px", "textTransform": "uppercase",
                               "letterSpacing": "0.05em"}),
    ]
    if sub:
        children.append(html.Div(sub, style={"fontSize": "0.7rem", "color": color,
                                             "marginTop": "2px", "opacity": "0.8"}))
    return html.Div(children, style={
        "flex": "1", "minWidth": "140px", "padding": "16px",
        "background": BG, "borderRadius": "8px", "border": f"1px solid {BORDER}",
    })

# --- App --------------------------------------------------------------------
app = dash.Dash(__name__, title="Securite Routiere Benin")

app.index_string = f'''<!DOCTYPE html>
<html>
<head>
    {{%metas%}}
    <title>{{%title%}}</title>
    {{%favicon%}}
    {{%css%}}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: {BG}; font-family: {FONT}; color: {WHITE}; }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: {BG}; }}
        ::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}
        .rc-slider-rail {{ background: {BORDER} !important; }}
        .rc-slider-track {{ background: {BLUE} !important; }}
        .rc-slider-handle {{ border-color: {BLUE} !important; background: {BLUE} !important; }}
        .Select-control {{ background: {CARD} !important; border-color: {BORDER} !important; color: {WHITE} !important; }}
        .Select-menu-outer {{ background: {CARD} !important; border-color: {BORDER} !important; }}
        .Select-option {{ background: {CARD} !important; color: {WHITE} !important; }}
        .Select-option:hover {{ background: {BORDER} !important; }}
        .Select-value-label {{ color: {WHITE} !important; }}
        .Select-placeholder {{ color: {MUTED} !important; }}
        .VirtualizedSelectOption {{ background: {CARD} !important; color: {WHITE} !important; }}
    </style>
</head>
<body>
    {{%app_entry%}}
    <footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
</body>
</html>'''

app.layout = html.Div(style={"padding": "24px 32px", "maxWidth": "1400px", "margin": "0 auto"}, children=[

    # --- Header
    html.Div([
        html.Div([
            html.Div([
                html.Span("Sécurite Routière", style={"color": WHITE, "fontWeight": "800", "fontSize": "1.5rem"}),
                html.Span(" | Bénin 2010-2022", style={"color": MUTED, "fontWeight": "400", "fontSize": "1.5rem"}),
            ]),
            html.P("Analyse des accidents et victimes  Centre National de Sécurite Routière (CNSR)",
                   style={"color": MUTED, "fontSize": "0.8rem", "marginTop": "4px"}),
        ]),
        html.Div("Données : CNSR via Open Data Benin",
                 style={"color": MUTED, "fontSize": "0.72rem", "alignSelf": "center",
                        "background": CARD, "padding": "6px 12px", "borderRadius": "6px",
                        "border": f"1px solid {BORDER}"}),
    ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start",
              "marginBottom": "24px", "paddingBottom": "20px", "borderBottom": f"1px solid {BORDER}"}),

    # --- KPIs
    html.Div([
        kpi_block(f"{int(last['tues']):,}".replace(",", " "), "Personnes tuees (2022)", RED),
        kpi_block(f"{int(last['accidents']):,}".replace(",", " "), "Accidents (2022)", BLUE),
        kpi_block(f"{last['taux_mortalite']:.0f} / 1000", "Taux de mortalite 2022", ORANGE, "tues par 1000 accidents"),
        kpi_block(f"+{delta_tues}", "Hausse des tues vs 2019", RED, f"taux +{delta_tx} points en 3 ans"),
        kpi_block(worst["departement"], "Dept le plus meurtrier", ORANGE, f"{worst['taux_mortalite']:.0f} tues / 1000 acc."),
    ], style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginBottom": "20px"}),

    # --- Graphique 1 : paradoxe
    html.Div([
        html.Div([
            html.H3("Le paradoxe : moins d'accidents, plus de morts",
                    style={"fontSize": "1rem", "fontWeight": "700", "color": WHITE}),
            html.P("Les accidents stagnent depuis 2010. Les deces, eux, ont explose a partir de 2019.",
                   style={"fontSize": "0.78rem", "color": MUTED, "marginTop": "4px"}),
        ], style={"marginBottom": "8px"}),
        dcc.Graph(id="graph-paradoxe", config={"displayModeBar": False}),
    ], style=card_style()),

    # --- Graphiques 2 & 3 cote a cote
    html.Div([
        # Bar chart
        html.Div([
            html.H3("Taux de mortalite par departement",
                    style={"fontSize": "1rem", "fontWeight": "700", "color": WHITE}),
            html.P("Glissez pour changer l'annee",
                   style={"fontSize": "0.75rem", "color": MUTED, "marginTop": "2px", "marginBottom": "12px"}),
            dcc.Slider(
                id="slider-annee",
                min=int(min(YEARS)), max=int(max(YEARS)), step=1, value=2022,
                marks={int(y): {"label": str(y), "style": {"color": MUTED, "fontSize": "0.65rem"}}
                       for y in YEARS},
            ),
            dcc.Graph(id="graph-bar", config={"displayModeBar": False}),
        ], style=card_style({"flex": "1"})),

        html.Div(style={"width": "16px"}),

        # Line chart
        html.Div([
            html.H3("Evolution par departement",
                    style={"fontSize": "1rem", "fontWeight": "700", "color": WHITE}),
            html.P("Selectionnez les departements a comparer",
                   style={"fontSize": "0.75rem", "color": MUTED, "marginTop": "2px", "marginBottom": "8px"}),
            dcc.Dropdown(
                id="dropdown-depts",
                options=[{"label": d, "value": d} for d in DEPTS],
                value=["Zou", "Alibori", "Littoral", "Atlantique"],
                multi=True,
                style={"backgroundColor": CARD, "borderColor": BORDER,
                       "color": "#000", "fontSize": "0.8rem"},
            ),
            dcc.Graph(id="graph-line", config={"displayModeBar": False}),
        ], style=card_style({"flex": "1"})),
    ], style={"display": "flex"}),

    # --- Note
    html.Div(
        "Note methodologique : une rupture de serie est observable en 2016-2017, probablement liee a un changement de collecte du CNSR.",
        style={"color": MUTED, "fontSize": "0.72rem", "textAlign": "center",
               "padding": "12px", "borderTop": f"1px solid {BORDER}"}
    ),
])

# --- Callbacks --------------------------------------------------------------

@app.callback(Output("graph-paradoxe", "figure"), Input("graph-paradoxe", "id"))
def graph_paradoxe(_):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df_nat["annee"], y=df_nat["accidents"],
        name="Accidents", marker_color=BLUE, opacity=0.45,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df_nat["annee"], y=df_nat["tues"],
        name="Personnes tuees", mode="lines+markers",
        line=dict(color=RED, width=3),
        marker=dict(size=8, color=RED, line=dict(color=WHITE, width=1.5)),
    ), secondary_y=True)
    fig.update_layout(**PLOT_LAYOUT, height=320,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                                  bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE)))
    fig.update_yaxes(title_text="Nb accidents", secondary_y=False,
                     gridcolor=BORDER, color=MUTED)
    fig.update_yaxes(title_text="Personnes tuees", secondary_y=True,
                     gridcolor=BORDER, color=RED, showgrid=False)
    return fig


@app.callback(Output("graph-bar", "figure"), Input("slider-annee", "value"))
def graph_bar(annee):
    df = df_dept[df_dept["annee"] == annee].sort_values("taux_mortalite")
    fig = px.bar(
        df, x="taux_mortalite", y="departement", orientation="h",
        color="taux_mortalite",
        color_continuous_scale=[[0, "#fca5a5"], [0.5, "#ef4444"], [1, "#7f1d1d"]],
        labels={"taux_mortalite": "Tues / 1000 acc.", "departement": ""},
    )
    fig.update_layout(**PLOT_LAYOUT, height=380,
                      title=dict(text=f"Annee {annee}", font=dict(color=MUTED, size=11)),
                      coloraxis_showscale=False,
                      yaxis=AXIS_STYLE,
                      xaxis=AXIS_STYLE)
    fig.update_traces(marker_line_width=0)
    return fig


@app.callback(Output("graph-line", "figure"), Input("dropdown-depts", "value"))
def graph_line(selected):
    if not selected:
        selected = DEPTS
    df = df_dept[df_dept["departement"].isin(selected)]
    fig = px.line(
        df, x="annee", y="taux_mortalite", color="departement",
        markers=True,
        labels={"taux_mortalite": "Tues / 1000 acc.", "annee": "Annee", "departement": ""},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(**PLOT_LAYOUT, height=380,
                      xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
                      legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE)))
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    return fig


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)