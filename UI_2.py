from tkinter import *
import re
import os
import sys
import pickle
root=Tk()
#store player emotions and emotional level's in a list
f = open('var.txt','r')
arg = f.readline()
player_count = int(arg )
player_emotions = []
player_emotion_values = []

v = []
v_emotions = []
for i in range(player_count):
     v.append(IntVar())
     v_emotions.append(DoubleVar())
for variable in v:
     variable.set(1)
for variable in v_emotions:
     variable.set(0)     
attributes = [("Fear"),("Happy"),("No Emotion"),("Anger"),("Contempt"),("Normal")]
emotion_dictionary = {0:'fear',1:'happy',2:'no-emotion',3:'anger',4:'contempt',5:'normal'}
# add no emotion for all players
for i in range(player_count):
     player_emotions.append(attributes[0])
     player_emotion_values.append(0)

def player_attribute_choice():
	return

def submit_button():
     for i in range(player_count):
     	player_emotions[i] = int(v[i].get())
     	player_emotion_values[i] = float(v_emotions[i].get())
     #to store object data to a file
     f = open( 'players_e.pickle', 'wb' )
     pickle.dump(player_emotions,f)
     f.close()
     f = open( 'players_p.pickle', 'wb' )
     pickle.dump(player_emotion_values,f)
     f.close()

     root.destroy()
     import UI_3

def data():
    row = 0
    for player_number in range(player_count):
       label_string = "Select the attribute of player %d" % player_number
       Label(frame, text=label_string,justify = LEFT,padx = 20).grid(row=row,column=0)
       row += 1
       i = 0
       for val, attribute in enumerate(attributes):
                             #To display the radio button 
       		Radiobutton(frame,text=attribute,justify = RIGHT, variable=v[player_number], command=player_attribute_choice,value=val).grid(row=row,column = 0)
       		row += 1

       # put the scroll bar
       Scale(frame,variable=v_emotions[player_number], orient=HORIZONTAL,length=300,from_= 0,to= 1,tickinterval=5,resolution=0.001).grid(row=row,column = 0)
       row += 1
    Button(frame, text = "Submit", width="27",bg="grey", command=submit_button).grid(row=row,column = 0)

def myfunction(event):
     #frame to display the contents of page
    canvas.configure(scrollregion=canvas.bbox("all"),width=700,height=600)
sizex = 800
sizey = 650
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
myframe.place(x=10,y=10)
#to display all the elements in the frame
canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
data()
root.title("Emotion Selection")
root.mainloop()
