import os
import zipfile
from core.logger import get_logger

logger = get_logger(__name__)


class Unzipper:
    """Classe responsável por descompactar arquivos ZIP."""

    def __init__(self, zip_dir: str = "data/zips", dest_dir: str = "data/processed"):
        # Garantir que o caminho seja absoluto
        self.zip_dir = os.path.abspath(zip_dir)
        self.dest_dir = os.path.abspath(dest_dir)
        os.makedirs(self.dest_dir, exist_ok=True)

    def unzip_file(self, zip_filename: str) -> str:
        """Descompacta um arquivo ZIP no diretório especificado."""

        zip_path = os.path.join(self.zip_dir, zip_filename)

        if not os.path.exists(zip_path):
            logger.error(f"O arquivo {zip_filename} não foi encontrado em {self.zip_dir}")
            raise FileNotFoundError(f"Arquivo {zip_filename} não encontrado.")

        logger.info(f"Iniciando a descompactação do arquivo {zip_filename}...")

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Listar os arquivos dentro do ZIP (geralmente só tem um, mas vamos verificar)
                zip_content = zf.namelist()
                logger.info(f"Conteúdo do arquivo ZIP: {zip_content}")

                # Extrair todos os arquivos
                zf.extractall(self.dest_dir)

                # Renomear o arquivo extraído para algo mais consistente, por exemplo, com o ano
                extracted_file = zip_content[0]  # Vamos supor que tenha apenas um arquivo
                extracted_file_path = os.path.join(self.dest_dir, extracted_file)

                # Renomear o arquivo extraído (se necessário)
                year = zip_filename.split("_")[-1].split(".")[0]
                # renamed_file = f"dea_fut_xls_{year}.xls"
                renamed_file = f"{year}.xls"
                renamed_path = os.path.join(self.dest_dir, renamed_file)

                # Verificar se o arquivo já existe e, se sim, removê-lo
                if os.path.exists(renamed_path):
                    logger.info(f"Arquivo {renamed_file} já existe, substituindo...")
                    os.remove(renamed_path)

                os.rename(extracted_file_path, renamed_path)

                logger.info(f"Arquivo descompactado e renomeado para: {renamed_file}")

                return renamed_path

        except zipfile.BadZipFile:
            logger.error(f"Erro ao abrir o arquivo ZIP: {zip_filename}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao descompactar {zip_filename}: {e}")
            raise
