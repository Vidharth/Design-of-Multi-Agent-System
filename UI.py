from tkinter import *
from tkinter import  messagebox
import re
import os

window=Tk()
window.title("page1")
window.geometry("900x600" )
players = 0

def page2():
   # try to convert the string value into an int
   try:
      # try to convert the number of players in
      num_players = int(str(playervalue.get()))
      # check if the number of players are between 2 to 9
      if( num_players < 2 or num_players > 9 ):
         # show message that invalid number of players, go back
         messagebox.showerror("Error", "Number of players must be between 2-9")
         # clear the text box
         playervalue.set('')
         return
   except:
      # show message invalid input
      messagebox.showerror("Error", "Invalid number : '" + str(playervalue.get()) + "'")
      # clear the text box
      playervalue.set('')
      return
      
   # int(str(playervalue.get()))
   players=playervalue.get()
   f = open( 'var.txt', 'w' )
   f.write( players)
   f.close()
   window.destroy()
   import UI_2

heading = Label(text = "ENTER PLAYERS TO CONTINUE").pack()

Label(text="Players :").place(x=15,y=50)


playervalue = StringVar()
Entry(window, textvariable = playervalue).place(x=15,y=90)
Button(window, text = "Proceed to game", width="27",bg="grey", command=page2 ).place(x=15, y=125)
window.title("Welcome to Poker")
window.mainloop()
