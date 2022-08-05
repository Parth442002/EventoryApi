import re


def emailValidator(email):
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.fullmatch(regex, str(email)):
        return True
    return False


def phoneValidator(phone):
    regex = re.compile(
        r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$")
    if re.match(regex, str(phone)):
        return True
    return False


def usernameValidator(s):
    if emailValidator(s) == False and phoneValidator(s) == False:
        return True
    else:
        return False
