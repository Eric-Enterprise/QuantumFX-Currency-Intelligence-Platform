import csv
import json
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from unittest.mock import patch
import pytest
from quantumfx.core import (number, convert, money, validate_rates, RateService,
                            Snapshot, Store, atomic_json, cached_snapshot, export_csv)


@pytest.mark.parametrize("raw,expected", [("0", "0"), (" 1234,56 ", "1234.56"),
    ("0.12345678", "0.12345678"), ("1000000000000", "1000000000000")])
def test_number(raw, expected):
    assert number(raw) == D(expected)


@pytest.mark.parametrize("raw", ["", " ", "NaN", "Infinity", "-1", "1e5", "1.234,56", "1 000",
    "0.123456789", "1000000000001", "1,2,3", ".5", "1" * 25])
def test_reject_unsafe_input(raw):
    with pytest.raises(ValueError):
        number(raw)


def test_cross_rate_and_fees():
    rates = validate_rates({"EUR": 1, "USD": 1.2, "GBP": .8})
    result = convert(D(100), "GBP", "USD", rates, D(2), D(1))
    assert result == {"rate": D("1.5"), "gross": D(150), "fee": D(3), "net": D("145.5")}


@pytest.mark.parametrize("amount,percent,fixed", [(100, 101, 0), (1, 0, 2), (-1, 0, 0), (1, -1, 0)])
def test_invalid_fees(amount, percent, fixed):
    with pytest.raises(ValueError):
        convert(D(amount), "EUR", "EUR", {"EUR": D(1)}, D(percent), D(fixed))


def test_identity_zero_and_full_fee():
    assert convert(D(0), "EUR", "EUR", {"EUR": D(1)})["net"] == 0
    assert convert(D(100), "EUR", "EUR", {"EUR": D(1)}, D(100))["net"] == 0
    with pytest.raises(ValueError):
        convert(D(1), "USD", "EUR", {"EUR": D(1)})


@pytest.mark.parametrize("rates", [{}, [], {"USD": 0}, {"USD": -1}, {"USD": "NaN"},
    {"USD": "Infinity"}, {"USD": True}, {"USD": None}, {"../": 1}, {"USD": 1e13}])
def test_bad_rates(rates):
    with pytest.raises(ValueError):
        validate_rates(rates)


def test_rounding():
    assert money(D("1.005"), "EUR") == "1,01"
    assert money(D("1234.5"), "JPY") == "1.235"
    assert money(D("0.004"), "USD") == "0,00"


def payload():
    return {"base": "EUR", "date": date.today().isoformat(), "rates": {"USD": 1.2, "GBP": .8}}


def fail(url):
    raise OSError("network down")


def test_online_cache_offline_roundtrip(tmp_path):
    live = RateService(tmp_path, lambda url: payload()).latest()
    assert live.source == "online" and live.rates["USD"] == D("1.2")
    cached = RateService(tmp_path, fail).latest()
    assert cached.source == "cache" and cached.day == live.day
    assert "network down" in cached.warning
    assert cached.rates == live.rates


def test_corrupt_cache_offline(tmp_path):
    (tmp_path / "rates.json").write_text("{bad")
    result = RateService(tmp_path, fail).latest()
    assert result.source == "demo" and result.day is None


def test_live_data_survives_cache_write_failure(tmp_path):
    with patch("quantumfx.core.atomic_json", side_effect=PermissionError):
        result = RateService(tmp_path, lambda url: payload()).latest()
    assert result.source == "online" and "nicht gespeichert" in result.warning


@pytest.mark.parametrize("mutation", [lambda p: p.update(base="USD"), lambda p: p.update(date="bad"),
    lambda p: p.update(date=(date.today() + timedelta(days=2)).isoformat()),
    lambda p: p.update(rates={"USD": 0})])
def test_invalid_api_never_becomes_live(tmp_path, mutation):
    p = payload()
    mutation(p)
    assert RateService(tmp_path, lambda url: p).latest().source == "demo"


def test_cache_bad_base_and_future():
    p = Snapshot({"EUR": D(1)}, date.today().isoformat(), datetime.now(timezone.utc).isoformat(), "online").payload()
    p["rates"]["EUR"] = "2"
    with pytest.raises(ValueError):
        cached_snapshot(p)
    p["rates"]["EUR"] = "1"
    p["fetched"] = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    with pytest.raises(ValueError):
        cached_snapshot(p)


def test_history_online_and_cache(tmp_path):
    today = date.today().isoformat()
    p = {"base": "EUR", "rates": {today: {"USD": 1.25}}}
    points, source = RateService(tmp_path, lambda url: p).history("EUR", "USD", 30)
    assert points == [(today, D("1.25"))] and source == "online"
    assert RateService(tmp_path, fail).history("EUR", "USD", 30) == (points, "cache")


def test_history_failure_no_fabrication(tmp_path):
    with pytest.raises(ValueError, match="nicht verfügbar"):
        RateService(tmp_path, fail).history("EUR", "USD", 90)
    points, source = RateService(tmp_path, fail).history("EUR", "EUR", 90)
    assert source == "identity" and all(p[1] == 1 for p in points)


def test_history_stale_cache_excluded(tmp_path):
    atomic_json(tmp_path / "chart-EUR-USD-30.json", {"base": "EUR", "rates": {"2001-01-01": {"USD": 1}}})
    with pytest.raises(ValueError):
        RateService(tmp_path, fail).history("EUR", "USD", 30)


def row():
    return dict(time="2026-01-01", amount="100", base="EUR", target="USD", net="120", rate="1.2",
                fee="0", date="2026-01-01", source="online")


def test_persistence_and_clear(tmp_path):
    s = Store(tmp_path)
    s.prefs["favorites"] = ["EUR/USD"]
    s.save()
    s.add(row())
    again = Store(tmp_path)
    assert again.rows == [row()] and again.prefs["favorites"] == ["EUR/USD"]
    again.clear()
    assert Store(tmp_path).rows == []


def test_write_failure_preserves_history(tmp_path):
    s = Store(tmp_path)
    s.add(row())
    with patch("quantumfx.core.atomic_json", side_effect=PermissionError):
        with pytest.raises(OSError):
            s.clear()
    assert len(s.rows) == 1


def test_malformed_local_data(tmp_path):
    atomic_json(tmp_path / "settings.json", [])
    atomic_json(tmp_path / "history.json", [None, {}, "x", row()])
    s = Store(tmp_path)
    assert s.prefs == {} and s.rows == [row()]


def test_csv_unicode_decimal_and_formula_escape(tmp_path):
    path = tmp_path / "out.csv"
    export_csv(path, [{"a": "=1+1", "b": "123.456", "c": "Währung"}], ["a", "b", "c"])
    with path.open(encoding="utf-8-sig", newline="") as f:
        assert list(csv.DictReader(f, delimiter=";")) == [{"a": "'=1+1", "b": "123.456", "c": "Währung"}]
