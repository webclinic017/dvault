import logging
import os
import pickle
import re
import shutil
import sys
import time as pytime
from datetime import (datetime,timedelta,timezone)
from os import path
from time import sleep
import shlex

class AssertionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def get_localzone(dt=None):
    # I don't like to rely on tz_local in my utils class, I want to keep it low dependency
    # So we rolled our own
    dt = datetime.now() if dt is None else dt
    return dt.astimezone().tzinfo

def parse_date(datestr, is_localized=True):
    if type(datestr) == datetime:
        return datestr
    thedate = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
    if is_localized:
        thedate = thedate.replace(tzinfo=get_localzone())
    return thedate


def format_date(date):
    return parse_date(date).strftime("%Y-%m-%dT%H:%M:%S")

def load_object_from_disk(filepath, initial_value_initializer):
    try:
        with open(filepath, "rb") as infile:
           return(pickle.load(infile))
    except FileNotFoundError as ex:
        logging.info("first time?, no file to load at: %s", filepath)
        return None if initial_value_initializer is None else initial_value_initializer()
    except EOFError as ex2:
        logging.info("Bad cached file?, could not load file at: %s", filepath)
        return None if initial_value_initializer is None else initial_value_initializer()

    raise Exception("This statment should not be reachble")

def save_object_to_disk(filepath, data):
    dirname = path.dirname(filepath)
    if not dirname:
        dirname = "."
    if not path.exists(dirname):
        raise Exception("parent directory of " + filepath + " does not exist")

    tmpfilename = "-".join([ str(x) for x in [
        ".save_object_to_disk",
        path.basename(filepath),
        datetime.now().timestamp(),
        os.getpid() ]])
    tmpfilepath = path.join(dirname, tmpfilename)
    with open(tmpfilepath,'wb') as outf:
        pickle.dump(data, outf)
    shutil.move(tmpfilepath, filepath)

def format_pct(n):
    return '{:6.1f}%'.format(round(n,1))

def sleep_until(time):
    """
    Stolen from: https://github.com/jgillick/python-pause/blob/master/pause/__init__.py#L39
    Pause your program until a specific end time.
    'time' is either a valid datetime object or unix timestamp in seconds (i.e. seconds since Unix epoch)
    """
    end = time

    # Convert datetime to unix timestamp and adjust for locality
    if isinstance(time, datetime):
        # If we're on Python 3 and the user specified a timezone, convert to UTC and get the timestamp.
        if sys.version_info[0] >= 3 and time.tzinfo:
            end = time.astimezone(timezone.utc).timestamp()
        else:
            zoneDiff = pytime.time() - (datetime.now()- datetime(1970, 1, 1)).total_seconds()
            end = (time - datetime(1970, 1, 1)).total_seconds() + zoneDiff

    # Type check
    if not isinstance(end, (int, float)):
        raise Exception('The time parameter is not a number or datetime object')

    # Now we wait
    while True:
        now = pytime.time()
        diff = end - now

        #
        # Time is up!
        #
        if diff <= 0:
            break
        else:
            # 'logarithmic' sleeping to minimize loop iterations
            sleep(diff / 2)

# Python program to illustrate the intersection
# of two lists
# from https://www.geeksforgeeks.org/python-intersection-two-lists/
# Python program to illustrate the intersection
# of two lists
def intersection(lst1, lst2):

    if not lst1 or not lst2:
        return []

    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

def convert_object_to_data(obj):
    """I should have wrote this function years ago"""

    if obj is None:
        return None
    elif isinstance(obj, (int,float,str)):
        return obj
    elif isinstance(obj, dict):
        plain_obj = {}
        for k,v in obj.items():
            plain_obj[k] = convert_object_to_data(v)
        return plain_obj
    elif isinstance(obj, list):
        plain_obj = [None] * len(obj)
        for i in range(len(obj)):
            plain_obj[i] = convert_object_to_data(obj[i])
        return plain_obj
    elif hasattr(obj,'__dict__'):
        return convert_object_to_data(obj.__dict__)
    elif isinstance(obj,datetime):
        return format_date(obj)
    else:
        return str(obj)

def _add_arg_helper(parser, arg_name):
    return {

            '--log-level':
            lambda parser, arg_name: parser.add_argument(arg_name,
                help="verbosity level for stderr logging",
                default=os.environ.get('LOG_LEVEL', 'INFO'),
                choices=["DEBUG", "INFO", "WARN", "ERROR"]),

            '--alpaca-api-key':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default=os.environ.get('APCA_API_KEY_ID', None),
                required='APCA_API_KEY_ID' not in os.environ,
                help="Alpaca API Key, default from APCA_API_KEY_ID env variable"),

            '--alpaca-secret-key':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default=os.environ.get('APCA_API_SECRET_KEY', None),
                required='APCA_API_SECRET_KEY' not in os.environ,
                help="Alpaca API Secret Key, default from APCA_API_SECRET_KEY env variable"),

            '--alpaca-api-data-key':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default=os.environ.get('APCA_API_DATA_KEY_ID', None) or os.environ.get('APCA_API_KEY_ID', None),
                required='APCA_API_DATA_KEY_ID' not in os.environ or 'APCA_API_KEY_ID' not in os.environ,
                help="Alpaca API Key, default from APCA_API_DATA_KEY_ID or APCA_API_KEY_ID env variable"),

            '--alpaca-secret-data-key':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default=os.environ.get('DATA_APCA_API_SECRET_KEY', None) or os.environ.get('APCA_API_SECRET_KEY', None),
                required='APCA_API_SECRET_KEY' not in os.environ or 'DATA_APCA_API_SECRET_KEY' not in os.environ,
                help="Alpaca API Secret Key, default from APCA_API_SECRET_KEY env variable"),

            '--universe-name':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default='fractionable_universe',
                help="Name of the universe of assets to use"),

            '--alpaca-base-url':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default=os.environ.get('APCA_API_BASE_URL', 'https://paper-api.alpaca.markets'),
                help="Alpaca API URL, default from APCA_API_BASE_URL env variable"),

            '--alpaca-data-url':
            lambda parser, arg_name: parser.add_argument(arg_name,
                default=os.environ.get('APCA_API_DATA_URL', 'https://data.alpaca.markets'),
                help="Alpaca Data API URL, defaulted from APCA_API_DATA_URL env variable"),

            '--alpaca-csv':
            lambda parser, arg_name: parser.add_argument(arg_name,
                help='csv file holding alpaca keys with columns: SERIES,EMAIL,ALPACA_API_KEY,ALPACA_SECRET_KEY,BASE_URL',
                action='append'),

            '--trade-days-per-bar':
                lambda parser, arg_name: parser.add_argument(arg_name,
                type=int,
                default=1,
                help="the value of the unit of the time frame to use when running the strategy"),

            '--strategy-max-assets':
                lambda parser, arg_name: parser.add_argument(arg_name,
                type=int,
                default=20,
                help="the most number of assets to hold in a time period"),

            '--strategy-min-assets':
                lambda parser, arg_name: parser.add_argument(arg_name,
                type=int,
                default=0,
                help="for diversification rick, if at least this many positions are not found, also include benchmark asset"),

            '--strategy-bet-size-usd':
                lambda parser, arg_name: parser.add_argument(arg_name,
                type=float,
                default=50.00,
                help="how much to risk in a single bet"),

            '--strategy-benchmark-symbol':
                lambda parser, arg_name: parser.add_argument(arg_name,
                default="SPY",
                help="asset(s) to include when there are not enough signals"),

            '--interactive-mode':
                lambda parser, arg_name: parser.add_argument(arg_name,
                action='store_true',
                help="Used for debugging, pause at key points during execution and prompt user to continue"),

            '--cache-dir':
                lambda parser, arg_name: parser.add_argument(arg_name,
                default='./dvault_cache',
                help="path to directory where files are cached"),

            '--blacklist-ticker':
                lambda parser, arg_name: parser.add_argument(arg_name,
                action='append',
                help="do not trade in these assets, supports multiple args or comma seperated list"),


            '--account-name':
                lambda parser, arg_name: parser.add_argument(arg_name,
                help="name of the account"),

            '--strategy-name':
                lambda parser, arg_name: parser.add_argument(arg_name,
                help="name of the strategy"),

            '--portfolio-name':
                lambda parser, arg_name: parser.add_argument(arg_name,
                help="name of the portfolio"),

            '--module-name':
                lambda parser, arg_name: parser.add_argument(arg_name,
                help="name of the module", required=True),

            '--entry-name':
                lambda parser, arg_name: parser.add_argument(arg_name,
                help="name of the variable", default='entry_point'),

            '--class-name':
                lambda parser, arg_name: parser.add_argument(arg_name,
                help="name of the class", required=True),

            '--tag-names':
                lambda parser, arg_name: parser.add_argument(arg_name,
                action='append', help="tags to associate"),

            '--dry-run':
                lambda parser, arg_name: parser.add_argument(arg_name,
                action='store_true', help="don't actually run it"),


            }[arg_name](parser, arg_name)

def list_from_strings(blacklist_ticker):
    blacklist_tickers = []
    for cur_ticker_arg in blacklist_ticker or []:
        for cur_ticker in cur_ticker_arg.split(','):
            blacklist_tickers.append(cur_ticker.strip())
    return blacklist_tickers


def get_bar_span(
        strategy_time_frame_unit,
        trade_days_per_bar):

    secs_per_unit = {
            "Min" : 60,
            "Hour": 60*60,
            "Day" : 60*60*24
            }[strategy_time_frame_unit]

    return timedelta(seconds=secs_per_unit * trade_days_per_bar)

def add_cmd_line_args(parser, *args):
    for arg in args:
        if isinstance(arg, list):
            for ca in arg:
                _add_arg_helper(parser, ca)
        else:
            _add_arg_helper(parser, arg)

def show_continue_or_abort_menu(interactive_menu):
    while interactive_menu:
        answer = input("[c]ontinue, [a]bort? : [c] ")
        answer = 'c' if answer=="" else answer.lower()
        if answer not in ['c','a']: continue
        if answer == 'a': raise Exception("user abort")
        print("Continuing...")
        break

def split_string(fund_set_str,delimiters=",| "):
    fund_set_list = re.split(delimiters, fund_set_str)
    return [x.strip() for x in fund_set_list]

def append_dict_of_lists(d,k,v):
    if k not in d:
        d[k] = [v]
    else:
        d[k].append(v)

def get_env(vtype,name,default):
    return vtype(os.environ.get(name,default))

def cash_round(x):
    return round(int(x*100.0)/100.0,2)

def cash_round_str(x):
    return "{:.2f}".format(cash_round(x))

def append_cmd_history(argv):
    with open('.dvault_cmd_history','a') as hfile:
        arglist = [shlex.quote(x) for x in argv]
        arglist.append('\n')
        hfile.write(' '.join(arglist))


