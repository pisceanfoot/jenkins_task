def __buildParameterName(name):
    return "${{{0}}}".format(name)

print __buildParameterName('aa')