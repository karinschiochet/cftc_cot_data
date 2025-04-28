import os
import requests
from datetime import datetime
from core.logger import get_logger


logger = get_logger(__name__)


class Downloader:
    """Classe responsável por baixar o arquivo zip do CFTC."""

    def __init__(self, save_dir: str = "data/zips"):
        # Garantir que o caminho seja absoluto
        self.save_dir = os.path.abspath(save_dir)
        # self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def download_current_year_zip(self) -> str:
        """Baixa o arquivo ZIP do ano atual e salva no diretório específicado."""

        year = datetime.now().year
        url = f"https://www.cftc.gov/files/dea/history/dea_fut_xls_{year}.zip"
        local_filename = f"{self.save_dir.replace(os.sep, '/')}/dea_fut_xls_{year}.zip"

        logger.info(f"Iniciando o download do arquivo para o ano {year}...")
        logger.info(f"URL: {url}")

        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            with open(local_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"Download concluído com sucesso: {local_filename}")
            return local_filename

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar o arquivo: {e}")
            raise
