import os
import sys

from core.unzipper import Unzipper

# Obtém o diretório do script atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Obtém o diretório raiz do projeto (um nível acima)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, PROJECT_ROOT)


if __name__ == "__main__":
    unzipper = Unzipper()
    zip_filename = "dea_fut_xls_2025.zip"  # O nome do arquivo ZIP que você baixou
    unzipper.unzip_file(zip_filename)
