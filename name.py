from pygame import mixer
#-----------------------------------------FUNCTIONS----------------------------------------------------

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
            elif quest.lower() in "n":
                return
            else:
                print("Please enter a valid response.")
        else:
            if plan == month1:
                print ("You currently have the Monthly Plan.")
            elif plan == month3:
                print ("You currently have the Quarterly Plan.")
            elif plan == month6:
                print ("You currently have the Half Yearly Plan.")
            elif plan == month12:
                print ("You currently have the Yearly Plan.")
            quest = input("Do you want to change your current plan?(y/n) => ")
            if quest.lower() in "y":
                CHANGE()
                Flag = True
            elif quest.lower() in "n":
                return
            else:
                print("Please enter a valid response.")
    elif query.lower() in "n":
        return 
    else:
        print("Please enter a valid response.")

def createPlaylist():
    try:
        Playlist1 = input("What do you want to name your playlist => ")
        q1 = "Create table if not exists {}(Sno Int Primary Key Auto_increment, Songname Varchar(255) Not Null)".format(Playlist1)
        cur1.execute(q1)
        while True: 
            songname = input("Enter the Name of the song you want to add to this playlist => ")
            q2 = "insert into {} (Songname) values ('{}')".format(Playlist1, songname)
            cur1.execute(q2)
            quest = input("Do you wish to add more songs?(y/n) => ")
            if quest.lower() in 'y':
                continue
            elif quest.lower() in "n":
                break
    except Exception as Satvik:
        print(Satvik)

def playSong(filename):
    
    mixer.music.load(filename+'.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        q = input("Enter 1 to pause song, 2 to play, 3 to finish")
        if q=='1':
            p.pause()
        elif q=='2':
            p.play()
        elif q=='3':
            break
    

def CHANGE():
    global plan
    print('''AVAILABLE PLANS
            (A) Monthly Plan for 1 month
            (B) Quarterly Plan for 3 months 
            (C) Half Yearly Plan for 6 months
            (D) Yearly Plan for 12 months ''')
    code1 = input("Enter the special code you've recieved => ")
    if code1 == month1:
        print ("You have now switched to the Monthly Plan.")
        plan = code1
    elif code1 == month3:
        print ("You have now switched to the Quarterly Plan.")
        plan = code1
    elif code1 == month6:
        print ("You have now switched to the Half Yearly Plan.")
        plan = code1
    elif code1 == month12:
        print ("You have now switched to the Yearly Plan.")
        plan = code1
    else:
        print ("Please enter a valid code.")



#--------------------------------------TEMPORARY------------------------------------------------


plan = "abcd"
month1 = "abcd"
month3 = "bcde"
month6 = "cdef"
month12= "defg"
Flag = True

#----------------------------------------MAIN---------------------------------------------------

import pymysql as p
con1 = p.connect (host = "localhost", user ="Satvik", passwd = "Satvik06#", database = "Rhythm")
cur1 = con1.cursor()
mixer.init()

print('''---------MAIN--MENU---------
(A) Search
(B) Create Playlist
(C) View Playlists
(D) Generate Report
(E) Check Subscription Plan
----------------------------''')


while True:
    query = input("Please Enter the task you want to carry out => ")
    playSong('dangerously')
    if query.lower() in "a":
        print ("To be done")
    elif query.lower() in "b":
        createPlaylist()
    elif query.lower() in "c":
        print ("To be done")
    elif query.lower() in "d":
        print ("To be done")
    elif query.lower() in "e":
        PLAN()
    else:
        print("Please enter a valid response")
