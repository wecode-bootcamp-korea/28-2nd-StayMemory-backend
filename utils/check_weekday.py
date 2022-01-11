from datetime import datetime,timedelta
def include_weekday_boolean(start_date, end_date):
        check_in_date  = datetime.strptime(start_date,'%Y-%m-%d')
        check_out_date = datetime.strptime(end_date,'%Y-%m-%d')
        days           = (check_out_date-check_in_date).days

        if days >= 4:
            return True

        weekend  = {4,5,6}
        weekdays = {(check_in_date+timedelta(days=i)).weekday() for i in range(days)}

        if weekdays-weekend:
            return True

        return False


if __name__=='__main__':
    result = include_weekday_boolean("2022-01-19", "2022-01-21")