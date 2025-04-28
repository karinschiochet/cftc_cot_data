# scripts/transform_data.py
import os
import sys


# Obtém o diretório do script atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Obtém o diretório raiz do projeto (um nível acima)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, PROJECT_ROOT)

from core.transformer import CotDataTransformer


def main():
    # Caminho do arquivo original já concatenado
    input_file = "data/processed/cot.csv"

    # Caminho onde salvará o arquivo tratado
    output_file = "data/processed/cot_transformed.csv"

    transformer = CotDataTransformer(input_path=input_file, output_path=output_file)

    # Executa o tratamento
    df_transformed = transformer.sanitize()

    # Salva o resultado
    transformer.save()

    # Exibe os 5 primeiros registros para conferência
    print(df_transformed.head())


if __name__ == "__main__":
    main()
