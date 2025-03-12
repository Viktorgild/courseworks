import datetime
import os
from functools import wraps
from typing import Any, Callable

import pandas as pd

from config import REPORTS_DIR

from .logging_config import setup_logger

# Настройка логгера
logger = setup_logger("reports")

# Путь к директории с отчетами
func_operation_reports = os.path.join(REPORTS_DIR, "func_operation.json")
default_path_func_operation_reports = os.path.join(REPORTS_DIR, "default_func_operation_report.json")


def generate_report(file_path: str | None = None) -> Callable:
    """Записывает в переданный файл результат, который возвращает функция, формирующая отчет."""

    def my_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            result = func(*args, **kwargs)
            path_to_save = file_path if file_path else default_path_func_operation_reports
            logger.info(f"Записываю получившийся результат функции {func.__name__} в файл {path_to_save}")
            result.to_json(path_to_save, orient="records", force_ascii=False, indent=4)
            return result

        return wrapper

    return my_decorator


# Декорируем функцию с помощью generate_report. Файл по умолчанию default_func_operation_report.json
@generate_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Any = None) -> Any:
    """
    Возвращает траты по заданной категории за последние три месяца от переданной даты.

    :param transactions: DataFrame с транзакциями
    :param category: Название категории
    :param date: Опциональная дата в формате "дд.мм.гггг". Если не указана, берется текущая дата
    :return: DataFrame с отфильтрованными данными по категории и дате
    """
    # Если дата не передана, берем текущую дату
    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    logger.info(f"Запускаю расчет трат для категории {category} за последние 3 месяца от {date.date()}")
    # Преобразуем столбец "Дата операции" в формат datetime
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    # Определяем дату 3 месяца назад
    three_months_ago = date - pd.DateOffset(months=3)

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date)
    ]

    # Преобразуем дату обратно в строковый формат
    filtered_transactions = filtered_transactions.assign(
        **{"Дата операции": filtered_transactions["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")}
    )
    logger.info(f"Данные успешно сгенерированы. Количество операций {len(filtered_transactions)}")
    return filtered_transactions