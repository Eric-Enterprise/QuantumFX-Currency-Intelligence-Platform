"""Catalog consistency, templates, errors, icons and number presentation."""
import ast
from pathlib import Path
from string import Formatter

import pytest

from quantumfx.i18n import CATALOGS, LANGUAGES, Translator
from quantumfx.ui import infer_icon


@pytest.mark.parametrize("language", LANGUAGES)
def test_catalogs_and_format_placeholders(language):
    def fields(text):
        return {name for _, name, _, _ in Formatter().parse(text) if name is not None}
    assert CATALOGS[language].keys() == CATALOGS["en"].keys()
    for key, value in CATALOGS[language].items():
        assert value.strip()
        assert fields(value) == fields(CATALOGS["en"][key]), key


def test_application_messages_have_catalog_entries():
    root = Path(__file__).resolve().parents[1] / "quantumfx"
    for file in ("app.py", "ui.py", "snake.py", "core.py"):
        for node in ast.walk(ast.parse((root / file).read_text(encoding="utf-8"))):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            translated = isinstance(node.func, ast.Attribute) and node.func.attr == "tr"
            error = isinstance(node.func, ast.Name) and node.func.id == "ValueError"
            if (translated or error) and isinstance(node.args[0], ast.Constant):
                assert node.args[0].value in CATALOGS["en"], (file, node.args[0].value)


@pytest.mark.parametrize("language, expected", [("en", "1,234.56"), ("de", "1.234,56"), ("ko", "1,234.56"), ("sv", "1 234,56")])
def test_locale_display_and_icons(language, expected):
    tr = Translator(language)
    assert tr.amount("1,234.56") == expected
    for label, icon in [("Copy", "copy"), ("★ Save pair", "star"), ("Convert & save  ↗", "swap"), ("Clear history", "trash")]:
        assert infer_icon(tr(label)) == icon
    assert str(tr.error("Request failed: Invalid rate.")) == tr("Request failed: {error}", error=tr("Invalid rate."))


def test_unknown_saved_language_falls_back_to_english():
    for saved in ("unknown", None, [], {}):
        assert Translator(saved).language == "en"
