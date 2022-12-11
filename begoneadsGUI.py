
#(c) 2022 Cid0rz (cid.kampeador@gmail.com)

import tkinter as tk
from tkinter import ttk
import begoneads.begoneads as bg
from pathlib import Path
from begoneads.helpers import is_admin
from begoneads.exceptions import NotElevatedException
import shutil, os, time, sys


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

    def delete_marked(self):
        marked = self.tw.tag_has('todelete')
        print('deleting...', marked)
        for item in marked:
            self.tw.delete(item)

class BCLabelscrolledtw(Labelscrolledtw):
    def __init__(self, parent, text='BCLabelscrolledtw', borderwidth=4, width=300, height=200, columns = [("ID", 20, 'center')], selectmode='none'):
        super().__init__(parent , text=text, borderwidth=borderwidth, width=width, height=height, columns = columns, selectmode=selectmode)
        self.make_backup_btn = tk.Button(self, text="make backup", width=12, command=self.make_backup)
        self.make_backup_btn.pack()
        self.restore_backup_btn = tk.Button(self, text="restore selected", width=12, command=self.restore_backup)
        self.restore_backup_btn.pack()
        self.delete_backups_btn = tk.Button(self, text="delete marked", width=12, command=self.delete_marked)
        self.delete_backups_btn.pack()

    def on_click(self, event):
        item = self.tw.identify('item', event.x, event.y)
        if not self.tw.tag_has('todelete', item):
            self.tw.selection_remove()
            self.tw.selection_toggle(item)
            
    def make_backup(self):

        if sys.platform.startswith('win'):
            source_path = r'c:\windows\system32\drivers\etc\hosts'
            backup_dir = r'c:\windows\system32\drivers\etc\hostsbackup'
        else:
           source_path = '/etc/hosts'
           backup_dir = "/etc/hostsbackup"

        filename = time.time()
        os.makedirs(backup_dir)
        #shutil.copy(source_path, f"{backup_dir}/{filename}")
        self.tw.insert()

        
    
    def restore_backup(self):
        pass
    
            

class App (tk.Tk):
    """Begoneads GUI in tkinter, some widgets tied together that invoke the begoneads functions. and extend its functionality"""
    
    def __init__(self):
        #if not is_admin(sys.platform.startswith('win')):
        #    raise NotElevatedException(
        #    'This program needs to be run as root to work properly')
        super().__init__()
        self.title("Begoneads GUI")
        self.geometry("650x750")
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
        self.remote_btns = tk.Frame(self)
        self.remote_btns.grid(row=2, column=0)
        self.add_remote_btn = tk.Button(self.remote_btns, text="Add remote", command=self.add_domain, width=10, height=2)
        self.add_remote_btn.grid(row=0, column=0, sticky='w', pady=10)
        self.remove_remotes_btn = tk.Button(self.remote_btns, text="Remove marked remotes\n(in red) ", command=self.remote_section.delete_marked)
        self.remove_remotes_btn.grid(row=0, column=1, sticky='w', pady=10)


        ################################################
        #LOCAL SECTION
        ##############################################
        
        self.local_section = Labelscrolledtw(self, text='Local Sources', borderwidth=4, width=300, height=200, columns=[("ID", 20, 'center'), ("Path", 300, 'w')])
        self.local_section.grid(padx=10, pady=20, row=3, column=0)
        self.add_local_entry=tk.Entry(self, width=45)
        self.add_local_entry.grid(row=4, column=0, sticky='ne', padx=10)
        #make a validation of the local inserted
        self.local_btns = tk.Frame(self)
        self.local_btns.grid(row=5, column=0)
        self.add_local_btn = tk.Button(self.local_btns, text="Add local", command=self.add_path, width=10, height=2 )
        self.add_local_btn.grid(row=0, column=0, sticky='w', pady=10)
        self.remove_local_btn = tk.Button(self.local_btns, text="Remove marked paths\n(in red) ", command=self.local_section.delete_marked)
        self.remove_local_btn.grid(row=0, column=1, sticky='w', pady=10)

        ################################################
        #ACTIONS SECTION
        ##############################################
        self.actions_section = ttk.Labelframe(self, text='Actions', borderwidth=4, width=200, height=200)
        self.actions_section.pack_propagate(False)
        self.actions_section.grid(row=0, column=1)
        self.play_bttn = tk.Button(self.actions_section, text='Play', command=self.install, width=8)
        self.play_bttn.pack(anchor='w', padx=5, pady=2)
        self.pause_bttn = tk.Button(self.actions_section, text='Pause', command=self.pause, width=8)
        self.pause_bttn.pack(anchor='w', padx=5, pady=2)
        self.stop_bttn = tk.Button(self.actions_section, text='Stop', command=self.stop, width=8)
        self.stop_bttn.pack(anchor='w', padx=5, pady=2)

        self.default_remotes_btn = tk.Button(self.actions_section, text="Default remotes", width=12, command=self.default_remotes)
        self.default_remotes_btn.pack(anchor='e')
        self.clear_local_btn = tk.Button(self.actions_section, text="Clear paths", command=self.clear_paths, width=12)
        self.clear_local_btn.pack(anchor='e')

        ################################################
        #BACKUPS SECTION
        ##############################################

        self.backups_section = BCLabelscrolledtw(self, text='Backups', columns=[("ID", 20, "center"), ("Timestamp", 120, "center"), ("Alias", 120, 'e')])
        self.backups_section.grid(row=1, column=1, rowspan=4, sticky='e')

        if sys.platform.startswith('win'):
            backup_dir = r'c:\windows\system32\drivers\etc\hostsbackup'
        else:
           backup_dir = "/etc/hostsbackup"

        if not os.path.isdir(backup_dir):
            os.makedirs(backup_dir)

        for filename in os.listdir(backup_dir):
            self.backups_section.tw.insert("",filename, filename,  )
        
        
    def default_remotes(self):
        for element in self.remote_section.tw.get_children():
            self.remote_section.tw.delete(element)
        self.sources = list(enumerate(bg.sources))
        for source in self.sources:
            self.remote_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.remote_section.tw.selection_add([str(i) for i in range(len(self.sources))])
            
    def clear_paths(self):
        for element in self.local_section.tw.get_children():
            self.local_section.tw.delete(element)

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
    def pause(self):
        pass
    def stop(self):
        bg.uninstall.callback()


        


#if __name__ == __main__:        
app = App()
app.mainloop()
