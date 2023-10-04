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
            songname = input("Enter the Name of the song you want to add to this playlist => ").upper().strip()
            cur1.execute(("Select * from Songs where upper(songName) LIKE '%{}%'").format(songname))
            result = cur1.fetchall()
            if result:
                print ("Adding song ", result[0][1])
                question = ("Confirm?(y/n) => ")
                if question.lower() in 'y':
                    q3 = "insert into {} (songID) values ('{}')".format(Playlist1, result[0][0])
                    cur1.execute(q3)
                    quest = input("Do you wish to add more songs?(y/n) => ")
                    if quest.lower() in 'y':
                        continue
                    elif quest.lower() in "n":
                        break
                else:
                    continue
            else:
                print ("This song does not exist in our current database. Sorry for inconvenience.")
    except Exception as Satvik:
        print(Satvik)



def playSong(filename):
    # playsound('C:\Resume\Rythym\dangerously.mp3') 
    mixer.music.load(filename+'.mp3')
    mixer.music.set_volume(0.7)
    mixer.music.play()
    while True:
        query = input("Press 1 to pause, 2 to resume, 3 to go forward => ")
        if query == '1':
            mixer.music.pause()     
        elif query == '2':
            mixer.music.unpause()
        elif query == '3':
            mixer.music.stop()
            break



def playPlaylist(playlist):
    for song in playlist:
        print('\n Playing "{}. {} by {} Songcode- {} \n'.format(str(i),result[1],result[2],str(result[0])))
        playSong(song[5])
    print('\n End of Playlist \n')



def searchSong():
    type = input("Do you want to search by name(N), genre(G) or artist(A)? => ").upper().strip()
    query = input("Enter search query => ").upper().strip()
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
    print(l[0][6])
    playSong(l[0][5])
    


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
from pygame import mixer

con1 = p.connect (host = "localhost", user ="root", passwd = "Siddharth@1234", database = "Rhythm")
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
    # playSong('dangerously')
    query = input("Please Enter the task you want to carry out => ")
    if query.lower() in "a":
        searchSong()
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

