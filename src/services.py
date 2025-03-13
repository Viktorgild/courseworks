import json

import pandas as pd

from .logging_config import setup_logger

# Настраиваем логирование
logger = setup_logger("services")


def analyze_cashback(data: pd.DataFrame, year: int, month: int) -> str:
    logger.info(f"Начинаю анализ кешбэка за {month}/{year}")

    # Преобразуем столбец с датой в формат datetime
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], dayfirst=True)
    logger.info("Преобразование даты завершено")

    # Фильтруем данные по году и месяцу
    data_filtered = data[(data["Дата операции"].dt.year == year) & (data["Дата операции"].dt.month == month)]
    logger.info(f"Фильтрация данных завершена. Найдено {len(data_filtered)} операций")

    # Группируем данные по категориям и суммируем кешбэк
    cashback_by_category = data_filtered.groupby("Категория")["Кэшбэк"].sum().to_dict()
    logger.info("Группировка и суммирование кешбэка завершены")

    # Конвертируем результат в JSON
    result_json = json.dumps(cashback_by_category, ensure_ascii=False, indent=4)
    logger.info("Конвертация в JSON завершена")

    return result_json