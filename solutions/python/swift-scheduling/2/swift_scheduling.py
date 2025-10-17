import re
from datetime import datetime, timedelta


def delivery_date(start:str, description:str):
    strt = datetime.fromisoformat(start)
    rem = re.compile('(\d{1,2})M')
    req = re.compile('Q(\d)')
    start_year = strt.year
    start_month = strt.month
    start_day = strt.day
    one_day = timedelta(days = 1)
    match description:
        case 'NOW':
            desc_date = strt + timedelta(hours=2)
        case 'ASAP':
            desc_date = datetime(start_year, start_month, start_day) + (timedelta(hours=17) if strt.hour < 13 else timedelta(hours=13, days=1))
        case 'EOW':
            dow_start = strt.isoweekday() #Monday is 1
            desc_date = datetime(start_year, start_month, start_day) - timedelta(days = dow_start) + \
                (timedelta(hours = 17, days = 5) if dow_start < 4 else timedelta(hours=20, days = 7))
        case desc if matches := rem.search(desc):
            desc_month = int(matches.group(1))
            desc_date = datetime(start_year + (0 if desc_month > start_month else 1), desc_month, 1, 8)
            while desc_date.isoweekday() > 5:
                desc_date += one_day
        case desc if matches := req.search(desc):
            desc_quarter = int(matches.group(1))
            start_quarter = 1 + (start_month - 1) // 3
            desc_date = datetime(\
                start_year + (0 if start_quarter <= desc_quarter else 1) + \
                (0 if desc_quarter % 4 else 1)\
                , (desc_quarter % 4) * 3 + 1, 1, 8) - timedelta(days=1) 
            while desc_date.isoweekday() > 5:
                desc_date -= one_day
        case desc:
            raise ValueError(f"{desc} is not a recognized code format")
    return desc_date.isoformat()