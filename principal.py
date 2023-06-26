import streamlit as st
import numpy as np
import streamlit.components.v1 as components
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation


def correlation(df):
    st.header("Relation between sucide rate income, population and year")
    st.text("Suicide rate is grouped by country using mean")
    df_ = df[df.population < 5*1e7]
    cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
    fig = sns.relplot(
        data=df_.groupby(["country"]).mean(),
        y="suicides/100k pop", x="gdp_per_capita ($)",
        size="population", hue = "year",
        palette=cmap, sizes=(10, 200),
    )
    st.pyplot(fig)


def timeplot(df):
    st.header("Suicide rate evolution per year")
    fig, ax = plt.subplots()
    sns.lineplot(x="year", y="suicides/100k pop",
             hue="sex",
             data=df, ax = ax)
    st.pyplot(fig)


def boxplot(df):
    st.header("Suicide rate per generation")
    fig, ax = plt.subplots()
    sns.boxplot(data = df, y = "suicides/100k pop", x = "generation", 
                ax = ax,
                order = ["Generation Z", "Millenials", "Generation X", "Boomers", "Silent", "G.I. Generation"])
    ax.set_ylim(0,300)
    st.pyplot(fig)


def barplot(df):
    st.header("Suicide rate per country")
    year = st.selectbox("Select year", ["All"]+list(np.unique(df.year)))
    if year == "All":
        fig, ax = plt.subplots(figsize=(20, 7))
        ax.tick_params(axis='x', labelrotation=90)
        sns.barplot(data = df, x = "country", y = "suicides/100k pop")
        st.pyplot(fig)
    else:
        df_ = df[df.year == int(year)]
        fig, ax = plt.subplots(figsize=(20, 7))
        ax.tick_params(axis='x', labelrotation=90)
        sns.barplot(data = df_, x = "country", y = "suicides/100k pop")
        st.pyplot(fig)


def animated_plot(df):
    def animate(year):
        plt.cla()
        ax.set_ylim(0, max(df["suicides/100k pop"])+10)
        ax.tick_params(axis='x', labelrotation=45)
        ax.set_title(f'Suicides per 100 000 population in {int(year)}')
        graph = sns.barplot(data=df[df.year == year], x="age", y="suicides/100k pop", hue = "sex", order=['5-14 years', '15-24 years', 
                                                                                                        '25-34 years', '35-54 years', '55-74 years', '75+ years'])
        return graph

    st.header("Evolution of sucide rate in diferent countries along years")
    country = st.selectbox("Select country",
        ('Albania', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba',
       'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
       'Barbados', 'Belarus', 'Belgium', 'Belize',
       'Bosnia and Herzegovina', 'Brazil', 'Brunei Darussalam',
       'Bulgaria', 'Cabo Verde', 'Canada', 'Chile',
       'China, Hong Kong SAR', 'Colombia', 'Costa Rica', 'Croatia',
       'Cuba', 'Cyprus', 'Czech Republic', 'Czechia', 'Denmark',
       'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt',
       'El Salvador', 'Estonia', 'Fiji', 'Finland', 'France', 'Georgia',
       'Germany', 'Greece', 'Grenada', 'Guatemala', 'Guyana', 'Hungary',
       'Iceland', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan',
       'Jordan', 'Kazakhstan', 'Kiribati', 'Kuwait', 'Kyrgyzstan',
       'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Macau',
       'Maldives', 'Malta', 'Mauritius', 'Mexico', 'Mongolia',
       'Montenegro', 'Netherlands', 'New Zealand', 'Nicaragua',
       'North Macedonia', 'Norway', 'Oman', 'Panama', 'Paraguay', 'Peru',
       'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar',
       'Republic of Korea', 'Republic of Moldova', 'Romania',
       'Russian Federation', 'Saint Kitts and Nevis', 'Saint Lucia',
       'Saint Vincent and Grenadines', 'Saint Vincent and the Grenadines',
       'San Marino', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia',
       'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Suriname',
       'Sweden', 'Switzerland', 'Tajikistan', 'Thailand',
       'Trinidad and Tobago', 'Turkey', 'Turkmenistan', 'Ukraine',
       'United Arab Emirates', 'United Kingdom', 'United States',
       'United States of America', 'Uruguay', 'Uzbekistan'))
    
    df = df[df.country == country]

    fig, ax = plt.subplots(figsize=(5, 7))
    plt.ylim(0,3)

    anim = animation.FuncAnimation(fig, animate, frames = np.unique(df.year), interval = 500)

    components.html(anim.to_jshtml(), height=1000)


if __name__ == "__main__":
    st.title("Suicide rate visual analysis")
    df = pd.read_csv("master.csv")
    df = df[df.year < 2017]
    if st.sidebar.checkbox("Suicide rate evolution per country (histogram)"):
        animated_plot(df)
    if st.sidebar.checkbox("Suicide rate evolution per year (lineplot)"):
        timeplot(df)
    if st.sidebar.checkbox("Suicide rate relation with, income, year and population (relplot)"):
        correlation(df)
    if st.sidebar.checkbox("Suicide rate per generation (boxplot)"):
        boxplot(df)
    if st.sidebar.checkbox("Suicide rate per country (barplot)"):
        barplot(df)
