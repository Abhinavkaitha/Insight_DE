import datetime as dt


def round_fun(number):
    number_dec = int(str(number - int(number))[2:3])
    if number_dec < 5:
        return int(number)
    return int(number) + 1


def is_date(string):
    try:
        dt.datetime.strptime(string, '%m/%d/%Y %I:%M:%S %p')
        return True

    except ValueError:
        return False


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def type_check(x):
    if type(x) is int:
        return x
    return 0
