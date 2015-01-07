from tkinter import *
from tkinter import ttk
class SOMEMSG:
    def __init__(self, parent,txt,temp):

        top = self.top = Toplevel(parent)
        self.top.iconbitmap('favicon.ico')
        self.top.title('Mpy3')
        Label(top, text=txt).pack()
        self.temp=temp
        self.e = Entry(top)
        self.e.pack(padx=5)
        self.top.bind("<Return>",self.ok)
        b = ttk.Button(top, text="OK")
        b.bind("<Button-1>",self.ok)
        b.pack(pady=5)

    def ok(self,event):
        self.temp.append(self.e.get())

        self.top.destroy()


class MSSG:
    def __init__(self, parent,txt):

        top = self.top = Toplevel(parent)

        Label(top, text=txt).pack()

        b = ttk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()

