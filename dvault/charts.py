from dvault import (bots)

class dvine_chart:
    entry_point_base = ["dvine_chart"]

class dvine_chart_orders:
    entry_point_base = dvine_chart.entry_point_base + [
            '--chart-type', 'orders',
            '--with-order-status', 'filled' ]

class dvine_chart_all_returns:
    entry_point_base = dvine_chart_orders.entry_point_base + [
            '--orders-max-spam', 1 ]

class dvine_chart_recent_returns:
    entry_point_base = dvine_chart_orders.entry_point_base + [
            '--orders-max-spam', 5,
            '--orders-with-fill-after', 'now']

class dvine_chart_us_equity_3Pct:
    bot = bots.dvine_us_equity_3Pct
    discord_webhook_url = "https://discordapp.com/api/webhooks/985010880771141663/iDyB-jVlcfvCdpIGm3cGlt7GLy3uoNozQCQIPihsF9BPQtVOSpeSYchit9SQRbo1gHo1"
    base_args = bot.strat.base_args + [
        '--discord-webhook-url', discord_webhook_url,
        '--bot-name', bot.__name__
        ]

class dvine_us_equity_3Pct_all_returns(dvine_chart_us_equity_3Pct):
    entry_point = \
            dvine_chart_all_returns.entry_point_base + \
            dvine_chart_us_equity_3Pct.bot.strat.base_args + \
            dvine_chart_us_equity_3Pct.base_args

class dvine_us_equity_3Pct_recent_returns(dvine_chart_us_equity_3Pct):
    entry_point = \
            dvine_chart_recent_returns.entry_point_base + \
            dvine_chart_us_equity_3Pct.bot.strat.base_args + \
            dvine_chart_us_equity_3Pct.base_args

