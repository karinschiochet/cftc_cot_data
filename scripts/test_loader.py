import os
import sys

# Obtém o diretório do script atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Obtém o diretório raiz do projeto (um nível acima)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, PROJECT_ROOT)

from core.loader import CotDataLoader

if __name__ == "__main__":
    loader = CotDataLoader()
    df = loader.load_data()
    print(df.head())
    print(df.columns)
    print(df.info)
