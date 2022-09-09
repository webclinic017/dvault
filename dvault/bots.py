import sys
import os
from os import path
import itertools
from dvault import strats
from dvault import discords
from dvault.accounts import (Alpaca,get_alpaca_args)
from dvault._charts import (get_chart_cmd_series, dmule_chart, chart_all_returns,
        get_chart_base_args, chart_recent_returns, chart_performance)


class dvine_us_equity:
    strat = strats.dvine
    entry_point_base = ["dvine"] + strat.default_args + [
            '--log-level', 'INFO',
            '--strategy-bet-size-usd', 100 ]


_DVINE_DAY_ARG_NAMES = [
        ( 1,200,50     ), # 0
        ( 2,213,53     ), # 1
        ( 3,220,55     ), # 2
        ( 4,227,57     ), # 3
        ( 5,233,58     ), # 4
        ( 6,240,60     ), # 5
        ( 7,247,62     ), # 6
        ( 8,253,63     ), # 7
        ( 9,260,65     ), # 8
        ( 10,267,67    ), # 9
        ( 11,273,68    ), # 10
        ( 12,280,70    ), # 11
        ( 13,286,71    ), # 12
        ( 14,293,73    ), # 13
        ( 15,300,75    ), # 14
        ( 16,307,77    ), # 15
        ( 17,313,78    ), # 16
        ( 18,320,80    ), # 17
        ( 19,327,82    ), # 18
        ( 20,333,83    ), # 19
        ( 21,340,85    ), # 20
        ( 22,347,87    ), # 21
        ( 23,353,88    ), # 22
        ( 24,360,90    ), # 23
        ( 25,367,92    ), # 24
        ( 26,373,93    ), # 25
        ( 27,380,95    ), # 26
        ( 28,387,97    ), # 27
        ( 29,393,98    ), # 28
        ( 30,400,100   ), # 29
        ( 33,419,104   ), # 30
        ( 36,439,109   ), # 31
        ( 39,459,114   ), # 32
        ( 43,486,121   ), # 33
        ( 47,513,128   ), # 34
        ( 52,546,136   ), # 35
        ( 57,579,144   ), # 36
        ( 63,619,154   ), # 37
        ( 69,659,164   ), # 38
        ( 76,705,175   ), # 39
        ( 84,759,189   ), # 40
        ( 93,818,203   ), # 41
        ( 100,900,300  ), # 42
        ( 150,1350,450 ), # 43
        ( 200,1800,600 ), # 44
        ( 253,2277,759 ) ]# 45

_VARIATION_ARG_NAMES = [
        '--trade-days-per-bar',
        '--objective-num-trade-days',
        '--threshold-num-trade-days' ]

# For some rason inside generator expressions you can't access your own class
# variables, so I have moved a lot of things out to the global namespace
#
# don't feel bad if you can't read the code below, it is write only.
# basically it is doing a mail merge cross multiply of the arg names with the
# day tuples to build a list of lists of cmd line arguments
_DVINE_DAYS = [
        list(itertools.chain.from_iterable(
            [ [arg_name, _DVINE_DAY_ARG_NAMES[i][j] ] for j, arg_name in enumerate(_VARIATION_ARG_NAMES) ]
            ))
        for i in range(len(_DVINE_DAY_ARG_NAMES))
        ]

def _get_purge_args(purge_base, postfix_args=[]):

    purge_orders_cmd = purge_base + [
            '--purge-type', 'orders', '--log-level', 'INFO']
    purge_positions_cmd = purge_base + [
            '--purge-type', 'positions', '--log-level', 'INFO']
    purge_sleep = ['sleep','2m']
    purge_cmds = [
            purge_orders_cmd + postfix_args,
            purge_sleep,
            purge_positions_cmd + postfix_args,
            purge_sleep,
            purge_positions_cmd + postfix_args ]
    return purge_cmds

def _output_to_file_cmd(command, outfile):
    #TODO quoting support
    return ['/bin/bash', '-c', ' '.join([str(x) for x in command + ['>', outfile]] )]

def _get_systemd_cmd(command, bot):
    service_name = bot if isinstance(bot, str) else bot.__name__
    return ['systemctl', command, service_name, '--user']

def _get_tmp_file(bot,filetype):
    service_name = bot if isinstance(bot, str) else bot.__name__
    return f"/tmp/dvault.bots.{service_name}.{filetype}"

def _get_write_journal_cmd(bot, options=['-n', 25], logfile=None):
    if logfile is None:
        logfile = _get_tmp_file(bot, "log")
    service_name = bot if isinstance(bot, str) else bot.__name__
    subcmd = ['journalctl', '-u', service_name, '--user'] + options
    # could not easily get journalctl out to a file without a redirect, so, wrap with bash commands
    return _output_to_file_cmd(subcmd, logfile)

def _get_upgrade_cmd(packages, venv_dir=None):
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




class dvine_us_equity_3Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_3Pct
    alpaca_args = get_alpaca_args(account)
    entry_point_base = dvine_us_equity.entry_point_base + alpaca_args + [
            '--nstd-thresh', 0.03,
            '--bot-name', 'dvine_us_equity_3Pct' ]
    first_base = entry_point_base
    rest_base = entry_point_base + [
            '--bar-shift-multiplier', -1,
            '--bar-shift-multiplier', 0,
            '--clear-persistence' ]
    compute_orders_cmds = None # Complicated initialization done below, outside the class
    purge_base = ['dvine_purge'] + dvine_us_equity.strat.base_args + alpaca_args
    purge_cmds = _get_purge_args(purge_base,
            ['--bot-name', 'dvine_us_equity_3Pct'])

    from_date_args = ['--from-date', '2022-06-08T00:00:00']
    orders_table_cmd = ['dmule_table',
            '--chart-type', 'orders'
            ] + alpaca_args + from_date_args

    dev_upgrade_cmds = _get_upgrade_cmd(
            {'dmark':None, 'dvine':"v2.2", 'dvault': None} )
    prod_upgrade_cmds = _get_upgrade_cmd(
            {'dmark':None, 'dvine':"v2.2", 'dvault': None},
            "~/.dvine_versions/v2.2" )



# The first command runs daily in the traditional sense with persistence
# The rest of the commands clear persistence, and then seed themselves with a
# -1 shft, and then run at now time.  Really we should write a new version of
# dvine that does this by default, so we don't have the workaround of the two
# --bar-shift-multiplier's
dvine_us_equity_3Pct.compute_orders_cmds = [
        dvine_us_equity_3Pct.first_base + _DVINE_DAYS[0]] + [
        dvine_us_equity_3Pct.rest_base  +  x for x in _DVINE_DAYS[1:36] ]


class dvine_us_equity_2Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_2Pct
    alpaca_args = get_alpaca_args(account)
    entry_point_base = dvine_us_equity.entry_point_base + alpaca_args + [
            '--nstd-thresh', 0.0249,
            '--strategy-bet-size-usd', 500.00,
            '--bot-name', 'dvine_us_equity_2Pct' ]
    rest_base = entry_point_base + [
            '--bar-shift-multiplier', -1,
            '--bar-shift-multiplier', 0,
            '--clear-persistence' ]
    compute_orders_cmds = None # Complicated initialization done below, outside the class
    purge_base = ['dvine_purge'] + dvine_us_equity.strat.base_args + alpaca_args
    purge_cmds = _get_purge_args(purge_base,
            ['--bot-name', 'dvine_us_equity_2Pct'])

    dev_upgrade_cmds = _get_upgrade_cmd(
            {'dmark':None, 'dvine':"v2.2", 'dvault': None} )
    prod_upgrade_cmds = _get_upgrade_cmd(
            {'dmark':None, 'dvine':"v2.2", 'dvault': None},
            "~/.dvine_versions/v2.2" )

dvine_us_equity_2Pct.compute_orders_cmds = [
        dvine_us_equity_2Pct.rest_base  +  x for x in _DVINE_DAYS[14:30] ]


def _get_chart_cmds(bot, chart, custom=[]):
    """get charting commands for any dvine bot"""
    return get_chart_cmd_series(
            bot.__name__,
            dmule_chart.entry_point,
            chart.base_args + get_chart_base_args(
                bot, bot.strat) + custom,
            bot.discord_webhook_url)

class dvine_us_equity_5Pct(dvine_us_equity):
    account = Alpaca.dvine_us_equity_5Pct
    alpaca_args = get_alpaca_args(account)
    entry_point_base = dvine_us_equity.entry_point_base + alpaca_args + [
            '--nstd-thresh', 0.05,
            '--strategy-bet-size-usd', 100.00,
            '--bot-name', 'dvine_us_equity_5Pct' ]
    rest_base = entry_point_base + [
            '--bar-shift-multiplier', -1,
            '--bar-shift-multiplier', 0,
            '--clear-persistence' ]
    compute_orders_cmds = None # Complicated initialization done below, outside the class
    purge_base = ['dvine_purge'] + dvine_us_equity.strat.base_args + alpaca_args
    purge_cmds = _get_purge_args(purge_base, [
            '--bot-name', 'dvine_us_equity_5Pct'])
    discord_webhook_url = discords.dvine_5pct.webhook_url

    dev_upgrade_cmds = _get_upgrade_cmd(
            {'dmark':None, 'dvine':"mark_refactor", 'dvault': None} )
    prod_upgrade_cmds = _get_upgrade_cmd(
            {'dmark':None, 'dvine':"mark_refactor", 'dvault': None},
            "~/.dvine_versions/mark_refactor" )


dvine_us_equity_5Pct.chart_all_returns_cmds = _get_chart_cmds(
        dvine_us_equity_5Pct, chart_all_returns, [
            '--orders-series', 'param',
            '--from-date', '2022-08-19T00:00:00'])

dvine_us_equity_5Pct.chart_recent_returns_cmds = _get_chart_cmds(
        dvine_us_equity_5Pct, chart_recent_returns, [
            '--orders-series', 'param',
            '--from-date', '2022-08-19T00:00:00'])

dvine_us_equity_5Pct.chart_performance_cmds = _get_chart_cmds(
        dvine_us_equity_5Pct, chart_performance, [
            '--orders-series', 'param',
            '--from-date', '2022-08-19T00:00:00'])

dvine_us_equity_5Pct.compute_orders_cmds = [
        dvine_us_equity_5Pct.rest_base  +  x for x in _DVINE_DAYS[31:] ]


class dmoon:
    strat = strats.dmoon
    entry_point_base = ["dmoon"] + strat.default_args + []
    packages = [ 'dmark', 'dmule', 'dmoon', 'dvault', 'dsquire']

class dmoon_adhoc(dmoon):
    discord_webhook_url = discords.dmoon_adhoc.webhook_url
    service_name = "dmoon_adhoc"

    common_args = ['--universe-name', 'crypto']
    entry_point_base = dmoon.entry_point_base + common_args + [
            '--discord-webhook-url', discord_webhook_url]

    entry_point = entry_point_base

class dmoon_adhoc_dev(dmoon_adhoc):
    account = Alpaca.play_time
    alpaca_args = get_alpaca_args(account)
    entry_point = dmoon_adhoc.entry_point_base + alpaca_args + [
            '--period-span-value', 1,
            '--period-span-units', 'Min',
            '--bot-name', 'dmoon_adhoc_dev',
            '--strategy-bet-size-usd', 50000,
            '--entry-signal-look-back-periods', 30,
            '--exit-signal-look-back-periods', 2 ]

    dev_upgrade_cmds = _get_upgrade_cmd(dmoon.packages)
    prod_upgrade_cmds = [
        _get_upgrade_cmd( dmoon.packages, "~/.dmoon_versions/None" ),
        _get_systemd_cmd('restart', dmoon_adhoc.service_name) ]

dmoon_adhoc_dev.chart_all_returns_cmds = _get_chart_cmds(
        dmoon_adhoc_dev, chart_all_returns, [
            '--orders-candle-unit', 'Min',
            '--orders-candle-value', 1,
            '--orders-series', 'param',
            '--universe-name', 'crypto',
#           '--orders-exclusion-max', 0.1,
#           '--orders-exclusion-min', -0.035,
            '--from-date', '2022-08-19T00:00:00'])

dmoon_adhoc_dev.chart_recent_returns_cmds = _get_chart_cmds(
        dmoon_adhoc_dev, chart_recent_returns, [
            '--orders-candle-unit', 'Min',
            '--orders-candle-value', 1,
            '--orders-series', 'param',
            '--universe-name', 'crypto',
#           '--orders-exclusion-max', 0.1,
#           '--orders-exclusion-min', -0.035,
            '--from-date', '2022-08-19T00:00:00'])

dmoon_adhoc_dev.chart_performance_cmds = _get_chart_cmds(
        dmoon_adhoc_dev, chart_performance, [
            '--universe-name', 'crypto',
            '--from-date', '2022-08-19T00:00:00'])

dmoon_adhoc_dev.tmp_logfile = _get_tmp_file(dmoon_adhoc_dev.service_name, "log")
dmoon_adhoc_dev.tmp_statusfile = _get_tmp_file(dmoon_adhoc_dev.service_name, "status")

dmoon_adhoc_dev.onfail_cmds = [
            _get_write_journal_cmd(dmoon_adhoc_dev.service_name),
            _output_to_file_cmd(
                 _get_systemd_cmd(
                     "status", dmoon_adhoc_dev.service_name) + [
                         '-n0', '|', 'head', '-n6'], dmoon_adhoc_dev.tmp_statusfile ),
            [ 'dsquire',
                '--content-file', dmoon_adhoc_dev.tmp_statusfile,
                '--embed-file', dmoon_adhoc_dev.tmp_logfile,
                '--discord-webhook-url', dmoon_adhoc_dev.discord_webhook_url ],
            [ 'mv', dmoon_adhoc_dev.tmp_logfile, dmoon_adhoc_dev.tmp_logfile + ".old" ] ,
            [ 'mv', dmoon_adhoc_dev.tmp_statusfile, dmoon_adhoc_dev.tmp_statusfile + ".old" ] ]





