plan = "abcd"
month1 = "abcd"
month3 = "bcde"
month6 = "cdef"
month12= "defg"
Flag = True
def PLAN():
    global Flag
    query = input("Do you want to view your current plan?(y/n) => ")
    if query.lower() in "y":
        if not Flag:
            print("This account currently does not have any membership. :( ")
            quest = input("Do you want to change your current plan?(y/n) => ")
            if quest.lower() in "y":
                CHANGE()
                Flag = True
        else:
            if plan == month1:
                print ("You currently have the Monthly Plan.")
            elif plan == month3:
                print ("You currently have the Quarterly Plan.")
            elif plan == month6:
                print ("You currently have the Half Yearly Plan.")
            elif plan == month12:
                print ("You currently have the Yearly Plan.")

def CHANGE():
    print('''AVAILABLE PLANS
            (A) Monthly Plan for 1 month
            (B) Quarterly Plan for 3 months 
            (C) Half Yearly Plan for 6 months
            (D) Yearly Plan for 12 months ''')
    code1 = input("Enter the special code you've recieved => ")
    if code1 == month1:
        print ("You have now switched to the Monthly Plan.")
    elif code1 == month3:
        print ("You have now switched to the Quarterly Plan.")
    elif code1 == month6:
        print ("You have now switched to the Half Yearly Plan.")
    elif code1 == month12:
        print ("You have now switched to the Yearly Plan.")
    else:
        print ("Please enter a valid code.")
PLAN()