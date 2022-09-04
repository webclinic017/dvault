
# Generic chart functionality, shared between bots and charts modules
#
# in general i am now trying to put logic for charts into the most
# appropriate 'module', bot charts in 'bots', strat charts in 'strats', and
# then overall charts in 'charts'
#
# These all need similar helper functions as they all use dmule (at the moment)
# so that common chart logic lives here

from os import path
import random
import string

def get_chart_tmp_args(chart_name):
    tmp_dir = path.join('/tmp', chart_name + ''.join(random.choice(string.digits) for i in range(5)) )
    return [
            '--plot-file', f'{tmp_dir}/{chart_name}.png',
            '--output-file-list', f'{tmp_dir}/{chart_name}.json']


def get_chart_base_args(bot,chart_name):

    return \
            bot.strat.base_args + \
            bot.alpaca_args + \
            [
                '--bot-name', bot.__name__,
                '--strategy-name', bot.strat.__name__
                ]

def get_chart_cmd_series(name, entry_point, base_args, discord_webhook_url):
    tmp_dir = path.join('/tmp','get_chart_cmd_series' + "." + name + '.' + ''.join(
        random.choice(string.digits) for i in range(5)) )

    pre_clean = [ 'rm', '-rf', tmp_dir ]
    create_dir = [ 'mkdir', '-p', tmp_dir]
    gen_chart = entry_point + base_args + [
                '--plot-file', f'{tmp_dir}/{name}.png',
                '--output-file-list', f'{tmp_dir}/{name}.json' ]

    notify = [ 'dsquire',
            '--embed-file-list', f'{tmp_dir}/{name}.json',
            '--discord-webhook-url', discord_webhook_url ]

    cleanup = [ 'rm', '-rf', tmp_dir ]

    return [pre_clean, create_dir, gen_chart, notify, cleanup ]

class dvine_chart:
    entry_point = ["dvine_chart"]

class dmule_chart:
    entry_point = ["dmule_chart"]

class chart_orders:
    base_args = [
            '--chart-type', 'orders',
            '--with-order-status', 'filled' ]

class chart_accounts:
    base_args = [
            '--chart-type', 'accounts' ]

class chart_all_returns:
    base_args = chart_orders.base_args + [
            '--orders-max-spam', 20 ]

class chart_recent_returns:
    base_args = chart_orders.base_args + [
            '--orders-max-spam', 20,
            '--orders-with-fill-after', 'now' ]

