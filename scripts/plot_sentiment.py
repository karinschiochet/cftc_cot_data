# scripts/plot_sentiment.py

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


def main():
    df = pd.read_csv("data/processed/cot_transformed.csv", parse_dates=['Data'])

    # Exemplo: gráfico de sentimento do Dólar (U.S. DOLLAR INDEX)
    usd_df = df[df['Market_Names'] == 'U.S. DOLLAR INDEX']

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=usd_df, x='Data', y='Sentimento')
    plt.title('Sentimento dos Especuladores - U.S. Dollar Index')
    plt.xlabel('Data')
    plt.ylabel('Sentimento (Net Position NonComm - Net Position Comm)')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
