import math
from datetime import (datetime, timedelta)
from contextlib import contextmanager

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

class LogTab(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()

class LogVal:
    def __init__(self, value, prefix="", postfix="", name=""):
        self.value = value
        self.name = name
        self.prefix = prefix
        self.postfix = postfix

    def value_str(self):
        return str(self.value)

    def __str__(self):
        npart="" if not self.name else "#{}:".format(self.name)
        vpart = "".join([self.prefix, self.value_str(), self.postfix])
        return "".join([npart,vpart])

class PercentLogVal(LogVal):
    def value_str(self):
        return str(None) if self.value is None else "{:.1f}".format(self.value*100.0)

    def __init__(self, value, name=None):
        super().__init__(value, postfix="%", name=name)

class DollarLogVal(LogVal):
    def __init__(self, value, name=None):
        super().__init__(value, prefix="$", name=name)
    def value_str(self):
        return str(None) if self.value is None else "{:.2f}".format(self.value)

def _is_nice_num(n):
    badnness = [None, float("inf"), float("-inf"), float('nan')]
    if n in badnness: return False
    return n==n

class FloatLogVal(LogVal):
    def __init__(self, value, name=None):
        if value is None:
            prefix=""
            self.template="{}"
        else:
            if _is_nice_num(value):
                smallpart = abs(value) - abs(int(value))
                if smallpart > .1:
                    digits = 2
                elif smallpart > .01:
                    digits = 3
                elif smallpart > .001:
                    digits = 4
                elif smallpart == 0:
                    digits = 1
                else:
                    digits = 6
            else:
                digits = 0

            # if the value we display is more than .1% off of the actual value
            # prefix with ~ for 'approx'
            display_tol = abs(value - round(value,digits))
            if display_tol > 0.001 * value:
                prefix="~"
            else:
                prefix=""

            self.template = "".join(["{:.", str(digits), "f}"])
        super().__init__(value, prefix=prefix, name=name)

    def value_str(self):

        return str(None) if self.value is None else self.template.format(self.value)

class TimeLogVal(LogVal):



    def __init__(self, value, name=None):
        super().__init__(value, name=name)
    def value_str(self):
        return self.value.astimezone(LOCAL_TIMEZONE).strftime("%Y-%m-%dT%H:%M:%S") if self.value else str(self.value)

class ListLogVal(LogVal):
    def __init__(self, value, name=None):
        super().__init__(
                value,
                name=name,
                prefix='[' if value is not None else '',
                postfix=']' if value is not None else '')
    def value_str(self):
        parts = []
        if self.value is not None:
            for cur_v in self.value:
                parts.append(str(cur_v))
        return ",".join(parts)

class MsgCode:
    summary_result="summary_result"
    intermediate_result="intermediate_result"
    explanatory="explanatory"
    milestone="milestone"

MSG_CODE_ABBREV = {
        MsgCode.summary_result: 'S',
        MsgCode.intermediate_result: 'i',
        MsgCode.explanatory: 'e',
        MsgCode.milestone: 'M'
        }

class LogMsg:
    def __init__(self, text, msg_code=MsgCode.explanatory, **kwargs):
        self.text = text
        self.msg_code = msg_code
        self._measurements = {}
        self.add_log_vals(**kwargs)

        #self.creation_time = datetime.now()

    _inset_stack = []
    @contextmanager
    def inset(inset='  '):
        try:
            LogMsg._inset_stack.append(inset)
            yield None
        finally:
            LogMsg._inset_stack.pop()



    def add_log_val(self, k, v):
        if v is None:
            meas = LogVal(name=k, value=v)
        elif isinstance(v,(int,str)):
            meas = LogVal(name=k, value=v)
        elif isinstance(v,float):
            meas = FloatLogVal(name=k, value=v)
        elif isinstance(v,datetime):
            meas = TimeLogVal( name=k, value=v)
        elif isinstance(v,timedelta):
            meas = LogVal(name=k, value=str(v))
        elif isinstance(v,list):
            meas = ListLogVal(name=k,value=v)
        elif isinstance(v,LogVal):
            meas = v
        else:
            raise Exception(
                    "Functionality does not handle logging: " +
                    str(type(v)) + ": " + str(v)
                    )
        self._measurements[k] = meas

    def add_log_vals(self, **kwargs):
        for k,v in kwargs.items():
            self.add_log_val(k,v)

    def __str__(self):
        parts = [
                MSG_CODE_ABBREV.get(self.msg_code, self.msg_code),
                "".join(LogMsg._inset_stack)
                ]

        for mapname, cur_measurement in self._measurements.items():
            if cur_measurement.name and mapname == cur_measurement.name:
                parts.append("({})".format(str(cur_measurement)))
            else:
                parts.append("({}={})".format(mapname,str(cur_measurement)))

        if self.text:
            parts.append('--')
            parts.append(self.text)

        return " ".join(parts)




