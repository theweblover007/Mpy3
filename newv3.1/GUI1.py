from tkinter import Tk, Text, BOTH, W, N, E, S
#from ttk import Frame, Button, Label, Style
from tkinter import ttk
from tkinter import *
from DownloadUrl import *
from emp3 import *
import sys
import os
import time
import threading

def update(name,label,dobj):
    global log
    while True:
        status,per=dobj.getstatus()
        size=dobj.getsize()
        if size>1024*1024:
            size=round(size/(1024*1024),2)
            size=str(size)+" Mb"
        else:
            size=str(size)+" Kb"
        label['text']=name+"-"+size+"-"+status+"-"+str(per)+"%"

def peer(event,name):
    os.system(name)

def handlelink(label,uri,name):
    uri=uri.replace(' ','%20')
    print(uri)
    d=downloadfile(uri)
    st=threading.Thread(target=update,args=(name,label,d))
    st.start()
    thread=[]
    if d.er():
        print("try later!:/")
        
        return
    d.namesize(name)
    if d.er():
        print("No file")
        return
    req=urllib.request.Request(uri)
    for i in range(0,d.notr):
        t=threading.Thread(target=d.downl,args=(i*d.schnk(),req))
        t.start()
        print("started",i)
        thread.append(t)

    for i in thread:
        i.join()
    if d.er():
        print('ERROR 101:/')
        return
    else:
        d.savefile()
        label.bind('<Button-1>',lambda event:peer(event,name))
        label.config(fg="blue",cursor="hand2")
    
        
class GUI(ttk.Frame):
  
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)   
         
        self.parent = parent
        self.links=[]
        self.urlnames=[]
        self.songthreads=[]
        self.songlabels=[]
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Mpy3")
        
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        lbl =ttk. Label(self, text="Name-size-status")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        self.area = Text(self,state=DISABLED)
        self.area.grid(row=1, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
        
        self.entry = Entry(self)
        self.entry.grid(row=5, column=0, padx=5,columnspan=3)

        obtn = ttk.Button(self, text="OK",command=self.startit)
        obtn.grid(row=5, column=3)
        self.parent.bind('<Return>',self.peertostart)
        
    def peertostart(self,event):
        self.startit()
    def startit(self):
         self.parent.withdraw()
         try:
             s=song_emp3(self.entry.get())
         except:
            return
         if not s.error:
             self.links=s.givelinks()
             self.urlnames=s.givenames()
             downuri,downame=self.getdownlink()
             l=Label(self.area,text=downame+"-Connecting")
             l.config(bg='white')  
             t=threading.Thread(target=handlelink,args=(l,downuri,downame))
             self.songthreads.append(t)
             t.start()
             
             l.pack()
             self.songlabels.append(l)
         self.parent.update()
         self.parent.deiconify()
    def getdownlink(self):
         try:
             for i in range(0,len(self.links)):
                 print(str(i+1)+">"+self.urlnames[i])
         except:
             pass
         i=int(input("Which one?"))-1
         name=input("Save as ?")
         name=name+".mp3"
         return (self.links[i],name)


     
def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = GUI(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()  
