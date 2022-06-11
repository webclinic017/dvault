from dvault.accounts import (Alpaca)

class Dvine:
    homepage = "https://github.com/AlwaysTraining/dvine"
    base_args = [
            "--alpaca-api-data-key", Alpaca.prime_time.api_key,
            "--alpaca-secret-api-data-key", Alpaca.prime_time.api_secret_key ]
    default_args = base_args + [
            "--universe-name", "us_equity",
            "--log-level", "INFO",
            "--alpaca-data-url", "https://data.alpaca.markets",
            "--strategy-max-assets", 10,
            "--strategy-min-assets", 0 ]




