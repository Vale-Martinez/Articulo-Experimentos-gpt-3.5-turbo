# imports
import pandas as pd
import numpy as np
import plotly.express as px
import os
import plotly.io as pio
import statsmodels.api as sm



pio.templates.default = "plotly"

"""
This Python script generates the tables and figures for the GPT paper.
"""


def produce_stadistics(dg_35turbo):
 

#Procesamos datos modelo GPT-3.5-turbo
    df_35turbo= dg_35turbo
    # Keep just the first 500 observations
    # note that due to model interruptions, 501 obs total
    df_35turbo = df_35turbo[:500]
    # Find alllocation in the model's response
    df_35turbo.loc[:, "Allocation"] = (
        df_35turbo["GPTResponse"].str.extract(r'(\d)',expand=False).astype(float)
        
    )

    df_35turbo["Allocation"].replace(
        {50: 5}, inplace=True
    )  # for these cases, it's saying split 50-50

    # Figure  The distribution of allocations in the GPT-3.5-turbo experiment
    fig = px.histogram(
        df_35turbo,
        x=["Allocation"],
        histnorm="density",
        range_x=[0, 10],
        text_auto=True,
        opacity=0.75,
        title= "Resultados de Modelo GPT-3.5-turbo ",
        template= "presentation",
    )

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency", xaxis_title="Allocation",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()
   
    #Crear el violin plot
    fig = px.violin(df_35turbo, title="Violin Plot de Resultados de GPT3.5",y="Allocation",template= "presentation" , box = True, )
    fig.update_traces(meanline_visible=True)
    # Mostrar el gráfico
    fig.show()

    #Crear descripcion estaditico
    print(df_35turbo["Allocation"].describe())
    
     # Figure 1: The distribution of allocations in the GPT experiment
    fig = px.histogram(
        df_35turbo, x="Allocation", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title="Resultados de Modelo GPT-3.5-turbo",template= "presentation")

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()


    # Figura data por engle 
    # Datos del metaanálisis de Engel (2011)
    engel_data = {
         "One Shot Studies": {
            "Allocation": [
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0,
            ],
            "Fraction": [
                0.3133,
                0.0794,
                0.0934,
                0.0922,
                0.078,
                0.2127,
                0.0304,
                0.0142,
                0.0092,
                0.0064,
                0.0702,
            ],
        },
    }
    
    # Convertir los datos a un DataFrame
    df_engel = pd.DataFrame(engel_data["One Shot Studies"])

    # Calcular la media ponderada de Engel
    engel_mean = df_engel["Allocation"].dot(df_engel["Fraction"])

    # Crear gráfico de barras con los datos de Engel
    fig = px.bar(df_engel, x="Allocation", y="Fraction", 
                 title="Representación de resultados Meta-estudio Engel (2011) contra medias modelo GPT",
                 template="presentation")

    # Personalizar el layout
    fig.update_layout(
        yaxis_range=[0, 0.4],
        xaxis=dict(tickmode="linear", tick0=0, dtick=0.1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        legend_title="Medias por modelos GPT"
    )
    # Añadir líneas verticales para la media de Engel y de cada modelo GPT
    fig.add_vline(
        x=engel_mean, line_width=3, line_dash="dash", line_color="firebrick",  name="Media Meta-estudio Engle (2011) = " + str(engel_mean),showlegend=True,
    )

    fig.add_vline(
        x=df_35turbo.Allocation.mean() / 10,
        line_width=3,
        line_dash="dash",
        line_color="black",
        name="Media GPT-3.5-turbo = "+ str (df_35turbo.Allocation.mean() / 10),
        showlegend=True,
    )
    fig.show()

# Read in Results

dg_results_35_turbo = pd.read_excel(
    os.path.join("..", "Articulo Cientifico", "dictator_game_log_35_turbo.xlsx")
)

# Call function to produce tables and figures
produce_stadistics (dg_results_35_turbo)
