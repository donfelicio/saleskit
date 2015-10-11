import datetime

#filters for list of reservations

def filter_res_status_attention(element):
    return element.res_status == '2'

def filter_res_status_final(element):
    return element.res_status == '1'

def filter_res_status_cancelled(element):
    return element.res_status == '3'

#i dont want to see:
# people touched today
#i do want to see:
#people untouched ever
#people touched not today

def filter_res_touchedtoday(element):
    today = datetime.date.today()
    if element.res_last_action_taken == today:
        return element.res_untouched != 'no'
    else:
        return element.res_untouched =='yes' or element.res_untouched == 'no'

def filter_res_status_sales_1(element):
    return element.res_status_sales != '1'

def filter_res_status_sales_2(element):
    return element.res_status_sales != '2'

def filter_res_status_sales_3(element):
    return element.res_status_sales != '3'

def filter_res_status_sales_4(element):
    return element.res_status_sales != '4'

def filter_res_status_sales_5(element):
    return element.res_status_sales != '5'

def filter_res_status_sales_6(element):
    return element.res_status_sales != '6'

def filter_res_status_sales_7(element):
    return element.res_status_sales != '7'

def filter_res_status_sales_8(element):
    return element.res_status_sales != '8'

def filter_res_status_sales_9(element):
    return element.res_status_sales != '9'