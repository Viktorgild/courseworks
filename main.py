from src.reports import spending_by_category
from src.services import analyze_cashback
from src.utils import read_excel_file
from src.views import get_summary_data

if __name__ == "__main__":
    # ====== WEB SERVICES ======
    print("=" * 50)
    print("💻 WEB SERVICES")
    print("=" * 50)

    web_info = get_summary_data("31.07.2020 12:30:50")
    print(web_info)

    # ======= SERVICES =======
    print("\n" + "=" * 50)
    print("💸 SERVICES (Анализ кешбэка)")
    print("=" * 50)

    transactions = read_excel_file()
    cashback_result = analyze_cashback(transactions, 2021, 11)
    print(cashback_result)

    # ======= REPORTS =======
    print("\n" + "=" * 50)
    print("📊 REPORTS (Траты по категории)")
    print("=" * 50)

    spending_by_category_result = spending_by_category(transactions, "Супермаркеты", "31.07.2020")
    print(spending_by_category_result.to_json(orient="records", indent=4, force_ascii=False))
