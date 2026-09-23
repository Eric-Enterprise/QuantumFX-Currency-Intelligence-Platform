"""Validated rates, decimal arithmetic and atomic local persistence."""
import csv
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from urllib.request import Request, urlopen

API = "https://api.frankfurter.dev/v1"
DEMO = {"EUR": 1, "USD": 1.16, "GBP": .87, "JPY": 184.1, "SEK": 10.82,
        "CHF": .91, "KRW": 1736.2, "CNY": 7.98}


def data_dir():
    return Path(os.environ.get("QUANTUMFX_DATA_DIR") or
                str(Path(os.environ.get("LOCALAPPDATA", Path.home())) / "QuantumFX"))


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         delete=False) as f:
            name = f.name
            json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def number(raw):
    """Accept an ungrouped decimal with comma OR dot; never guess grouping."""
    raw = str(raw).strip()
    if len(raw) > 24 or not re.fullmatch(r"\d+(?:[.,]\d{1,8})?", raw):
        raise ValueError("Enter a number without thousands separators, e.g. 1234.56 (up to 8 decimal places).")
    try:
        value = Decimal(raw.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("Invalid number.") from exc
    if not value.is_finite() or value > Decimal("1000000000000"):
        raise ValueError("Amount must not exceed 1,000,000,000,000.")
    return value


def validate_rates(rates):
    if not isinstance(rates, dict) or not rates:
        raise ValueError("No valid rate data.")
    valid = {}
    for code, value in rates.items():
        if not isinstance(code, str) or not re.fullmatch("[A-Z]{3}", code) or isinstance(value, bool):
            raise ValueError("Invalid currency.")
        try:
            dec = Decimal(str(value))
        except InvalidOperation as exc:
            raise ValueError("Invalid rate.") from exc
        if not dec.is_finite() or not 0 < dec < Decimal("1e12"):
            raise ValueError("Invalid rate.")
        valid[code] = dec
    return valid


@dataclass
class Snapshot:
    rates: dict
    day: str | None
    fetched: str | None
    source: str
    warning: str = ""

    def payload(self):
        return {"rates": {k: str(v) for k, v in self.rates.items()},
                "date": self.day, "fetched": self.fetched, "base": "EUR"}


def cached_snapshot(data):
    if not isinstance(data, dict) or data.get("base") != "EUR":
        raise ValueError("Invalid cache.")
    day = date.fromisoformat(data["date"])
    fetched = datetime.fromisoformat(data["fetched"])
    if day > date.today() or fetched.tzinfo is None or fetched > datetime.now(timezone.utc) + timedelta(minutes=5):
        raise ValueError("Invalid cache date.")
    rates = validate_rates(data["rates"])
    if rates.get("EUR") != 1:
        raise ValueError("Invalid base currency.")
    return Snapshot(rates, day.isoformat(), fetched.isoformat(), "cache")


def request_json(url):
    req = Request(url, headers={"User-Agent": "QuantumFX/2.0", "Accept": "application/json"})
    with urlopen(req, timeout=12) as response:
        body = response.read(4_000_001)
        if len(body) > 4_000_000:
            raise ValueError("Response is too large.")
        return json.loads(body)


class RateService:
    def __init__(self, folder=None, fetch=request_json):
        self.folder = Path(folder) if folder else data_dir()
        self.fetch = fetch

    def cached(self):
        try:
            return cached_snapshot(read_json(self.folder / "rates.json"))
        except (ValueError, TypeError, KeyError):
            return Snapshot(validate_rates(DEMO), None, None, "demo")

    def latest(self):
        try:
            data = self.fetch(API + "/latest?base=EUR")
            if data.get("base") != "EUR":
                raise ValueError("Incorrect base currency.")
            day = date.fromisoformat(data["date"])
            if day > date.today():
                raise ValueError("Rate date is in the future.")
            rates = validate_rates(data["rates"])
            rates["EUR"] = Decimal(1)
            result = Snapshot(rates, day.isoformat(), datetime.now(timezone.utc).isoformat(), "online")
        except Exception as exc:
            result = self.cached()
            result.warning = "Request failed: " + str(exc)[:180]
            return result
        try:
            atomic_json(self.folder / "rates.json", result.payload())
        except OSError:
            result.warning = "Rates loaded; the local cache could not be saved."
        return result

    def history(self, base, target, days):
        if not all(re.fullmatch("[A-Z]{3}", x) for x in (base, target)) or days not in (30, 90, 365):
            raise ValueError("Invalid period or currency.")
        end = date.today()
        start = end - timedelta(days=days)
        if base == target:
            return [(start.isoformat(), Decimal(1)), (end.isoformat(), Decimal(1))], "identity"
        path = self.folder / f"chart-{base}-{target}-{days}.json"
        def parse(data):
            if not isinstance(data, dict) or data.get("base") != base:
                raise ValueError("Invalid time series.")
            points = []
            for day, rates in data["rates"].items():
                d = date.fromisoformat(day)
                value = validate_rates(rates)[target]
                if start <= d <= end:
                    points.append((day, value))
            if not points:
                raise ValueError("No rates available for the selected period.")
            return sorted(points)
        try:
            data = self.fetch(f"{API}/{start}..{end}?base={base}&symbols={target}")
            points = parse(data)
        except Exception:
            try:
                return parse(read_json(path)), "cache"
            except (ValueError, KeyError, TypeError, AttributeError):
                raise ValueError("Rate history is unavailable. Check your internet connection and try again.")
        try:
            atomic_json(path, data)
        except OSError:
            pass
        return points, "online"


def convert(amount, base, target, rates, percent=Decimal(0), fixed=Decimal(0)):
    for value in (amount, percent, fixed):
        if not value.is_finite() or value < 0:
            raise ValueError("Negative or invalid amounts are not allowed.")
    if percent > 100:
        raise ValueError("Percentage fee must be between 0 and 100.")
    if base not in rates or target not in rates:
        raise ValueError("Currency not available in this rate snapshot.")
    fee = amount * percent / 100 + fixed
    if fee > amount:
        raise ValueError("Fees exceed the source amount.")
    rate = rates[target] / rates[base]
    return {"gross": amount * rate, "net": (amount - fee) * rate,
            "fee": fee, "rate": rate}


def money(value, currency):
    digits = 0 if currency in {"JPY", "KRW", "ISK", "CLP", "VND"} else 2
    rounded = value.quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return f"{rounded:,.{digits}f}"


class Store:
    def __init__(self, folder=None):
        self.folder = Path(folder) if folder else data_dir()
        prefs = read_json(self.folder / "settings.json", {})
        self.prefs = prefs if isinstance(prefs, dict) else {}
        rows = read_json(self.folder / "history.json", [])
        required = {"time", "amount", "base", "target", "net", "rate", "fee", "date", "source"}
        self.rows = [r for r in rows if isinstance(r, dict) and required <= r.keys()
                     and all(isinstance(r[k], str) for k in required)][:1000] if isinstance(rows, list) else []

    def save(self):
        atomic_json(self.folder / "settings.json", self.prefs)

    def add(self, row):
        rows = [row] + self.rows[:999]
        atomic_json(self.folder / "history.json", rows)
        self.rows = rows

    def clear(self):
        atomic_json(self.folder / "history.json", [])
        self.rows = []


def export_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            # Imported local records must never become spreadsheet formulas.
            writer.writerow({key: ("'" + str(row.get(key, "")) if str(row.get(key, "")).startswith(("=", "+", "-", "@"))
                                   else row.get(key, "")) for key in fields})
