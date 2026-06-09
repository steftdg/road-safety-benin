# road-safety-benin
Une exploration et analyse des données d'accidents routiers au Bénin


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
├── assets/
│   └── style.css         # Style du dashboard
│
├── requirements.txt
└── README.md
```

## 🔍 Insights clés

- 📈 Les décès ont quasi doublé entre 2019 et 2022 malgré une baisse des accidents
- 🌙 Les accidents de nuit sans éclairage public sont disproportionnellement mortels
- 🛵 Les 2-roues motorisés concentrent la majorité des victimes

## 🚀 Lancer le dashboard

```bash
pip install -r requirements.txt
python dashboard/app.py
```

## 🛠️ Stack

- Python 3.10+
- Dash + Plotly
- Pandas
- GeoPandas

---

*Projet réalisé par [Trésor Steffi TADOGBE](https://github.com/steftdg)*
