from dvault.strats import (Dvine)
from dvault.accounts import (Alpaca)

# class MetaPrinter(type):
#     def __repr__(cls):
#         return "__repr__ on the metaclass"
#
#     def __str__(cls):
#         return "__str__ on the metaclass"
#
# class dvine_us_equity_3Pct(metaclass=MetaPrinter):

class dvine_us_equity:
    strat = Dvine
    entry_point_base = ["dvine"] + strat.default_args + [
            '--strategy-bet-size-usd', 100 ]


class dvine_us_equity_3Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_3Pct
    entry_point = dvine_us_equity.entry_point_base + [
            '--alpaca-base-url', account.base_url,
            '--nstd-thresh', 0.05 ]

class dvine_us_equity_5Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_5Pct
    entry_point = dvine_us_equity.entry_point_base + [
            '--alpaca-base-url', account.base_url,
            '--nstd-thresh', 0.03 ]


