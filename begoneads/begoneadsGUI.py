
import tkinter as tk
from tkinter import ttk
from begoneads import begoneads


class App (tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Begoneads")
        self.geometry("600x400")

        self.host_section = ttk.LabelFrame(self, text='Sources', borderwidth=4, width=300, height=200)
        self.host_section.pack(padx=10, pady=20, side='top', anchor='nw')
        self.tw_scroll=tk.Scrollbar(self.host_section)
        self.tw_scroll.pack(side='right', fill='y')
        self.sources = list(enumerate(begoneads.sources))
        for i in self.sources:
            print(i)
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
        self.host_tw.bind('<1>', self.on_click)
        self.add_host_entry=tk.Entry(self, width=45)
        self.add_host_entry.pack(side='left', anchor='nw', padx=(10,0))
        #make a validation of the host inserted
        self.add_host_btn = tk.Button(self, text="add source")
        self.add_host_btn.pack(side='left', anchor='nw', padx=5)
        
    def on_click(self, event):
        item = self.host_tw.identify('item', event.x, event.y)
        self.host_tw.selection_toggle(item)
    def on_right_click(self, event):
        item = self.host_tw.identify('item', event.x, event.y)
        
        
    def add_domain(self):
        domain = self.add_host_entry.get()
        self.sources += [(len(self.sources + 1), domain )]
        source = self.sources[-1]
        self.host_tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.host_tw.selection_toggle(str(source[0]))
        

        
app = App()
app.mainloop()
