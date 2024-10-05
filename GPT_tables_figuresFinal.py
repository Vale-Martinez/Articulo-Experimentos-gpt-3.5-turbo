# imports
import pandas as pd
import numpy as np
import plotly.express as px
import os
import plotly.io as pio
import statsmodels.api as sm
import re

pio.templates.default = "plotly"

"""
This Python script generates the tables and figures for the GPT paper.
"""


def produce_tables_figures(dg_results,datatitle):
    """
    This function produces the tables and figures of results for
    Brookins and DeBacker.

    Args:
        dg_results (pandas.DataFrame): dataframe of dictator game results
        pd_results (pandas.DataFrame): dataframe of prisoner's dilemma results
        gpt_model (str): model used to generate results (e.g., "GPT-3.5" or "GPT-4")

    Returns:
        None (image and tex files saved to disk)
    """
    df = dg_results
    # Keep just the first 500 observations
    # note that due to model interruptions, 501 obs total
    df = df[:500]
    # Find alllocation in the model's response
    df.loc[:, "Allocation"] = (
        df["GPTResponse"].str.extract(r'(\d)',expand=False).astype(float)
    )

    df["Allocation"].replace(
        {50: 5}, inplace=True
    )  # for these cases, it's saying split 50-50
    
    # Figure 1: The distribution of allocations in the GPT experiment
    fig = px.histogram(
        df, x="Allocation", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title=datatitle
    )

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
        
    if not os.path.exists("images"):
      os.mkdir("images")
      fig.write_image("images/fig1.pdf")

    fig.show()
  
    print("figura 1 listo")


# Read in Results
dg_results_35 = pd.read_excel(
    os.path.join("..", "CodigoTFGVale", "dictator_game_log_135.xlsx")
)


# Call function to produce tables and figures
produce_tables_figures(dg_results_35,"dictator_game_log_135")
