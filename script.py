import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Définition de la page
st.set_page_config(
    page_title="Analyse de modèles de voitures",
    layout="centered",
    initial_sidebar_state="auto",
)


# Chargement de la base
@st.cache_data
def load_df():
    return pd.read_csv("cars.csv")


df_cars = load_df()
df = df_cars

# Side bar et widgets
with st.sidebar:
    continents = {"-": "tous", " US.": "USA", " Europe.": "Europe", " Japan.": "Japon"}
    # continents = list(df["continent"].unique())
    # continents.insert(0, "-")
    continent = st.selectbox("Choix du continent : ", continents.keys())
    if continent != "-":
        df = df_cars[df_cars.continent == continent]
    else:
        df = df_cars

st.title("Analyse de modèles de voitures")

# Graphique de corrélation
st.header(f"Corrélation pour : {continents[continent]}")
viz_correlation = sns.heatmap(
    df.corr(), center=0, cmap=sns.color_palette("vlag", as_cmap=True)
)

st.pyplot(viz_correlation.figure)

with st.expander("Analyse"):
    st.write(
        "On note dans le graphique ci-dessus une forte corrélation positive entre les paramètres suivants : "
    )
    st.write("cylindres, mètres cube, puissance (hp) et poids")

    st.write(
        "On note également une forte corrélation négative entre puissance (hp) et accélération(time to 60)"
    )

with st.expander("Graphiques détaillés"):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    sns.lineplot(ax=ax[0], data=df, x="cylinders", y="hp")
    sns.lineplot(ax=ax[1], data=df, x="hp", y="time-to-60")
    sns.scatterplot(ax=ax[2], data=df, x="mpg", y="weightlbs", hue="continent")
    st.pyplot(fig.figure)
