import json
from unittest.mock import Mock, patch

import pandas as pd

from src.services import analyze_cashback
from src.utils import read_excel_file


@patch("pandas.read_excel")
def test_analyze_cashback(mock_excel: Mock, trans_data: list) -> None:
    mock_excel.return_value = pd.DataFrame(trans_data)
    result = analyze_cashback(read_excel_file(), 2023, 1)
    result = json.loads(result)

    assert result == {"продукты": 1.0}

    result = analyze_cashback(read_excel_file(), 2023, 2)
    result = json.loads(result)

    assert result == {"развлечения": 1.50}
