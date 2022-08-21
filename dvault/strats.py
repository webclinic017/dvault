from dvault.accounts import (Alpaca, get_alpaca_data_args)

class Dvine:
    homepage = "https://github.com/AlwaysTraining/dvine"
    base_args = get_alpaca_data_args()
    default_args = base_args + [
            "--universe-name", "us_equity",
            "--log-level", "INFO",
            "--alpaca-data-url", "https://data.alpaca.markets",
            "--strategy-max-assets", 10,
            "--strategy-min-assets", 0 ]



class Dmoon:
    homepage = "https://github.com/AlwaysTraining/dmoon"
    base_args = get_alpaca_data_args()
    default_args = base_args + [
            "--universe-name", "unittest_universe",
            "--alpaca-data-url", "https://stream.data.alpaca.markets",
            ]

