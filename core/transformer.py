from pathlib import Path
import pandas as pd
from core.logger import get_logger


logger = get_logger(__name__)


class CotDataTransformer:
    """Classe responsável por tratar e transformar os dados do arquivo COT."""

    def __init__(self, input_path: str, output_path: str = "data/processed/cot_transformed.csv"):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.df = None

    def sanitize(self):
        """Realiza o tratamento, criação de campos derivados e padronização dos dados."""

        if not self.input_path.exists():
            logger.error(f"Arquivo {self.input_path} não encontrado.")
            raise FileNotFoundError(f"Arquivo {self.input_path} não encontrado.")

        logger.info("Iniciando o tratamento dos dados...")
        df = pd.read_csv(self.input_path)

        # Conversão da coluna de data
        df['Report_Date_as_MM_DD_YYYY'] = pd.to_datetime(df['Report_Date_as_MM_DD_YYYY'], format="%Y-%m-%d",
                                                         errors='coerce')

        # Seleção das colunas necessárias
        df = df[['Market_and_Exchange_Names', 'Report_Date_as_MM_DD_YYYY', 'CFTC_Contract_Market_Code',
                 'Open_Interest_All', 'NonComm_Positions_Long_All', 'NonComm_Positions_Short_All',
                 'Comm_Positions_Long_All', 'Comm_Positions_Short_All']].copy()

        # Criação de novas colunas
        df["Dia"] = df['Report_Date_as_MM_DD_YYYY'].dt.day
        df["Mes"] = df['Report_Date_as_MM_DD_YYYY'].dt.month
        df["Ano"] = df['Report_Date_as_MM_DD_YYYY'].dt.year

        df['NonComm_Total'] = df['NonComm_Positions_Long_All'].abs() + df['NonComm_Positions_Short_All'].abs()
        df['NonComm_Long_%'] = (df['NonComm_Positions_Long_All'] / df['NonComm_Total'] * 100).round(2)
        df['NonComm_Short_%'] = (df['NonComm_Positions_Short_All'] / df['NonComm_Total'] * 100).round(2)
        df['Net_Position_NonComm'] = df['NonComm_Positions_Long_All'] - df['NonComm_Positions_Short_All']

        df['Comm_Total'] = df['Comm_Positions_Long_All'].abs() + df['Comm_Positions_Short_All'].abs()
        df['Comm_Long_%'] = (df['Comm_Positions_Long_All'] / df['Comm_Total'] * 100).round(2)
        df['Comm_Short_%'] = (df['Comm_Positions_Short_All'] / df['Comm_Total'] * 100).round(2)
        df['Net_Position_Comm'] = df['Comm_Positions_Long_All'] - df['Comm_Positions_Short_All']

        df['Sentimento'] = df['Net_Position_NonComm'] - df['Net_Position_Comm']

        # Correções de nomes específicos
        corrections = {
            'USD INDEX - ICE FUTURES U.S.': 'U.S. DOLLAR INDEX - ICE FUTURES U.S.',
            'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE': 'NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE',
            'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE': 'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE'
        }
        df['Market_and_Exchange_Names'] = df['Market_and_Exchange_Names'].replace(corrections)

        # Separar Market e Exchange
        split_market = df['Market_and_Exchange_Names'].str.split(" - ", n=1, expand=True)
        df['Market_Names'] = split_market[0]
        # Se quiser manter o Exchange separado, pode criar também:
        df['Exchange_Names'] = split_market[1]

        # Renomear as colunas
        df.rename(columns={
            'Report_Date_as_MM_DD_YYYY': 'Data',
            'Open_Interest_All': 'Open_Interest',
            'NonComm_Positions_Long_All': 'NonComm_Long',
            'NonComm_Positions_Short_All': 'NonComm_Short',
            'Comm_Positions_Long_All': 'Comm_Long',
            'Comm_Positions_Short_All': 'Comm_Short',
        }, inplace=True)

        self.df = df
        logger.info("Tratamento concluído com sucesso.")
        return df

    def save(self):
        """Salva o DataFrame transformado."""
        if self.df is None:
            logger.error("Nenhum dado tratado para salvar. Execute o método sanitize() antes.")
            raise ValueError("Nenhum dado tratado para salvar.")

        self.output_path.parent.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir
        self.df.to_csv(self.output_path, index=False)
        logger.info(f"Arquivo tratado salvo em {self.output_path}.")
