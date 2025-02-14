from dvault import (bots)
from os import path
import string
import random
from datetime import datetime
from dvault.accounts import (Alpaca, get_alpaca_data_args, get_alpaca_args)
from dvault.discords import (dvine_3pct, dvine_2pct)

# These charts must run with with dvine v2.2
#
# Prior to v2.2 dmark was not used, so the orders made by these old bots
# can not be properly organized, and live on legacy island.  When and if
# we stop running the two old dvine v2.2 bots (3Pct and 2Pct) we can
# erase this file

class dvine_chart:
    entry_point_base = ["dvine_chart"]

class dvine_chart_orders:
    entry_point_base = dvine_chart.entry_point_base + [
            '--chart-type', 'orders',
            '--with-order-status', 'filled' ]

class dvine_chart_accounts:
    entry_point_base = dvine_chart.entry_point_base + [
            '--chart-type', 'accounts'
            ]

class dvine_chart_all_returns:
    entry_point_base = dvine_chart_orders.entry_point_base + [
            '--orders-max-spam', 1 ]

class dvine_chart_recent_returns:
    entry_point_base = dvine_chart_orders.entry_point_base + [
            '--orders-max-spam', 2,
            '--orders-with-fill-after', 'now' ]



def _get_chart_cmd_series(name, base_args, discord_webhook_url):
    tmp_dir = path.join('/tmp','_get_chart_cmd_series' + ''.join(random.choice(string.digits) for i in range(5)) )
    pre_clean = [ 'rm', '-rf', tmp_dir ]
    create_dir = [ 'mkdir', '-p', tmp_dir]
    gen_chart = base_args + [
                '--plot-file', f'{tmp_dir}/{name}.png',
                '--output-file-list', f'{tmp_dir}/{name}.json' ]

    notify = [ 'dsquire',
            '--embed-file-list', f'{tmp_dir}/{name}.json',
            '--discord-webhook-url', discord_webhook_url ]

    cleanup = [ 'rm', '-rf', tmp_dir ]

    return [pre_clean, create_dir, gen_chart, notify, cleanup ]


def _get_chart_tmp_args(chart_name):
    tmp_dir = path.join('/tmp', chart_name + ''.join(random.choice(string.digits) for i in range(5)) )
    return [
            '--plot-file', f'{tmp_dir}/{chart_name}.png',
            '--output-file-list', f'{tmp_dir}/{chart_name}.json']


def _get_chart_base_args(bot,chart_name):

    return \
            bot.strat.base_args + \
            bot.alpaca_args + \
            [
                '--bot-name', bot.__name__,
                ]

## us_equity universe, 3% std dev filter

class dvine_chart_us_equity_3Pct:
    tmp_dir = path.join('/tmp', 'dvine_chart_us_equity_3Pct' + ''.join(random.choice(string.digits) for i in range(5)) )
    bot = bots.dvine_us_equity_3Pct
    discord_webhook_url = dvine_3pct.webhook_url

    from_date_args = bot.from_date_args
    base_args = \
            bot.strat.base_args + \
            bot.alpaca_args + \
            [
                '--plot-file', f'{tmp_dir}/dvine_chart_us_equity_3Pct.png',
                '--output-file-list', f'{tmp_dir}/dvine_chart_us_equity_3Pct.json',
                '--bot-name', bot.__name__ ]

class dvine_us_equity_3Pct_all_returns(dvine_chart_us_equity_3Pct):
    entry_point = _get_chart_cmd_series(
            'dvine_us_equity_3Pct_all_returns',
            dvine_chart_all_returns.entry_point_base +
                dvine_chart_us_equity_3Pct.bot.strat.base_args +
                dvine_chart_us_equity_3Pct.base_args +
                dvine_chart_us_equity_3Pct.from_date_args,
            dvine_chart_us_equity_3Pct.discord_webhook_url)

class dvine_us_equity_3Pct_recent_returns(dvine_chart_us_equity_3Pct):
    entry_point = _get_chart_cmd_series(
            'dvine_us_equity_3Pct_recent_returns',
            dvine_chart_recent_returns.entry_point_base +  dvine_chart_us_equity_3Pct.base_args,
            dvine_chart_us_equity_3Pct.discord_webhook_url)

class dvine_us_equity_3Pct_performance(dvine_chart_accounts):
    entry_point = _get_chart_cmd_series(
            'dvine_us_equity_3Pct_performance',
            dvine_chart_accounts.entry_point_base +
                dvine_chart_us_equity_3Pct.bot.strat.base_args +
                dvine_chart_us_equity_3Pct.base_args +
                dvine_chart_us_equity_3Pct.from_date_args + [
                    '--accounts-floor', 75000.00],
            dvine_chart_us_equity_3Pct.discord_webhook_url)



## us_equity universe, 2.49% std dev filter

class dvine_chart_us_equity_2Pct:
    tmp_dir = path.join('/tmp', 'dvine_chart_us_equity_2Pct' + ''.join(random.choice(string.digits) for i in range(5)) )
    bot = bots.dvine_us_equity_2Pct
    discord_webhook_url = dvine_2pct.webhook_url
    from_date_args = ['--from-date', '2022-08-03T00:00:00']

    base_args = _get_chart_tmp_args("dvine_chart_us_equity_2Pct") + _get_chart_base_args(bot, "dvine_chart_us_equity_2Pct")

class dvine_us_equity_2Pct_all_returns(dvine_chart_us_equity_2Pct):
    entry_point = _get_chart_cmd_series(
            'dvine_us_equity_2Pct_all_returns',
            dvine_chart_all_returns.entry_point_base +
                dvine_chart_us_equity_2Pct.bot.strat.base_args +
                dvine_chart_us_equity_2Pct.base_args +
                dvine_chart_us_equity_2Pct.from_date_args,
            dvine_chart_us_equity_2Pct.discord_webhook_url)

class dvine_us_equity_2Pct_recent_returns(dvine_chart_us_equity_2Pct):
    entry_point = _get_chart_cmd_series(
            'dvine_us_equity_2Pct_recent_returns',
            dvine_chart_recent_returns.entry_point_base +  dvine_chart_us_equity_2Pct.base_args,
            dvine_chart_us_equity_2Pct.discord_webhook_url)

class dvine_us_equity_2Pct_performance(dvine_chart_accounts):
    entry_point = _get_chart_cmd_series(
            'dvine_us_equity_2Pct_performance',
            dvine_chart_accounts.entry_point_base +
                dvine_chart_us_equity_2Pct.bot.strat.base_args +
                dvine_chart_us_equity_2Pct.base_args +
                dvine_chart_us_equity_2Pct.from_date_args + [
                    '--accounts-floor', 25000.00],
            dvine_chart_us_equity_2Pct.discord_webhook_url)


