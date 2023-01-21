
#Copyright  (c) 2022 Cid0rz (cid.kampeador@gmail.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import begoneads.begoneads as bg
from pathlib import Path
from begoneads.helpers import is_admin
from begoneads.exceptions import NotElevatedException
import shutil, os, time, sys, datetime


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
        """Delete records previously marked for deletion"""
        marked = self.tw.tag_has('todelete')
        for item in marked:
            self.tw.delete(item)

class BCLabelscrolledtw(Labelscrolledtw):
    """A subclass of the scrolled treeview to manage the backups."""
    def __init__(self, parent, text='BCLabelscrolledtw', borderwidth=4, width=300, height=200,  columns=[("Timestamp", 120, "center"), ("Alias", 120, 'e')], selectmode='none'):
        super().__init__(parent , text=text, borderwidth=borderwidth, width=width, height=height, columns = columns, selectmode=selectmode)
        self.make_backup_btn = tk.Button(self, text="make new backup", width=32, command=self.make_backup)
        self.make_backup_btn.pack()
        self.restore_backup_btn = tk.Button(self, text="restore selected (in green)", width=32, command=self.restore_backup)
        self.restore_backup_btn.pack()
        self.delete_backups_btn = tk.Button(self, text="delete marked (in red)", width=32, command=self.delete_marked)
        self.delete_backups_btn.pack()

        if sys.platform.startswith('win'):
            self.source_path = r'c:\windows\system32\drivers\etc\hosts'
            self.backups_dir = r'c:\windows\system32\drivers\etc\hostsbackup'
        else:
           self.source_path = '/etc/hosts'
           self.backups_dir = "/etc/hostsbackup"
        self.populate_backups()
        

    def check_backups_dir(self):
        """Check for the existence of a backups directory. If it doesnt exist, offer to create it.
        If the folder does not exist and is not created, disable the widget."""
        if not os.path.exists(self.backups_dir):
            result = messagebox.askyesno("Directory Not Found", f"The backups directory doesn't exist. Do you want to create it in {self.backups_dir}?")
        else:
            self.config(text=f"Backups at\n[{self.backups_dir}]")
            return True

        if result:
            os.makedirs(self.backups_dir)
            self.make_backup_btn.config(state='normal')
            self.restore_backup_btn.config(state='normal')
            self.delete_backups_btn.config(state='normal')
            self.config(text=f"Backups at\n[{self.backups_dir}]")
            return True
        else:
            messagebox.showwarning(title="Missing backups directory", message="No backups directory")
            self.config(text=f"Backups\n NOT AVAILABLE")
            self.make_backup_btn.config(state='disabled')
            self.restore_backup_btn.config(state='disabled')
            self.delete_backups_btn.config(state='disabled')
            return False

    def on_click(self, event):
        item = self.tw.identify('item', event.x, event.y)
        if not self.tw.tag_has('todelete', item):
            self.tw.selection_remove(self.tw.selection())
            self.tw.selection_toggle(item)

    def populate_backups(self):
        """Display the information about the backups dir"""
        if not self.check_backups_dir():
            return
        self.tw.delete(*self.tw.get_children())
        for nr, filename in enumerate(os.listdir(self.backups_dir)):
            timestamp = int(filename.split(".")[0])
            dt = datetime.datetime.fromtimestamp(timestamp)
            timestr = dt.strftime('%d/%m/%y-%H:%M:%S')
            alias = filename.split(".")[1]
            self.tw.insert("", index=nr, iid=str(nr) , values=(timestr,alias))
        
    def make_backup(self, alias=None):
        timestamp = int(time.time())
        dt = datetime.datetime.fromtimestamp(timestamp)
        timestr = dt.strftime('%d/%m/%y-%H:%M:%S')
        filename = int(timestamp)
        if not alias:
            alias = simpledialog.askstring(title="Define alias", prompt="Please enter the alias for your backup: ")
        shutil.copy(self.source_path, f"{self.backups_dir}/{filename}.{alias}.bck")
        pos = len(self.tw.get_children())
        self.tw.insert("", index=pos, iid=pos, values=(timestr, alias) )

        
    
    def restore_backup(self):
        item = self.tw.item(self.tw.selection())
        if item['values'] == '':
            messagebox.showinfo(title='Error', message="Please select a backup to restore")
            return
        dt = datetime.datetime.strptime(item['values'][0], '%d/%m/%y-%H:%M:%S')
        filename = int(datetime.datetime.timestamp(dt))
        alias = item['values'][1]
        item_path = Path(self.backups_dir)
        shutil.copy(f"{self.backups_dir}/{filename}.{alias}.bck", self.source_path)
        print(f"{self.backups_dir}/{filename}.{alias}.bck has been restored in hosts")
        
        
    def delete_marked(self):
        """Remove previously selected backups from the view and delete the
        corresponding  backup files."""

        marked = self.tw.tag_has('todelete')
        for item in marked:
            dt = datetime.datetime.strptime(self.tw.item(item)['values'][0], '%d/%m/%y-%H:%M:%S')
            filename = int(datetime.datetime.timestamp(dt))
            alias = self.tw.item(item)['values'][1]
            item_path = Path(self.backups_dir)
            os.remove(item_path / Path(f"{filename}.{alias}.bck") )
            self.tw.delete(item)
        self.populate_backups()
            
            

class App (tk.Tk):
    """Begoneads GUI in tkinter, some widgets tied together that invoke the
    begoneads functions. and extend its functionality"""
    
    def __init__(self):
        super().__init__()
        self.title("Begoneads GUI")
        self.geometry("650x750")
        if not is_admin(sys.platform.startswith('win')):
            messagebox.showinfo(title="Needs to run as admin", message='This program needs to be run as root to work properly')
            raise NotElevatedException('This program needs to be run as root to work properly')
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
        self.actions_section.grid(row=0, column=1)
        self.play_bttn = tk.Button(self.actions_section, text='Play', command=self.install, width=8)
        self.play_bttn.pack(padx=5, pady=2)
        self.pause_bttn = tk.Button(self.actions_section, text='Pause', command=self.pause, width=8)
        self.pause_bttn.pack(padx=5,pady=2)
        self.stop_bttn = tk.Button(self.actions_section, text='Stop', command=self.stop, width=8)
        self.stop_bttn.pack(padx=5,pady=2)
        self.check_button = tk.Button(self.actions_section, text='Check', command=self.check, width=8)
        self.check_button.pack(padx=5, pady=2)

        self.default_remotes_btn = tk.Button(self.actions_section, text="Default remotes", width=12, command=self.default_remotes)
        self.default_remotes_btn.pack(anchor='e')
        self.clear_local_btn = tk.Button(self.actions_section, text="Clear paths", command=self.clear_paths, width=12)
        self.clear_local_btn.pack(anchor='e')

        ################################################
        #BACKUPS SECTION
        ##############################################

        self.backups_section = BCLabelscrolledtw(self, text='Backups')
        self.backups_section.grid(row=1, column=1, rowspan=4, sticky='e')
        

        
    def default_remotes(self):
        """Get the default remotes from begoneads configuration."""
        for element in self.remote_section.tw.get_children():
            self.remote_section.tw.delete(element)
        self.sources = list(enumerate(bg.sources))
        for source in self.sources:
            self.remote_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.remote_section.tw.selection_add([str(i) for i in range(len(self.sources))])
            
    def clear_paths(self):
        """Remove all the paths from the local section"""
        for element in self.local_section.tw.get_children():
            self.local_section.tw.delete(element)

    def add_domain(self):
        """Add an url to retrieve a hosts file from, it has to be a properly formated file."""
        domain = self.add_remote_entry.get()
        if domain == '':
            return
        self.sources += [(len(self.sources), domain )]
        source = self.sources[-1]
        self.remote_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.remote_section.tw.selection_toggle(str(source[0]))
   
    def add_path(self):
        """Add a path as a local hosts file source."""
        path = self.add_local_entry.get()
        if path == '':
            return
        self.local_sources += [(len(self.local_sources), path )]
        source = self.local_sources[-1]
        self.local_section.tw.insert(parent='', index=source[0], iid=str(source[0]), values=source )
        self.local_section.tw.selection_toggle(str(source[0]))

    def install(self):
        """Call beagoneads install with the currrently selected local and remote sources."""
        sel=self.remote_section.tw.selection()
        sel2=self.local_section.tw.selection()
        remotes = ",".join([self.remote_section.tw.item(i)['values'][1] for i in sel])
        paths = ",".join([self.local_section.tw.item(i)['values'][1] for i in sel2])
        #print (remotes)
        #print(paths)
        #print([i.strip() for i in remotes.split(',')])
        bg.install.callback(remotes, paths)
    def pause(self):
        """Create a backup and uninstall begoneads from the hosts file."""
        self.backups_section.make_backup(alias="Backup")
        messagebox.showinfo(title="Info", message="Backup created, when you want to resume, restore it.")
        print("Backup created, when you want to resume, restore it.")
        self.stop()
    def stop(self):
        """Call Uninstall begoneads."""
        bg.uninstall.callback()
    def check(self):
        """Check if begoneads is installed in the system."""
        chk = bg.check.callback()
        if chk:
            messagebox.showinfo(title='Check', message="Begoneads IS installed")
        else:
            messagebox.showinfo(title='Check', message="Begoneads NOT installed")


        


#if __name__ == __main__:        
app = App()
app.mainloop()
