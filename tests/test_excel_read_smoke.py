from pathlib import Path

from src.utils.excel_io import ExcelConfig, iter_rows

def test_excel_read_smoke():
    cfg = ExcelConfig(
        path=Path("data/input/CorregirSIMS.xlsx"),
        sheet="iq09"
    )

    rows = list(iter_rows(cfg))

    assert len(rows) == 3