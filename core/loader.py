from pathlib import Path
import pandas as pd
from core.logger import get_logger

logger = get_logger(__name__)

class CotDataLoader:
    """Classe responsável por carregar e tratar o arquivo COT."""

    def __init__(self, cot_csv_path: str = "data/processed/cot.csv"):
        self.cot_csv_path = Path(cot_csv_path)
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Carrega o arquivo cot.csv e realiza o tratamento básico."""
        if not self.cot_csv_path.exists():
            logger.error(f"Arquivo {self.cot_csv_path} não encontrado.")
            raise FileNotFoundError(f"Arquivo {self.cot_csv_path} não encontrado.")

        try:
            logger.info(f"Carregando o arquivo {self.cot_csv_path}...")
            df = pd.read_csv(self.cot_csv_path)

            logger.info("Tratando os dados...")

            # Exemplo de ajustes iniciais:
            df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]  # padronizar nomes
            if 'report_date_as_mm/dd/yyyy' in df.columns:
                df['report_date_as_mm/dd/yyyy'] = pd.to_datetime(df['report_date_as_mm/dd/yyyy'], errors='coerce')

            # Exemplo: converter para numérico algumas colunas se soubermos quais são
            numeric_columns = [
                'open_interest_all', 'noncommercial_positions_long_all',
                'noncommercial_positions_short_all', 'commercial_positions_long_all',
                'commercial_positions_short_all'
                # ... você pode adicionar mais conforme for necessário
            ]
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            self.df = df
            logger.info("Arquivo carregado e tratado com sucesso.")
            return df

        except Exception as e:
            logger.error(f"Erro ao carregar ou tratar o arquivo: {e}")
            raise
