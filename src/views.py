import json

from src.utils import (calculate_card_details, filter_last_month_data, get_currency_rates, get_exchange_rates,
                       get_greetings, read_excel_file, top_transactions)


def get_summary_data(date_str: str) -> str:
    """Собирает все данные и возвращает JSON-ответ."""
    greeting = get_greetings()
    data = read_excel_file()
    filter_data = filter_last_month_data(data, date_str)
    card_details = calculate_card_details(filter_data)
    top_trans = top_transactions(filter_data)
    currency_rates = get_currency_rates()
    stock_prices = get_exchange_rates()

    json_data = {
        "greeting": greeting,
        "cards": card_details,
        "top_transactions": top_trans,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(json_data, ensure_ascii=False, indent=4)
