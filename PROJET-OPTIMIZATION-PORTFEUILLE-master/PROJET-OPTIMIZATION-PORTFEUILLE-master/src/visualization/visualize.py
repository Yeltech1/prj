import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def plot_returns_distribution(returns, save_path=None):
    """
    Plot the distribution of returns for each asset.
    
    Parameters:
    - returns: DataFrame of daily returns
    - save_path: Path to save the figure (optional)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for col in returns.columns:
        sns.kdeplot(returns[col], ax=ax, label=col)
    
    ax.set_title('Distribution des Rendements')
    ax.set_xlabel('Rendement Journalier')
    ax.set_ylabel('Densité')
    ax.legend()
    
    if save_path:
        plt.savefig(save_path)
    
    return fig

def plot_correlation_matrix(returns, save_path=None):
    """
    Plot correlation matrix of returns.
    
    Parameters:
    - returns: DataFrame of daily returns
    - save_path: Path to save the figure (optional)
    """
    corr = returns.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', 
                linewidths=0.5, ax=ax, vmin=-1, vmax=1)
    
    ax.set_title('Matrice de Corrélation')
    
    if save_path:
        plt.savefig(save_path)
    
    return fig

def plot_efficient_frontier(frontier, optimal_portfolio=None, save_path=None):
    """
    Plot the efficient frontier with Plotly.
    
    Parameters:
    - frontier: DataFrame with 'Return' and 'Volatility' columns
    - optimal_portfolio: Tuple of (return, volatility) for the optimal portfolio (optional)
    - save_path: Path to save the figure (optional)
    """
    fig = px.scatter(frontier, x='Volatility', y='Return', 
                    title='Frontière Efficiente',
                    labels={'Volatility': 'Volatilité (Risque)', 'Return': 'Rendement Attendu'})
    
    # Add optimal portfolio if provided
    if optimal_portfolio:
        fig.add_trace(go.Scatter(
            x=[optimal_portfolio[1]],
            y=[optimal_portfolio[0]],
            mode='markers',
            marker=dict(size=15, color='red'),
            name='Portefeuille Optimal'
        ))
    
    fig.update_layout(
        xaxis_title='Volatilité (Risque)',
        yaxis_title='Rendement Attendu',
        legend_title='Portefeuilles',
        font=dict(size=12)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig

def plot_portfolio_performance(portfolio_values, benchmark=None, save_path=None):
    """
    Plot portfolio performance over time.
    
    Parameters:
    - portfolio_values: Series of portfolio values over time
    - benchmark: Series of benchmark values over time (optional)
    - save_path: Path to save the figure (optional)
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=portfolio_values.index,
        y=portfolio_values.values,
        mode='lines',
        name='Portefeuille Optimisé'
    ))
    
    if benchmark is not None:
        fig.add_trace(go.Scatter(
            x=benchmark.index,
            y=benchmark.values,
            mode='lines',
            name='Benchmark'
        ))
    
    fig.update_layout(
        title='Performance du Portefeuille',
        xaxis_title='Date',
        yaxis_title='Valeur Cumulée',
        legend_title='Stratégies',
        font=dict(size=12)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig
