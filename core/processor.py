from pathlib import Path
import pandas as pd
from glob import glob
from core.logger import get_logger

logger = get_logger(__name__)

class CotProcessor:
    """Classe responsável por processar os arquivos COT e gerar o CSV unificado."""

    def __init__(self, source_dir: str = "data/processed", output_dir: str = "data/processed"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Garante que o diretório de saída exista

    def create_cot_csv(self, output_filename: str = "cot.csv"):
        """Concatena todos os arquivos XLS e gera um único CSV."""

        logger.info("Iniciando o processo de união dos arquivos .xls...")

        # Buscar todos os arquivos que começam com '20' (anos)
        cot_files = sorted(glob(str(self.source_dir / '20*.xls')))

        if not cot_files:
            logger.error("Nenhum arquivo .xls encontrado para processar.")
            raise FileNotFoundError("Nenhum arquivo .xls encontrado.")

        logger.info(f"{len(cot_files)} arquivos encontrados para processamento.")

        try:
            # Lendo e concatenando todos os arquivos
            dataframes = []
            for file in cot_files:
                logger.info(f"Lendo arquivo: {file}")
                df = pd.read_excel(file)
                dataframes.append(df)

            combined_df = pd.concat(dataframes, ignore_index=True)

            # Definindo caminho final do CSV
            output_path = self.output_dir / output_filename

            # Salvando CSV
            combined_df.to_csv(output_path, index=False, sep=',')

            logger.info(f"Arquivo CSV criado com sucesso em: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Erro ao processar arquivos: {e}")
            raise
