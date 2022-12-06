import tkinter as tk
from tkinter import ttk
from begoneads import begoneads


class App (tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Begoneads")
        self.geometry("600x400")

        self.host_section = ttk.LabelFrame(self, text='Hosts', borderwidth=4, width=300, height=200)
        self.host_section.pack(padx=10, pady=20)
        self.tw_scroll=tk.Scrollbar(self.host_section)
        self.tw_scroll.pack(side='right', fill='y')
        self.sources = list(enumerate(begoneads.sources))
        self.host_tw = ttk.Treeview(self.host_section, columns=["ID", "Address"], yscrollcommand=self.tw_scroll.set, selectmode="none", displaycolumns=["ID", "Address"])
        self.host_tw.pack()
        self.host_tw.column("#0", width=0, stretch="no")
        self.host_tw.column("ID", width=20, anchor="center")
        self.host_tw.column("Address", width=300, anchor="w")
        self.host_tw.heading("ID", text="ID")
        self.host_tw.heading("Address", text="Address")
        for source in self.sources:
            self.host_tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.host_tw.selection_add([str(i) for i in range(len(self.sources))])
        self.tw_scroll.config(command=self.host_tw.yview)

        
app = App()
