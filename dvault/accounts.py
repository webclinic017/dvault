
class Alpaca:

    class prime_time:
        email = "derrick.karimi@gmail.com"
        api_key = "PKOJLZ8A51XL5ZXEC2K8"
        api_secret_key = "kAo94szbgveo8N2S2megBkpK9QS86Gxr4x1IlIGd"
        base_url = "https://paper-api.alpaca.markets"


    class dvine_us_equity_2Pct:
        email = "derrick.karimi+dvine_us_equity_2Pct@gmail.com"
        api_key = "PKCKDGNC3A582IX8TF37"
        api_secret_key = "R5ncBJB4zLhOGvLdv8NKc9opnTPTiuj5eO7yezh2"
        base_url = "https://paper-api.alpaca.markets"

    class dvine_us_equity_3Pct:
        # last reset 2022-09-07
        email = "derrick.karimi+dvine_us_equity_3Pct@gmail.com"
        api_key = "PKITWDO0YROMDABRLNKS"
        api_secret_key = "ELWrXUPMeE7akfxFhcRsxcGz0CrBmzCk8FGUqBAi"
        base_url = "https://paper-api.alpaca.markets"

    class dvine_us_equity_5Pct:
        # retried 2022-08-03
        # revived 2022-08-19
        # reset 2022-09-04
        email = "derrick.karimi+dvine_us_equity_5Pct@gmail.com"
        api_key = "PK2ZN7V6XG1E1WQKEK6D"
        api_secret_key = "1qRnTszQV1O8jttgRwZfv3cVyA4LQJGC0jA21F4z"
        base_url = "https://paper-api.alpaca.markets"


    class play_time:
        # last reset 2022-09-07
        email = "derrick.karimi+dvine_fractionable_universe_3Hour@gmail.com"
        api_key = "PK75KYQLSUBLZ7TQ0AXD"
        api_secret_key = "v4vwf1ostRuZZHwZxHnntKpwwK76FXVbT3cYc7So"
        base_url = "https://paper-api.alpaca.markets"

    class dmoon_alpha:
        email = "derrick.karimi+dvine_fractionable_universe_1Min@gmail.com"
        api_key = "PKMWPAAJ4URQJSM2X1KI"
        api_secret_key = "OATplWoidbTHrrn9HXAprWCcOXgT7QQoEyJakNrJ"
        base_url = "https://paper-api.alpaca.markets"

def get_alpaca_args(account):
    return [ '--alpaca-base-url', account.base_url,
             '--alpaca-api-key', account.api_key,
             '--alpaca-secret-key', account.api_secret_key ]

def get_alpaca_data_args():
    return [
            "--alpaca-api-data-key", Alpaca.prime_time.api_key,
            "--alpaca-secret-data-key", Alpaca.prime_time.api_secret_key ]

