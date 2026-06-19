import streamlit as st
import pandas as pd
import plotly.express as px
from src.models.mpt import efficient_frontier, calculate_portfolio_metrics, optimize_portfolio

st.title("Optimisation de Portefeuille d'Investissement")

# Load data
returns = pd.read_csv('../data/processed/returns.csv', index_col='Date', parse_dates=True)
returns, cov_matrix = calculate_portfolio_metrics(returns)

# User inputs
tickers = st.multiselect("Sélectionner les actifs", returns.columns, default=returns.columns[:3])
target_return = st.slider("Rendement cible", min_value=0.0, max_value=0.3, value=0.1, step=0.01)

# Calculate efficient frontier
frontier = efficient_frontier(returns[tickers], cov_matrix.loc[tickers, tickers])

# Plot efficient frontier
fig = px.scatter(frontier, x='Volatility', y='Return', title='Frontière Efficiente')
st.plotly_chart(fig)

# Display optimal weights
weights = optimize_portfolio(returns[tickers], cov_matrix.loc[tickers, tickers], target_return)
st.write("Poids optimaux du portefeuille :", pd.Series(weights, index=tickers))