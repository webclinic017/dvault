from dvault import (bots)
from os import path
import string
import random
from datetime import datetime
from dvault.accounts import (Alpaca, get_alpaca_data_args, get_alpaca_args)
from dvault.discords import (dvine_5pct, dvine_3pct, dvine_2pct, dstock_dspam)
from dvault._charts import (
        get_chart_cmd_series, chart_all_returns, chart_recent_returns,
        chart_accounts, dvine_chart, dmule_chart, get_chart_base_args, get_chart_tmp_args)

#
# ## us_equity universe, 3% std dev filter
#
# class dvine_chart_us_equity_3Pct:
#     tmp_dir = path.join('/tmp', 'dvine_chart_us_equity_3Pct' + ''.join(random.choice(string.digits) for i in range(5)) )
#     bot = bots.dvine_us_equity_3Pct
#     discord_webhook_url = dvine_3pct.webhook_url
#
#     from_date_args = bot.from_date_args
#     base_args = \
#             bot.strat.base_args + \
#             bot.alpaca_args + \
#             [
#                 '--plot-file', f'{tmp_dir}/dvine_chart_us_equity_3Pct.png',
#                 '--output-file-list', f'{tmp_dir}/dvine_chart_us_equity_3Pct.json',
#                 '--bot-name', bot.__name__ ]
#
# class dvine_us_equity_3Pct_all_returns(dvine_chart_us_equity_3Pct):
#     entry_point = get_chart_cmd_series(
#             'dvine_us_equity_3Pct_all_returns',
#             dvine_chart.entry_point,
#             chart_all_returns.base_args +
#                 dvine_chart_us_equity_3Pct.bot.strat.base_args +
#                 dvine_chart_us_equity_3Pct.base_args +
#                 dvine_chart_us_equity_3Pct.from_date_args,
#             dvine_chart_us_equity_3Pct.discord_webhook_url)
#
# class dvine_us_equity_3Pct_recent_returns(dvine_chart_us_equity_3Pct):
#     entry_point = get_chart_cmd_series(
#             'dvine_us_equity_3Pct_recent_returns',
#             dvine_chart.entry_point,
#             chart_recent_returns.base_args +  dvine_chart_us_equity_3Pct.base_args,
#             dvine_chart_us_equity_3Pct.discord_webhook_url)
#
# class dvine_us_equity_3Pct_performance(chart_accounts):
#     entry_point = get_chart_cmd_series(
#             'dvine_us_equity_3Pct_performance',
#             dvine_chart.entry_point,
#             chart_accounts.base_args +
#                 dvine_chart_us_equity_3Pct.bot.strat.base_args +
#                 dvine_chart_us_equity_3Pct.base_args +
#                 dvine_chart_us_equity_3Pct.from_date_args + [
#                     '--accounts-floor', 75000.00],
#             dvine_chart_us_equity_3Pct.discord_webhook_url)
#
#
#
# ## us_equity universe, 2.49% std dev filter
#
# class dvine_chart_us_equity_2Pct:
#     tmp_dir = path.join('/tmp', 'dvine_chart_us_equity_2Pct' + ''.join(random.choice(string.digits) for i in range(5)) )
#     bot = bots.dvine_us_equity_2Pct
#     discord_webhook_url = dvine_2pct.webhook_url
#     from_date_args = ['--from-date', '2022-08-03T00:00:00']
#
#     base_args = _get_chart_tmp_args("dvine_chart_us_equity_2Pct") + _get_chart_base_args(bot, "dvine_chart_us_equity_2Pct")
#
# class dvine_us_equity_2Pct_all_returns(dvine_chart_us_equity_2Pct):
#     entry_point = get_chart_cmd_series(
#             'dvine_us_equity_2Pct_all_returns',
#             dvine_chart.entry_point,
#             chart_all_returns.base_args +
#                 dvine_chart_us_equity_2Pct.bot.strat.base_args +
#                 dvine_chart_us_equity_2Pct.base_args +
#                 dvine_chart_us_equity_2Pct.from_date_args,
#             dvine_chart_us_equity_2Pct.discord_webhook_url)
#
# class dvine_us_equity_2Pct_recent_returns(dvine_chart_us_equity_2Pct):
#     entry_point = get_chart_cmd_series(
#             'dvine_us_equity_2Pct_recent_returns',
#             dvine_chart.entry_point,
#             chart_recent_returns.base_args +  dvine_chart_us_equity_2Pct.base_args,
#             dvine_chart_us_equity_2Pct.discord_webhook_url)
#
# class dvine_us_equity_2Pct_performance(chart_accounts):
#     entry_point = get_chart_cmd_series(
#             'dvine_us_equity_2Pct_performance',
#             dvine_chart.entry_point,
#             chart_accounts.base_args +
#                 dvine_chart_us_equity_2Pct.bot.strat.base_args +
#                 dvine_chart_us_equity_2Pct.base_args +
#                 dvine_chart_us_equity_2Pct.from_date_args + [
#                     '--accounts-floor', 25000.00],
#             dvine_chart_us_equity_2Pct.discord_webhook_url)
#


# Diagram:
# https://sketchviz.com/@AlwaysTraining/5b68a4e3e5494e5f7cf2ed20678bcced/b47f5491f7c4fbd5736128f96004552f4ec0c685

class dmule_chart_all_tikr_returns(chart_all_returns):

    discord_webhook_url = dstock_dspam.webhook_url

    entry_point = get_chart_cmd_series(
            'dmule_chart_all_tikr_returns',
            # TODO this is dedicated to one account only right now, this should
            # change to shared account
            dmule_chart.entry_point,
            chart_all_returns.base_args +
            get_alpaca_data_args() +
            get_alpaca_args(Alpaca.play_time) +
            [
                '--from-date', '2022-08-25T00:00:00',
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
            get_alpaca_args(Alpaca.play_time) +
            [
                '--from-date', '2022-08-25T00:00:00',
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
            get_alpaca_args(Alpaca.play_time) +
            [
                '--from-date', '2022-08-25T00:00:00',
                '--to-date', datetime.now().replace(hour=23,minute=59,second=59,microsecond=0).isoformat(),
                '--orders-series', 'strat',
                '--universe-name', 'crypto',
                '--orders-max-spam', 1,
                '--orders-y-max', 0.04,
                '--orders-y-min', -0.04
                ],
            discord_webhook_url)

class dmule_chart_dmoon_adhoc_dev:
    bot = bots.dmoon_adhoc_dev
    discord_webhook_url = bot.discord_webhook_url
    from_date_args = [
            '--from-date', '2022-08-18T00:00:00',
            '--to-date', datetime.now().replace(microsecond=0).isoformat(),
            '--orders-series', 'tikr',
            ]

    base_args = get_chart_tmp_args("dmule_chart_dmoon_adhoc_dev") + get_chart_base_args(bot, "dmule_chart_dmoon_adhoc_dev") + bot.common_args


class dmule_chart_dmoon_adhoc_dev_all_returns(dmule_chart_dmoon_adhoc_dev):

    discord_webhook_url = dstock_dspam.webhook_url
    entry_point = get_chart_cmd_series(
            'dmule_chart_dmoon_adhoc_dev_all_returns',
            dmule_chart.entry_point,
            chart_all_returns.base_args +
                dmule_chart_dmoon_adhoc_dev.bot.strat.base_args +
                dmule_chart_dmoon_adhoc_dev.base_args +
                dmule_chart_dmoon_adhoc_dev.from_date_args,
            dmule_chart_dmoon_adhoc_dev.discord_webhook_url)

