import re

import requests

from handlers.crypto import crypto
from services.crypto_compare import CryptoCompare


class TestCrypto:
    def test_smoke_url(self):
        url_test = "https://min-api.cryptocompare.com/data"

        request = requests.get(url_test)

        assert request.status_code == 200

    def test_service_positive(self):
        rate = CryptoCompare.get_rate(["BTC"], ["USD"])

        assert "BTC" in rate and "USD" in rate['BTC']

    def test_service_empty_args(self):
        rate = CryptoCompare.get_rate()

        assert "BTC" in rate and "USD" in rate['BTC']

    def test_service_negative(self):
        rate = CryptoCompare.get_rate(["RGR"])

        assert "Error" in rate['Response']

    def test_handler_positive(self, bot, update):
        message_regex = re.compile(r'(BTC).*(\$).*')

        crypto(bot, update)
        message = bot.get_message()

        assert message_regex.search(message) is not None
