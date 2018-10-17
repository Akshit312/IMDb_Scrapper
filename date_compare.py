import datetime
def check_date(inputDate):
    if inputDate=="":
        return False
    else:
        DateFormat = "%d%b%Y"
        outPutDateFormat = "%Y-%d-%m"
        a=datetime.datetime.strptime(inputDate , DateFormat )
        b=datetime.datetime.now()
        return a>b
