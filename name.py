import threading,ctypes,pytimedinput #pip install pytimedinput

#-----------------------------------------FUNCTIONS----------------------------------------------------

def PLAN():
    global user
    query = input("Do you want to view your current plan?(y/n) => ")
    if query.lower() in "y":
        if not user[4]:
            print("This account currently does not have any membership. :( ")
            quest = input("Do you want to change your current plan?(y/n) => ")
            if quest.lower() in "y":
                CHANGE()
            elif quest.lower() in "n":
                return
            else:
                print("Please enter a valid response.")
        else:
            print ("Your plan expires on", user[4])
            quest = input("Do you want to change your current plan?(y/n) => ")
            if quest.lower() in "y":
                CHANGE()
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
        songList = []
        while True: 
            songname = input("Enter the Name of the song you want to add to this playlist => ").upper().strip()
            cur1.execute(("Select * from Songs where upper(songName) LIKE '%{}%'").format(songname))
            result = cur1.fetchall()
            if result:
                print ("Adding song ", result[0][1])

                question = input("Confirm?(y/n) => ")
                if question.lower() in 'y':
                    # q3 = "insert into {} (songID) values ('{}')".format(Playlist1, result[0][0])
                    # cur1.execute(q3)
                    songList.append(str(result[0][0]))

                    quest = input("Do you wish to add more songs?(y/n) => ")
                    if quest.lower() in 'y':
                        continue
                    elif quest.lower() in "n":
                        break
                else:
                    continue
            else:
                print ("This song does not exist in our current database. Sorry for inconvenience.")
        # print(user[2])
        print(user)
        q1 = "insert into playlists(songsList, owner, sharedUsers, playlistName) VALUES('{}','{}','{}','{}')".format(','.join(songList), user[2],"",Playlist1)
        cur1.execute(q1)
        con1.commit()
    except:
        pass

class thread_with_exception(threading.Thread):
    def __init__(self, name, func):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
             
    def run(self):
        self.func()
          
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
            
def f1():
    print("Press 1 to pause, 2 to resume, 3 to go forward => ")
    while True:
        query = pytimedinput.timedInput(timeout=5)
        if query[0] == '1':
            mixer.music.pause()     
        elif query[0] == '2':
            mixer.music.unpause()
        elif query[0] == '3':
            # mixer.music.fadeout()
            mixer.music.stop()
            break
    return   
def f2(duration):
    while True:
         if mixer.music.get_pos() > (duration-1)*1000:
             break
         time.sleep(2)
    return

def playSong(filename,duration):
    # global stopF1
    global listentime
    listentime-= duration
    # playsound('C:\Resume\Rythym\dangerously.mp3') 
    mixer.music.load('songs/'+filename+'.mp3')
    mixer.music.set_volume(0.7)
    mixer.music.play()
    
    t1 = thread_with_exception('F1',lambda:f1())
    t2 = thread_with_exception('F2',lambda: f2(duration) )
    t1.start()
    t2.start()
    while True:
        if not t1.is_alive():
            print("Song ended")
            t2.raise_exception()
            t2.join()
            break
        if not t2.is_alive():
            print("Song over")
            t1.raise_exception()
            t1.join()
            break
            
    print("Hey")
    mixer.music.stop()    
    
    if listentime<0 and not user[4]:
        print("Time for an ad")
        chosenAd = random.choice(adsList)
        mixer.music.load(f'ads/{chosenAd[0]}.mp3')
        mixer.music.play()
        time.sleep(chosenAd[1])
        listentime = 30



def playPlaylist(playlist):
    i=1
    print("Playing playlist {}".format(playlist[1]))
    l = playlist[2].split(',')
    cur1.execute(f'UPDATE Playlists SET listenCount = listenCount + 1 WHERE SNo = {l[0]}')
    
    for song in playlist[2].split(','): 
        cur1.execute(f'Select * from Songs where songID={song}')
        song = cur1.fetchall()[0]
        print('\n Playing "{}. {} by {} \n'.format(str(i),song[1],song[2]))
        if user[4]:
            print('\n {} \n'.format(song[6]))
        cur1.execute(f'UPDATE Songs SET listenCount = listenCount + 1 where songID= {l[0]}')
        con1.commit()
        
        playSong(song[5], song[4])
        
        i+=1
        
    print('\n End of Playlist \n')

def searchSong(user):
    type = input("Do you want to search by name(N), genre(G) or artist(A)?").upper().strip()
    query = input("Enter search query: ").upper().strip()

    if type=='N':
        cur1.execute(("Select * from Songs where UPPER(songName) LIKE '%{}%'").format(query))
    elif type=='G':
        cur1.execute(("Select * from Songs where UPPER(genre) LIKE '%{}%'").format(query))
    elif type=='A':
        cur1.execute(("Select * from Songs where UPPER(artist) LIKE '%{}%'").format(query))
    else: 
        print("Invalid input")
        return
    print('\n Results:- \n')
    i=1
    songs = cur1.fetchall()
    for result in songs:
        print ("{}. {} by {} Songcode- {}".format(str(i),result[1],result[2],str(result[0])))
        i+=1
    q = input("Enter songcode to play the song or q to quit => ").upper().strip()
    if 'Q' in q:
        return
    l=[]
    for song in songs:
        if song[0]==int(q):
            l.append(song)
    if l==[]:
        print("Couldn't find songcode")
        return
    if user[4]:
        print(l[0][6])
    else:
        print("For lyrics, buy Rhythm premium")
    cur1.execute(f'UPDATE Songs SET listenCount = listenCount + 1 where songId = {l[0][0]}')
    con1.commit()
    playSong(l[0][5],l[0][4])
    


def CHANGE():
    global user
    print('''AVAILABLE PLANS
            (A) Monthly Plan for 1 month
            (B) Quarterly Plan for 3 months 
            (C) Half Yearly Plan for 6 months
            (D) Yearly Plan for 12 months ''')
    code1 = input("Enter the special code you've recieved => ")
    if code1 == month1:
        print ("You have now switched to the Monthly Plan.")
        cur1.execute(f"UPDATE acc SET premium = CURRENT_DATE + INTERVAL 31 DAY WHERE username = '{user[2]}'")
        cur1.execute(f"UPDATE save SET premium = CURRENT_DATE + INTERVAL 31 DAY WHERE username = '{user[2]}'")
    elif code1 == month3:
        print ("You have now switched to the Quarterly Plan.")
        cur1.execute(f"UPDATE acc SET premium = CURRENT_DATE + INTERVAL 92 DAY WHERE username = '{user[2]}'")
        cur1.execute(f"UPDATE save SET premium = CURRENT_DATE + INTERVAL 92 DAY WHERE username = '{user[2]}'")
        plan = code1
    elif code1 == month6:
        print ("You have now switched to the Half Yearly Plan.")
        cur1.execute(f"UPDATE acc SET premium = CURRENT_DATE + INTERVAL 183 DAY WHERE username = '{user[2]}'")
        cur1.execute(f"UPDATE save SET premium = CURRENT_DATE + INTERVAL 183 DAY WHERE username = '{user[2]}'")
        plan = code1
    elif code1 == month12:
        print ("You have now switched to the Yearly Plan.")
        cur1.execute(f"UPDATE acc SET premium = CURRENT_DATE + INTERVAL 365 DAY WHERE username = '{user[2]}'")
        cur1.execute(f"UPDATE save SET premium = CURRENT_DATE + INTERVAL 365 DAY WHERE username = '{user[2]}'")
    else:
        print ("Please enter a valid code.")
    con1.commit()
    cur1.execute(f"Select * from acc where username = '{user[2]}'")
    user = cur1.fetchall()[0]
    if user[4]:
        print("Your plan expires on",user[4])
    else:
        print("You don't have a premium plan")
            
def topSongs():
    cur1.execute("Select * from songs order by listencount DESC LIMIT 5")
    result = cur1.fetchall()
    i=1
    for song in result:
        print(f'{i}. {song[1]} Listens - {song[7]}')
        i+=1

def viewPlaylist():
    cur1.execute(f"SELECT * from Playlists where owner='{user[2]}'")
    pList = cur1.fetchall()
    # print(pList)
    for p in pList:
        print("Playlist {}, code - {}".format(p[1],p[0]))
    q = input("Press p to play or q to quit:").upper().strip()
    
    if 'q' in q:
        return
    # elif 'p' in q:
    q = input("Enter playlist code:")
    temp = [x for x in pList if str(x[0])==q]
    if temp ==[]:
        print("Playlist not found")
    else:
        playPlaylist(temp[0])
    # elif 'v' in q:
        # v = input("Enter playlist code to v")
        # temp = [x for x in pList if str(x[0])==q][0] 
        # print('\n'.join(temp[2].split(',')))
    
# def sharePlaylist():
        

#--------------------------------------SETUP------------------------------------------------



month1 = "abcd"
month3 = "bcde"
month6 = "cdef"
month12= "defg"



import pymysql as sql
import smtplib
import random
import time


con1= sql.connect(host="localhost" , user="root" , passwd="Siddharth@1234" , database="Rhythm")
cur1= con1.cursor()
adsList = [['MokshAd',18],['lyricAd',24],['simpleAd',19],['bullySatvik',26]]

# with open('name.py') as h:
#     file = h.read()
#     for comm in h.split(';'):
#         cur1.exec(comm)

#--------------------------------------USER STUFF------------------------------------------------

def forgotPassword():
    email = input("Enter your email").lower()
    q = f"select * from acc where emailid={email}"
    cur1.execute(q)
    result = cur1.fetchall()
    if result==[]:
        print("Account not found by that email")
        return
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()

    server.starttls()
    server.login('siddharth1411agrawal@gmail.com', 'qsys xkmh xvlj tvbc')
    code = random.randrange(1000,9999)
    server.sendmail(email, result[0][1], f'Your otp is {code}. Enter this in app to change password')
    server.close()

    userCode = int(input("Enter code sent to your email to update password:"))
    if userCode ==code:
        newPass = input("Enter new password, and is baar mat bhulna")
        q = cur1.execute(f"UPDATE acc SET password={newPass}")
        print("New Password set")
    else:
        print("Incorrect code, please repeat process")
        

def signup():
    q= "create table if not exists acc ( name varchar(20) not null ,\
                                         emailid varchar (50) not null,\
                                         username varchar(30)not null primary key,\
                                         password varchar(40) not null,\
                                         premium DATE )"
    q2= "create table if not exists save ( name varchar(20) not null ,\
                                         emailid varchar (50) not null,\
                                         username varchar(30)not null primary key,\
                                         password varchar(40) not null,\
                                         premium DATE)"
    cur1.execute(q)
    cur1.execute(q2)
    n= input("enter full name")
    flag=0
    while flag==0:
        u= input ("enter username")
        query = "SELECT * FROM acc WHERE username = '{}' ".format (u)
        cur1.execute(query)
        result = cur1.fetchall()
        if result:
            print ("username already taken")
        else:
            flag=1
    p= input ("Enter Password:")
    e= input ("Enter Email ID:")
    q1="insert into acc values ('{}','{}','{}','{}',NULL)".format(n,e,u,p)
    cur1.execute(q1)
    con1.commit()
    print("WELCOME")
    save=input("Do you want to save login information?").lower()
    if save in "yes":
        q1="insert into save values ('{}','{}','{}','{}',NULL)".format(n,e,u,p)
        cur1.execute(q1)
        con1.commit()
    
    return [n,e,u,p,None]
    
   
def login():
        
    user=input("Enter Username:")
    passw=input("Enter Password:")
    q1="select * from acc where username='{}' and password='{}' ".format(user,passw)
    res=cur1.execute(q1)
    if res:
        print("welcome")
        return res[0]
    else:
        print("no such account exists")

#----------------------------------------MAIN---------------------------------------------------

import pymysql as p
from pygame import mixer
import datetime

con1 = p.connect (host = "localhost", user ="root", passwd = "Siddharth@1234", database = "Rhythm", port =3306)
cur1 = con1.cursor()
mixer.init()
user = None
listentime = 30 #30 minutes of uninterrupted listening

while True: 
    try:
        q="select * from save"
        cur1.execute(q)
        result = cur1.fetchall()
        if result:
            print("Login already exists")
            user = result[0]
            print ("welcome")
            break 
    except:
        pass
    choice=input('''Do you want to
    (A) Sign Up
    (B) Log in
    (C) Forgot Password
    ''').lower()

    if choice =='a':
        user = signup()
        if user:
            break
    elif choice=='b':
        user = login()
        if user:
            break
    elif choice=='c':
        forgotPassword()
    elif choice=='d':
        break

    else:
        print("Please enter valid value")

if user[4] and user[4]< datetime.date.today():
    print("Your subscription has expired")
    cur1.execute(f"UPDATE acc SET premium = NULL WHERE username = '{user[2]}'")
    cur1.execute(f"UPDATE save SET premium = NULL WHERE username = '{user[2]}'")
    user[4] = None
    con1.commit()
        




while True:
        # playSong('dangerously')
    print('''---------MAIN--MENU---------
(A) Search
(B) Create Playlist
(C) View Playlists
(D) Generate Report
(E) Check Subscription Plan
(F) Logout
(G) End Program
----------------------------''')
    query = input("Please Enter the task you want to carry out => ")
    if query.lower() in "a":
        searchSong(user)
    elif query.lower() in "b":
        createPlaylist()
    elif query.lower() in "c":
        viewPlaylist()
    elif query.lower() in "d":
        topSongs()
    elif query.lower() in "e":
        PLAN()
    elif query.lower() in "f":
        cur1.execute("drop table save")
        print("Logged out")        
        break
    elif query.lower() in "g":
        break
        
    else:
        print("Please enter a valid response")

print("Thank you for using Rhythm")
con1.commit()
con1.close()


# GUI attempt

# ... Your existing functions ...

# def open_search_song():
#     query = simpledialog.askstring("Search Song", "Enter search query:")
#     if query:
#         searchSong(query)

# def open_create_playlist():
#     createPlaylist()

# def open_view_playlists():
#     messagebox.showinfo("View Playlists", "This feature is not implemented yet.")

# def open_generate_report():
#     messagebox.showinfo("Generate Report", "This feature is not implemented yet.")

# def open_check_subscription_plan():
#     PLAN()

# # Create the main application window
# root = tk.Tk()
# root.title("Music Player")

# # Create buttons for each action
# search_button = tk.Button(root, text="Search", command=open_search_song)
# create_playlist_button = tk.Button(root, text="Create Playlist", command=open_create_playlist)
# view_playlists_button = tk.Button(root, text="View Playlists", command=open_view_playlists)
# generate_report_button = tk.Button(root, text="Generate Report", command=open_generate_report)
# check_subscription_button = tk.Button(root, text="Check Subscription Plan", command=open_check_subscription_plan)

# # Place buttons on the GUI window
# search_button.pack()
# create_playlist_button.pack()
# view_playlists_button.pack()
# generate_report_button.pack()
# check_subscription_button.pack()

# # Start the Tkinter event loop
# root.mainloop()

