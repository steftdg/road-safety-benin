# 🚗 Road Safety Bénin — Tableau de bord interactif

> *Au Bénin, les accidents de la route baissent. Les morts, eux, augmentent.*
> *12 ans de données CNSR analysées pour comprendre pourquoi.*

## 📊 Aperçu

Dashboard interactif explorant les données d'accidents routiers au Bénin (2010–2022), construit avec **Dash + Plotly**.

**Source des données :** Centre National de Sécurité Routière (CNSR) via [Open Data Bénin](https://benin.opendataforafrica.org)

## 🗂️ Structure

```
road-safety-benin/
│
├── data/
│   ├── raw/              # Données brutes CNSR (xlsx)
│   └── processed/        # Données nettoyées (csv)
│
├── notebooks/
│   └── 01_exploration.ipynb   # Nettoyage + analyse exploratoire
│
├── dashboard/
│   └── app.py            # Application Dash
│
├── requirements.txt
└── README.md
```

## 🔍 Insights clés

- 📈 Les décès ont quasi doublé entre 2019 et 2022 malgré une baisse des accidents
- 🗺️ Le département du Zou affiche le taux de mortalité le plus élevé en 2022 (332 tués / 1000 accidents)
- 📉 Le taux de mortalité national est passé de 106 à 250 tués pour 1000 accidents entre 2016 et 2022

## 🚀 Lancer le dashboard

```bash
pip install -r requirements.txt
python dashboard/app.py
```

Ouvrir ensuite `http://127.0.0.1:8050` dans le navigateur.

## 🛠️ Stack

- Python 3.10+
- Dash 2.17 + Plotly
- Pandas

## 🐛 Notes techniques — Problèmes rencontrés au démarrage

Le dashboard a nécessité plusieurs corrections avant de fonctionner correctement sur Windows. Ces notes sont documentées ici pour référence.

### 1. Erreur 500 sur `/_dash-layout` — chemins de fichiers

**Symptôme :** le navigateur affichait "Erreur de chargement de la mise en page" dès l'ouverture.

**Cause :** le chargement des CSV utilisait `os.path.abspath(__file__)` qui se comporte différemment selon le répertoire depuis lequel on lance le script sur Windows.

**Fix :**
```python
# Avant — fragile sur Windows
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE, "data/processed/fichier.csv"))

# Après — robuste sur Windows et Linux
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE / "data" / "processed" / "fichier.csv")
```

`Path(__file__).resolve()` retourne le chemin absolu réel du fichier indépendamment du répertoire de lancement. Les opérateurs `/` de `pathlib` gèrent automatiquement les séparateurs Windows (`\`) et Linux (`/`).

### 2. Erreur `TypeError: keys must be str, int, float, bool or None, not numpy.int64`

**Symptôme :** nouvelle erreur 500 sur `/_dash-layout` après le fix des chemins.

**Cause :** le composant `dcc.Slider` utilise un dictionnaire `marks` dont les clés doivent être des types Python natifs. Or `YEARS` était une liste de `numpy.int64` issus de `pandas`, que le sérialiseur JSON de Dash ne sait pas convertir.

**Fix :**
```python
# Avant — clés numpy.int64, incompatibles avec JSON
marks={y: str(y) for y in YEARS}

# Après — clés int Python natif
marks={int(y): str(y) for y in YEARS}
```

### 3. Graphiques absents — callback sans déclencheur initial

**Symptôme :** le dashboard s'affichait avec le style et les KPIs, mais les graphiques restaient vides au chargement.

**Cause :** le callback de `graph-paradoxe` utilisait `Input("graph-paradoxe", "id")` comme déclencheur — une propriété statique qui ne déclenche pas toujours le callback au premier rendu.

**Fix :** ajout d'un `dcc.Store` comme déclencheur explicite au chargement initial.
```python
# Dans le layout
dcc.Store(id="store-init", data=1),

# Dans le callback
@app.callback(Output("graph-paradoxe", "figure"), Input("store-init", "data"))
def graph_paradoxe(_):
    ...
```

### 4. `TypeError: got multiple values for keyword argument 'legend'` / `'yaxis'`

**Symptôme :** les graphiques ne s'affichaient toujours pas après le fix du Store. Le terminal montrait des erreurs 500 sur `/_dash-update-component`.

**Cause :** `PLOT_LAYOUT` (le dictionnaire de style commun à tous les graphiques) contenait déjà les clés `legend`, `xaxis` et `yaxis`. Ces mêmes clés étaient repassées explicitement dans chaque appel `fig.update_layout(**PLOT_LAYOUT, legend=..., xaxis=..., yaxis=...)`, provoquant un conflit d'arguments.

**Fix :** retirer `legend`, `xaxis`, `yaxis` de `PLOT_LAYOUT` et créer un dictionnaire `AXIS_STYLE` réutilisable.
```python
# PLOT_LAYOUT ne contient plus que les propriétés vraiment communes
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT, color=WHITE, size=12),
    margin=dict(t=50, b=40, l=60, r=20),
)

# Style des axes réutilisable séparément
AXIS_STYLE = dict(gridcolor=BORDER, zerolinecolor=BORDER, color=WHITE, linecolor=BORDER)

# Dans chaque callback, on passe xaxis et yaxis explicitement
fig.update_layout(**PLOT_LAYOUT, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE)
```

---

*Projet réalisé par [Trésor Steffi TADOGBE](https://github.com/steftdg)*