import logging
import os
from logging import Logger

from config import LOGS_DIR


def setup_logger(name_module: str) -> Logger:
    # Определяем путь к файлу логов относительно текущего файла
    log_file_path = os.path.join(LOGS_DIR, f"{name_module}.log")
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Создаем логгер
    logger = logging.getLogger(name_module)
    logger.setLevel(logging.DEBUG)

    # Проверяем, есть ли уже обработчики у логгера
    if not logger.handlers:
        # Создаем обработчик для записи в файл
        file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Форматирование логов
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        logger.addHandler(file_handler)

    return logger
