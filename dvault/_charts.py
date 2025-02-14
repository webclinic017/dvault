
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

class chart_performance:
    base_args = [
            '--chart-name', 'Equity Curve',
            '--chart-type', 'accounts' ]

class chart_all_returns:
    base_args = chart_orders.base_args + [
            '--chart-name', 'All Returns',
            '--orders-max-spam', 1 ]

class chart_recent_returns:
    base_args = chart_orders.base_args + [
            '--chart-name', "Recent Returns",
            '--orders-max-spam', 2,
            '--orders-with-fill-after', 'now' ]

def get_upgrade_cmd(packages, venv_dir=None):
    if isinstance(packages, list):
        pdict = {}
        for cur_package in packages:
            pdict[cur_package] = None
        packages = pdict

    upgrade_toks = []
    for package, version in packages.items():
        upgrade_toks += \
            [f"git+ssh://git@github.com/AlwaysTraining/{package}.git@{version}"] \
            if version else \
            [f"git+ssh://git@github.com/AlwaysTraining/{package}.git"]

    venv_launch = [] if not venv_dir else \
            ['venv_launch.sh', path.expandvars(path.expanduser(venv_dir))]

    return venv_launch + ['pip', 'install'] + upgrade_toks + ['--upgrade']

