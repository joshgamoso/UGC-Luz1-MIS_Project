from tkinter import *
import mysql.connector
root = Tk()

def loginFunc(user,pasw):
    cursor.execute("SELECT username FROM admin")
    userDB=sum(cursor.fetchall(),())[0]

    cursor.execute("SELECT password FROM admin")
    paswDB=sum(cursor.fetchall(),())[0]

    if((user == userDB) and (pasw==paswDB)):
        root.destroy()
        import main
    else:
        print("failed")
    
    print("user: %s\\%s \ndb: %s %s"%(user,pasw,userDB,paswDB))
        
connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
cursor=connect.cursor()

topFrame=Frame(root)
topFrame.pack()
botFrame=Frame(root)
botFrame.pack()

title=Label(topFrame, text="Security Login", font=("palatino",16))
title.grid(row=0,column=0)

usLbl=Label(botFrame, text="username:")
pwLbl=Label(botFrame, text="password:")
usLbl.grid(row=0,column=0)
pwLbl.grid(row=1,column=0)

usVar=StringVar()
pwVar=StringVar()

usBox=Entry(botFrame, text="username:", textvariable=usVar, font=("Helvetica",12))
pwBox=Entry(botFrame, text="password:", textvariable=pwVar, show="\u2022", font=("Helvetica",12))

usBox.grid(row=0,column=1)
pwBox.grid(row=1,column=1)

logBtn=Button(botFrame, text="login",width=8, command=lambda:loginFunc(usVar.get(),pwVar.get()))
logBtn.grid(columnspan=2)

root.wm_title("Login")
root.mainloop()
