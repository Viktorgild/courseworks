from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests
from pandas.testing import assert_frame_equal

from src.utils import (calculate_card_details, filter_last_month_data, get_currency_rates, get_exchange_rates,
                       get_greetings, read_excel_file, top_transactions)


@patch("pandas.read_excel")
def test_read_excel_file(mock_excel: Mock, trans_data: list) -> None:
    mock_excel.return_value = trans_data
    result = read_excel_file()

    assert result == trans_data


def test_read_excel_file_invalid_path_file() -> None:
    with pytest.raises(FileNotFoundError):
        read_excel_file("test_path.xlsx")


@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (datetime(2024, 12, 1, 12), "Добрый день"),
        (datetime(2024, 12, 1, 18), "Добрый вечер"),
        (datetime(2024, 12, 1, 4), "Доброй ночи"),
        (datetime(2024, 12, 1, 6), "Доброе утро"),
    ],
    ids=["Приветствие днем", "Приветствие вечером", "Приветствие ночью", "Приветствие утром"],
)
@patch("datetime.datetime")
def test_get_greeting(mock_date: Mock, hour: datetime, expected_greeting: str) -> None:
    mock_date.now.return_value = hour
    assert get_greetings() == expected_greeting


@patch("requests.get")
def test_get_stock_prices(mock_request: Mock) -> None:
    response_data = [
        {"symbol": "AAPL", "price": 222.83},
        {"symbol": "TSLA", "price": 347.13},
        {"symbol": "AMZN", "price": 206.44},
    ]

    mock_request.return_value.json.return_value = response_data
    result = get_exchange_rates()

    assert result == [
        {"stock": "AAPL", "price": 222.83},
        {"stock": "TSLA", "price": 347.13},
        {"stock": "AMZN", "price": 206.44},
    ]


@patch("requests.get")
def test_get_currency_rates(mock_get: Mock, mock_api_response: dict) -> None:
    mock_get.return_value.json.return_value = mock_api_response

    result = get_currency_rates()

    assert result == {"EUR": 105.04201680672269, "USD": 97.08737864077669}


@patch("requests.get")
def test_get_currency_rates_with_raise(mock_response: Mock) -> None:
    mock_response.side_effect = requests.exceptions.RequestException
    assert get_currency_rates() == {}


def test_card_info(trans_data: dict) -> None:
    df = pd.DataFrame(trans_data)
    result = calculate_card_details(df)
    assert result == [
        {"cashback": 1.0, "last_digits": "1234", "total_spent": 100.0},
        {"cashback": 1.0, "last_digits": "5678", "total_spent": 150.0},
    ]


def test_top_five_transactions_by_payment_amount(trans_data: dict) -> None:
    df = pd.DataFrame(trans_data)
    result = top_transactions(df)
    assert result == [
        {
            "Дата операции": "01.02.2023 00:00:00",
            "Категория": "развлечения",
            "Описание": "кинотеатр",
            "Сумма операции": 150.0,
        },
        {
            "Дата операции": "01.01.2023 00:00:00",
            "Категория": "продукты",
            "Описание": "магазин",
            "Сумма операции": 100.0,
        },
    ]


def test_filter_transactions_by_date(sample_transactions: pd.DataFrame) -> None:
    """Тестируем фильтрацию транзакций по указанной дате."""
    date = "15.11.2024 00:00:00"
    expected_data = {
        "Дата операции": [
            "01.11.2024 10:15:30",
            "05.11.2024 12:45:00",
            "30.11.2024 09:30:00",
        ],
        "Сумма операции": [1000, 500, 300],
        "Валюта": ["RUB", "RUB", "EUR"],
    }
    expected_df = pd.DataFrame(expected_data)
    filtered_df = filter_last_month_data(sample_transactions, date)

    # Проверка количества отфильтрованных транзакций
    assert len(filtered_df) == 3, "Должно быть три транзакции за ноябрь 2024"

    #Проверка содержимого DataFrame
    assert_frame_equal(filtered_df.reset_index(drop=True), expected_df)
