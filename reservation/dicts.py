#all dicts and lists you'll use in the views

def salestip(sales_status):
    if sales_status == '1':
        message = "A new request showed up in your S2M reservations, give the client a call and get to know them and find a great collaboration. If they are happy as is and don't need a tour, offer or any other help, just change the status to 'success'"
    elif sales_status == '2':
        message = "You have called the customer. Invite them for a tour of the location, or send them an offer."
    elif sales_status == '3':
        message = "You've met the customer and gave them a tour. Now it's time to send them a great offer!"
    elif sales_status == '4':
        message = "You've sent the customer an offer. Now call to see if they received it, and if there are any questions?"
    elif sales_status == '5':
        message = "You've called and discussed the offer. Prepare for the meeting by double checking the reservation or rehearsing the event script"
    elif sales_status == '6':
        message = "You've prepared the meeting or event with the customer. When it's over, start your aftersales."
    elif sales_status == '7':
        message = "The meeting or event was a success (hopefully:)! Call the customer to evaluate, thank them and ask if they might have a future collaboration in mind."
    elif sales_status == '8':
        message = "Your sale funnel was a success!"
    elif sales_status == '9':
        message = "Your sale failed, too bad. You aren't supposed to see this anymore."
    else:
        message = "Er is geen status bekend!!"
    return message

def short_salestip(sales_status):
    if sales_status == '1':
        message = "Call customer."
    elif sales_status == '2':
        message = "Invite for a tour."
    elif sales_status == '3':
        message = "Send an offer"
    elif sales_status == '4':
        message = "Call about offer"
    elif sales_status == '5':
        message = "Double-check the preparations"
    elif sales_status == '6':
        message = "Wait until after meeting."
    elif sales_status == '7':
        message = "Evaluate and plan ahead."
    elif sales_status == '8':
        message = "Nothing:)"
    elif sales_status == '9':
        message = "Nothing:)"
    else:
        message = "Er is geen status bekend!!"
    return message


