# scripts/plot_multiple_markets.py

import os
import sys


# Obtém o diretório do script atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Obtém o diretório raiz do projeto (um nível acima)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, PROJECT_ROOT)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_sentiment_over_time(df, markets):
    plt.figure(figsize=(14, 7))

    for market in markets:
        market_df = df[df['Market_Names'] == market]
        sns.lineplot(data=market_df, x='Data', y='Sentimento', label=market)

    plt.title('Sentimento dos Especuladores por Mercado')
    plt.xlabel('Data')
    plt.ylabel('Sentimento')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_last_positions(df, markets):
    latest_date = df['Data'].max()
    latest_df = df[df['Data'] == latest_date]

    filtered = latest_df[latest_df['Market_Names'].isin(markets)]

    # Ajuste o tamanho da figura conforme o número de mercados
    plt.figure(figsize=(14, 7))
    bar_width = 0.35
    x = range(len(filtered))

    plt.bar(x, filtered['NonComm_Long'], width=bar_width, label='NonComm Long', color='green')
    plt.bar([p + bar_width for p in x], filtered['NonComm_Short'], width=bar_width, label='NonComm Short', color='red')

    plt.xticks([p + bar_width/2 for p in x], filtered['Market_Names'], rotation=45)
    plt.ylabel('Número de Contratos')
    plt.title(f'Posições Long x Short dos Especuladores ({latest_date.date()})')
    plt.legend()
    plt.tight_layout()
    plt.grid(True, axis='y')
    plt.show()


def main():
    df = pd.read_csv("data/processed/cot_transformed.csv", parse_dates=['Data'])

    # Seleção de mercados para exemplo
    selected_markets = [
        'U.S. DOLLAR INDEX',
        'EURO FX',
        'JAPANESE YEN',
        'BRITISH POUND STERLING',
        'SWISS FRANC',
        'CANADIAN DOLLAR',
        'AUSTRALIAN DOLLAR',
        'NEW ZEALAND DOLLAR'
    ]

    plot_sentiment_over_time(df, selected_markets)
    plot_last_positions(df, selected_markets)


if __name__ == "__main__":
    main()
