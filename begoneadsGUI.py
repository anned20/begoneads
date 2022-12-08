
import tkinter as tk
from tkinter import ttk
import begoneads.begoneads as bg


class Labelscrolledtw(ttk.LabelFrame):
    """ A modded Labelframe with a treeview and a scrollbar attached. The treeview is configured in a specific way that of course can be changed. """
    def __init__(self, parent, text='Labelscrolledtw', borderwidth=4, width=300, height=200, columns = [("ID", 20, 'center')], selectmode='none'):
        super().__init__(parent, text=text, borderwidth=borderwidth, width=width, height=height)
        self.twscroll = tk.Scrollbar(self)
        self.twscroll.pack(side='right', fill='y')
        self.tw = ttk.Treeview(self, columns=[col[0] for col in columns], yscrollcommand=self.twscroll.set,
                               selectmode=selectmode, displaycolumns=[col[0] for col in columns])
        self.tw.pack()
        self.tw.column("#0", width=0, stretch='no')
        for col in columns:
            self.tw.column(col[0], width=col[1], anchor=col[2])
        for col in columns:
            self.tw.heading(col[0], text=col[0])
        
        self.tw.tag_configure('todelete', background='red')
        self.twscroll.config(command=self.tw.yview)
        self.tw.bind('<1>', self.on_click)
        self.tw.bind('<3>', self.on_right_click)

    def on_click(self, event):
        item = self.tw.identify('item', event.x, event.y)
        if not self.tw.tag_has('todelete', item):
            self.tw.selection_toggle(item)
    def on_right_click(self, event):
        item = self.tw.identify('item', event.x, event.y)
        #print(item)
        self.tw.selection_remove(item)
        if self.tw.tag_has('todelete', item):
            self.tw.item(str(item), tags=())
        else:
            self.tw.item(str(item), tags='todelete')
        #print("tag has: ", self.tw.tag_has('todelete'))
        

class App (tk.Tk):
    """Begoneads GUI in tkinter, some widgets tied together that invoke the begoneads functions. and extend its functionality"""
    
    def __init__(self):
        super().__init__()
        self.title("Begoneads")
        self.geometry("600x650")
        self.resizable(False, False)
        self.style=ttk.Style()
        self.style.map('Treeview', background=[('selected', 'green')])

        
        ################################################
        #REMOTE SECTION
        ##############################################
        self.remote_section = Labelscrolledtw(self, text='Remote Sources', borderwidth=4, width=300, height=200, columns=[("ID", 20, 'center'), ("Address", 300, 'w')])
        self.remote_section.grid(padx=10, pady=20, row=0, column=0)
        self.sources = list(enumerate(bg.sources))
        self.local_sources = []
        #for i in self.sources:
            #print(i)

        for source in self.sources:
            self.remote_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.remote_section.tw.selection_add([str(i) for i in range(len(self.sources))])
        self.add_remote_entry=tk.Entry(self, width=45)
        self.add_remote_entry.grid(row=1, column=0, sticky='ne', padx=(0,10))
        #make a validation of the remote inserted
        self.add_remote_btn = tk.Button(self, text="add remote", command=self.add_domain)
        self.add_remote_btn.grid(row=1, column=1, sticky='nw')


        ################################################
        #LOCAL SECTION
        ##############################################
        
        self.local_section = Labelscrolledtw(self, text='Local Sources', borderwidth=4, width=300, height=200, columns=[("ID", 20, 'center'), ("Path", 300, 'w')])
        self.local_section.grid(padx=10, pady=20, row=2, column=0)
        self.add_local_entry=tk.Entry(self, width=45)
        self.add_local_entry.grid(row=3, column=0, sticky='ne', padx=(0,10))
        #make a validation of the local inserted
        self.add_local_btn = tk.Button(self, text="add local", command=self.add_path)
        self.add_local_btn.grid(row=3, column=1, sticky='nw')


        ################################################
        #ACTIONS SECTION
        ##############################################
        self.actions_section = ttk.Labelframe(self, text='Actions', borderwidth=4, width=200, height=200)
        self.actions_section.grid(row=0, column=1)
        self.play_bttn = tk.Button(self.actions_section, text='play', command=self.install)
        self.play_bttn.pack()
       
    def add_domain(self):
        domain = self.add_remote_entry.get()
        if domain == '':
            return
        self.sources += [(len(self.sources), domain )]
        source = self.sources[-1]
        self.remote_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.remote_section.tw.selection_toggle(str(source[0]))
   
    def add_path(self):
        path = self.add_local_entry.get()
        if path == '':
            return
        self.local_sources += [(len(self.local_sources), path )]
        source = self.local_sources[-1]
        self.local_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.local_section.tw.selection_toggle(str(source[0]))

    def install(self):
        sel=self.remote_section.tw.selection()
        sel2=self.local_section.tw.selection()
        remotes = ",".join([self.remote_section.tw.item(i)['values'][1] for i in sel])
        paths = ",".join([self.local_section.tw.item(i)['values'][1] for i in sel2])
        print (remotes)
        print(paths)
        print([i.strip() for i in remotes.split(',')])
        bg.install.callback(remotes, paths)
        
app = App()
app.mainloop()
