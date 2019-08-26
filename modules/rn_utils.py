import re


def validate_name(node_name):
    la = __splitUpper(node_name)
    und = __change_symbol("_", la)
    das = __change_symbol("-", und)
    spa = __change_symbol(" ", das)
    return "".join(spa)


def __splitUpper(string):
    return re.sub( r"([A-Z])", r" \1", string).split()


def __change_symbol(symbol, la):
    und = []
    for i in la:
        for u in i.split(symbol):
            und.append(u.title())
    return und
