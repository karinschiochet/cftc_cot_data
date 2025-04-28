import logging
import os
from logging.handlers import TimedRotatingFileHandler


def get_logger(name: str, log_dir: str = "logs", level=logging.INFO) -> logging.Logger:
    """Cria e retorna um logger com rotação automática diária dos arquivos."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    if not logger.handlers:
        os.makedirs(log_dir, exist_ok=True)

        # Handler para console (terminal)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para logs gerais, com rotação diária
        general_log_path = os.path.join(log_dir, "general.log")
        general_handler = TimedRotatingFileHandler(
            general_log_path,
            when="midnight",   # Rotaciona TODO dia à meia-noite
            interval=1,
            backupCount=7,     # Mantém os últimos 7 dias de logs
            encoding="utf-8",
            utc=False          # Usa horário local (False). Se preferir UTC, mude para True.
        )
        general_handler.setFormatter(formatter)
        general_handler.setLevel(level)
        logger.addHandler(general_handler)

        # Handler para logs de erro, também rotacionados
        error_log_path = os.path.join(log_dir, "error.log")
        error_handler = TimedRotatingFileHandler(
            error_log_path,
            when="midnight",
            interval=1,
            backupCount=30,    # Mantém os últimos 30 dias de erros
            encoding="utf-8",
            utc=False
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)

    return logger
