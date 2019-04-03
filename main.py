import mysql.connector
from openpyxl import Workbook
from openpyxl.styles import Font
from tkinter import *
import tkinter
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import tkcalendar
import time
import datetime
import os, os.path
import glob
from itertools import chain

now = datetime.datetime.now()

class CalendarDialog(tkinter.simpledialog.Dialog):
    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()
    def apply(self):
        self.result = self.calendar.selection_get()

def login(fr1,fr2,fr3):
    fr1.destroy()
    fr2.destroy()
    fr3.destroy()
    def onLogin(un,pw,ubox,pbox):
        connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
        cursor=connect.cursor()
        cursor.execute("SELECT username FROM admin WHERE username='%s'"%(un))
        undb=cursor.fetchone()
        if undb!=None:
            undb=undb[0]
        cursor.execute("SELECT password FROM admin WHERE username='%s'"%(un))
        pwdb=cursor.fetchone()
        if pwdb!=None:
            pwdb=pwdb[0]
        if undb==un and pw==pwdb:
            lb=Listbox(topFrame)
            messagebox.showinfo("Login Successful","Successfully login, Welcome %s!"%(un))
            main(menFrame,topFrame,botFrame,-1,lb)
        else:
            connect.close()
            messagebox.showerror("Failed to login","Username/Password invalid!")
            ubox.delete(0,END)
            pbox.delete(0,END)
            ubox.focus()
            
    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    menFrame.pack()
    topFrame.pack()
    botFrame.pack()

    menu=Menu(root)
    root.config(menu=menu)
    fileMenu=Menu(menu, tearoff=0)

    photo = PhotoImage(file=r"Asset\login.png")
    logo = Label(menFrame, image=photo, bg="#7a8694")
    logo.grid(row=0,column=0,sticky=E,pady=10)
    
    lbl=Label(topFrame,text="Security Login",font=("Unispace",20), bg="#7a8694")
    
    usrLbl=Label(topFrame, text="Username:",font=("Helvetica",12,"bold"), bg="#7a8694")
    pasLbl=Label(topFrame, text="Password:",font=("Helvetica",12,"bold"), bg="#7a8694")

    usrVar=StringVar()
    pasVar=StringVar()
    usrBox=Entry(topFrame, textvariable=usrVar,font=("Helvetica",12))
    pasBox=Entry(topFrame, textvariable=pasVar,font=("Helvetica",12),show="\u2022")
    usrBox.bind("<Return>",lambda event: onLogin(usrVar.get(),pasVar.get(),usrBox,pasBox))
    pasBox.bind("<Return>",lambda event: onLogin(usrVar.get(),pasVar.get(),usrBox,pasBox))
    usrBox.focus()
    subBtn=Button(topFrame, text="Login",font=("Helvetica",12,"bold"),width=10,command=lambda: onLogin(usrVar.get(),pasVar.get(),usrBox,pasBox))
    
    lbl.grid(column=0,row=0,columnspan=2,pady=5)
    usrLbl.grid(column=0,row=1)
    pasLbl.grid(column=0,row=2)
    usrBox.grid(column=1,row=1)
    pasBox.grid(column=1,row=2)
    subBtn.grid(column=1,row=3,pady=10,sticky=E)

    root.config(bg="#7a8694")
    root.state('normal')
    root.geometry('400x310')
    root.minsize(400,310)
    root.wm_title("UGC-MIS Inventory System | Login")
    root.mainloop()
    
def main(fr1,fr2,fr3,it_no,it_cl):
    global boo
    keyBind=True
    fr1.destroy()
    fr2.destroy()
    fr3.destroy()

    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    
    menFrame.pack()
    topFrame.pack()
    botFrame.pack()

    photo = PhotoImage(file=r"Asset\logo.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.grid(row=0,column=0,sticky=E,pady=10)
    
    lbl=Label(topFrame, text="Luz1-Inventory", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E)
    
    def onSave(svtype,lb0,lb1,lb2,lb3,lb4,lb5,lb6):
        book = Workbook()
        sheet = book.active
        rowHd=(("Item No.","Area","Type","Description","Serial No.","Date of purchase","Qnty"),)
        
        for row in rowHd:
            sheet.append(row)
        for row in zip(lb0.get(0,END),lb1.get(0,END),lb2.get(0,END),lb3.get(0,END),lb4.get(0,END),lb5.get(0,END),lb6.get(0,END)):
            sheet.append(row)
        if svtype=="saveas":
            path = filedialog.asksaveasfilename(initialdir = "Output",title="Save file",filetypes=(("Excel Workbook","*.xlsx"),("All files","*.*")))
            if path:
                print(path)
                book.save("%s.xlsx"%(path))
        elif svtype=="autosave":
            fileno = sum(1 for f in os.listdir("Output") if os.path.isfile(os.path.join("Output", f)) and f[0] != '.')+1
            if fileno<=9:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno<=99:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno<=999:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno<=9999:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno>=10000:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            book.save("Output\%s.xlsx"%(filename))
            messagebox.showinfo("Successfully Saved","File: %s has been saved as excel at output folder"%(filename))
    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
    def onVSB(*args):
        lb0.yview(*args)
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)
    def OnMouseWheel(event):
        lb0.yview("scroll",-event.delta,"units")
        lb1.yview("scroll",-event.delta,"units")
        lb2.yview("scroll",-event.delta,"units")
        lb3.yview("scroll",-event.delta,"units")
        lb4.yview("scroll",-event.delta,"units")
        lb5.yview("scroll",-event.delta,"units")
        lb6.yview("scroll",-event.delta,"units")
        return "break"
    def onSearch(choice,order,query,lb0,lb1,lb2,lb3,lb4,lb5,lb6):
        lb0.delete(0,END)
        lb1.delete(0,END)
        lb2.delete(0,END)
        lb3.delete(0,END)
        lb4.delete(0,END)
        lb5.delete(0,END)
        lb6.delete(0,END)
        
        choiceQ=""
        queryQ=""
        orderQ=""
        
        if (choice=="Select all"):
            if(order=="item_no"):
                itemVar.set("Item No.")
            elif(order=="area"):
                areaVar.set("Area")
            elif(order=="type"):
                typeVar.set("Type")
            elif(order=="des"):
                descVar.set("Description")
            elif(order=="sn"):
                serlVar.set("Serial No.")
            elif(order=="qty"):
                qntyVar.set("Qnty")

        areaQ=""
        typeQ=""
        dateQ=""
        if dateVar.get()!=str(now.isoformat())[0:10] and dateVar.get()!="Date of purchase":
            dateQ=dateVar.get()
        if (choice=="Select all" or choice=="ASC" or choice=="DESC")and (order=="dop"):
            dateVar.set("Date of purchase")
            dateQ=""
        if (str(choice)==str(now.isoformat())[0:10]):
            dateQ=dateVar.get()
        if areaVar.get()=="Area":
            areaQ=""
        else:
            areaQ=areaVar.get()
        if typeVar.get()=="Type":
            typeQ=""
        else:
            typeQ=typeVar.get()
        
        if not query:
            queryQ="WHERE 1"
        else:
            queryQ="WHERE (item_no LIKE '%{0}%' OR area LIKE '%{0}%' OR type LIKE '%{0}%' OR des LIKE '%{0}%' OR sn LIKE '%{0}%' OR dop LIKE '%{0}%' OR qty LIKE '%{0}%')".format(query)
        if choice=="Select all":
            choiceQ=" AND (area LIKE '%{0}%' AND type LIKE '%{1}%' AND dop LIKE '%{2}%')".format(areaQ,typeQ,dateQ)
        elif choice=="ASC" or choice=="DESC":
            orderQ=" AND (area LIKE '%{0}%' AND type LIKE '%{1}%' AND dop LIKE '%{2}%') ORDER BY {3} {4}".format(areaQ,typeQ,dateQ,order,choice)
        else:
            choiceQ=" AND (area LIKE '%{0}%' AND type LIKE '%{1}%' AND dop LIKE '%{2}%')".format(areaQ,typeQ,dateQ)
            

        cursor.execute("SELECT item_no FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i0=sum(cursor.fetchall(),())
        for i in i0:
            lb0.insert(END,i)
        cursor.execute("SELECT area FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i1=sum(cursor.fetchall(),())
        for i in i1:
            lb1.insert(END,i)
        cursor.execute("SELECT type FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i2=sum(cursor.fetchall(),())
        for i in i2:
            lb2.insert(END,i)
        cursor.execute("SELECT des FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i3=sum(cursor.fetchall(),())
        for i in i3:
            lb3.insert(END,i)
        cursor.execute("SELECT sn FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i4=sum(cursor.fetchall(),())
        for i in i4:
            lb4.insert(END,i)
        cursor.execute("SELECT dop FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i5=sum(cursor.fetchall(),())
        for i in i5:
            lb5.insert(END,i)
        cursor.execute("SELECT qty FROM items {0} {1} {2}".format(queryQ,choiceQ,orderQ))
        i6=sum(cursor.fetchall(),())
        for i in i6:
            lb6.insert(END,i)

        if(query and lb0.size()==0 and order=="item_no"):
            messagebox.showinfo("Search results","0 results found! for %s"%(query))
        
    def onDate(event,choice,query,lb0,lb1,lb2,lb3,lb4,lb5,lb6):
        if event=="Select all":
            onSearch("Select all", "dop", query,lb0,lb1,lb2,lb3,lb4,lb5,lb6)
        elif event=="Pick a date":
            global cd
            cd = CalendarDialog(topFrame)
            if str(cd.result) !='None':
                dateVar.set(cd.result)
                onSearch(cd.result, "dop",query,lb0,lb1,lb2,lb3,lb4,lb5,lb6)
            else:
                onSearch("Select all", "dop", query,lb0,lb1,lb2,lb3,lb4,lb5,lb6)
        elif event=="ASC" or event=="DESC":
            onSearch(event, "dop", query,lb0,lb1,lb2,lb3,lb4,lb5,lb6)
    def onDelete(item_no):
        check=messagebox.askokcancel("Delete entry","WARNING!\n\nAre you want to Delete Item no: %s\nThis can't be undone!"%(item_no),icon="warning",default="cancel")
        if check:
            cursor.execute("DELETE FROM items WHERE item_no='%s'"%(item_no))
            connect.commit()
            connect.close()
            messagebox.showinfo("","Successfully deleted the record of item no: %s"%(item_no))
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes("-fullscreen", boo)
    menu=Menu(root)
    root.config(menu=menu)
    fileMenu=Menu(menu, tearoff=0)
    
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",command=lambda: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    fileMenu.add_command(label="Save as",command=lambda: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))

    botFrame.focus_set()
    botFrame.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    botFrame.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    botFrame.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    botFrame.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    botFrame.bind("<F11>",lambda event: onFullscreen())
    botFrame.bind("<Escape>",lambda event: root.attributes("-fullscreen", False))
    

    connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
    cursor=connect.cursor()

    itemVar=StringVar()
    areaVar=StringVar()
    typeVar=StringVar()
    descVar=StringVar()
    serlVar=StringVar()
    dateVar=StringVar()
    qntyVar=StringVar()

    itemCho=("ASC","DESC")
    cursor.execute("SELECT DISTINCT area FROM items")
    areaCho=sum(cursor.fetchall(),())
    cursor.execute("SELECT DISTINCT type FROM items")
    typeCho=sum(cursor.fetchall(),())
    descCho=("ASC","DESC")
    serlCho=("ASC","DESC")
    dateCho=("Pick a date","ASC","DESC")
    qntyCho=("ASC","DESC")

    itemVar.set("Item No.")
    areaVar.set("Area")
    typeVar.set("Type")
    descVar.set("Description")
    serlVar.set("Serial No.")
    dateVar.set("Date of purchase")
    qntyVar.set("Qnty")
    
    srcVar=StringVar()
    srcBox=Entry(topFrame,textvariable=srcVar, font=("Helvetica",14))
    srBtn=Button(topFrame,text="Search", font=("Helvetica",12), command=lambda:onSearch("Select all","item_no",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    srcBox.grid(row=1,column=1,sticky=W)
    srBtn.grid(row=1,column=1,pady=10)
    srcBox.bind('<Return>', lambda event: onSearch("Select all","item_no",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    srcBox.bind('<Escape>', lambda event: onFullscreen())
    srcBox.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    srcBox.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    srcBox.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    srcBox.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    
    itemBtn=OptionMenu(botFrame, itemVar, "Select all", *itemCho, command=lambda event: onSearch(event,"item_no",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    areaBtn=OptionMenu(botFrame, areaVar, "Select all", *areaCho, command=lambda event: onSearch(event,"area",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    typeBtn=OptionMenu(botFrame, typeVar, "Select all", *typeCho, command=lambda event: onSearch(event,"type",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    descBtn=OptionMenu(botFrame, descVar, "Select all", *descCho, command=lambda event: onSearch(event,"des",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    serlBtn=OptionMenu(botFrame, serlVar, "Select all", *serlCho, command=lambda event: onSearch(event,"sn",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    dateBtn=OptionMenu(botFrame, dateVar, "Select all", *dateCho, command=lambda event: onDate(event,"dop",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    qntyBtn=OptionMenu(botFrame, qntyVar, "Select all", *qntyCho, command=lambda event: onSearch(event,"qty",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    
    itemBtn.configure(width= 6, font=("Helvetica",12,"bold"),bd=4)
    areaBtn.configure(width= 7, font=("Helvetica",12,"bold"),bd=4)
    typeBtn.configure(width=11, font=("Helvetica",12,"bold"),bd=4)
    descBtn.configure(width=31, font=("Helvetica",12,"bold"),bd=4)
    serlBtn.configure(width=11, font=("Helvetica",12,"bold"),bd=4)
    dateBtn.configure(width=13, font=("Helvetica",12,"bold"),bd=4)
    qntyBtn.configure(width= 5, font=("Helvetica",12,"bold"),bd=4)
    
    fr=Frame(botFrame)
    fr.grid(row=1, column=7)
    VSB=Scrollbar(fr,orient="vertical",command=onVSB)

    lb0=Listbox(botFrame, height=25, width=11, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))
    lb1=Listbox(botFrame, height=25, width=12, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))
    lb2=Listbox(botFrame, height=25, width=16, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))
    lb3=Listbox(botFrame, height=25, width=36, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))
    lb4=Listbox(botFrame, height=25, width=16, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))
    lb5=Listbox(botFrame, height=25, width=18, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))
    lb6=Listbox(botFrame, height=25, width=10, yscrollcommand=VSB.set, exportselection=0, font=("Helvetica",12))

    def selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,sed):
        lb0.selection_clear(0,END)
        lb0.selection_set(sed)
        lb0.activate(sed)
        lb1.selection_clear(0,END)
        lb1.selection_set(sed)
        lb1.activate(sed)
        lb2.selection_clear(0,END)
        lb2.selection_set(sed)
        lb2.activate(sed)
        lb3.selection_clear(0,END)
        lb3.selection_set(sed)
        lb3.activate(sed)
        lb4.selection_clear(0,END)
        lb4.selection_set(sed)
        lb4.activate(sed)
        lb5.selection_clear(0,END)
        lb5.selection_set(sed)
        lb5.activate(sed)
        lb6.selection_clear(0,END)
        lb6.selection_set(sed)
        lb6.activate(sed)
    def clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6):
        lb0.selection_clear(0, END)
        lb1.selection_clear(0, END)
        lb2.selection_clear(0, END)
        lb3.selection_clear(0, END)
        lb4.selection_clear(0, END)
        lb5.selection_clear(0, END)
        lb6.selection_clear(0, END)
        botFrame.focus_set()
        
    botFrame.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    botFrame.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    botFrame.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    botFrame.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb0.bind("<MouseWheel>", OnMouseWheel)
    lb1.bind("<MouseWheel>", OnMouseWheel)
    lb2.bind("<MouseWheel>", OnMouseWheel)
    lb3.bind("<MouseWheel>", OnMouseWheel)
    lb4.bind("<MouseWheel>", OnMouseWheel)
    lb5.bind("<MouseWheel>", OnMouseWheel)
    lb6.bind("<MouseWheel>", OnMouseWheel)
    lb0.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb0.curselection()[0]),"item"  ))
    lb1.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb1.curselection()[0]),"area"  ))
    lb2.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb2.curselection()[0]),"type"  ))
    lb3.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb3.curselection()[0]),"desc"  ))
    lb4.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb4.curselection()[0]),"serl"  ))
    lb5.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb5.curselection()[0]),"date"  ))
    lb6.bind("<Double-Button-1>", lambda event:edit( menFrame,topFrame,botFrame,lb0.get(lb6.curselection()[0]),"qnty"  ))
    lb0.bind("<Delete>", lambda event:onDelete(lb0.get(lb0.curselection()[0])))
    lb1.bind("<Delete>", lambda event:onDelete(lb0.get(lb1.curselection()[0])))
    lb2.bind("<Delete>", lambda event:onDelete(lb0.get(lb2.curselection()[0])))
    lb3.bind("<Delete>", lambda event:onDelete(lb0.get(lb3.curselection()[0])))
    lb4.bind("<Delete>", lambda event:onDelete(lb0.get(lb4.curselection()[0])))
    lb5.bind("<Delete>", lambda event:onDelete(lb0.get(lb5.curselection()[0])))
    lb6.bind("<Delete>", lambda event:onDelete(lb0.get(lb6.curselection()[0])))
    lb0.bind("<Button-3>", lambda event:onDelete(lb0.get(lb0.curselection()[0])))
    lb1.bind("<Button-3>", lambda event:onDelete(lb0.get(lb1.curselection()[0])))
    lb2.bind("<Button-3>", lambda event:onDelete(lb0.get(lb2.curselection()[0])))
    lb3.bind("<Button-3>", lambda event:onDelete(lb0.get(lb3.curselection()[0])))
    lb4.bind("<Button-3>", lambda event:onDelete(lb0.get(lb4.curselection()[0])))
    lb5.bind("<Button-3>", lambda event:onDelete(lb0.get(lb5.curselection()[0])))
    lb6.bind("<Button-3>", lambda event:onDelete(lb0.get(lb6.curselection()[0])))
    lb0.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb1.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb2.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb3.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb4.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb5.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb6.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb0.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb1.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb2.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb3.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb4.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb5.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb6.bind("<F5>",lambda event: main(menFrame,topFrame,botFrame,-1,lb0))
    lb0.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb1.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb2.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb3.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb4.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb5.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb6.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb0.bind("<Control-o>",lambda event: onOpen())
    lb1.bind("<Control-o>",lambda event: onOpen())
    lb2.bind("<Control-o>",lambda event: onOpen())
    lb3.bind("<Control-o>",lambda event: onOpen())
    lb4.bind("<Control-o>",lambda event: onOpen())
    lb5.bind("<Control-o>",lambda event: onOpen())
    lb6.bind("<Control-o>",lambda event: onOpen())
    lb0.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb1.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb2.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb3.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb4.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb5.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb6.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb0.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb1.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb2.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb3.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb4.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb5.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb6.bind("<Escape>",lambda event: clearer(lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb0.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb0.curselection()))
    lb1.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb1.curselection()))
    lb2.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb2.curselection()))
    lb3.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb3.curselection()))
    lb4.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb4.curselection()))
    lb5.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb5.curselection()))
    lb6.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb6.curselection()))
    lb0.bind("<F11>",lambda event: onFullscreen())
    lb1.bind("<F11>",lambda event: onFullscreen())
    lb2.bind("<F11>",lambda event: onFullscreen())
    lb3.bind("<F11>",lambda event: onFullscreen())
    lb4.bind("<F11>",lambda event: onFullscreen())
    lb5.bind("<F11>",lambda event: onFullscreen())
    lb6.bind("<F11>",lambda event: onFullscreen())

    VSB.pack(side='left',fill='y')
    for i in range(23):
        o=Label(fr,text='',bg="#7a8694")
        o.pack()

    onSearch("Select all","item_no",srcVar.get(),lb0,lb1,lb2,lb3,lb4,lb5,lb6)
    #on back highlight and focus previously selected
    if it_no!=-1:
        if it_cl=="item":
            lb0.focus_set()
        elif it_cl=="area":
            lb1.focus_set()
        elif it_cl=="type":
            lb2.focus_set()
        elif it_cl=="desc":
            lb3.focus_set()
        elif it_cl=="serl":
            lb4.focus_set()
        elif it_cl=="date":
            lb5.focus_set()
        elif it_cl=="qnty":
            lb6.focus_set()
        lb0.selection_set(it_no-1)
        lb0.activate(it_no-1)
        lb1.selection_set(it_no-1)
        lb1.activate(it_no-1)
        lb2.selection_set(it_no-1)
        lb2.activate(it_no-1)
        lb3.selection_set(it_no-1)
        lb3.activate(it_no-1)
        lb4.selection_set(it_no-1)
        lb4.activate(it_no-1)
        lb5.selection_set(it_no-1)
        lb5.activate(it_no-1)
        lb6.selection_set(it_no-1)
        lb6.activate(it_no-1)

    itemBtn.grid(row=0,column=0)
    areaBtn.grid(row=0,column=1)
    typeBtn.grid(row=0,column=2)
    descBtn.grid(row=0,column=3)
    serlBtn.grid(row=0,column=4)
    dateBtn.grid(row=0,column=5)
    qntyBtn.grid(row=0,column=6)

    lb0.grid(row=1,column=0)
    lb1.grid(row=1,column=1)
    lb2.grid(row=1,column=2)
    lb3.grid(row=1,column=3)
    lb4.grid(row=1,column=4)
    lb5.grid(row=1,column=5)
    lb6.grid(row=1,column=6)

    root.config(bg="#7a8694")
    root.state('zoomed')
    root.minsize("1200","700")
    root.wm_title("UGC-MIS Inventory System | Main")
    root.mainloop()

def create(fr1,fr2,fr3):
    global boo
    fr1.destroy()
    fr2.destroy()
    fr3.destroy()
    
    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")

    menFrame.pack(anchor="w")
    topFrame.pack()
    botFrame.pack()

    photo = PhotoImage(file=r"Asset\create.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummy"))
    logo.grid(row=0, column=0,pady=20)

    lbl=Label(topFrame, text="Add Entry", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)
    
    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
    def onclick(event):
        global cd
        cd = CalendarDialog(topFrame)
        if str(cd.result) !='None':
            dateVar.set(cd.result)
    def onSubmit(area,typ,desc,serl,date,qty,ar,ty,de,se,da,qu):
        if area=="Please choose" or typ=="Please choose" or not desc or not date or not desc or not serl or not qty:
            messagebox.showwarning("Invalid!", "Please fill all the entry fields")
        else:
            connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
            cursor=connect.cursor()
            cursor.execute("INSERT INTO items (area,type,des,sn,dop,qty) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(area,typ,desc,serl,date,qty))
            connect.commit()
            connect.close()
            messagebox.showinfo("Success","Successfully added entry!")
            ar.set("Please choose")
            ty.set("Please choose")
            de.set("")
            se.set("")
            da.set(str(now.isoformat())[0:10])
            qu.set("")
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)
    def onBack():
        global boo
        if boo:
            boo=False
            root.attributes('-fullscreen',boo)
        else:
            main(menFrame,topFrame,botFrame,-1,"dummy")
    menu=Menu(root)
    root.config(menu=menu)

    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",state="disabled")
    fileMenu.add_command(label="Save as",state="disabled")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))
    
    botFrame.focus_set()
    botFrame.bind("<Escape>",lambda event: onBack())
    botFrame.bind("<F11>",lambda event: onFullscreen())
    botFrame.bind("<Control-o>",lambda event: onOpen())
            
    areaLbl=Label(topFrame, text="Area:", font=("Helvetica",12), bg="#7a8694")
    typeLbl=Label(topFrame, text="Type:", font=("Helvetica",12), bg="#7a8694")
    descLbl=Label(topFrame, text="Description:", font=("Helvetica",12), bg="#7a8694")
    serlLbl=Label(topFrame, text="Serial No.:", font=("Helvetica",12), bg="#7a8694")
    dateLbl=Label(topFrame, text="Date:", font=("Helvetica",12), bg="#7a8694")
    qntyLbl=Label(topFrame, text="Quantity:", font=("Helvetica",12), bg="#7a8694")

    areaVar=StringVar()
    typeVar=StringVar()
    descVar=StringVar()
    serlVar=StringVar()
    dateVar=StringVar()
    qntyVar=StringVar()
    
    areaVar.set("Please choose")
    areaBox=OptionMenu(topFrame, areaVar, "La Union", "Irisan", "Calasiao", "VIllasis", "Bantay", "Isabela", "Pampanga", "Nueva Ecija")
    areaBox.configure(font=("Helvetica",12),width=20)
    typeVar.set("Please choose")
    typeBox=OptionMenu(topFrame, typeVar, "Desktop Set", "Laptop", "Printer", "Router/Switch","Monitor", "HDD/SSD", "RAM/Video Card", "Mouse/Keyboard", "CCTV")
    typeBox.configure(font=("Helvetica",12),width=20)
    
    descBox=Entry(topFrame, textvariable=descVar, width="24", font=("Helvetica",12))
    serlBox=Entry(topFrame, textvariable=serlVar, width="24", font=("Helvetica",12))
    
    dateVar.set(str(now.isoformat())[0:10])
    dateBox = Entry(topFrame, textvariable=dateVar, width="24", font=("Helvetica",12), bg='white')
    dateBox.bind('<Double-Button-1>',onclick)
    qntyBox=Entry(topFrame, textvariable=qntyVar, width="24", font=("Helvetica",12))
    qntyBox.bind('<Return>',lambda event: onSubmit(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),
                                                   areaVar,typeVar,descVar,serlVar,dateVar,qntyVar))
    subtBtn=Button(topFrame, text="Submit", font=("Helvetica",12),width=8, command=lambda:
                   onSubmit(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),
                            areaVar,typeVar,descVar,serlVar,dateVar,qntyVar))
    canlBtn=Button(topFrame, text="Cancel", font=("Helvetica",12),width=8, command=lambda:main(menFrame,topFrame,botFrame,-1,""))

    descBox.bind("<Escape>",lambda event: botFrame.focus_set())
    serlBox.bind("<Escape>",lambda event: botFrame.focus_set())
    dateBox.bind("<Escape>",lambda event: botFrame.focus_set())
    qntyBox.bind("<Escape>",lambda event: botFrame.focus_set())
    
    areaLbl.grid(column=0,row=1,pady=3,sticky=E)
    typeLbl.grid(column=0,row=2,pady=3,sticky=E)
    descLbl.grid(column=0,row=3,pady=3,sticky=E)
    serlLbl.grid(column=0,row=4,pady=3,sticky=E)
    dateLbl.grid(column=0,row=5,pady=3,sticky=E)
    qntyLbl.grid(column=0,row=6,pady=3,sticky=E)
    
    areaBox.grid(column=1,row=1,pady=3,sticky=W)
    typeBox.grid(column=1,row=2,pady=3,sticky=W)
    descBox.grid(column=1,row=3,pady=3,sticky=W)
    serlBox.grid(column=1,row=4,pady=3,sticky=W)
    dateBox.grid(column=1,row=5,pady=3,sticky=W)
    qntyBox.grid(column=1,row=6,pady=3,sticky=W)
    subtBtn.grid(column=1,row=7,pady=40,padx=1,sticky=W)
    canlBtn.grid(column=1,row=7,pady=40,padx=1,sticky=NS)
    root.geometry('1200x700')
    root.minsize("800", "600")
    root.wm_title("UGC-MIS Inventory System Add")
    root.mainloop()

def edit(fr1,fr2,fr3,item_no,item_clicked):
    global boo
    fr1.destroy()
    fr2.destroy()
    fr3.destroy()
    
    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")

    menFrame.pack(anchor="w")
    topFrame.pack()
    botFrame.pack()

    def onUpdate(area,typ,desc,serl,date,qty,item_no):
        if area=="Please choose" or typ=="Please choose" or not desc or not date or not desc or not serl or not qty:
            messagebox.showwarning("Invalid!", "Some fields are empty, please fill all the entry fields")
        else:
            connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
            cursor=connect.cursor()
            cursor.execute("UPDATE items SET area='{0}', type='{1}', des='{2}', sn='{3}', dop='{4}', qty='{5}' WHERE item_no='{6}'".format(area,typ,desc,serl,date,qty,item_no))
            connect.commit()
            connect.close()
            messagebox.showinfo("Success","Successfully updated entry!")
            main(menFrame,topFrame,botFrame,item_no,item_clicked)
    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')        
    def onclick(event):
        global cd
        cd = CalendarDialog(topFrame)
        if str(cd.result) !='None':
            dateVar.set(cd.result)
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)
    def onBack():
        global boo
        if boo:
            boo=False
            root.attributes('-fullscreen',boo)
        else:
            main(menFrame,topFrame,botFrame,-1,"dummy")

    menu=Menu(root)
    root.config(menu=menu)
    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save")
    fileMenu.add_command(label="Save as")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))
            
    photo = PhotoImage(file=r"Asset\edit.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummyObject"))
    logo.grid(row=0, column=0,pady=20)
    
    lbl=Label(topFrame, text="Edit Record", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)

    itemLbl=Label(topFrame, text="Item No.:", font=("Helvetica",12), bg="#7a8694")
    areaLbl=Label(topFrame, text="Area:", font=("Helvetica",12), bg="#7a8694")
    typeLbl=Label(topFrame, text="Type:", font=("Helvetica",12), bg="#7a8694")
    descLbl=Label(topFrame, text="Description:", font=("Helvetica",12), bg="#7a8694")
    serlLbl=Label(topFrame, text="Serial No.:", font=("Helvetica",12), bg="#7a8694")
    dateLbl=Label(topFrame, text="Date:", font=("Helvetica",12), bg="#7a8694")
    qntyLbl=Label(topFrame, text="Quantity:", font=("Helvetica",12), bg="#7a8694")

    itemVar=StringVar()
    areaVar=StringVar()
    typeVar=StringVar()
    descVar=StringVar()
    serlVar=StringVar()
    dateVar=StringVar()
    qntyVar=StringVar()
    
    connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
    cursor=connect.cursor()

    cursor.execute("SELECT area FROM items WHERE item_no='%s'"%(item_no))
    areaVar.set(cursor.fetchone()[0])
    cursor.execute("SELECT type FROM items WHERE item_no='%s'"%(item_no))
    typeVar.set(cursor.fetchone()[0])
    cursor.execute("SELECT des FROM items WHERE item_no='%s'"%(item_no))
    descVar.set(cursor.fetchone()[0])
    cursor.execute("SELECT sn FROM items WHERE item_no='%s'"%(item_no))
    serlVar.set(cursor.fetchone()[0])
    cursor.execute("SELECT dop FROM items WHERE item_no='%s'"%(item_no))
    dateVar.set(cursor.fetchone()[0])
    cursor.execute("SELECT qty FROM items WHERE item_no='%s'"%(item_no))
    qntyVar.set(cursor.fetchone()[0])
    itemVar.set(item_no)

    itemBox=Entry(topFrame, text=itemVar, width="24",font=("Helvetica",12),state=DISABLED)
    areaBox=OptionMenu(topFrame, areaVar, "La Union", "Irisan", "Calasiao", "VIllasis", "Bantay", "Isabela", "Pampanga", "Nueva Ecija")
    areaBox.configure(font=("Helvetica",12),width=20)
    typeBox=OptionMenu(topFrame, typeVar, "Desktop Set", "Laptop", "Printer", "Router/Switch","Monitor", "HDD/SSD", "RAM/Video Card", "Mouse/Keyboard", "CCTV")
    typeBox.configure(font=("Helvetica",12),width=20)
    descBox=Entry(topFrame, textvariable=descVar, width="24", font=("Helvetica",12))
    serlBox=Entry(topFrame, textvariable=serlVar, width="24", font=("Helvetica",12))
    
    dateBox = Entry(topFrame, textvariable=dateVar, width="24", font=("Helvetica",12), bg='white')
    dateBox.bind('<Double-Button-1>',onclick)
    qntyBox=Entry(topFrame, textvariable=qntyVar, width="24", font=("Helvetica",12))
    qntyBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
    subtBtn=Button(topFrame, text="Submit", font=("Helvetica",12),width=8, command=lambda:
                   onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
    canlBtn=Button(topFrame, text="Cancel", font=("Helvetica",12),width=8, command=lambda:main(menFrame,topFrame,botFrame,item_no,item_clicked))

    itemBox.bind("<F11>",lambda event: onFullscreen())
    areaBox.bind("<F11>",lambda event: onFullscreen())
    typeBox.bind("<F11>",lambda event: onFullscreen())
    descBox.bind("<F11>",lambda event: onFullscreen())
    serlBox.bind("<F11>",lambda event: onFullscreen())
    dateBox.bind("<F11>",lambda event: onFullscreen())
    qntyBox.bind("<F11>",lambda event: onFullscreen())
    
    if(item_clicked=="item"):
        itemBox.focus()
        itemLbl.config(font=("Helvetica","12","bold"))
        itemBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        itemBox.bind("<Escape>",lambda event: onBack())
    if(item_clicked=="area"):
        areaBox.focus()
        areaLbl.config(font=("Helvetica","12","bold"))
        areaBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        areaBox.bind("<Escape>",lambda event: onBack())
    elif(item_clicked=="type"):
        typeBox.focus()
        typeLbl.config(font=("Helvetica","12","bold"))
        typeBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        typeBox.bind("<Escape>",lambda event: main(menFrame,topFrame,botFrame,item_no,item_clicked))
    elif(item_clicked=="desc"):
        descBox.focus()
        descBox.icursor(END)
        descLbl.config(font=("Helvetica","12","bold"))
        descBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        descBox.bind("<Escape>",lambda event: onBack())
    elif(item_clicked=="serl"):
        serlBox.focus()
        serlBox.icursor(END)
        serlLbl.config(font=("Helvetica","12","bold"))
        serlBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        serlBox.bind("<Escape>",lambda event: onBack())
    elif(item_clicked=="date"):
        dateBox.focus()
        dateBox.icursor(END)
        dateLbl.config(font=("Helvetica","12","bold"))
        dateBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        dateBox.bind("<Escape>",lambda event: onBack())
    elif(item_clicked=="qnty"):
        qntyBox.focus()
        qntyBox.icursor(END)
        qntyLbl.config(font=("Helvetica","12","bold"))
        qntyBox.bind('<Return>',lambda event: onUpdate(areaVar.get(),typeVar.get(),descVar.get(),serlVar.get(),dateVar.get(),qntyVar.get(),item_no))
        qntyBox.bind("<Escape>",lambda event: onBack())
        
    itemLbl.grid(column=0,row=1,pady=3,sticky=E)
    areaLbl.grid(column=0,row=2,pady=3,sticky=E)
    typeLbl.grid(column=0,row=3,pady=3,sticky=E)
    descLbl.grid(column=0,row=4,pady=3,sticky=E)
    serlLbl.grid(column=0,row=5,pady=3,sticky=E)
    dateLbl.grid(column=0,row=6,pady=3,sticky=E)
    qntyLbl.grid(column=0,row=7,pady=3,sticky=E)

    itemBox.grid(column=1,row=1,pady=3,sticky=W)
    areaBox.grid(column=1,row=2,pady=3,sticky=W)
    typeBox.grid(column=1,row=3,pady=3,sticky=W)
    descBox.grid(column=1,row=4,pady=3,sticky=W)
    serlBox.grid(column=1,row=5,pady=3,sticky=W)
    dateBox.grid(column=1,row=6,pady=3,sticky=W)
    qntyBox.grid(column=1,row=7,pady=3,sticky=W)
    subtBtn.grid(column=1,row=8,pady=40,padx=1,sticky=W)
    canlBtn.grid(column=1,row=8,pady=40,padx=1,sticky=NS)
    
    root.state('zoomed')
    root.minsize("800", "600")
    root.wm_title("UGC-MIS Inventory System | Edit")
    root.mainloop()
    
def administrator(fr1,fr2,fr3):
    global boo
    fr1.destroy()
    fr2.destroy()
    fr3.destroy()

    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    menFrame.pack()
    topFrame.pack()
    botFrame.pack()

    photo = PhotoImage(file=r"Asset\admin.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummyObject"))
    logo.grid(row=0, column=0,pady=20)
    
    lbl=Label(topFrame, text="Admin settings", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)
    
    botFrame.bind("<Escape>",lambda event: main(menFrame,topFrame,botFrame,-1,"dummyObject"))

    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)

    def onBack():
        global boo
        if boo:
            boo=False
            root.attributes('-fullscreen',boo)
        else:
            main(menFrame,topFrame,botFrame,-1,"dummy")

    def onChange(nusr,npas,rpas,usr,pas,dum):
        if not nusr or not npas or not rpas or not usr:
            messagebox.showerror("Null User/Pass","Please fill all the empty fields!")
        elif npas!=rpas:
            dum.set("Passwords do not match!")
        else:
            connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
            cursor=connect.cursor()
            cursor.execute("SELECT username FROM admin WHERE username='%s'"%(usr))
            undb=cursor.fetchone()
            if undb!=None:
                undb=undb[0]
            cursor.execute("SELECT password FROM admin WHERE username='%s'"%(usr))
            pwdb=cursor.fetchone()
            if pwdb!=None:
                pwdb=pwdb[0]
            if undb==usr and pas==pwdb:
                lb=Listbox(topFrame)
                cursor.execute("UPDATE admin SET username='%s', password='%s' WHERE username='%s'"%(nusr,npas,usr))
                connect.commit()
                connect.close()
                messagebox.showinfo("Change Successful","Successfully changed username/password")
                login(menFrame,botFrame,topFrame)
            else:
                messagebox.showerror("Change User/Pass Failed!","Invalid username/password!")
                ubox.delete(0,END)
                pbox.delete(0,END)
                ubox.focus()
        
    menu=Menu(root)
    root.config(menu=menu)
    root.config(bg="#7a8694")
    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",state="disabled")
    fileMenu.add_command(label="Save as",state="disabled")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))

    dumVar=StringVar()
    newuLbl=Label(botFrame,text="New Username:",font="Helvetica 12",bg="#7a8694")
    newpLbl=Label(botFrame,text="New Password:",font="Helvetica 12",bg="#7a8694")
    newrLbl=Label(botFrame,text="Re-type Pass:",font="Helvetica 12",bg="#7a8694")
    dummyLbl=Label(botFrame,text=" ",textvariable=dumVar,font="Helvetica 12",bg="#7a8694",fg="red")
    olduLbl=Label(botFrame,text="Old Username:",font="Helvetica 12",bg="#7a8694")
    oldpLbl=Label(botFrame,text="Old Password:",font="Helvetica 12",bg="#7a8694")
    dummy2Lbl=Label(botFrame,text=" ",bg="#7a8694",font="Helvetica 24")

    newuVar=StringVar()
    newpVar=StringVar()
    newrVar=StringVar()
    olduVar=StringVar()
    oldpVar=StringVar()
    
    newuBox=Entry(botFrame,textvariable=newuVar,font="Helvetica 12")
    newuBox.focus_set()
    newpBox=Entry(botFrame,textvariable=newpVar,font="Helvetica 12",show="\u2022")
    newrBox=Entry(botFrame,textvariable=newrVar,font="Helvetica 12",show="\u2022")
    olduBox=Entry(botFrame,textvariable=olduVar,font="Helvetica 12")
    oldpBox=Entry(botFrame,textvariable=oldpVar,font="Helvetica 12",show="\u2022")

    subBtn=Button(botFrame,text="Submit",font="Helvetica 12", command=lambda:onChange(newuBox.get(),newpBox.get(),newrBox.get(),olduBox.get(),oldpBox.get(),dumVar))
    canBtn=Button(botFrame,text="Cancel",font="Helvetica 12", command=lambda:main(menFrame,topFrame,botFrame,-1,"dummVar"))

    newuBox.bind("<Escape>", lambda event: botFrame.focus_set())
    newpBox.bind("<Escape>", lambda event: botFrame.focus_set())
    newrBox.bind("<Escape>", lambda event: botFrame.focus_set())
    olduBox.bind("<Escape>", lambda event: botFrame.focus_set())
    oldpBox.bind("<Escape>", lambda event: botFrame.focus_set())
    oldpBox.bind("<Return>", lambda event: onChange(newuBox.get(),newpBox.get(),newrBox.get(),olduBox.get(),oldpBox.get(),dumVar))

    newuBox.bind("<F11>", lambda event: onFullscreen())
    newpBox.bind("<F11>", lambda event: onFullscreen())
    newrBox.bind("<F11>", lambda event: onFullscreen())
    olduBox.bind("<F11>", lambda event: onFullscreen())
    oldpBox.bind("<F11>", lambda event: onFullscreen())
    botFrame.bind("<F11>", lambda event: onFullscreen())
    newuBox.bind("<Control-o>", lambda event: onOpen())
    newpBox.bind("<Control-o>", lambda event: onOpen())
    newrBox.bind("<Control-o>", lambda event: onOpen())
    olduBox.bind("<Control-o>", lambda event: onOpen())
    oldpBox.bind("<Control-o>", lambda event: onOpen())
    botFrame.bind("<Control-o>", lambda event: onOpen())
    newuBox.bind("<Control-n>", lambda event: create(menFrame,topFrame,botFrame))
    newpBox.bind("<Control-n>", lambda event: create(menFrame,topFrame,botFrame))
    newrBox.bind("<Control-n>", lambda event: create(menFrame,topFrame,botFrame))
    olduBox.bind("<Control-n>", lambda event: create(menFrame,topFrame,botFrame))
    oldpBox.bind("<Control-n>", lambda event: create(menFrame,topFrame,botFrame))
    botFrame.bind("<Control-n>", lambda event: create(menFrame,topFrame,botFrame))
    
    newuLbl.grid(column=0,row=1,sticky=E,pady=3)
    newpLbl.grid(column=0,row=2,sticky=E,pady=3)
    newrLbl.grid(column=0,row=3,sticky=E,pady=3)
    dummyLbl.grid(column=1,row=4,sticky=E,pady=3)
    olduLbl.grid(column=0,row=5,sticky=E,pady=3)
    oldpLbl.grid(column=0,row=6,sticky=E,pady=3)
    newuBox.grid(column=1,row=1,sticky=W,pady=3)
    newpBox.grid(column=1,row=2,sticky=W,pady=3)
    newrBox.grid(column=1,row=3,sticky=W,pady=3)
    olduBox.grid(column=1,row=5,sticky=W,pady=3)
    oldpBox.grid(column=1,row=6,sticky=W,pady=3)
    dummy2Lbl.grid(column=0,row=7,columnspan=2,pady=3)
    canBtn.grid(column=1,row=8,sticky=W)
    subBtn.grid(column=1,row=8,sticky=E)
    
    root.state('zoomed')
    root.minsize("800", "600")
    root.wm_title("UGC-MIS Inventory System | Admin")
    root.mainloop()

def view(fr1,fr2,fr3):
    global boo
    def onSave(svtype,lb0,lb1,lb2,lb3,lb4,lb5,lb6):
        book = Workbook()
        sheet = book.active
        def integerizer(t):
            indx=0
            for i in range(len(t)):
                if t[indx].isdigit():
                    t[indx]=int(t[indx])
                else:
                    t[indx]=""
                indx+=1
            return t
        
        lbh=(("Bantay","Calasiao","Irisan","Isabela","La Union", "Nueva Ecija", "Pampanga", "Villasis", "Type Total","Type Total"),)
        lb1g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb1.get(0,END)))))
        lb2g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb2.get(0,END)))))
        lb3g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb3.get(0,END)))))
        lb4g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb4.get(0,END)))))
        lb5g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb5.get(0,END)))))
        lb6g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb6.get(0,END)))))
        lb7g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb7.get(0,END)))))
        lb8g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb8.get(0,END)))))
        lb9g=integerizer(list(chain(*(i if isinstance(i, tuple) else (i,) for i in lb9.get(0,END)))))
        for headr in lbh:
            sheet.append(headr)
        for row in zip(lb0.get(0,END),lb1g,lb2g,lb3g,lb4g,lb5g,lb6g,lb7g,lb8g,lb9g):
            sheet.append(row)
        if svtype=="saveas":
            path = filedialog.asksaveasfilename(initialdir = "Output",title="Save file",filetypes=(("Excel Workbook","*.xlsx"),("All files","*.*")))
            if path:
                print(path)
                book.save("%s.xlsx"%(path))
        elif svtype=="autosave":
            fileno = sum(1 for f in os.listdir("Output") if os.path.isfile(os.path.join("Output", f)) and f[0] != '.')+1
            if fileno<=9:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno<=99:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno<=999:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno<=9999:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            elif fileno>=10000:
                filename="UGCMIS-LUZ1IS-%s-%i"%(str(now.isoformat())[0:10],fileno)
            book.save("Output\%s.xlsx"%(filename))
            messagebox.showinfo("Successfully Saved","File: %s has been saved as excel at output folder"%(filename))

    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
            
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)
        
    connect = mysql.connector.connect(user='root', password='', host='localhost', database='luz1_inventory')
    cursor=connect.cursor()
    fr1.destroy()
    fr2.destroy()
    fr3.destroy()

    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    menFrame.pack()
    topFrame.pack()
    botFrame.pack()

    photo = PhotoImage(file=r"Asset\statistics.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummyObject"))
    logo.grid(row=0, column=0,pady=20)
    
    lbl=Label(topFrame, text="Statistical View", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)

    menu=Menu(root)
    root.config(menu=menu)

    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",command=lambda: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    fileMenu.add_command(label="Save as",command=lambda: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6),state="disabled")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))

    def selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,sed):
        lb0.selection_clear(0,END)
        lb0.selection_set(sed)
        lb0.activate(sed)
        lb1.selection_clear(0,END)
        lb1.selection_set(sed)
        lb1.activate(sed)
        lb2.selection_clear(0,END)
        lb2.selection_set(sed)
        lb2.activate(sed)
        lb3.selection_clear(0,END)
        lb3.selection_set(sed)
        lb3.activate(sed)
        lb4.selection_clear(0,END)
        lb4.selection_set(sed)
        lb4.activate(sed)
        lb5.selection_clear(0,END)
        lb5.selection_set(sed)
        lb5.activate(sed)
        lb6.selection_clear(0,END)
        lb6.selection_set(sed)
        lb6.activate(sed)
        lb7.selection_clear(0,END)
        lb7.selection_set(sed)
        lb7.activate(sed)
        lb8.selection_clear(0,END)
        lb8.selection_set(sed)
        lb8.activate(sed)
        lb9.selection_clear(0,END)
        lb9.selection_set(sed)
        lb9.activate(sed)
        
    lab0=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Type",font=("Helvetica","14","bold"))
    lab1=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Bantay",font=("Helvetica","14","bold"))
    lab2=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Calasiao",font=("Helvetica","14","bold"))
    lab3=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Irisan",font=("Helvetica","14","bold"))
    lab4=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Isabela",font=("Helvetica","14","bold"))
    lab5=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="La Union",font=("Helvetica","14","bold"))
    lab6=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Nueva Ecija",font=("Helvetica","14","bold"))
    lab7=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Pampanga",font=("Helvetica","14","bold"))
    lab8=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Villasis",font=("Helvetica","14","bold"))
    lab9=Label(botFrame,bd=1,relief="solid",bg="#a6a6a6",text="Type Total",font=("Helvetica","14","bold"))
        
    lb0=Listbox(botFrame,height=9,width=16,font=("Helvetica","14","bold"),exportselection=0)
    lb1=Listbox(botFrame,height=9,width=6,font=("Helvetica","14"),exportselection=0)
    lb2=Listbox(botFrame,height=9,width=7,font=("Helvetica","14"),exportselection=0)
    lb3=Listbox(botFrame,height=9,width=5,font=("Helvetica","14"),exportselection=0)
    lb4=Listbox(botFrame,height=9,width=6,font=("Helvetica","14"),exportselection=0)
    lb5=Listbox(botFrame,height=9,width=7,font=("Helvetica","14"),exportselection=0)
    lb6=Listbox(botFrame,height=9,width=10,font=("Helvetica","14"),exportselection=0)
    lb7=Listbox(botFrame,height=9,width=10,font=("Helvetica","14"),exportselection=0)
    lb8=Listbox(botFrame,height=9,width=7,font=("Helvetica","14"),exportselection=0)
    lb9=Listbox(botFrame,height=9,width=10,font=("Helvetica","14","bold"),exportselection=0)

    lb0.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb0.curselection()))
    lb1.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb1.curselection()))
    lb2.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb2.curselection()))
    lb3.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb3.curselection()))
    lb4.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb4.curselection()))
    lb5.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb5.curselection()))
    lb6.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb6.curselection()))
    lb7.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb7.curselection()))
    lb8.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb8.curselection()))
    lb9.bind("<<ListboxSelect>>", lambda event: selector(lb0,lb1,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb9,lb9.curselection()))

    cursor.execute("SELECT DISTINCT type FROM items ORDER BY type ASC")
    ch1=sum(cursor.fetchall(),())
    
    for i in ch1:
        lb0.insert(END,i)
    lb0.insert(END,"Grand Total")
    
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Bantay' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb1.insert(END,"---")
        else:
            lb1.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Calasiao' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb2.insert(END,"---")
        else:
            lb2.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Irisan' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb3.insert(END,"---")
        else:
            lb3.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Isabela' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb4.insert(END,"---")
        else:
            lb4.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='La Union' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb5.insert(END,"---")
        else:
            lb5.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Nueva Ecija' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb6.insert(END,"---")
        else:
            lb6.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Pampanga' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb7.insert(END,"---")
        else:
            lb7.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Villasis' and TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb8.insert(END,"---")
        else:
            lb8.insert(END,x)
    for i in ch1:
        cursor.execute("SELECT SUM(qty) FROM items WHERE TYPE='%s'"%(i))
        x=sum(cursor.fetchall(),())
        if str(x)=="(None,)":
            lb9.insert(END,"---")
        else:
            lb9.insert(END,x)
        
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Bantay'")
    lb1.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Calasiao'")
    lb2.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Irisan'")
    lb3.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Isabela'")
    lb4.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='La Union'")
    lb5.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Nueva Ecija'")
    lb6.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Pampanga'")
    lb7.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items WHERE AREA='Villasis'")
    lb8.insert(END,sum(cursor.fetchall(),()))
    cursor.execute("SELECT SUM(qty) FROM items")
    lb9.insert(END,sum(cursor.fetchall(),()))

    lb0.select_set(END)
    lb1.select_set(END)
    lb2.select_set(END)
    lb3.select_set(END)
    lb4.select_set(END)
    lb5.select_set(END)
    lb6.select_set(END)
    lb7.select_set(END)
    lb8.select_set(END)
    lb9.select_set(END)
    lb9.event_generate("<<ListboxSelect>>")
    lb9.focus_set()
    lb9.activate(END)

    lb0.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb1.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb2.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb3.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb4.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb5.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb6.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb7.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb8.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb9.bind("<F5>",lambda event: view(menFrame,topFrame,botFrame))
    lb0.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb1.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb2.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb3.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb4.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb5.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb6.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb7.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb8.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb9.bind("<Control-s>",lambda event: onSave("saveas",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb0.bind("<Control-o>",lambda event: onOpen())
    lb1.bind("<Control-o>",lambda event: onOpen())
    lb2.bind("<Control-o>",lambda event: onOpen())
    lb3.bind("<Control-o>",lambda event: onOpen())
    lb4.bind("<Control-o>",lambda event: onOpen())
    lb5.bind("<Control-o>",lambda event: onOpen())
    lb6.bind("<Control-o>",lambda event: onOpen())
    lb7.bind("<Control-o>",lambda event: onOpen())
    lb8.bind("<Control-o>",lambda event: onOpen())
    lb9.bind("<Control-o>",lambda event: onOpen())
    lb0.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb1.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb2.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb3.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb4.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb5.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb6.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb7.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb8.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb9.bind("<Control-n>",lambda event: create(menFrame,topFrame,botFrame))
    lb0.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb1.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb2.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb3.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb4.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb5.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb6.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb7.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb8.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb9.bind("<F12>",lambda event: onSave("autosave",lb0,lb1,lb2,lb3,lb4,lb5,lb6))
    lb0.bind("<F11>",lambda event: onFullscreen())
    lb1.bind("<F11>",lambda event: onFullscreen())
    lb2.bind("<F11>",lambda event: onFullscreen())
    lb3.bind("<F11>",lambda event: onFullscreen())
    lb4.bind("<F11>",lambda event: onFullscreen())
    lb5.bind("<F11>",lambda event: onFullscreen())
    lb6.bind("<F11>",lambda event: onFullscreen())
    lb7.bind("<F11>",lambda event: onFullscreen())
    lb8.bind("<F11>",lambda event: onFullscreen())
    lb9.bind("<F11>",lambda event: onFullscreen())
    lb0.grid(column=0,row=1,sticky="nsew")
    lb1.grid(column=1,row=1,sticky="nsew")
    lb2.grid(column=2,row=1,sticky="nsew")
    lb3.grid(column=3,row=1,sticky="nsew")
    lb4.grid(column=4,row=1,sticky="nsew")
    lb5.grid(column=5,row=1,sticky="nsew")
    lb6.grid(column=6,row=1,sticky="nsew")
    lb7.grid(column=7,row=1,sticky="nsew")
    lb8.grid(column=8,row=1,sticky="nsew")
    lb9.grid(column=9,row=1,sticky="nsew")
    lab0.grid(column=0,row=0,sticky="nsew")
    lab1.grid(column=1,row=0,sticky="nsew")
    lab2.grid(column=2,row=0,sticky="nsew")
    lab3.grid(column=3,row=0,sticky="nsew")
    lab4.grid(column=4,row=0,sticky="nsew")
    lab5.grid(column=5,row=0,sticky="nsew")
    lab6.grid(column=6,row=0,sticky="nsew")
    lab7.grid(column=7,row=0,sticky="nsew")
    lab8.grid(column=8,row=0,sticky="nsew")
    lab9.grid(column=9,row=0,sticky="nsew")

    root.config(bg="#7a8694")
    root.state('zoomed')
    root.minsize("1200", "700")
    root.wm_title("UGC-MIS Inventory System | Stats")
    root.mainloop()
    

def helps(fr1,fr2,fr3):
    global boo
    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
            
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)

    fr1.destroy()
    fr2.destroy()
    fr3.destroy()

    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    menFrame.pack()
    topFrame.pack()
    botFrame.pack()

    photo = PhotoImage(file=r"Asset\help.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummyObject"))
    logo.grid(row=0, column=0,pady=20)
    
    lbl=Label(topFrame, text="User Help", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)

    menu=Menu(root)
    root.config(menu=menu)
    root.config(bg="#7a8694")
    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",state="disabled")
    fileMenu.add_command(label="Save as",state="disabled")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))

    botFrame.focus_set()
    botFrame.bind("<F11>",lambda event: onFullscreen())
    botFrame.bind("<Escape>",lambda event: main(menFrame,topFrame,botFrame,-1,"dummyVariable"))
    botFrame.bind("<Control-o>",lambda event:onOpen())
    botFrame.bind("<Control-n>",lambda event:create(menFrame,topFrame,botFrame))
    
    lab1=Label(botFrame,text="Ctrl + N:",font=("Courier New","14","bold"),bd=2,relief="solid")
    lab2=Label(botFrame,text="Ctrl + O:",font=("Courier New","14","bold"),bd=2,relief="solid")
    lab3=Label(botFrame,text="Ctrl + S:",font=("Courier New","14","bold"),bd=2,relief="solid")
    lab4=Label(botFrame,text="F12:",     font=("Courier New","14","bold"),bd=2,relief="solid")
    lab5=Label(botFrame,text="F11:",     font=("Courier New","14","bold"),bd=2,relief="solid")
    lab6=Label(botFrame,text="F5:",      font=("Courier New","14","bold"),bd=2,relief="solid")
    lab7=Label(botFrame,text="Escape:",  font=("Courier New","14","bold"),bd=2,relief="solid")
    lab8=Label(botFrame,text="Delete:",  font=("Courier New","14","bold"),bd=2,relief="solid")
    lab9=Label(botFrame,text="Enter",        font=("Courier New","14","bold"),bd=2,relief="solid")
    lab10=Label(botFrame,text="Double Click:",font=("Courier New","14","bold"),bd=2,relief="solid")
    lab11=Label(botFrame,text="Right Click:", font=("Courier New","14","bold"),bd=2,relief="solid")
    lab12=Label(botFrame,text="Logo Click:",  font=("Courier New","14","bold"),bd=2,relief="solid")

    inf1=Label(botFrame,text="Opens create entry window",                        font=("Helvetica","12"),bd=2,relief="solid")
    inf2=Label(botFrame,text="Prompts in opening excel files",                   font=("Helvetica","12"),bd=2,relief="solid")
    inf3=Label(botFrame,text="Prompts save as window",                           font=("Helvetica","12"),bd=2,relief="solid")
    inf4=Label(botFrame,text="Quick save to \Output\ folder",                    font=("Helvetica","12"),bd=2,relief="solid")
    inf5=Label(botFrame,text="Fullscreen window",                                font=("Helvetica","12"),bd=2,relief="solid")
    inf6=Label(botFrame,text="Refreshes the data tables",                        font=("Helvetica","12"),bd=2,relief="solid")
    inf7=Label(botFrame,text="[Main window]: Unfocus the selection\n[New/Edit Window]: Go back to main window", font=("Helvetica","12"),bd=2,relief="solid")
    inf8=Label(botFrame,text="[Main window]: Deletes the current selection row", font=("Helvetica","12"),bd=2,relief="solid")
    inf9=Label(botFrame,text="[Search box]: Submit the data",                    font=("Helvetica","12"),bd=2,relief="solid")
    inf10=Label(botFrame,text="[Main window]: Edits the current selection row\n[New window]: Double click the date box to pop-ups the date picker",font=("Helvetica","12"),bd=2,relief="solid")
    inf11=Label(botFrame,text="[Main window]: Deletes the current selection row",font=("Helvetica","12"),bd=2,relief="solid")
    inf12=Label(botFrame,text="Go back to main window",                          font=("Helvetica","12"),bd=2,relief="solid")

    homBtn=Button(botFrame,text="Home",font="Helvetica 12",command=lambda:main(menFrame,topFrame,botFrame,-1,"dummVar"),width=12)
    homBtn.grid(row=12,column=1,pady=20,sticky=E)
    
    lab1.grid(row=0,column=0,sticky="nsew")
    lab2.grid(row=1,column=0,sticky="nsew")
    lab3.grid(row=2,column=0,sticky="nsew")
    lab4.grid(row=3,column=0,sticky="nsew")
    lab5.grid(row=4,column=0,sticky="nsew")
    lab6.grid(row=5,column=0,sticky="nsew")
    lab7.grid(row=6,column=0,sticky="nsew")
    lab8.grid(row=7,column=0,sticky="nsew")
    lab9.grid(row=8,column=0,sticky="nsew")
    lab10.grid(row=9,column=0,sticky="nsew")
    lab11.grid(row=10,column=0,sticky="nsew")
    lab12.grid(row=11,column=0,sticky="nsew")

    inf1.grid(row=0,column=1,sticky="nsew")
    inf2.grid(row=1,column=1,sticky="nsew")
    inf3.grid(row=2,column=1,sticky="nsew")
    inf4.grid(row=3,column=1,sticky="nsew")
    inf5.grid(row=4,column=1,sticky="nsew")
    inf6.grid(row=5,column=1,sticky="nsew")
    inf7.grid(row=6,column=1,sticky="nsew")
    inf8.grid(row=7,column=1,sticky="nsew")
    inf9.grid(row=8,column=1,sticky="nsew")
    inf10.grid(row=9,column=1,sticky="nsew")
    inf11.grid(row=10,column=1,sticky="nsew")
    inf12.grid(row=11,column=1,sticky="nsew")
    
    root.config(bg="#7a8694")
    root.state('zoomed')
    root.minsize("800", "600")
    root.wm_title("UGC-MIS Inventory System | Help")
    root.mainloop()
    

def credit(fr1,fr2,fr3):
    global boo
    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
            
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)

    fr1.destroy()
    fr2.destroy()
    fr3.destroy()
    
    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    menFrame.pack()
    topFrame.pack()
    botFrame.pack()

    photo = PhotoImage(file=r"Asset\credits.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummyObject"))
    logo.grid(row=0, column=0,pady=20)
    
    lbl=Label(topFrame, text="System information", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)

    menu=Menu(root)
    root.config(menu=menu)
    root.config(bg="#7a8694")
    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",state="disabled")
    fileMenu.add_command(label="Save as",state="disabled")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))

    botFrame.focus_set()
    botFrame.bind("<F11>",lambda event: onFullscreen())
    botFrame.bind("<Escape>",lambda event: main(menFrame,topFrame,botFrame,-1,"dummyVariable"))
    botFrame.bind("<Control-o>",lambda event:onOpen())
    botFrame.bind("<Control-n>",lambda event:create(menFrame,topFrame,botFrame))

    pyphoto = PhotoImage(file=r"Asset\credit\python.png")
    pylogo = Label(botFrame, image=pyphoto, bg="#7a8694")
    pylogo.grid(row=1, column=0)

    pylbl=Label(botFrame, text="The system is mainly coded on the Python 3.4 programming language,\nAlgorithm of the front and back end is coded in this language", font=("Helvetica","12","italic"), bg="#7a8694",justify="left")
    pylbl.grid(row=1, column=1,sticky="w")

    tkphoto = PhotoImage(file=r"Asset\credit\tk.png")
    tklogo = Label(botFrame, image=tkphoto, bg="#7a8694")
    tklogo.grid(row=2, column=0,sticky="e",pady=10)

    pylbl=Label(botFrame, text="The Tkinter GUI is the library used for the user-interface/experience,using its\n other sub-libraries such as TkCalendar, TkDialogs TkMessageBox.", font=("Helvetica","12","italic"), bg="#7a8694",justify="left")
    pylbl.grid(row=2, column=1,sticky="w")

    sqphoto = PhotoImage(file=r"Asset\credit\sql.png")
    sqlogo = Label(botFrame, image=sqphoto, bg="#7a8694")
    sqlogo.grid(row=3, column=0,sticky="e",pady=20)

    sqlbl=Label(botFrame, text="The MySql.connector is used for database connection module,\nUsed as connection to phpmyadmin/MariaDB for database modifications.", font=("Helvetica","12","italic"), bg="#7a8694",justify="left")
    sqlbl.grid(row=3, column=1,sticky="w")

    opphoto = PhotoImage(file=r"Asset\credit\op.png")
    oplogo = Label(botFrame, image=opphoto, bg="#7a8694")
    oplogo.grid(row=4, column=0,sticky="e",pady=10)

    oplbl=Label(botFrame, text="The OpenPyxl library for exporting the data to Excel format,\nThe library will process to a spreadsheet xlsx format.", font=("Helvetica","12","italic"), bg="#7a8694",justify="left")
    oplbl.grid(row=4, column=1,sticky="w")

    xmphoto = PhotoImage(file=r"Asset\credit\xampp.png")
    xmlogo = Label(botFrame, image=xmphoto, bg="#7a8694")
    xmlogo.grid(row=5, column=0,sticky="e",pady=20)

    xmlbl=Label(botFrame, text="The XAMPP software, used to manage Apache local server and PhpMyAdmin\nfor the database setup", font=("Helvetica","12","italic"), bg="#7a8694",justify="left")
    xmlbl.grid(row=5, column=1,sticky="w")
    
    root.config(bg="#7a8694")
    root.state('zoomed')
    root.minsize("800", "600")
    root.wm_title("UGC-MIS Inventory System | Credits")
    root.mainloop()

def about(fr1,fr2,fr3):
    global boo
    def onOpen():
        path=filedialog.askopenfilename(initialdir = "Output",title = "Select file",filetypes = (("Excel Workbook","*.xlsx"),("all files","*.*")))
        if path:
            os.startfile(path, 'Open')
            
    def onFullscreen():
        global boo
        if boo:
            boo=False
        else:
            boo=True
        root.attributes('-fullscreen',boo)

    fr1.destroy()
    fr2.destroy()
    fr3.destroy()

    menFrame=Frame(root, bg="#7a8694")
    topFrame=Frame(root, bg="#7a8694")
    botFrame=Frame(root, bg="#7a8694")
    menFrame.pack()
    topFrame.pack()
    botFrame.pack(side=BOTTOM)

    menu=Menu(root)
    root.config(menu=menu)
    root.config(bg="#7a8694")
    fileMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New entry",command=lambda: create(menFrame,topFrame,botFrame))
    fileMenu.add_command(label="Open",command=lambda: onOpen())
    fileMenu.add_command(label="Quick Save",state="disabled")
    fileMenu.add_command(label="Save as",state="disabled")
    viewMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="Statistic view",command=lambda: view(menFrame,topFrame,botFrame))
    viewMenu.add_command(label="Fullscreen",command=lambda: onFullscreen())
    adminMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Admin",menu=adminMenu)
    adminMenu.add_command(label="Change password",command=lambda: administrator(menFrame,topFrame,botFrame))
    helpMenu=Menu(menu, tearoff=0)
    menu.add_cascade(label="Help",menu=helpMenu)
    helpMenu.add_command(label="Help",command=lambda: helps(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="Information",command=lambda: credit(menFrame,topFrame,botFrame))
    helpMenu.add_command(label="About",command=lambda: about(menFrame,topFrame,botFrame))
    
    photo = PhotoImage(file=r"Asset\information.png")
    logo = Label(topFrame, image=photo, bg="#7a8694")
    logo.bind('<Button-1>',lambda event:main(menFrame,topFrame,botFrame,-1,"dummyObject"))
    logo.grid(row=0, column=0,pady=20)
    
    lbl=Label(topFrame, text="About Us", font=("Unispace",36), bg="#7a8694")
    lbl.grid(row=0, column=1,sticky=E,pady=20)

    txt1="""
 This  system  purpose  was to create  a user friendly, intuitive  experience and  reliably secured
 inventory system. The system is  exclusively and  solely dedicated to the MIS department in  Union
 Galvasteel Corporation company,  We the Lorma OJT 2018 would like to thank Engr. Ulyses V. Agtarap
 for his patience and effort in training us all through the 70 days On-the-job training, we learned
 a lot of technical and computing skills that is essential on our field as IT professional.
 """
    txt2="""
                               Supervisor Engineer: Engr. Ulyses V. Agtarap
                            Senior Project manager: John Carlos Buccat
                            Database adminostrator: Terry Carl G. Cuesta
                               Software programmer: Joshua F. Gamoso

                                   (c) All rights reserved 2018
"""
    paraTxt=Text(botFrame, font=("Courier New","11","bold"), width=100, height=13,bg="#dffff7")
    paraTxt.insert(END,txt1)
    paraTxt.insert(END,txt2)
    paraTxt.configure(state="disabled")
    paraTxt.grid(row=0, column=0)

    bphoto = PhotoImage(file=r"Asset\galvaboys.png")
    blogo = Label(botFrame, image=bphoto, bg="#7a8694")
    blogo.grid(row=1, column=0)
    

    botFrame.focus_set()
    botFrame.bind("<F11>",lambda event: onFullscreen())
    botFrame.bind("<Escape>",lambda event: main(menFrame,topFrame,botFrame,-1,"dummyVariable"))
    botFrame.bind("<Control-o>",lambda event:onOpen())
    botFrame.bind("<Control-n>",lambda event:create(menFrame,topFrame,botFrame))
    
    root.config(bg="#7a8694")
    root.state('zoomed')
    root.minsize("800", "600")
    root.wm_title("UGC-MIS Inventory System | About")
    root.mainloop()
    
root = Tk()
root.iconbitmap(r'Asset\favicon.ico')
fra=Frame(root)
lb=Listbox(root)

boo=False

login(fra,fra,fra)
