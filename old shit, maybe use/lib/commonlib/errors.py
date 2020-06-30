import sys, datetime

class termcolor:
    def colored(message, color):
        return message

def info(msg):
    print("[{}][ INFO  ] ".format(datetime.datetime.now()) + msg)

def warn(msg):
    print(termcolor.colored(
        "[{}][ WARN  ] ".format(datetime.datetime.now())
        + msg, "yellow"))

def error(msg):
    print(termcolor.colored(
        "[{}][ ERROR ] ".format(datetime.datetime.now())
        + msg, "red"), file=sys.stderr)

def fatal(msg, error=True):
    print(termcolor.colored(
        "[{}][ FATAL ] ".format(datetime.datetime.now())
        + msg, "red"), file=sys.stderr)
    if error:
        raise Exception(msg)

def debug(msg):
    print("[{}][ DEBUG ] ".format(datetime.datetime.now()) + msg)


#[20-2-19 10:24:32][ DEBUG ]: TEST
#[20-2-19 10:24:33][ INFO  ]: wow its not oofd
#[20-2-19 10:24:34][ WARN  ]: oof it returned something else
#[20-2-19 10:24:36][ ERROR ]: Wow there's an  error
#[20-2-19 10:24:38][ FATAL ]: asdf movie is cool
