"""
Core Logger — Logging centralizado para projetos RPA.

Formato: [timestamp] [LEVEL] [arquivo] [linha] [usuário] mensagem
Handlers: RotatingFileHandler (100MB, 5 backups) + StreamHandler (console)
"""

from __future__ import annotations

import getpass
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class RPAFormatter(logging.Formatter):
    """Formatter customizado com contexto de usuário e caller real."""

    def __init__(self, user: str) -> None:
        self.user = user
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_file = os.path.basename(record.pathname)
        caller_line = record.lineno
        return (
            f"[{timestamp}] [{record.levelname}] "
            f"[{caller_file}] [{caller_line}] "
            f"[{self.user}] {record.getMessage()}"
        )


class RPALogger:
    """Logger centralizado para projetos RPA.

    Params:
        project_name: Nome do projeto (usado no nome do arquivo de log).
        log_dir: Diretório onde os logs serão salvos.
        user: Usuário atual. Default: getpass.getuser().
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        max_bytes: Tamanho máximo do arquivo de log antes de rotação.
        backup_count: Número de backups mantidos na rotação.
        console_output: Se True, também imprime no console.
    """

    def __init__(
        self,
        project_name: str,
        log_dir: str,
        user: str | None = None,
        level: str = "INFO",
        max_bytes: int = 100_000_000,  # 100MB
        backup_count: int = 5,
        console_output: bool = True,
    ) -> None:
        self.project_name = project_name
        self.log_dir = log_dir
        self.user = user or getpass.getuser()
        self.level = getattr(logging, level.upper(), logging.INFO)

        # Garante que diretório de logs exista
        os.makedirs(self.log_dir, exist_ok=True)

        # Logger interno — nome único por projeto para evitar colisão
        self.logger = logging.getLogger(f"rpa3003.{project_name}")
        self.logger.setLevel(self.level)
        self.logger.propagate = False

        # Evita handlers duplicados em recriação
        if not self.logger.handlers:
            formatter = RPAFormatter(self.user)

            # RotatingFileHandler — {project}_{YYYY-MM-DD}.log
            today = datetime.now().strftime("%Y-%m-%d")
            log_filename = f"{project_name}_{today}.log"
            log_path = os.path.join(self.log_dir, log_filename)

            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # StreamHandler — console
            if console_output:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(self.level)
                stream_handler.setFormatter(formatter)
                self.logger.addHandler(stream_handler)

    # -- Métodos públicos ------------------------------------------------
    # stacklevel=2 → pula este wrapper, record.pathname/lineno aponta
    # para o caller real (quem chamou logger.info(), etc.)

    def debug(self, message: str) -> None:
        """Log nível DEBUG."""
        self.logger.debug(message, stacklevel=2)

    def info(self, message: str) -> None:
        """Log nível INFO."""
        self.logger.info(message, stacklevel=2)

    def warning(self, message: str) -> None:
        """Log nível WARNING."""
        self.logger.warning(message, stacklevel=2)

    def error(self, message: str) -> None:
        """Log nível ERROR."""
        self.logger.error(message, stacklevel=2)

    def critical(self, message: str) -> None:
        """Log nível CRITICAL."""
        self.logger.critical(message, stacklevel=2)
