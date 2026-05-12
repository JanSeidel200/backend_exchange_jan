import json
from pathlib import Path

from app.storage.file_storage import FileStorage


def test_save_settings_writes_json(tmp_path: Path):
    storage = FileStorage(data_dir=str(tmp_path))
    storage.save_settings({"base": "EUR", "symbols": ["CZK"]})
    written = json.loads((tmp_path / "settings.json").read_text())
    assert written["base"] == "EUR"


def test_append_history_writes_jsonl(tmp_path: Path):
    storage = FileStorage(data_dir=str(tmp_path))
    storage.append_analysis_history(
        request={"base": "EUR"},
        response={"strongest_currency": "CZK"},
    )
    storage.append_analysis_history(
        request={"base": "USD"},
        response={"strongest_currency": "GBP"},
    )
    lines = (
        (tmp_path / "analysis_history.jsonl").read_text().strip().splitlines()
    )
    assert len(lines) == 2
    assert json.loads(lines[0])["request"]["base"] == "EUR"