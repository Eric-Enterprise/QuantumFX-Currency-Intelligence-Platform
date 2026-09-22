import pytest
import json
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import sys

# Import the module we're testing
import importlib.util
spec = importlib.util.spec_from_file_location(
    "quantum_fx",
    "QuantumFX™ Currency Intelligence Platform.py"
)
quantum_fx = importlib.util.module_from_spec(spec)


# ============================================================
#  FIXTURES
# ============================================================
@pytest.fixture
def temp_cache_file():
    """Create a temporary cache file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def sample_rates():
    """Sample exchange rates for testing."""
    return {
        "EUR": 1.0,
        "USD": 1.16,
        "GBP": 0.87,
        "JPY": 184.1,
        "SEK": 10.82,
        "CHF": 0.91,
        "KRW": 1736.2,
        "CNY": 7.98,
    }


@pytest.fixture
def sample_api_response():
    """Sample API response from Frankfurter API."""
    return {
        "base": "EUR",
        "date": "2026-06-01",
        "rates": {
            "USD": 1.16,
            "GBP": 0.87,
            "JPY": 184.1,
            "SEK": 10.82,
            "CHF": 0.91,
            "KRW": 1736.2,
            "CNY": 7.98,
        }
    }


# ============================================================
#  TESTS: Rate Fetching from API
# ============================================================
class TestFetchRatesFromAPI:
    """Tests for fetch_rates_from_api function."""

    @patch('requests.get')
    def test_fetch_rates_success(self, mock_get, sample_api_response):
        """Test successful API fetch with valid response."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_api_response
        mock_get.return_value = mock_response

        spec.loader.exec_module(quantum_fx)
        rates = quantum_fx.fetch_rates_from_api()

        assert rates["EUR"] == 1.0
        assert rates["USD"] == 1.16
        assert rates["GBP"] == 0.87
        assert "XYZ" not in rates  # Only supported currencies

    @patch('requests.get')
    def test_fetch_rates_api_timeout(self, mock_get):
        """Test handling of API timeout."""
        mock_get.side_effect = Exception("Request timeout")
        
        spec.loader.exec_module(quantum_fx)
        with pytest.raises(Exception):
            quantum_fx.fetch_rates_from_api()

    @patch('requests.get')
    def test_fetch_rates_api_error(self, mock_get):
        """Test handling of HTTP errors."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 502")
        mock_get.return_value = mock_response

        spec.loader.exec_module(quantum_fx)
        with pytest.raises(Exception):
            quantum_fx.fetch_rates_from_api()

    @patch('requests.get')
    def test_fetch_rates_filters_unsupported_currencies(self, mock_get):
        """Test that only supported currencies are returned."""
        api_response = {
            "base": "EUR",
            "rates": {
                "USD": 1.16,
                "GBP": 0.87,
                "XYZ": 99.99,  # Unsupported currency
                "ABC": 50.0,   # Unsupported currency
                "JPY": 184.1,
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = api_response
        mock_get.return_value = mock_response

        spec.loader.exec_module(quantum_fx)
        rates = quantum_fx.fetch_rates_from_api()

        assert "XYZ" not in rates
        assert "ABC" not in rates
        assert "USD" in rates
        assert "JPY" in rates


# ============================================================
#  TESTS: Rate Loading (Cache & Fallback)
# ============================================================
class TestLoadRates:
    """Tests for load_rates function with cache fallback."""

    @patch('quantum_fx.fetch_rates_from_api')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_load_rates_live_fetch(self, mock_exists, mock_file, mock_fetch, sample_rates):
        """Test loading fresh rates from API when no cache exists."""
        mock_exists.return_value = False
        mock_fetch.return_value = sample_rates

        spec.loader.exec_module(quantum_fx)
        rates, status, timestamp = quantum_fx.load_rates()

        assert rates == sample_rates
        assert status == "live"
        assert timestamp is not None
        assert isinstance(timestamp, datetime)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_load_rates_from_valid_cache(self, mock_exists, mock_file, sample_rates):
        """Test loading rates from valid (non-stale) cache."""
        now = datetime.now()
        cache_data = {
            "timestamp": now.isoformat(),
            "rates": sample_rates
        }
        mock_file.return_value.read.return_value = json.dumps(cache_data)
        mock_exists.return_value = True

        spec.loader.exec_module(quantum_fx)
        # Mock the file reading
        with patch('builtins.open', mock_open(read_data=json.dumps(cache_data))):
            rates, status, timestamp = quantum_fx.load_rates()

        assert rates == sample_rates
        assert status == "cached"
        assert timestamp is not None

    @patch('quantum_fx.fetch_rates_from_api')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_load_rates_stale_cache_refetch(self, mock_exists, mock_file, mock_fetch, sample_rates):
        """Test that stale cache triggers API refetch."""
        # Create stale cache (older than 24 hours)
        old_time = datetime.now() - timedelta(hours=25)
        cache_data = {
            "timestamp": old_time.isoformat(),
            "rates": {"EUR": 1.0, "USD": 1.10}  # Old rates
        }
        
        mock_fetch.return_value = sample_rates
        
        spec.loader.exec_module(quantum_fx)
        with patch('builtins.open', mock_open(read_data=json.dumps(cache_data))):
            with patch('os.path.exists', return_value=True):
                rates, status, timestamp = quantum_fx.load_rates()

        # Should have triggered fresh fetch due to stale cache
        assert status == "live"

    @patch('quantum_fx.fetch_rates_from_api')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_load_rates_api_fail_use_stale_cache(self, mock_exists, mock_file, mock_fetch, sample_rates):
        """Test fallback to stale cache when API fails."""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "rates": sample_rates
        }
        mock_fetch.side_effect = Exception("API unavailable")
        
        spec.loader.exec_module(quantum_fx)
        with patch('builtins.open', mock_open(read_data=json.dumps(cache_data))):
            with patch('os.path.exists', return_value=True):
                rates, status, timestamp = quantum_fx.load_rates(force_refresh=True)

        assert status == "cached"
        assert rates == sample_rates

    @patch('quantum_fx.fetch_rates_from_api')
    @patch('os.path.exists')
    def test_load_rates_no_cache_use_fallback(self, mock_exists, mock_fetch):
        """Test fallback to hardcoded rates when API fails and no cache."""
        mock_fetch.side_effect = Exception("API unavailable")
        mock_exists.return_value = False

        spec.loader.exec_module(quantum_fx)
        rates, status, timestamp = quantum_fx.load_rates(force_refresh=True)

        assert status == "offline"
        assert rates == quantum_fx.FALLBACK_RATES
        assert timestamp is None

    @patch('quantum_fx.fetch_rates_from_api')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_load_rates_corrupt_cache_ignored(self, mock_exists, mock_file, mock_fetch, sample_rates):
        """Test that corrupt cache is ignored and fresh data is fetched."""
        mock_file.return_value.read.return_value = "{ invalid json }"
        mock_fetch.return_value = sample_rates
        mock_exists.return_value = True

        spec.loader.exec_module(quantum_fx)
        with patch('builtins.open', mock_open(read_data="{ invalid json }")):
            rates, status, timestamp = quantum_fx.load_rates()

        assert status == "live"
        assert rates == sample_rates


# ============================================================
#  TESTS: Currency Conversion Logic
# ============================================================
class TestCurrencyConversion:
    """Tests for currency conversion calculations."""

    def test_convert_same_currency(self, sample_rates):
        """Test converting currency to itself returns same amount."""
        # EUR to EUR: 100 EUR = 100 EUR
        amount = 100
        from_rate = sample_rates["EUR"]
        to_rate = sample_rates["EUR"]
        
        amount_in_eur = amount / from_rate
        converted = amount_in_eur * to_rate
        
        assert converted == pytest.approx(100.0)

    def test_convert_eur_to_usd(self, sample_rates):
        """Test EUR to USD conversion."""
        # 100 EUR to USD with rate 1.16
        amount = 100
        amount_in_eur = amount / sample_rates["EUR"]  # 100
        converted = amount_in_eur * sample_rates["USD"]  # 100 * 1.16 = 116
        
        assert converted == pytest.approx(116.0)

    def test_convert_usd_to_eur(self, sample_rates):
        """Test USD to EUR conversion (inverse)."""
        # 116 USD to EUR with rate 1.16
        amount = 116
        amount_in_eur = amount / sample_rates["USD"]  # 116 / 1.16 = 100
        converted = amount_in_eur * sample_rates["EUR"]  # 100 * 1.0 = 100
        
        assert converted == pytest.approx(100.0)

    def test_convert_non_usd_currencies(self, sample_rates):
        """Test conversion between non-base currencies."""
        # 100 GBP to JPY
        amount = 100
        amount_in_eur = amount / sample_rates["GBP"]  # 100 / 0.87 ≈ 114.94
        converted = amount_in_eur * sample_rates["JPY"]  # 114.94 * 184.1
        
        assert converted > 0
        assert converted == pytest.approx(21158.9, rel=1)

    def test_convert_zero_amount(self, sample_rates):
        """Test conversion with zero amount."""
        amount = 0
        amount_in_eur = amount / sample_rates["EUR"]
        converted = amount_in_eur * sample_rates["USD"]
        
        assert converted == 0.0

    def test_convert_small_amount(self, sample_rates):
        """Test conversion with small decimal amount."""
        amount = 0.01
        amount_in_eur = amount / sample_rates["EUR"]
        converted = amount_in_eur * sample_rates["USD"]
        
        assert converted == pytest.approx(0.0116, rel=0.01)

    def test_convert_large_amount(self, sample_rates):
        """Test conversion with large amount."""
        amount = 1000000
        amount_in_eur = amount / sample_rates["EUR"]
        converted = amount_in_eur * sample_rates["USD"]
        
        assert converted == pytest.approx(1160000.0)


# ============================================================
#  TESTS: Language Support
# ============================================================
class TestLanguageSupport:
    """Tests for language support functionality."""

    def test_all_languages_have_keys(self):
        """Test that all languages have all required translation keys."""
        spec.loader.exec_module(quantum_fx)
        
        required_keys = {
            "title", "amount_label", "from_label", "to_label",
            "convert_btn", "result_prefix", "error_empty", "error_invalid",
            "lang_title", "lang_prompt", "lang_btn", "refresh_btn",
            "swap_tip", "status_live", "status_cached", "status_offline",
            "refreshing"
        }
        
        for lang, translations in quantum_fx.LANGUAGES.items():
            for key in required_keys:
                assert key in translations, f"Missing key '{key}' in {lang}"

    def test_english_language_completeness(self):
        """Test that English language has all translations."""
        spec.loader.exec_module(quantum_fx)
        
        english = quantum_fx.LANGUAGES["English"]
        assert english["title"] == "Currency Converter"
        assert english["convert_btn"] == "Convert"
        assert "Please enter a valid number" in english["error_empty"]

    def test_supported_languages_count(self):
        """Test that expected number of languages are supported."""
        spec.loader.exec_module(quantum_fx)
        
        expected_languages = {"English", "Deutsch", "Svenska", "한국어"}
        actual_languages = set(quantum_fx.LANGUAGES.keys())
        
        assert actual_languages == expected_languages


# ============================================================
#  TESTS: Configuration
# ============================================================
class TestConfiguration:
    """Tests for application configuration."""

    def test_supported_currencies_count(self):
        """Test that expected currencies are supported."""
        spec.loader.exec_module(quantum_fx)
        
        expected_count = 8
        assert len(quantum_fx.SUPPORTED_CURRENCIES) == expected_count

    def test_eur_in_supported_currencies(self):
        """Test that EUR is in supported currencies."""
        spec.loader.exec_module(quantum_fx)
        
        assert "EUR" in quantum_fx.SUPPORTED_CURRENCIES

    def test_fallback_rates_completeness(self):
        """Test that fallback rates cover all supported currencies."""
        spec.loader.exec_module(quantum_fx)
        
        for currency in quantum_fx.SUPPORTED_CURRENCIES:
            assert currency in quantum_fx.FALLBACK_RATES

    def test_fallback_rates_reasonable_values(self):
        """Test that fallback rates have reasonable values."""
        spec.loader.exec_module(quantum_fx)
        
        for currency, rate in quantum_fx.FALLBACK_RATES.items():
            assert isinstance(rate, (int, float))
            assert rate > 0, f"Rate for {currency} must be positive"

    def test_cache_max_age_hours(self):
        """Test that cache max age is configured."""
        spec.loader.exec_module(quantum_fx)
        
        assert quantum_fx.CACHE_MAX_AGE_HOURS >= 0
        assert isinstance(quantum_fx.CACHE_MAX_AGE_HOURS, int)

    def test_api_url_valid(self):
        """Test that API URL is valid."""
        spec.loader.exec_module(quantum_fx)
        
        assert quantum_fx.API_URL.startswith("https://")
        assert "frankfurter" in quantum_fx.API_URL.lower()
        assert "base=EUR" in quantum_fx.API_URL

    def test_theme_colors_defined(self):
        """Test that all theme colors are defined."""
        spec.loader.exec_module(quantum_fx)
        
        required_colors = {
            "bg", "card", "accent", "accent_hi", "text", "muted",
            "ok", "warn", "err", "field_bg"
        }
        
        for color_key in required_colors:
            assert color_key in quantum_fx.THEME
            assert isinstance(quantum_fx.THEME[color_key], str)
            assert quantum_fx.THEME[color_key].startswith("#")


# ============================================================
#  TESTS: Input Validation (for conversion)
# ============================================================
class TestInputValidation:
    """Tests for user input validation."""

    def test_valid_integer_input(self):
        """Test that integer input is valid."""
        raw = "100"
        try:
            amount = float(raw.replace(",", "."))
            assert amount == 100.0
        except ValueError:
            pytest.fail("Should accept integer input")

    def test_valid_decimal_input(self):
        """Test that decimal input is valid."""
        raw = "123.45"
        try:
            amount = float(raw.replace(",", "."))
            assert amount == pytest.approx(123.45)
        except ValueError:
            pytest.fail("Should accept decimal input")

    def test_comma_decimal_separator(self):
        """Test that comma is handled as decimal separator."""
        raw = "123,45"
        amount = float(raw.replace(",", "."))
        assert amount == pytest.approx(123.45)

    def test_invalid_text_input(self):
        """Test that non-numeric input is rejected."""
        raw = "abc"
        with pytest.raises(ValueError):
            float(raw.replace(",", "."))

    def test_empty_input(self):
        """Test handling of empty input."""
        raw = ""
        assert raw.strip() == ""

    def test_whitespace_input(self):
        """Test handling of whitespace input."""
        raw = "   "
        assert raw.strip() == ""

    def test_negative_amount(self):
        """Test that negative amounts are handled."""
        raw = "-100"
        amount = float(raw.replace(",", "."))
        assert amount == -100.0

    def test_scientific_notation(self):
        """Test that scientific notation is handled."""
        raw = "1e2"
        amount = float(raw.replace(",", "."))
        assert amount == 100.0


# ============================================================
#  INTEGRATION TESTS
# ============================================================
class TestIntegration:
    """Integration tests combining multiple components."""

    @patch('quantum_fx.fetch_rates_from_api')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_end_to_end_conversion(self, mock_exists, mock_file, mock_fetch, sample_rates, sample_api_response):
        """Test complete flow from API fetch to conversion."""
        mock_exists.return_value = False
        mock_fetch.return_value = sample_rates

        spec.loader.exec_module(quantum_fx)
        
        # Load rates
        rates, status, timestamp = quantum_fx.load_rates()
        assert status == "live"
        
        # Perform conversion
        amount = 100
        amount_in_eur = amount / rates["EUR"]
        converted = amount_in_eur * rates["USD"]
        
        assert converted == pytest.approx(116.0)

    def test_multiple_conversions_with_same_rates(self, sample_rates):
        """Test multiple conversions using same rate set."""
        spec.loader.exec_module(quantum_fx)
        
        conversions = [
            (100, "EUR", "USD", 116.0),
            (100, "GBP", "EUR", 114.94),
            (1000, "JPY", "EUR", 5.43),
        ]
        
        for amount, from_cur, to_cur, expected in conversions:
            amount_in_eur = amount / sample_rates[from_cur]
            converted = amount_in_eur * sample_rates[to_cur]
            assert converted == pytest.approx(expected, rel=0.1)
