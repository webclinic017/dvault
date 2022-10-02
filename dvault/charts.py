# Diagram:
# https://sketchviz.com/@AlwaysTraining/5b68a4e3e5494e5f7cf2ed20678bcced/b47f5491f7c4fbd5736128f96004552f4ec0c685

from dvault import (bots)
from os import path
import string
import random
from datetime import datetime
from dvault.accounts import (Alpaca, get_alpaca_data_args, get_alpaca_args)
from dvault._charts import (
        get_chart_cmd_series, chart_all_returns,
        dmule_chart, get_chart_base_args, get_chart_tmp_args, get_upgrade_cmd)
from dvault.discords import (dstock_dspam)

class dmule_chart_all_tikr_returns(chart_all_returns):

    discord_webhook_url = dstock_dspam.webhook_url

    entry_point = get_chart_cmd_series(
            'dmule_chart_all_tikr_returns',
            # TODO this is dedicated to one account only right now, this should
            # change to shared account
            dmule_chart.entry_point,
            chart_all_returns.base_args +
            get_alpaca_data_args() +
            get_alpaca_args(Alpaca.dmark_herd) +
            [
                '--from-date', '2022-09-30T00:00:00',
                '--to-date', datetime.now().replace(hour=23,minute=59,second=59,microsecond=0).isoformat(),
                '--orders-series', 'tikr',
                '--universe-name', 'crypto',
                '--orders-max-spam', 1,
                '--orders-y-max', 0.04,
                '--orders-y-min', -0.04
                ],
            discord_webhook_url)

class dmule_chart_all_bot_returns(chart_all_returns):

    discord_webhook_url = dstock_dspam.webhook_url

    entry_point = get_chart_cmd_series(
            'dmule_chart_all_bot_returns',
            dmule_chart.entry_point,
            chart_all_returns.base_args +
            get_alpaca_data_args() +
            get_alpaca_args(Alpaca.dmark_herd) +
            [
                '--from-date', '2022-09-30T00:00:00',
                '--to-date', datetime.now().replace(hour=23,minute=59,second=59,microsecond=0).isoformat(),
                '--orders-series', 'bot',
                '--universe-name', 'crypto',
                '--orders-max-spam', 1,
                '--orders-y-max', 0.04,
                '--orders-y-min', -0.04
                ],
            discord_webhook_url)


class dmule_chart_all_strat_returns(chart_all_returns):

    discord_webhook_url = dstock_dspam.webhook_url

    entry_point = get_chart_cmd_series(
            'dmule_chart_all_strat_returns',
            dmule_chart.entry_point,
            chart_all_returns.base_args +
            get_alpaca_data_args() +
            get_alpaca_args(Alpaca.dmark_herd) +
            [
                '--from-date', '2022-09-30T00:00:00',
                '--to-date', datetime.now().replace(hour=23,minute=59,second=59,microsecond=0).isoformat(),
                '--orders-series', 'strat',
                '--universe-name', 'crypto',
                '--orders-max-spam', 1,
                '--orders-y-max', 0.04,
                '--orders-y-min', -0.04
                ],
            discord_webhook_url)

class dmule_chart_upgrade:
    dev_upgrade_cmds = get_upgrade_cmd(['dmark', 'dmule', 'dvault'])
    prod_upgrade_cmds = get_upgrade_cmd(
            ['dmark', 'dmule', 'dvault'],
            "~/.dmule_versions/None" )

