# långsammare
# flerspecifika
# replay
# minnesceller
# []\
#   []-[]
# []/
# /files\/load\/graphics\/save options\

try:
    from Tkinter import *
    from Tkinter import font as tkFont
    #from Tinter.ttk import Frame, Button, Styl
    from Tkinter.colorchooser import *
except:
    #import tkinter as tkint
    from tkinter import *
    from tkinter import font as tkFont
    from tkinter.colorchooser import *
    #from tkinter.ttk import Frame, Button, Style
import math
import time
import copy
import pickle
import datetime
import os
import sys
from PIL import Image, ImageTk, ImageDraw
from inspect import getframeinfo, stack

def Scroll(event):
    if event.num == 4 or event.delta == 120:
        cam.move(z = cam.z * 1.1, speed = .5)
    elif event.num == 5 or event.delta == -120:
        cam.move(z = cam.z / 1.1, speed = .5)
    zoom.set(cam.z)

class files:
    '''A collection of file-related functions'''
    def __init__(self, prefix, parent = None):
        self.prefix = ''
        if not parent is None: self.prefix = parent.prefix
        self.prefix += prefix

    def __delitem__(self, file):
        os.remove(self.prefix + file)
    
    def create(self, file):
        try:
            open(self.prefix + file, 'w+')
        except:
            if not os.path.exists(os.path.dirname(self.prefix + file)):
                os.makedirs(os.path.dirname(self.prefix + file))
    
    def fetch(self, file):
        with open(self.path(file), 'rb') as file_:
            return pickle.load(file_)

    def __setitem__(self, file, data):
        with open(self.path(file), 'wb') as file_:
            pickle.dump(data, file_)

    def __getitem__(self, file):
        return self.fetch(file)

    def path(self, file):
        return self.prefix + file
'''except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise'''

class myrandom:
    '''my own little random class'''
    m = 982451653
    def __init__(self, seed = 0):
        self.seed = seed
        self.n = seed
    def getrand(self):
        self.n = (756062753 * self.n + 314605069) % myrandom.m
        return self.n / myrandom.m
    randfloat = lambda self, x, x2: x + ((self.getrand()) * (x2 - x))
    if 0:
        randint = lambda self, x, x2: x + int(self.getrand() / (1 / (x2 - x)))
    else:
        randint = lambda self, x, x2: round(self.randfloat(x - .5, x2 + .5))
    choice = lambda self, array: array[self.randint(0, len(array) - 1)]
rpick = lambda st, nd: rnd.randint(st, nd) # bör tas bort
rchance = lambda nd, comp = 1: nd > (rnd.randfloat(0, comp))
ispos = lambda val: ((val > 0) * 1) + ((val < 0) * -1)

def cap(val, Max = None, Min = None): # bör byggas om
    Min = val if Min is None else Min
    Max = val if Max is None else Max 
    #Min, Max = (not Min) or val, Max or val
    return Max * (val > Max) + (val < Min) * Min + val * int(not((val < Min) or (val > Max)))

rpos = lambda: (rnd.randint(0, 1) - .5) * 2
rpower = lambda: rnd.randfloat(-1, 1)

#print(dir(list))
if 0:
    def compr(val, a, b):
        return (val > a / 2) * a + (val < b / 2) * b
else:
    compr = lambda ef, a, b: cap(((1 / (1 + (math.e**(-(abs(ef) - .5) * (260 / 10)))))) * ispos(ef), a, b)
rnd = myrandom(0)

'''filename = '/data/index.txt'
if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))
filename = '/data/seeds/index.txt'
if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))'''

####################################################################################################################################################################

class pal:
    
    def __init__(self, colors = tuple()):
        self.all = {}
        self.switches = {}
        self.extend(colors)
        
    def __getitem__(self, key):
        return self.all[key].color

    def __setitem__(self, key, data, first = set()):
        self.all[key].color = data
        first.add(self)
        for ab in self.all[key].bound:
            if not ab in first: ab.__setitem__(data, first = self)

    def __delitem__(self, key):
        for slot in self.all[key].slots:
            del slot[key]

    def extend(self, colors):
        for color in colors:
             palcolor(self, color, colors[color])

    def __len__(self):
        return len(self.all)

    def __iter__(self):
        self.n = -1
        self.end = len(self.all) - 1
        self.keys = tuple(self.all.keys())
        return self

    def __next__(self):  
        if self.n == self.end:
            raise StopIteration 
        else: 
            self.n += 1
            return self.keys[self.n]

    def keys(self):
        return self.all.keys()

    def get(self):
        return self.all

class palswitch(pal):

    def __init__(self, parent, tag = 'e'):
        self.white = []
        self.black = []
        self.all = {}
        parent.switches[tag] = self

    def switch(self):
        for ab in range(len(self.white)):
            white = self.white[ab]
            black = self.black[ab]
            white.color, black.color = \
                         black.color, white.color
            vitcopy = copy.copy(white.bound)
            for cd in black.bound:
                black.unbind(cd)
                white.bind(cd)
            for cd in vitcopy:
                white.unbind(cd)
                black.bind(cd)
        
class palcolor(pal):
    
    def __init__(self, parent, tag, hexval, bound = None):
        parent.all[tag] = self
        self.bound = []
        if not (bound is None): self.bind(bound)
        else: self.color = hexval

    def bind(self, other, n = True):
        self.bound.append(other)
        if n:
            other.bind(self, n = False)
            self.color = other.color

    def unbind(self, other = 'All', n = True):
        if other == 'All':
            for ab in self.bound:
                ab.unbind(self)
        else:
            self.bound.remove(other)
            if n: other.unbind(self, n = False)

    def __setitem__(self, data, first = set()):
        self.color = data
        first.add(self)
        for ab in self.bound:
            if not ab in first: first = ab.__setitem__(data, first = first)
        return first
    

# ------------ MAIN MENU -----------

class menumaster:
    def __init__(self):
        self.tabs = {}

# ------------- BLANK --------------
        
class blanktab(Label):
    
    def __init__(self, Menu, Tag, master = None, cnf = {}, **kw):
        super().__init__(master, cnf, **kw)
        self.Menu_ = Menu
        Menu.tabs[Tag] = self

    def hovering(self, event):
        event.widget.configure(bg = palette['white'], fg = palette['dark'])

    def nolongerhover(self, event):
        event.widget.configure(bg = palette['darkblue'], fg = palette['white'])

    def deselect(self):
        self.configure(bg = palette['darkblue'], font = ('ARIAL', 10), relief = FLAT, borderwidth = 2)
        self.hover = self.bind('<Enter>', self.hovering)
        self.nohover = self.bind('<Leave>', self.nolongerhover)
        try: self.tabframe.destroy()
        except: pass

    def alert(self, text, command = None):
        global saveruta
        txtbg = palette['darkgrey']
        txtfg = palette['white']
        thisalerttk = Toplevel(saveruta, bg = txtbg)
        thisalerttk.attributes('-topmost', True)
        thisalerttk.option_add('*Button.width', 10)
        thisalert = Frame(thisalerttk, bd = 5, bg = txtbg)
        thisalert.grid()
        text = text.split('\n')
        longest = len(max(text, key = lambda elem: len(elem)))
        for row, string in enumerate(text):
            Label(thisalert, text = string, bg = txtbg, fg = txtfg, \
                  font = ('Arial', 13 + (row == 0) * 5), width = None).grid(row = row)
        ok = Button(thisalert, text = 'OK', command = command, bg = palette['red'], \
                    relief = FLAT, fg = txtfg)
        ok.grid(row = len(text), column = 0, sticky = W)
        ok.bind('<Enter>', lambda event: event.widget.configure(background = palette['grey']))
        ok.bind('<Leave>', lambda event: event.widget.configure(background = palette['red']))
        cancel = Button(thisalert, text = 'CANCEL', command = thisalerttk.destroy, bg = palette['darkgreen'], \
               relief = FLAT, activebackground = palette['white'], fg = txtfg)
        cancel.grid(row = len(text), column = 0, sticky = E)
        cancel.bind('<Enter>', lambda event: event.widget.configure(background = palette['grey']))
        cancel.bind('<Leave>', lambda event: event.widget.configure(background = palette['darkgreen']))

    def select(self, event = False):
        if event: widget = event.widget
        global selectedtab, saveruta
        st = selectedtab
        st.deselect()
        st = selectedtab = self
        st.unbind('<Enter>', st.hover)
        st.unbind('<Leave>', st.nohover)
        st.configure(font = ('Arial', 12, 'bold'), bg = palette['blue'], relief = FLAT, borderwidth = 2, fg = palette['white'])
        self.tabframe = LabelFrame(saveruta, relief = FLAT, bg = palette['blue'], \
                                   fg = palette['white'], width = 385, height = 246)
        self.tabframe.grid(row = 1, column = 0, columnspan = 10)
        self.tabframe.grid_propagate(False)
        
        txtcol = palette['orange']
        
        self.tabframe.option_add('*Label.anchor', W)
        self.tabframe.option_add('*Label.foreground', palette['dark'])
        self.tabframe.option_add('*Label.background', palette['blue'])
        self.tabframe.option_add('*Entry.background', palette['dark'])
        self.tabframe.option_add('*Entry.foreground', txtcol)
        self.tabframe.option_add('*Entry.width', '20')
        self.tabframe.option_add('*Frame.background', palette['blue'])
        self.tabframe.option_add('*Labelframe.foreground', palette['white'])
        self.tabframe.option_add('*Labelframe.background', palette['blue'])
        #self.tabframe.option_add('*Labelframe.relief', RIDGE)
        self.tabframe.option_add('*Entry.insertbackground', palette['green'])
        self.tabframe.option_add('*Entry.font', ('Arial', 10, 'bold'))
        #self.tabframe.option_add('*Label.font', ('Arial', 10, 'bold'))
        self.labelcnf = {'width': 10}
        self.entrycnf = {'bd': 1, 'relief': SUNKEN, 'background': palette['dark'], \
                         'foreground': txtcol}
        self.listcnf = {'bg': palette['dark'], 'fg': palette['orange'], 'width': 19, \
                        'height': 13, 'selectforeground': palette['dark'], 'selectbackground': \
                        palette['green']}
        self.entryfont = ('Arial', 10, 'bold')

# ------------- FILES --------------

class filetab(blanktab):

    def update_index(self):
        filemaster['index.txt'] = saved_seeds
        
    def startnewseed(self):
        #show warning if current seed is not saved
        tag = self.seedsorder[self.changenameentry.ind]
        obj = saved_seeds[tag]
        self.Menu_.tabs['Load'].select(seedobj = tag)
        if not obj['file'] is None:
            runobj.initialise(seed = int(obj['seed']))
        else:
            file = filemaster[obj['file']]
            runobj.initialise(seed = int(obj['seed']), graph = obj['averages'], random = obj['random'], \
                              state = 'initialize', startgen = obj['gens'])
        self.update_index()

    def sorttime(self, elem):
        return saved_seeds[elem]['lastused']

    def updatelistbuttons(self, state):
        self.deleteseed.configure(state = state)
        self.changenameentry.delete(0, END)
        self.changenameentry.configure(state = state)
        self.changenamelabel.configure(state = state)
        self.changeseedentry.configure(state = state, text = '', bg = palette['dark' if state is NORMAL else 'darkblue'])
        self.changeseedlabel.configure(state = state)
        self.dateentry.configure(state = state, text = '', bg = palette['dark' if state is NORMAL else 'darkblue'])
        self.datelabel.configure(state = state)
        self.startbutton.configure(state = state)

    def updatename(self, event):
        global saved_seeds
        getval = event.widget.get()
        saved_seeds[getval] = saved_seeds.pop(event.widget.key)
        event.widget.key = event.widget.get()
        self.seedlist.delete(event.widget.ind)
        ab = getval
        self.seedlist.insert(event.widget.ind, str(ab))

    def removeseed(self): #Del
        global saved_seeds
        self.updatelistbuttons(DISABLED)
        name = self.seedsorder[self.seedlist.curselection()[0]]
        saved_seeds.pop(self.seedsorder[self.seedlist.curselection()[0]])
        del self.seedsorder[self.seedlist.curselection()[0]]
        self.seedlist.delete(ACTIVE)
        del seedfiles[name + '.txt']
        print(saved_seeds)
        self.update_index()

    def choosenseed(self, event):
        if 1:#try:
            self.updatelistbuttons(NORMAL)
            self.changenameentry.key = self.seedsorder[self.seedlist.curselection()[0]]
            self.changenameentry.ind = self.seedlist.index(self.seedlist.curselection()[0])
            self.changenameentry.insert(END, self.seedsorder[self.changenameentry.ind])
            self.changeseedentry.config(text = saved_seeds[self.seedsorder[self.changenameentry.ind]]['seed'])
            self.dateentry.config(text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(saved_seeds[self.seedsorder[self.changenameentry.ind]]['lastused'])))
            self.changenameentry.bind('<KeyRelease>', self.updatename)
        #except: self.updatelistbuttons(DISABLED)
    
    def savefileseed(self): # save new seed
        global saved_seeds
        seed = self.seedentry.get()
        name = str(self.nameentry.get())
        self.deleteseed.configure(state = DISABLED)
        if seed.isdigit() and (not name in self.seedsorder):
            if int(seed) == runobj.seed:
                saved_seeds[name] = {'seed': seed, 'lastused': time.time(), 'name': name, \
                                     'gens': gen, 'file': 'seeds/' + name + '.txt'}
                datafiles.create(saved_seeds[name]['file'])
                datafiles[saved_seeds[name]['file']] = {'genpool': runobj.genpool, \
                                     'averages': averages, 'random': runobj.rndstateinit}
            else:
                saved_seeds[name] = {'seed': seed, 'lastused': time.time(), 'name': name, \
                                     'gens': 0, 'file': None}
            filemaster['index.txt'] = saved_seeds
            self.seedsorder = list(reversed(sorted(saved_seeds.keys(), key = self.sorttime)))
            self.seedentry.delete(0, END)
            self.nameentry.delete(0, END)
            self.seedlist.delete(0, END)
            pickle.dump(saved_seeds, open('saved_seeds.txt', 'wb'))
            for ab in self.seedsorder:
                self.seedlist.insert(END, str(ab))
        elif not seed.isdigit():
            self.seedentry.delete()
            self.errorlabel.config(text = 'Seed has to be a number')
        else:
            self.nameentry.delete(0, END)
            self.errorlabel.config(text = 'Name is already in use')

    def select(self, event = False): # create tab
        #sätta till fler defaults
        super().select(event)
        self.saveseedframe = LabelFrame(self.tabframe, text = 'Save new seed')
        self.saveseedframe.grid(row = 0, column = 0, sticky = E + W + N + S)
        self.saveframe = Frame(self.saveseedframe)
        self.saveframe.grid(row = 0, column = 0, columnspan = 1)
        
        self.seedlabel = Label(self.saveframe, text = 'Seed', cnf = self.labelcnf)
        self.seedlabel.grid(row = 0, column = 0, sticky = W)
        self.seedentry = Entry(self.saveframe, insertbackground = palette['green'], \
                               font = self.entryfont)
        self.seedentry.insert(END, rnd.seed)
        self.seedentry.grid(row = 0, column = 1, sticky = W + E)
        
        namelabel = Label(self.saveframe, text = 'Name', cnf = self.labelcnf)
        namelabel.grid(row = 1, column = 0, sticky = W)
        self.nameentry = Entry(self.saveframe, insertbackground = palette['green'], font = self.entryfont)
        self.nameentry.grid(row = 1, column = 1)
        
        self.errorlabel = Label(self.saveseedframe, fg = palette['white'], anchor = E, width = 20)
        self.errorlabel.grid(row = 3, column = 0, sticky = E)
        save = Button(self.saveseedframe, text = 'Save', command = self.savefileseed)
        save.grid(row = 4, column = 0, sticky = E + W)

        # ---- Savedseedslist ----

        self.savedlistframe = LabelFrame(self.tabframe, text = 'Seeds')
        self.savedlistframe.grid(row = 0, column = 1, rowspan = 4, sticky = S + N)
        self.filescrolly = Scrollbar(self.savedlistframe)
        self.seedlist = Listbox(self.savedlistframe, yscrollcommand = self.filescrolly.set, \
                                font = self.entryfont, cnf = self.listcnf)
        self.seedsorder = list(reversed(sorted(saved_seeds.keys(), key = self.sorttime)))
        for ab in self.seedsorder:
            self.seedlist.insert(END, str(ab))
        self.filescrolly.config(command = self.seedlist.yview)
        self.filescrolly.grid(row = 0, column = 1, sticky = S + N)
        self.seedlist.bind('<<ListboxSelect>>', self.choosenseed)
        self.seedlist.grid(row = 0, column = 0)

        # ----- Renameframe -----

        self.renameframe = LabelFrame(self.tabframe, text = 'Data')
        self.renameframe.grid(row = 1, column = 0, sticky = N + E + W)
        self.changenamelabel = Label(self.renameframe, text = 'Rename', cnf = self.labelcnf, \
                                     state = DISABLED, disabledforeground = palette['darkblue'])
        self.changenamelabel.grid(row = 0, column = 0, sticky = W)
        self.changenameentry = Entry(self.renameframe, state = DISABLED, \
                                     disabledbackground = palette['darkblue'])
        self.changenameentry.grid(row = 0, column = 1, sticky = E)
        self.changeseedlabel = Label(self.renameframe, text = 'Seed', cnf = self.labelcnf, \
                                     state = DISABLED, disabledforeground = palette['darkblue'])
        self.changeseedlabel.grid(row = 1, column = 0, sticky = W)
        self.changeseedentry = Label(self.renameframe, bg = palette['darkblue'], \
                                     state = DISABLED, cnf = self.entrycnf, font = self.entryfont)
        self.changeseedentry.grid(row = 1, column = 1, sticky = W + E)
        self.datelabel = Label(self.renameframe, cnf = self.labelcnf, text = 'Last used', \
                               state = DISABLED, disabledforeground = palette['darkblue'])
        self.datelabel.grid(row = 2, column = 0, sticky = W)
        self.dateentry = Label(self.renameframe, bg = palette['darkblue'], \
                               cnf = self.entrycnf, font = self.entryfont)
        self.dateentry.grid(row = 2, column = 1, sticky = W + E)
        self.startbutton = Button(self.renameframe, text = 'Load', command = self.startnewseed, state = DISABLED)
        self.startbutton.grid(column = 0, columnspan = 2, sticky = E + W)

        # ----- Deletebutton ----

        self.deleteseed = Button(self.tabframe, text = 'Delete', command = lambda: self.alert(text = 'This act is not reversable\n Are you sure?', command = self.removeseed), state = DISABLED)
        self.deleteseed.grid(row = 2, column = 0, sticky = W + E)
        
# ------------ LOADFILE ------------

class loadtab(blanktab):

    def select(self, event = False, seedobj = None):
        super().select(event)
        if seedobj is None: self.data = {'Seed': '', 'Name': '', 'Date': '', \
                                         'Gen': 0, 'File': None}
        else: self.data = {'Seed': saved_seeds[seedobj]['seed'], 'Name': seedobj, \
                           'Date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(saved_seeds[seedobj]['lastused'])),
                           'Gen': saved_seeds[seedobj]['gens'], 'File': saved_seeds[seedobj]['file']}

        self.tabframe.option_add('*Label.width', 10)
        self.dataframe = LabelFrame(self.tabframe, text = 'Data')
        self.dataframe.grid(sticky = N)
        
        Label(self.dataframe, text = 'Seed').grid(row = 0, column = 0, sticky = W)
        self.seedentry = Entry(self.dataframe, cnf = self.entrycnf)
        self.seedentry.grid(row = 0, column = 1)
        Label(self.dataframe, text = 'Name').grid(row = 1, column = 0, sticky = W)
        self.nameentry = Entry(self.dataframe, cnf = self.entrycnf)
        self.nameentry.grid(row = 1, column = 1)
        Label(self.dataframe, text = 'Last used').grid(row = 2, column = 0, sticky = W)
        self.dateentry = Label(self.dataframe, cnf = self.entrycnf, text = self.data['Date'])
        self.dateentry.grid(row = 2, column = 1, sticky = E + W)
        Label(self.dataframe, text = 'Generations').grid(row = 3, column = 0, sticky = W)
        self.genentry = Label(self.dataframe, cnf = self.entrycnf, text = self.data['Gen'])
        self.genentry.grid(row = 3, column = 1, sticky = E + W)

        self.seedentry.insert(0, self.data['Seed'])
        self.nameentry.insert(0, self.data['Name'])

        # ----- Loadoptions -----
        
        self.startoptframe = LabelFrame(self.tabframe, text = 'Loadsettings')
        self.startoptframe.grid(row = 0, column = 1)

        Label(self.startoptframe, text = 'Start at gen').grid()
        self.startatgenlist = Listbox(self.startoptframe, cnf = self.listcnf, \
                                      font = self.entryfont, height = 2)
        self.startatgenlist.grid(row = 1, column = 0)
        self.startatgenlist.insert(END, 0)
        if self.data['Gen'] != 0: self.startatgenlist.insert(END, self.data['Gen'])

class savedfiles(blanktab):

    def selectfile(self):
        pass

    def select(self, event = False):
        super().select(event)

# -------- Optionmenutabsinit --------

def savecommand():
    try:
        global saveruta
        Label(saveruta)
    except:
        saveruta = Toplevel(background = palette['darkblue'])
        saveruta.resizable(height = 0, width = 0)
        saveruta.attributes('-topmost', True)
        tab = StringVar()
        tab.set('Save')
        Main_Menu = menumaster()
        
        filemenubuttons = []
        classes = (filetab, loadtab, blanktab)
        for ab, cd in enumerate(('Files', 'Load', 'Gamerules')):
            filemenubuttons.append(classes[ab](Main_Menu, cd, saveruta, text = cd, relief = FLAT, bg = palette['darkblue'], \
                                         fg = palette['white'], anchor = N))
            this = filemenubuttons[-1]
            this.grid(row = 0, column = ab, sticky = S + E + W, padx = (int(ab == 0) * 10, 0))
            this.hover = this.bind('<Enter>', this.hovering)
            this.nohover = this.bind('<Leave>', this.nolongerhover)
            this.bind('<Button-1>', this.select)
        global selectedtab, tabframe
        tabframe = LabelFrame(saveruta, relief = FLAT)
        tabframe.grid(row = 1, column = 0, columnspan = 10)
        selectedtab = filemenubuttons[0]
        selectedtab.select()

def restart():
    try:
        global ruta
        Label(ruta)
        #Label(ruta)
    except:

        def pickseed():
            global ruta

            def newseed():
                initialize(int(choose_preset.ACTIVE))
                ruta.destroy()
                loop()

            def setseed(event):
                print(choose_preset.get(ACTIVE))
                choose.set(choose_preset.get(ACTIVE))
                chosenseed.update()

            ruta.destroy()
            ruta = Toplevel()
            ruta.attributes('-topmost', True)
            ruta.resizable(height = 0, width = 0)
            preset = LabelFrame(ruta, text = 'Preset', borderwidth = 2)
            preset.grid(row = 0, sticky = N)
            seed_frame = LabelFrame(ruta, text = 'Seed')
            seed_frame.grid(row = 0, column = 1, sticky = N)
            choose = StringVar()
            chosenseed = Entry(seed_frame, textvariable = choose)
            chosenseed.insert(0, 0)
            chosenseed.grid(sticky = N + S)
            done = Button(ruta, text = "Done", command = newseed)
            done.grid(row = 1, column = 1, sticky = E, pady = 0)
            choose_preset_scrollbar = Scrollbar(preset)
            choose_preset = Listbox(preset, yscrollcommand = choose_preset_scrollbar.set)
            choose_preset.insert(END, 'Random')
            for ab, cd in saved_seeds.items():
                choose_preset.insert(END, ab)
            choose_preset.insert(END, 'New')
            choose_preset_scrollbar.config(command = choose_preset.yview)
            choose_preset.grid(row = 1, column = 1, sticky = W)
            choose_preset_scrollbar.grid(row = 1, column = 2, sticky = S + N)
            a, b = ruta.grid_size()
            for ab in range(b):
                ruta.grid_rowconfigure(ab, minsize = 20)
            choose_preset.bind('<Button-1>', setseed)
            ruta.resizable(0, 0)

        ruta = Toplevel()
        ruta.attributes('-topmost', True)
        ruta.resizable(height = 0, width = 0)
        newseedalert = Label(ruta, text = 'This will restart your\nprogress with a new seed,\n\nIs that what you want to do?',\
                             fg = '#000022')
        newseedalert.grid(row = 0)
        yeah = Button(ruta, text = 'yes', command = pickseed, bg = palette['green'])
        yeah.grid(row = 1, sticky = E)
#rply = Button(replay, text="REPLAY", command=callback)
#rply.pack()
'''frame = Frame(tk, relief=RAISED, borderwidth=1)
frame.grid()#pack(fill=BOTH, expand=True)'''
####################################################################################################

class Game:
    # ska byggas om

    def __init__(self, z = 100, NNwidth = 13, NNheight = 9):
        global backgcolor
        self.NNwidth = NNwidth
        self.NNheight = NNheight
        self.z = z
        self.input = []
        self.level = 0
        self.blocks = {}
        self.taken = set()
        self.layers = [(0, .5, 0), (.35, .35, 1), (.8, .1, 0)]
        self.colors = {1: ((palette, 'grey'),(palette, 'lightgrey'), 3), \
                       -1: ((palette, 'red'), (palette, 'lightred'), 3), \
                       -2: ((palette, 'orange'), (palettetheme, 'bg'), 2), \
                       -3: ((palette, 'purple'), (palette, 'pink'), 3), \
                       2: ((palette, 'darkblue'), (palette, 'blue'), 3), \
                       3: ((palette, 'darkgreen'), (palette, 'green'), 3)}
        self.chains = [] # set()
        self.chunks = {}
        self.clumping = {-2: 0, 2: 1, 3: 1, -3: 1, -1: -1, 1: 1}

    def getblockat(self,x,y):
        return self.blocks[(x, y)]

    def run(self):
        arti.currentlyusedneurons = set()
        arti.currentlyusedneurons.add(runobj.inputs['bias'])
        runobj.inputs['bias'].set(1)
        roundx = round(cap(spelare.x // 800 - 1.375, Min = 0)) # -1 0?
        checkedrows = set()
        for chunkHash in range(round(roundx), round(roundx + 2.625)):
            chunk = self.chunks[chunkHash]
            chunkrows = chunk['rows']
            for chain in chunkrows:
                typ = chain.type
                xz = len(chain.blocks)
                x = chain.blocks[0].x + xz / 2 - spelare.x / self.z
                y = chain.blocks[0].y - spelare.y / self.z
                yz = 1
                if Collider.col(x, y, xz, yz, 0, 0, self.NNwidth - 1, self.NNheight - 1) and not chain in checkedrows:
                    x = round(-x + self.NNwidth / 2)
                    y = round(y + (self.NNheight - 1) / 2)
                    leftmost, rightmost = int(x - xz / 2), int(x + xz / 2)
                    leftmost = cap(leftmost, Min = 0)
                    rightmost = cap(rightmost, Max = self.NNwidth)
                    for bx in range(leftmost, rightmost):
                        runobj.inputs[(bx, y)].set(self.clumping[typ])
                        arti.currentlyusedneurons.add(runobj.inputs[(bx, y)])
                checkedrows.add(chain)
                arti.currentlyusedneurons.add(runobj.inputs['bias'])
            roundx += 1

    def addground(self, x, y,val):
        self.taken.add((x, y))
        self.blocks[(x, y)] = Block(x, y, val, self)

    def checkvis(self, x, y, zx, zy, replacer):
        if col.col(x, y, zx, zy, spelare.x, spelare.y, (self.NNwidth - 1) * self.z, (self.NNheight - 1) * self.z):
            x = cap(int((-(x - spelare.x) / self.z + self.NNwidth / 2)), self.NNwidth - 1, 0)
            y = int((y - spelare.y) / self.z + self.NNheight / 2)
            runobj.inputs[(x, y)].charge = replacer
            for link in runobj.inputs[(x, y)].outg: link.lastused = arti.tick
            arti.currentlyusedneurons.add(runobj.inputs[(x, y)])
            #arti.currentlyusedneurons.add(arti.neurons[('input', 'field', x, y)])

    def checkifground(self, x, y, zx, zy):
        temp = set()
        possible = [[-1, 1], [0, 1], [1, 1], [-1, 0], [0, 0], [1, 0], [-1, -1], [0, -1],[1, -1]]
        ax = x / gameobj.z
        ay = y / gameobj.z
        de = []
        for ab in range(0, len(possible)):
            if not Collider.col(ax * self.z, ay * self.z, zx, zy, (int(ax + possible[ab][0])) * self.z, \
                           (int(ay + possible[ab][1])) * self.z, self.z * 1, self.z * 1):
                de.append(possible[ab])
        for ab in range(len(de)):
            possible.remove(de[ab])
        ax = int(ax)
        ay = int(ay)
        for ab in range(len(possible)):
            if (ax + possible[ab][0], ay + possible[ab][1]) in self.taken:
                temp.add(self.blocks[(ax + possible[ab][0], ay + possible[ab][1])].chain)
        return temp

    def render(self):
        for kl in range(cap(int(spelare.x // 800 - 3), Min = 0), cap(int((spelare.x // 800 + 3)), Max = len(self.chunks) - 1)):
            chunk = self.chunks[kl]['rows']
            for ij in chunk:
                typ = ij.type
                x = ij.x # ij.blocks[0].x + (ij.blocks[-1].x - ij.blocks[0].x) * .5
                y = ij.y
                xz = ij.xz
                yz = 1
                if Collider.col(cam.cx(x * self.z), cam.cy(y * self.z), xz * self.z, yz * self.z, 0, 0, scrw, scrh):
                    ij.render()

    def createground(self, first, last):
        for chunkx, chunk in enumerate(maps[first: last + 1]):
            if not chunkx in self.chunks:
                self.chunks[chunkx] = {'raw': [], 'rows': []}
                for x in range(len(chunk)):
                    self.chunks[chunkx]['raw'].append(set())
                    for y in chunk[x]:
                        if chunk[x][y] != 0:
                            self.chunks[chunkx]['raw'][-1].add(y)
                            self.addground(x + chunkx * 8, y, chunk[x][y])
                self.chunks[chunkx]['raw'] = tuple(self.chunks[chunkx]['raw'])
    
'####################################################################################################'

class Chain(Game):
    def __init__(self, block):
        self.blocks = [block]
        self.type = block.type
        self.colors = block.colors
        block.mother.chains.append(self)
        self.chunks = [block.chunk]
        block.mother.chunks[block.chunk]['rows'].append(self)
        self.mother = block.mother
        self.y = block.y
        self.x = block.x
        self.xz = 1

        if ispos(self.type) == -1: self.run = lambda self, player: player.kill()
        elif self.type != 2: self.run = lambda self, player: self.act(player)
        else:
            def func(self, player):
                self.act(player)
                player.friction = .975
            self.run = func

    def addblocktochain(self, block):
        self.blocks.append(block)
        if not block.chunk in self.chunks: # if the chain isn't already in block chunk add chain to chunk
            self.chunks.append(block.chunk)
            block.mother.chunks[block.chunk]['rows'].append(self)
        start = self.start()
        self.x = start.x + (block.x - start.x) / 2
        self.xz += 1

    start = lambda self: self.blocks[0]

    end = lambda self: self.blocks[-1]

    def act(self, player):
        z = self.mother.z
        if self.mother.checkifground(player.x, player.y - player.yvel, player.z, player.z):
            player.x = z * self.x - ispos(player.xvel) * (player.z)
            player.xvel = 0
        else:
            player.TouchMap['vertical'] = -ispos(player.yvel)
            player.y = z * self.y - ispos(player.yvel) * (player.z)
            player.yvel = 0

    def render(self):
        mother = self.mother
        colors = self.colors
        x, y = cam.cx(self.x * mother.z), cam.cy(self.y * mother.z)
        for ab in mother.layers[0: colors[2]]:
            RendObj.square(x, y, *cam.cz(mother.z * self.xz - mother.z * ab[0], \
                           2 * mother.z * ab[1]), colors[ab[2]][0][colors[ab[2]][1]])
            # RendObj.write(str(self.xz), cam.cx(self.x * mother.z), cam.cy(self.y * mother.z))
            # måttligt häftig idé
            
'####################################################################################################'

class Block(Game):
    
    def __init__(self, x, y, typ, mother):
        self.x = x
        self.y = y
        self.chunk = len(mother.chunks) - 1
        self.type = typ
        self.mother = mother
        self.colors = mother.colors[typ]
        chained = 0
        if (x - 1, y) in mother.blocks:
            linkblock = mother.blocks[(x - 1, y)]
            if linkblock.type == self.type:
                self.chain = linkblock.chain
                self.chain.addblocktochain(self)
                chained = 1
        if not chained: self.chain = Chain(self)

####################################################################################################
            
class Collider:
    
    @staticmethod
    def col(x, y, ix, iy, x2, y2, ix2, iy2):
        return abs(x - x2) < (ix / 2 + ix2 / 2) and abs(y - y2) < (iy / 2 + iy2 / 2)
    
####################################################################################################

class Camera():
    '''The Camera Object'''
    def __init__(self, x = 0, y = 0, z = 1):
        self.x = x
        self.y = y
        self.z = z

    def move(self, x = None, y = None, z = None, speed = 1):
        '''Transistions towards a point with a certain speed'''
        z = self.z if z is None else z
        x = self.x if x is None else x
        y = self.y if y is None else y
        self.x += (x - self.x) * speed
        self.y += (y - self.y) * speed
        self.z += (z - self.z) * speed
        
    cx = lambda self, x: int((x - self.x) * self.z)
    cy = lambda self, y: int((y - self.y) * self.z)
    cz = lambda self, *z: [_z * self.z for _z in z]
    bx = lambda self, x: x / self.z + self.x
    by = lambda self, y: y / self.z + self.y
    
####################################################################################################
class RenderingObject: # behöver byggas om

    def __init__(self, monitor = None):
        self.configure(monitor or MainDis)

    def configure(self, display):
        self.scr = display
        self.scrw = display.width
        self.scrh = display.height

    def center(self, x, y, xt = .5, yt = .5):
        return x + self.scrw * xt, y + self.scrh * yt

    def ry(self, y):
        return -(y - self.scrh)

    def write(self, txt, x, y, color = '#ffffff', font = ('Arial', 10), anchor = CENTER):
        x, y = self.center(x, y)
        self.scr.create_text(x, self.ry(y), fill = color, text = str(txt), font = font, anchor = anchor)

    def sdot(self, x, y, size, color):
        x, y = self.center(x, y)
        self.scr.create_oval(int(x + size * -.5), int(self.ry(y) + size * -.5), int(x + size * .5), int(self.ry(y) + size * .5), fill = color, width = 0)

    def dot(self, x, y, size, color):
        x = cam.cx(x)
        y = cam.cy(y)
        size *= cam.z
        self.sdot(x, y, size, color)

    def thx(self, rgb):
        return "#%02x%02x%02x" % (int(cap(rgb[0], 255, 0)), int(cap(rgb[1], 255, 0)), int(cap(rgb[2], 255, 0)))

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def trans(self, rgb, rgb2, percent):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        r2 = rgb2[0]
        g2 = rgb2[1]
        b2 = rgb2[2]
        return (r + ((r2 - r) * percent), g + ((g2 - g) * percent), b + ((b2 - b) * percent))

    def randcolor(self, r, g, b):
        return rnd.randint(0, r), rnd.randint(0, g), rnd.randint(0, b)

    def line(self, x1, y1, x2, y2, z, color):
        x1, y1, x2, y2 = *self.center(x1, y1), *self.center(x2, y2)
        self.scr.create_line(x1, self.ry(y1), x2, self.ry(y2), width = z, fill = color)

    def polygon(self, cords, color, **extra):
        self.scr.create_polygon(cords, fill = color, **extra)

    def triangle(self, x, y, sin, cos, w, h, color, **extra):
        x, y = self.center(x, y)
        self.polygon([x + sin * h, self.ry(y + cos * h), x + sin * -h + cos * w, self.ry(y + cos * -h + sin * -w), \
                   x + sin * -h + cos * -w, self.ry(y + cos * -h + sin * w)], color, **extra)

    def square(self, x, y, width, height, color = '', bw = 0, **extra):
        x, y = self.center(x, y)
        width /= 2
        height /= 2
        self.scr.create_rectangle(x + width, self.ry(y - height), x - width, self.ry(y + height), \
                                  fill = color, width = bw, **extra)
        
####################################################################################################################################################################

class Player:
    def __init__(self):
        self.oldx = -1842
        self.oldy = 0
        self.xvel = 0.0
        self.yvel = 0.0
        self.z = 100
        self.rl = 1
        self.i = 0
        self.score = 0
        self.state = 'alive'
        self.controls = {'up': 0, 'right': 0, 'left': 0, 'down': 0}
        self.old = self.controls
        self.j = 20.0
        self.x = 0
        self.y = gameobj.z * 5
        self.jumpnum = 0
        self.friction = .975
        self.down = 'e'
        self.name = rnd.choice(player_names) # internal variable
        self.TouchMap = {'vertical': 0, 'horizontal': 0}
        
    def jump(self):
        self.yvel = self.j

    def kill(self): self.state = 'killed'
        
    def run(self):
        if spelare.state == 'alive':
            self.oldx = self.x
            self.oldy = self.y
            self.x += self.xvel
            self.y += self.yvel
            if self.y < 0: self.kill()
            self.i += 1
            iground = gameobj.checkifground(self.x, self.y, self.z, self.z)
            self.TouchMap = {'vertical': 0, 'horizontal': 0}
            touchground = iground == set()

            self.friction = .95
            for ab in [1]:
                for chain in iground.copy():
                    chain.run(chain, self)
                    #iground = gameobj.checkifground(self.x, self.y, self.z, self.z)
            if self.TouchMap['vertical']:
                self.yvel = 0
                self.jumpnum = 2 * (self.TouchMap['vertical'] == 1)
                self.down = 'e'
            if all((self.jumpnum > 0, self.controls['up'], self.old['up'] != 1)):
                self.jump()
                self.jumpnum -= 1
            #if all((not self.TouchMap['vertical'], self.controls['down'], not self.old['down'])):
            #    self.yvel = -10
            self.yvel -= (1 + -.5 * (self.controls['up'] - self.controls['down']))
            self.xvel = (self.xvel + .75 * (self.controls['right'] - self.controls['left'])) * self.friction
            self.old = copy.copy(self.controls)
            
    def render(self, border = False):
        noborder = not border
        x, y = cam.cx(self.x), cam.cy(self.y)
        if border:
            xvel, yvel = cam.cx(self.x + self.xvel * 10), \
                         cam.cy(self.y + self.yvel * 10)
            
            color = palette['blue']
            RendObj.line(x, y, xvel, y, cam.cz(self.z * .25), color = color)
            RendObj.triangle(xvel, y, ispos(self.xvel), 0, *cam.cz(self.z * .5, self.z * .25), color = color)
            
            color = palette['lightred']
            RendObj.line(x, y, x, yvel, cam.cz(self.z * .25), color = color)
            RendObj.triangle(x, yvel, 0, ispos(self.yvel), *cam.cz(self.z * .5, self.z * .25), color = color)
            
            color = palettetheme['contrast']
            RendObj.square(x, y, *cam.cz(self.z + 24, self.z + 24), color)
            color = palettetheme['bg']
            RendObj.square(x, y, *cam.cz(self.z + 12, self.z + 12), color)
            color = self.colors[0]
            RendObj.square(x, y, *cam.cz(self.z, self.z), color)
            color = self.colors[1]
            RendObj.square(x, y, *cam.cz(self.z * .75, self.z * .75), color)
        else:
            stipple = 'gray50'
            color = self.colors[0]
            RendObj.square(x, y, *cam.cz(self.z, self.z), color, stipple = stipple, \
                           bw = cam.cz(6)[0], outline = palettetheme['contrast'], \
                           outlinestipple = stipple)
            color = self.colors[1]
            RendObj.square(x, y, *cam.cz(self.z * .75, self.z * .75), color, stipple = stipple)

####################################################################################################################################################################
class enemy:
    def __init__(self, x,y,z, xvel,possiblespawns,was):
        temp=possiblespawns[len(was)%len(possiblespawns)]
        self.x=x
        self.y=y
        self.z=z
        self.xvel=xvel
        self.yvel=0
    def run(self):
        self.x=(self.x+self.xvel)
        self.y=(self.y+self.yvel)
        iground=g.checkifground(self.x, self.y, self.z, self.z)
        if not iground==[]:
            for ab in iground:
                if col.col(ab[0]*g.z,ab[1]*g.z,g.z,g.z,self.x,self.y,self.z,self.z)==1:
                    if g.checkifground(self.x, self.y-self.yvel, self.z, self.z) == []:
                        self.y=g.z*ab[1]+-ispos(self.yvel)*(self.z)
                        self.yvel=0
                    else:
                        self.x=g.z*ab[0]+-ispos(self.xvel)*(self.z)
                        self.xvel=-self.xvel
        self.yvel=self.yvel-1
        if spelare.state=="alive":
            if((col.col(self.x, self.y, self.z, self.z,spelare.x,spelare.y,spelare.z,spelare.z) == True)):
                if (spelare.yvel<self.yvel) and (col.col(self.x, self.y, self.z, self.z,spelare.x,spelare.y-spelare.yvel,spelare.z,spelare.z) == False):
                    return "killed"
                else:
                    spelare.x=self.x-((ispos(spelare.xvel))*self.z)
                    spelare.xvel=-spelare.xvel
                    self.xvel=-self.xvel
                    return "splardo"
            elif 0>self.y+self.yvel:
                return "del"
                self.delete()
            else:
                g.checkvis(self.x,self.y,self.z,self.z,-1)
                return "grate"
        elif 0>self.y+self.yvel:
            return "del"
            self.delete()
        else:
            g.checkvis(self.x,self.x,self.y,self.z,-1)
            return "grate"
    def render(self):
        color="#bb0033"
        rendobj.square(self.x,self.y,1,0,self.z*.5,self.z*.5,color,0)
        color="#ff0066"
        rendobj.square(self.x,self.y,1,0,self.z*.375,self.z*.375,color,0)
    def delete(self):
        pass
    
####################################################################################################################################################################

class Network:

    layertag = 0
    width = 12
    height = 8
    LinkInn = 0
    NodeInn = 0
    LinkCasts = {}
    NodeCasts = set()

    '######################################################################################################################################################'

    #classmethods

    @classmethod
    def loadsaved(cls, file):
        print(cls)

    @classmethod
    def NewLinkCast(cls, Inn, cast):
        cls.LinkCasts[Inn] = CastLink(cast['Start'], cast['End'])

    @classmethod
    def NewNodeCast(cls, Inn):
        cls.NodeCasts.add(Inn)

    @classmethod
    def GetLinkInn(cls, cast, addInn = 1):
        if cast in cls.LinkCasts.values():
            Inn = tuple(cls.LinkCasts.keys())[tuple(cls.LinkCasts.values()).index(cast)]
        else:
            cls.NewLinkCast(cls.LinkInn, cast)
            Inn = cls.LinkInn
            cls.LinkInn += addInn
        return Inn

    @classmethod
    def GetNodeInn(cls, Inn, addInn = 1):
        if not Inn in cls.NodeCasts:
            cls.NewNodeCast(Inn)
            cls.NodeInn += addInn
        return Inn

    '######################################################################################################################################################'

    def __init__(self, ancestor, gen_, mutate):
        self.mut = mutate
        self.chancedata = {'totstch': 0, 'totndch': 0}
        self.layers = {}
        self.order = []
        self.parent = 'e'
        self.startlinks = {} # neuron (not Inn): links
        if ancestor != {}:
            self.new(output = False)
            self.load(ancestor)
        else:
            self.new()
        dark = rnd.choice(tuple(darktolight.keys()))
        self.color = (palette[dark], palette[darktolight[dark]])
        spelare.colors = self.color
        if mutate: self.mutate()
        self.DelOverFlow()
        self.tick = 0

        self.finalise() # The last thing that is to be done. (Dramatic Dot)

        # Kom ihåg att det är något fel på inputlagret #
        ' Kom ihåg att det är något fel på inputlagret '
        # Kom ihåg att det är något fel på inputlagret #

    '######################################################################################################################################################'

    def finalise(self):
        self.ifded = self.saveself()
        set(map(lambda node: node.finalise(), self.nodes.values()))
        set(map(lambda link: link.finalise(), self.links.values()))
##        for node in self.nodes.values():
##            node.finalise()
##        for link in self.links.values():
##            link.finalise()
            
    '######################################################################################################################################################'

    def load(self, ancestors):
        nodes = {}
        links = {}
        layers = {}
        
        for gentag, genome in enumerate(ancestors):
            for tag, layer in genome['Layers'].items():
                if not tag in layers: layers[tag] = layer
                
            for Inn, node in genome['Nodes'].items():
                if Inn in nodes: nodes[Inn][gentag] = node
                else: nodes[Inn] = {gentag: node}
            
            for Inn, link in genome['Links'].items():
                if Inn in links: links[Inn][gentag] = link
                else: links[Inn] = {gentag: link}

        for tag, layer in layers.items():
            Layer(self, tag, stchance = layer['stchance'], ndchance = layer['ndchance'], x = layer['x'])

        for Inn, genome in nodes.items():
            node = genome[rnd.choice(tuple(genome))]
            self.AddNode(layer = self.layers[node['layer']], y = node['y'], Inn = Inn, activation = node['activation'])

        for Inn, genome in links.items():
            link = genome[rnd.choice(tuple(genome))]
            self.AddLink(Inn = Inn, weight = link['weight'])

    '######################################################################################################################################################'

    def saveself(self):
        savef = {}
        savef['Nodes'] = {}
        savef['Links'] = {}
        savef['Layers'] = {}
        
        for Inn, node in self.nodes.items():
            savef['Nodes'][Inn] = {'layer': node.layer, 'y': node.y, 'activation': node.activation}
                # layer behövs kanske inte
                
        for Inn, link in self.links.items():
            savef['Links'][Inn] = {'weight': link.weight}

        for tag, layer in self.layers.items():
            if tag != 'input': savef['Layers'][tag] = {'x': layer.x, 'stchance': layer.stchance, 'ndchance': layer.ndchance}
            
        return savef

    '######################################################################################################################################################'

    def DelOverFlow(self):
        found = True
        while found:
            found = False
            for LayerTag in self.order[1: ]:
                if LayerTag != self.order[-1]:
                    layer = self.layers[LayerTag]
                    for ef in layer.nodes.copy():
                        node = self.nodes[ef]
                        if node.OutG == set() or node.InG == set():
                            node.destroy()
                            found = True
                            if layer.nodes == set(): self.removelayer(LayerTag)

    '######################################################################################################################################################'

    def new(self, output = 1):
        self.ActiveNodes = set()
        self.fitness = 0
        self.links = {} # Inn: link
        self.nodes = {} # Inn: node
        self.rates = {
                      'bias': {'rate': .2},
                      'newneuron':{'rate': .2},
                      'newlink': {'rate': .25},
                      'removelink': {'rate': .1},
                      'mutatetoneuron': {'rate': .1},
                      'movelink': {'rate': .15}
                      }
        last = Layer(self, 'input', x = 1, ndchance = 0, stchance = 6, children = runobj.inputsset)
        if output:
            last = Layer(self, 'output', x = 21, stchance = 0, ndchance = 4)
            for y, Inn in enumerate(('up', 'down', 'right', 'left')):
                self.AddNode(layer = last, Inn = Inn, activation = 'Treshold', y = y * 2 + 1)

    '######################################################################################################################################################'

    def run(self):
        '''
        Does an iteration of the network.

        The input nodes have already been set.
        '''
        for layer in self.order[1: ]:
            for node in self.layers[layer].nodes:
                node()
        spelare.controls = {node: self.nodes[node].charge for node in ('left', 'right', 'down', 'up')}
        if spelare.state == 'alive':
            self.fitness = int((((spelare.x / 2) - self.tick / 3) - len(self.links)) * 10)
            self.tick += 1

    '######################################################################################################################################################'

    def mutate(self):
        self.mutaterates([])
        self.removestuff()
        self.changestuff()
        self.addstuff()

    '######################################################################################################################################################'

    def mutaterates(self,rates):
        pass
        '''for ab in rates:
            pass
        return rates'''

    '######################################################################################################################################################'

    def removestuff(self):
        while rchance(self.rates['removelink']['rate']) and len(self.links) != 0:
           rnd.choice(tuple(self.links.values())).destroy()

    '######################################################################################################################################################'

    def changestuff(self):
        '''while rchance(self.rates['movelink']['rate']) and len(self.startlinks) != 0:
            res = rnd.choice(tuple(self.startlinks))
            link = rnd.choice(tuple(self.startlinks[res]))
            x = cap(link.start.fieldx + rnd.randint(rnd.randint(-1, 0), rnd.randint(0, 1)), 12, 0)
            y = cap(link.start.fieldy + rnd.randint(rnd.randint(-1, 0), rnd.randint(0, 1)), 8, 0)
            newstart = runobj.inputs[(x, y)]
            link.start = newstart'''
        
        for ab in self.links.values():
            if rchance(.2):
                ab.weight = cap(ab.weight + rpos() * rnd.randfloat(0, rnd.randfloat(0, rnd.randfloat(0, .5))), 1, -1)

        # Mutates links to add new neuron in between            
        while rchance(self.rates['mutatetoneuron']['rate']) and len(self.links) != 0:
            link = rnd.choice(tuple(self.links.values()))
            end = link.end
            start = link.start
            layer = Layer(self, Network.layertag, x = rnd.randfloat(self.layers[end.layer].x + .001, self.layers[start.layer].x - .001))
            Network.layertag += 1

            middle = self.AddNode(layer = layer, Inn = Network.NodeInn).Inn
            start = start.Inn
            end = end.Inn
            
            self.AddLink(start = start, end = middle, weight = rpower())
            self.AddLink(start = middle, end = end, weight = rpower())

    '######################################################################################################################################################'

    def addstuff(self):
        self.chancedata = {'totstch': 0, 'totndch': 0}
        for ab, cd in self.layers.items():
            self.chancedata['totstch'] += cd.stchance
            self.chancedata['totndch'] += cd.ndchance
        while rchance(self.rates['newlink']['rate']):
            startlist = {ab: self.layers[ab].stchance for ab in self.order}
            start = Network.go_until_over(startlist, rnd.randfloat(0, self.chancedata['totstch']))
            ndchance = 0
            endlist = {}
            for ab in self.order[self.order.index(start) + 1:]:
                endlist[ab] = self.layers[ab].ndchance
                ndchance += self.layers[ab].ndchance
            end = Network.go_until_over(endlist, rnd.randfloat(0, ndchance))
            startneur = self.pickstneur(start)
            try: endneur = rnd.choice(tuple(self.layers[end].nodes))
            except:
                a = 0
                for ab in self.order[self.order.index(start) + 1:]:
                    a += self.layers[ab].ndchance
                print('Expect', a, self.order.index(start) + 1, self.order)
                print(ndchance)
                raise KeyError
            if rchance(self.rates['newneuron']['rate']):
                StartX = self.layers[start].x
                EndX = self.layers[end].x
                last = Layer(self, Network.layertag, x = rnd.randfloat(StartX + .0001, EndX - .0001))
                Network.layertag += 1
                
                middle = self.AddNode(layer = last, Inn = Network.NodeInn).Inn
                
                for ab in range(rnd.randint(1, rnd.randint(1, 3))):
                    self.AddLink(start = startneur, end = middle, weight = rpower())
                    startneur = self.pickstneur(Network.go_until_over(startlist, rnd.randfloat(0, self.chancedata['totstch'])))
                    self.AddLink(start = middle, end = endneur, weight = rpower())
                    
                self.chancedata = {'totstch': 0, 'totndch': 0}
                for ab, cd in self.layers.items():
                    self.chancedata['totstch'] += cd.stchance
                    self.chancedata['totndch'] += cd.ndchance
            else: self.AddLink(start = startneur, end = endneur, weight = rpower())

    '######################################################################################################################################################'

    def pickstneur(self, layer):
        if layer == 'input' and rchance(self.rates['bias']['rate']): return runobj.inputs['bias'].Inn
        else: return rnd.choice(tuple(self.layers[layer].nodes))

    '######################################################################################################################################################'

    def go_until_over(whatever, x):
        i = 0
        for ab, cd in whatever.items():
            i += cd
            if i >= x: return ab
        else:
            print(whatever, x)
            return 'WHAT!?'

    '######################################################################################################################################################'

    def save(self):
        pass

    '######################################################################################################################################################'

    def picklayer(self):
        if rfloat(0, 1) < self.rates['middle']['rate'] and len(self.neurons) != 3:
            layer = rnd.choice(self.getpos(1, len(self.neurons) - 1, 1, 'occupied'))
        else:
            layer = 0
        return layer

    '######################################################################################################################################################'

    def pickfromlayer(self, layer):
        if layer != 'input':
            return self.neurons[layer][rnd.choice(list(self.neurons[layer]))]

    '######################################################################################################################################################'

    def getpos(self, st, nd, fair):
        st = cap(st, len(self.neurons) - 1, 0)
        pos = list()
        empty = set()
        for cd in self.layers[st, nd]:
            pos.extend([cd] * len
                       (len(cd.layerneurons)) * fair + [cd] * int(not fair))
        return pos

    '######################################################################################################################################################'

    def AddLink(self, **kwargs):
        '''
        AddLink(Inn = ...) --> Link object
        Addlink(cast = ...) --> Link object
        Addlink(start = , end = ...) --> Link object
        '''
        if 'Inn' in kwargs:
            cast = Network.LinkCasts[kwargs['Inn']]()
            Inn = kwargs['Inn']
        elif 'cast' in kwargs:
            cast = kwargs['cast']
            Inn = Network.GetLinkInn(cast)
        else:
            cast = {'Start': kwargs['start'], 'End': kwargs['end']}
            Inn = Network.GetLinkInn(cast)
        weight = kwargs['weight']
        if not Inn in self.links:
            return StartLink(cast = cast, weight = weight, net = self) if not cast['Start'] in self.nodes \
                   else Link(cast = cast, weight = weight, net = self)
        return None

    '######################################################################################################################################################'

    def AddNode(self, activation = None, y = None, **kwargs):
        layer = kwargs['layer']
        Inn = kwargs['Inn']
        y = rnd.randfloat(0, 8) if y is None else y
        return Node(y = y, layer = layer, Inn = Inn, activation = activation)

    '######################################################################################################################################################'

    def AddLayer(self, tag, x): pass

    '######################################################################################################################################################'

    def removelayer(self, layer):
        self.order.remove(layer)
        del self.layers[layer]

    '######################################################################################################################################################'

    def render(self, x, y, z):
        self.currentlyusedneurons = set()
        gameobj.run()
        clrs = [palette['green'], palette['middlered'], '#226622', '#662266', \
                RendObj.hex_to_rgb(palette['middleblue']), RendObj.hex_to_rgb(palette['middlered']), \
                RendObj.hex_to_rgb(palettetheme['bgshade'])]

        ########
        pos = lambda ix, iy: (x + ix * z * 3, y + iy * z * 3)
        linkcol = lambda charge, used: clrs[int(.5 + ispos(charge) / -2) + (1 - used) * 2]
        neuroncol = lambda charge: RendObj.trans(grey, clrs[int(4.5 - (charge) * .5)], abs(charge))
        ########

        grey = RendObj.hex_to_rgb(palettetheme['bgshade'])
        
        if neurrendmode.get() == 1:
            RendObj.square(x + z * -18, y + z * 12, z * gameobj.NNwidth * 3 + z * .5, z * gameobj.NNheight * 3 + z, palettetheme['contrast'], 0)
            RendObj.square(x + z * -18, y + z * 12, z * gameobj.NNwidth * 3, z * gameobj.NNheight * 3, palettetheme['bgshade'], 0)
            
            for neuron in self.currentlyusedneurons: # draw inputneurons
                position = pos(neuron.x, neuron.y)
                Network.drawnode(position[0], position[1], z * (2 + 1 * int(neuron.field)), RendObj.thx(neuroncol(neuron.charge)), not(neuron.field), neuron.charge != 0)

            for LayerTag in self.order[1: ]: # draw the rest of the neurons
                layer = self.layers[LayerTag]
                for neuron in layer.nodes:
                    position = pos(layer.x, neuron.y)
                    Network.drawnode(position[0], position[1], z * 2, RendObj.thx(neuroncol(neuron.charge)), 1, neuron.charge != 0)
                    #MainDis.create_image(*RendObj.center(position[0], position[1]), image = ImageTk.PhotoImage(Image.open(iconfiles.path(neuron.activation + '.png'))))
                
            times = 2
##            writeneurons = {runobj.inputs['bias']: (E, -z * times), self.nodes['up']: (W, z * times), \
##                            self.nodes['down']: (W, z * times), self.nodes['right']: (W, z * times), \
##                            self.nodes['left']: (W, z * times)}
            writeneurons = {runobj.inputs['bias'], *self.nodes.values()}
            layers = {'input': (E, -z * times, 0), 'output': (W, z * times, 0)}
            for qr in writeneurons:
                pos1 = qr.GetPos()
                position = pos(pos1[0], pos1[1])
                op = layers[qr.layer] if qr.layer in layers else (N, 0, -z * times)
                RendObj.write(str(qr.Inn).capitalize(), position[0] + op[1], position[1] + op[2], \
                              '#ff9900', ('Arial', z * 2, 'bold'), anchor = op[0])
            for qr in self.links.values():
                startpos = qr.start.GetPos()
                pos1, pos2 = pos(startpos[0], startpos[1]), pos(self.layers[qr.end.layer].x, qr.end.y)
                half = pos1[0] + (pos2[0] - pos1[0]) / 2, \
                       pos2[1] + (pos1[1] - pos2[1]) / 2
                RendObj.line(pos1[0], pos1[1], pos2[0], pos2[1], z * .666 * abs(qr.weight), linkcol(qr.weight, qr.using))
                RendObj.write(str(qr.Inn), half[0], half[1], \
                              palette['middleblue'], ('Arial', z * 2, 'bold'), S)

    '######################################################################################################################################################'

    def drawnode(x, y, z, color, outline, activated):
        RendObj.square(x, y, z * 1.5 * int(outline), z * 1.5 * int(outline), palettetheme['contrast'] * \
                        int(activated) + palettetheme['contrastshade'] * int(not(activated)), 0)
        RendObj.square(x, y, z, z, color, 0)

'####################################################################################################'

class Cast(Network):
    '''
    The class that all Cast classes originate from.
    '''

'####################################################################################################'

class CastNode(Cast):
    '''
    Creates a node cast for other nodes to use as a preset.

    Properties:
    
        X. Determines where on the x-axis
           the node shall be placed.
        Inn. The node innovation. Essenti-
             ally a kind of tag.
        Only for middle nodes: {
            Start.
            End.
        } These properties are choosen
              when the cast is created
              and refer to the start of
              the ingoing link and the
              end of the outgoing link
              respectively.

    Ideas:

        Save all links connected to the node.

    Currently we only check if the Inn already exists
    in any of the presets. If it doesn't a new cast is
    created out of the information of the node. This
    makes it only have an effect when you're merging
    old networks. If the Inn is in the 'list' the
    node's Inn stays the same.
    '''

    def __init__(self, Inn, x):
        self.x = x
        self.Inn = Inn

    def __eq__(self, other):
        return self.x == other['x']
    
'####################################################################################################'

class CastLink(Cast):
    '''
    Creates a link cast for links to use as a preset to
    save memory when saving the network.

    Properties:

        Start: The node at the start of
            the link.
        End: The node at the end of the
            link.

    When a link is created we check if there already
    exists a link with the same Inn or the Start and
    End are identical to any cast. If there is the
    link will take the Inn of that cast, otherwise
    the Inn will stay the same.
    '''

    def __init__(self, Start, End):
        '''Start.Inn, End.Inn'''
        self.Start = Start
        self.End = End

    def __eq__(self, other):
        return self.Start == other['Start'] and self.End == other['End'] if isinstance(other, dict) \
               else self is other

    def __call__(self):
        return {'Start': self.Start, 'End': self.End}

    def __str__(self):
        return str(self())
  
'####################################################################################################'

class Link(Network):
    '''
    Also called axon. They connect nodes together and
    send charges forward in the network that activate
    nodes. The charge is calculated by getting the
    charge of the starting node times the links weight.
    '''

    def __init__(self, **kwargs):
        if 'Inn' in kwargs: cast = Network.LinkCasts[kwargs['Inn']]
        elif 'cast' in kwargs: cast = kwargs['cast']
        else: cast = {'Start': kwargs['start'], 'End': kwargs['end']}
        self.net = kwargs['net']
        self.Inn = Network.GetLinkInn(cast)
        self.net.links[self.Inn] = self
        #self.cast = cast
        if not isinstance(self, StartLink): self.net.nodes[cast['Start']].OutG.add(self.Inn)
        self.weight = kwargs['weight']
        self.using = 0
        start = self.net.nodes[cast['Start']] if not isinstance(self, StartLink) \
                else runobj.inputs[cast['Start']]
        end = self.net.nodes[cast['End']]
        end.InG.add(self.Inn)
        self.start = start
        self.end = end

    def __call__(self):
        self.using = self.start.charge != 0
        return self.start.charge * self.weight

    def __bool__(self):
        return self.using

    def destroy(self):
        self.net.links.pop(self.Inn)
        self.end.InG.remove(self.Inn)
        self.start.OutG.remove(self.Inn)

    def finalise(self):
        cast = Network.LinkCasts[self.Inn]()
        end = self.net.nodes[cast['End']]
        end.InG.remove(self.Inn)
        end.InG.add(self)
        self.start = self.net.nodes[cast['Start']]
        #delattr(self, 'end')
        '''self.net.nodes[cast['start']].end.remove(self.cast)
        self.net.nodes[cast['start']].end.add(self)'''

'####################################################################################################'

class StartLink(Link):
    '''
    A special type of link that is connected to the
    input layer. They have some unique attributes
    and methods.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lastused = -15
        start = runobj.inputs[Network.LinkCasts[self.Inn].Start]
        if not start in self.net.startlinks: self.net.startlinks[start] = set()
        self.net.startlinks[start].add(self)

    def __call__(self):
        self.using = self.start.act == (self.net.tick, self.net) and self.start.charge != 0
        return self.start.charge * self.using * self.weight

    def __bool__(self):
        return self.using

    def destroy(self):
        self.net.links.pop(self.Inn)
        try:
            self.net.startlinks[self.start].remove(self)
        except:
            print(self.net.startlinks)
            raise OSError
        if self.net.startlinks[self.start] == set(): self.net.startlinks.pop(self.start)
        self.end.InG.remove(self.Inn)

    def finalise(self):
        cast = Network.LinkCasts[self.Inn]()
        end = self.net.nodes[cast['End']]
        end.InG.remove(self.Inn)
        end.InG.add(self)
        self.start = runobj.inputs[cast['Start']]
        #delattr(self, 'end')

'####################################################################################################'

class Node(Network):
    '''
    Also called neuron, the nodes have charges that
    are transfered forward in the network using
    links until reaching the output layer. The
    node's charge is calculated by taking the sum
    of the charges recieved from the ingoing links
    and running that through an activation function.
    '''

    activation_methods = {'Sigmoid': lambda n, e = 2.718: 1 / (1 + (e ** (-n * 8))),
                          'Rectify': lambda n: (n > 0) * n,
                          'Treshold': lambda n, coff = 0: n > coff,
                          'Hyperbolic': lambda n, e = 2.718: 2 * ((1 / (1 + (e ** (-n * 8)))) - .5)}

    def __init__(self, **kwargs):
        self.Inn = Network.GetNodeInn(kwargs['Inn']) # Bygg om
        kwargs['layer'].mother.nodes[self.Inn] = self
        self.y = kwargs['y']
        self.OutG = set() # dict() cast: link
        self.InG = set() # dict() cast: link
        self.charge = 0
        layer = kwargs['layer']
        self.net = layer.mother
        self.layer =layer.tag # Layer.tag
        layer.nodes.add(self.Inn)
        activation = rnd.choice(tuple(Node.activation_methods)) if kwargs['activation'] is None else kwargs['activation']
        try:
            self.activation = activation
            self.activation_method = Node.activation_methods[activation] 
        except:
            keys = tuple(Node.activation_methods.keys())
            raise NameError('''Unknown activation method '%s'. Activation method has to be one of %s''' % (activation, str(keys[0: -1]).strip('(,)') + ' or \'' + keys[-1] + '\''))

    def __call__(self):
        '''call node --> charge'''
        self.charge = self.activation_method(sum(map(lambda link: link(), self.InG)))
        return self.charge

    def destroy(self):
        for link in copy.copy(self.OutG.union(self.InG)): self.net.links[link].destroy()
        self.net.layers[self.layer].nodes.remove(self.Inn)
        self.net.nodes.pop(self.Inn)

    def __str__(self):
        return 'Innovation: ' + str(self.Inn)

    def __hash__(self):
        return hash(str(self.layer) + str(self.Inn))

    def finalise(self):
        layer = self.net.layers[self.layer]
        layer.nodes.remove(self.Inn)
        layer.nodes.add(self)
        delattr(self, 'OutG')
        return ('Wooho! Elis tö e nou bäst din snygge fan!')

    def GetPos(self):
        return self.net.layers[self.layer].x, self.y

'####################################################################################################'

class InputNode(Node):
    
    def __init__(self, x, y, visx, visy, Inn, field):
        #self.dynamic = False
        self.fieldx = x
        self.fieldy = y
        self.x = visx
        self.y = visy
        self.charge = 0
        self.layer = 'input'
        self.field = field
        self.act = -123
        self.Inn = Inn

    def set(self, value):
        self.charge = value
        self.act = copy.copy((arti.tick, arti))
        return value

    def destroy(self):
        raise AttributeError('%s object is not deletable' % (type(self).__name__))

    def GetPos(self):
        return self.x, self.y

'####################################################################################################'

class Layer(Network):
    
    def __init__(self, mother, tag, stchance = 1, ndchance = 1, x = 0, children = None):
        mother.layers[tag] = self
        children = set() if children is None else children
        index = 0
        for layer in mother.order:
            if x > mother.layers[layer].x:
                index = mother.order.index(layer)
                break
        mother.order.insert(index + 1, tag)
        self.x = x
        self.tag = tag
        self.nodes = children
        self.stchance = stchance
        self.ndchance = ndchance
        self.mother = mother

    def __iter__(self):
        pass

    def __str__(self):
        return 'Tag: %s, Nodes: %s' % (self.tag, self.nodes)

    def __bool__(self):
        return len(self.nodes) != 0

'####################################################################################################'

class Species(Network):

    tag = 0
    family = {}

    # Idéer:
    #
    # Då nätverken skapas kontrolleras om det
    # är kompatibelt med föräldrarna.
    #   # Då nätverken skapats slås kompatibla
    #   # nätverk ihop.

    def __init__(self, net = None):
        self.links = {}
        self.nodes = {}
        self.NetCount = 0
        if not net is None: self.add(net)
        self.tag = copy.copy(Species.tag)
        Species.tag += 1

    def add(self, net):
        self.NetCount += 1
        for Inn, link in net['Links'].items():
            if not Inn in self.links:
                self.links[Inn] = {'occurances': 0, 'weight': 0}
            self.links[Inn]['occurances'] += 1
            self.links[Inn]['weight'] += (link['weight'] - self.links[Inn]['weight']) / self.links[Inn]['occurances']
        for Inn in net['Nodes']:
            if not Inn in self.nodes:
                self.nodes[Inn] = {'occurances': 0}
            self.nodes[Inn]['occurances'] += 1
    
    def FindDisjoint(self, other):
        return {'Links': set(self.links).difference(set(other.links)), \
                'Nodes': set(self.nodes).difference(set(other.nodes))}

    def FindCommon(self, other):
        return {'Links': set(self.links).intersection(set(other.links))}#, \
                #'Nodes': set(genomes[0].nodes).intersection(set(genomes[1].nodes))}

    def IsCompatible(self, other):
        N = max((self, other), key = lambda item: len(item.links) + len(item.nodes))
        N = len(N.links) + len(N.nodes)
        disjoint = self.FindDisjoint(other)
        e = 0
        for gen in disjoint['Links']: e += self.links[gen]['occurances'] / self.NetCount
        for gen in disjoint['Nodes']: e += self.nodes[gen]['occurances'] / self.NetCount
        common = self.FindCommon(other)['Links']
        W = 0
        for n, link in enumerate(common):
            W += (abs(self.links[link]['weight'] - other.links[link]['weight']) * (self.links[link]['occurances'] / self.NetCount)) / (n + 1)
        return e + W

    def __str__(self):
        return str('Tag: %s\nLinks:\n    %s\nNodes:\n    %s\n' % \
                  (self.tag, str(['(Innovation: %s, Occurances: %s, Weight: %s)' % \
                  (Inn, link['occurances'], link['weight']) for Inn, link in self.links.items()]).strip('[]'), \
                  str(['(Innovation: %s, Occurances: %s)' % \
                  (Inn, node['occurances']) for Inn, node in self.nodes.items()]).strip('[]')))

    def join(self, other): pass

'''
Network:
Link(Network):
StartLink(Link):
Node(Network):
InputNode(Node):
Layer(Network):
NetComp(Network): ?
Species(NetComp):
'''
        
####################################################################################################

class loadobj:

    def __init__(self):
        self.s_, self.n_, self.e_, self.best_ = spelare, arti, was, best
        alive.append(self)

    def set(self, was, best):
        self.e_, self.best_ = was, best

    def load(self):
        global spelare, arti, was, best
        spelare, arti, was, best = self.s_, self.n_, self.e_, self.best_

####################################################################################################
        
def render(splrnd, lasttime, frames, fps, mn):
    global lastalive

    cam.z = zoom.get()
    MainDis.config(bg = palettetheme['bg'])
    pick_player_field.config(bg = palettetheme['bg'], fg = palettetheme['contrast'])

    def getfitness(elem):
        return elem.n_.fitness

    if namesbool.get():

        def renderplayer(player):
            player.render()
            RendObj.write(player.name, cam.cx(player.x), cam.cy(player.y + (player.z / 2 + 45)), player.colors[1 - darkbool.get()], ('Arial', int(15 * (cam.z / .36)), 'bold'))

    else:

        def renderplayer(player):
            player.render()

    alive_players = sorted(alive[mn], key = getfitness)
    if not lastalive == alive[mn]:
        pick_player_field.delete(0, END)
        for ab in reversed(alive_players):
            pick_player_field.insert(END, ab.s_.name)

    if pick_player_field.curselection():
        pick_player_field.config(selectbackground = alive_players[-1 - pick_player_field.curselection()[0]].s_.colors[1 - darkbool.get()], \
                                 selectforeground = palettetheme['bg'])
        alive_players[-1 - pick_player_field.curselection()[0]].load()
    else:
        pick_player_field.config(selectbackground = alive_players[0].s_.colors[1 - darkbool.get()], selectforeground = palettetheme['bg'])
        pick_player_field.activate(0)

    cursx, cursy = tk.winfo_pointerx() - tk.winfo_rootx(), RendObj.ry(tk.winfo_pointery() - tk.winfo_rooty())
    if spelare.state == 'alive' and draw:
        for ab in was:
            ab.render()
        gameobj.render()
        if not splrnd:
            for ab in alive_players:
                renderplayer(ab.s_)
        spelare.render(True)

        if namesbool.get():
            arial_ = tkFont.Font(family = 'Arial', size = 15, weight = 'bold')
            width = arial_.measure(spelare.name) * 3
            RendObj.square(cam.cx(spelare.x), cam.cy(spelare.y + (spelare.z / 2) + 45), *cam.cz(width, 50), palettetheme['contrast'])
            RendObj.write(spelare.name, cam.cx(spelare.x), cam.cy(spelare.y + (spelare.z / 2 + 45)), \
                          spelare.colors[darkbool.get()], ('Arial', int(15 * (cam.z / .36)), 'bold'))

        if neurrendmode.get():
            arti.render(scrw * -.5 + 12 * 19.5, scrh * .5 -12 * 13.5, 6)
        RendObj.write('seed {}'.format(rnd.seed), scrw * .5 - 25, scrh * .5 - 25, \
                      '#00aaff', ('Arial', 15, 'bold'), anchor = NE)
        RendObj.write(Gen, 0, scrh * -.25, palettetheme['contrast'], ('Arial', 45, 'bold'))
        RendObj.write('%s %s' % (str(left), str(curgroup)), 0, scrh * -.3, palettetheme['contrast'], ('Arial', 30))
        RendObj.write('fps {}'.format(fps), 0, scrh * -.35, palettetheme['contrast'], ('Arial', 25))
        if (time.time() - lasttime) >= 1:
            fps = (int(((frames) / float((time.time() - lasttime))) * 10)) / 10.0
            frames -= fps
            lasttime = time.time()
        else: frames += 1
    RendObj.line(cam.cx(runobj.bestx), -(scrh / 2), cam.cx(runobj.bestx), scrh / 2, 2, palette['yellow'])
    MainDis.update()
    lastalive = alive[mn].copy()
    return lasttime, frames, fps

'######################################################################################################################################################'

def viewrend(data):
    RendObj.configure(score_graph)
    RendObj.scr.configure(bg = palettetheme['bg'])
    dx, dy, width, height = *RendObj.center(6, 6, xt = -.5, yt = -.5), RendObj.scrw - 18, RendObj.scrh - 18
    score_graph.delete('all')
    if data[0]:
        bestscore = data[-1][-1]
        startx = dx + 50
        bottom = dy + 10
        top = height - 10
        plus = 12
##      RendObj.ssquare(dx + width / 2, dy + height / 2, width + (3 + plus) * 2, \
##                        height + (3 + plus) * 2, palettetheme['contrast'], 0)
##        RendObj.ssquare(dx + width / 2, dy + height / 2, width + plus * 2, \
##                      height + plus * 2, palettetheme['bgshade'], 0)
        width -= 50
        for ab in range(4):
            RendObj.line(startx, bottom + (ab / 3) * top, startx + width, bottom + (ab / 3) * top, 2, palettetheme['bgshshade'])
            RendObj.write(round(bestscore * (ab / 3)), startx - 3, bottom + (ab / 3) * top, palette['blue'], ('Arial', 12, 'bold'), anchor = E)

        colors = palettetheme['contrastorange'], palette['blue']
        for ef in range(2):
            cd = 1 - ef
            color = colors[-cd - 1]
            x = copy.copy(startx)
            datlen = len(data[cd])
            y = 0
            for ab in range(datlen):
                x2 = x
                x = x + (width / (datlen))
                n = (data[cd][ab] / bestscore) * top
                fraction = 1 + ((datlen > 13) * 4) + ((datlen > 124) * 20)
                if cd == 1 and (ab % (fraction)) == (fraction - 1):
                    RendObj.line(x, bottom, x, bottom + top, 2, palettetheme['bgshshade'])
                    RendObj.write(str(ab + 1), x, dy, palette['yellow'], ('Arial', 12, 'bold'))
                RendObj.line(x2, bottom + y, x, bottom + n, 2, color)
                y = n
    else: RendObj.write('Graph', 0, 0)
    RendObj.configure(MainDis)
    score_graph.update()
        
def run(runspeed, hurg, best):
    for ef in range(runspeed):
        if arti.fitness > best[0]:
            best = (arti.fitness, tim)
            if runobj.bestx < spelare.x + spelare.z / 1.5:
                runobj.bestx = spelare.x + spelare.z / 1.5
        elif tim - best[1] > 30:
            spelare.state = 'killed'
            break
        #if (spelare.oldx // 1) == (spelare.x // 1):
        gameobj.run()
        arti.run()
        spelare.run()
    return hurg, best, was

'######################################################################################################################################################'

class TrackEditor:
    def __init__(self, track):
        self.item = 0
        self.tiles = filemaster[track]
        self.track = track

    def scrollfunc(self, event):
        if event.num == 5 or event.delta == -120:
            self.switch(n = -1)
        if event.num == 4 or event.delta == 120:
            self.switch(n = 1)

    def add(self, event = None):
        x, y = self.CursX - 1, round(selfCursY)
        chunk = round(x) // 8
        InX = x % 8
        if self.AddLayer_[0]:
            if self.AddLayer_[2]: tiles.insert(self.AddLayer_[1], [{} for ab in range(8)])
            else: del tiles[self.AddLayer_[1]]
        else:
            x = round(self.CursX) - 1
            InX = x % 8
            if chunk < len(tiles) and chunk >= 0:
                if item: tiles[chunk][InX][y] = item
                elif y in tiles[chunk][InX]: del tiles[chunk][InX][y]

    def render(self):
        self.AddLayer_ = (False, 0, None)
        tile_colors = {0: '#202040', 1: '#8080c0', -1: '#ff0080', -2: '#ff8000', 2: '#00ffff', -3: '#8000c0', 3: '#00ff80'}
        x = 0
        for n, chunk in enumerate(tiles):
            last = x + 0
            width = len(chunk)
            if collider.col(0, 0, scrw, scrh, cam.cx(last + (width + 1) / 2), 0, cam.z * width, cam.z):
                for strip in chunk:
                    x += 1
                    for y, tile in strip.items():
                        RendObj.square(x, y, 1, 1, tile_colors[tile])
                y = -.5
                ix = last + (width + 1) / 2
                color = '#00ff80'
                if collider.col(ix, y, .75, .75, CursX, CursY, 0, 0):
                    self.AddLayer_ = (True, n, False)
                    color = '#ff0080'
                    RendObj.ssquare(cam.cx(ix), 0, width * cam.z, scrh, color = '#ff0000', stipple = 'gray50')
                RendObj.line(last + .5, y, x + .5, y, .05, color)
                RendObj.dot(ix, y, .8, color)
                RendObj.dot(ix, y, .75, '#101020')
                RendObj.write('-', cam.cx(ix), cam.cy(y + .05), font = ('Arial', int(cam.z / 2)), color = color)
            else:
                x += width
                if cam.cx(x) > scrw / 2: break
        last = 0
        for chunk in range(len(tiles) + 1):
            y = cam.by(-50)
            color = '#00ff80'
            if collider.col(last + .5, y, .75, .75, CursX, CursY, 0, 0):
                self.AddLayer_ = (True, chunk, True)
                color = '#ffff00'
            RendObj.line(last + .5, -240, last + .5, 240, .05, color)
            RendObj.dot(last + .5, y, .8, color)
            RendObj.dot(last + .5, y, .75, '#101020')
            RendObj.write('+', cam.cx(last + .5), cam.cy(y), font = ('Arial', int(cam.z / 2)), color = color)
            last += 8
        x = CursX
        if not self.AddLayer_[0]: RendObj.square(round(x), round(CursY), 1, 1, bw = 5, border = '#ffff00')
        for n, block in enumerate(items):
            x, y = RendObj.center(50 * (n + 1), 40, -.5, -.5)
            if item is block:
                RendObj.ssquare(x, y, 50, 50, color = tile_colors[block], bw = 5, border = '#ffffff')
            else:
                RendObj.ssquare(x, y, 40, 40, color = tile_colors[block], bw = 5, border = '#c0c0c0')

    def switch(self, event = None, n = 1):
        self.ItemTag = (ItemTag + n) % len(items)
        self.item = items[ItemTag]

    def save(self):
        filemaster['EditMade.txt'] = tiles

    def run(self):
        self.CursX, self.CursY = RendObj.center(tk.winfo_pointerx() - MainDis.winfo_rootx(), \
                                  RendObj.ry(tk.winfo_pointery() - MainDis.winfo_rooty()), -.5, -.5)
        self.CursX, self.CursY = cam.bx(CursX), cam.by(CursY)
######################################################################################################
'####################################################################################################'
######################################################################################################

class rungame:

    def __init__(self):
        '''öhö'''

    def configinputs(self, width, height):
        self.inputsset = set()
        self.inputs = {}
        for x in range(width):
            for y in range(height):
                self.inputs[(x, y)] = InputNode(x, y, -x, y, (x, y), True)
                self.inputsset.add((x, y))
        self.inputs['bias'] = InputNode(0, 0, 0, -3, 'bias', False)
        self.inputs['bias'].charge = 1
        self.inputsset.add('bias')
    
    def initialise(self, seed = 0, startgen = 0, random = None, graph = [[], []], state = 'start', \
                   NNwidth = 13, NNheight = 9, groups = 20):
        global rnd,spelare,alive,cam,left,arti,was,possiblespawns,Gen,pz,draw,averages,st,best,RendObj, \
               maps,bests,startlevel,curgroup,tk,chunksforward,neurrendmode,showstats,frames, \
               fps,starttime,lasttime,backgcolor
        if not random is None: rnd = myrandom(random)
        else: rnd = myrandom(seed)
        self.seed = seed
        Gen = startgen + 0
        pz = 300
        self.groups = groups
        draw = 1
        averages = graph
        st = {}
        best = []
        RendObj = RenderingObject()
        # MainDis.bind('<Configure>', lambda event: RendObj.configure(event))
        maps = trackfiles['EditMade.txt']
        bests = []
        startlevel = 0
        curgroup = 0
        self.state = state
        self.bestx = 0
        self.configinputs(13, 9)
        self.SpeciesCount = []
        #Layertag
        
    def loop(self):
        # Yes, that is a huge list of global declarations
        #
        # It's stupid.
        global tim, gameobj, spelare, alive, cam, left, arti, was, possiblespawns, Gen, pz, \
               draw, averages, st, best, RendObj, maps, bests, startlevel, curgroup, tk, \
               chunksforward, neurrendmode, showstats, frames, fps, starttime, lasttime
        gameobj = Game()
        gameobj.level = startlevel
        gameobj.createground(first = 0, last = len(maps))
        while 1:
            bestrates = []
            if self.state == 'start':
                
                Gen += 1
                if Gen != 1:

                    self.genpool = list(sorted(kork, key = lambda elem: elem.fitness, reverse = True))

                    for ab in range(int(len(self.genpool) / 3), len(self.genpool)):
                        del self.genpool[rnd.randint(rnd.randint(0, len(self.genpool) - 1), len(self.genpool) - 1)]
                    averages[0].append(av)
                    averages[1].append(self.genpool[0].fitness)
                    for ab, cd in enumerate(self.genpool): self.genpool[ab] = cd.ifded
                    
                    genpool = {}
                    for tag, net in enumerate(self.genpool):
                        genpool[tag] = {'net': net}
                    self.genpool = genpool

                    self.species = {}
                    for i, group in self.genpool.items():
                        net = Species(group['net'])
                        for specy in sorted(self.species.values(), key = lambda item: item.nets):
                            if specy.IsCompatible(net) < .3:
                                group['species'] = specy.tag
                                specy.add(group['net'])
                                specy.nets.append(i)
                                break
                        else:
                            species = Species(group['net'])
                            self.species[species.tag] = species
                            species.nets = [i]
                            group['species'] = species.tag

                    self.SpeciesCount.append([])
                    for species in self.species.values():
                        self.SpeciesCount[-1].append(species.NetCount)
                        species.nets.sort()
                    # todo:
                    # species class with average network.
                    # only need to check if network is compatible
                    # with the species of its parents
                else:
                    self.genpool = {}
                self.rndstateinit = rnd.n
                self.state = 'initialize'
                
            elif self.state == 'initialize':
                viewrend(averages)
                kork = []
                print('Generation: ' + str(Gen))
                av = 0
                things = []
                alive = []
                plars = []
                for kl in range(pz):
                    spelare = Player()
                    if Gen != 1:
                        if kl != 0:
                            i = rnd.randint(0, rnd.randint(0, len(self.genpool)-1))
                            group = self.genpool[i]['species']
                            i2 = self.species[group].nets[rnd.randint(0, rnd.randint(0, len(self.species[group].nets) - 1))]
                            arti = Network([self.genpool[i]['net'], self.genpool[i2]['net']], Gen, True)
                        else:
                            i = self.genpool[0]['net']
                            arti = Network([i, i], Gen, False)
                    else:
                        arti = Network(st, Gen, True)
                    was = []
                    best = [0, 0]
                    a = loadobj()
                    things.append(a)
                l = int(pz / self.groups)
                alive = []
                for ab in range(0, self.groups):
                    alive.append([])
                    for cd in range(l):
                        alive[ab].append(things[ab * l + cd])
                for ab in range(len(things) % l):
                    alive[-1].append(things[int(len(things) / l) + ab])
                self.state = {'state': 'run', 'group': 0, 'player#': 0}
                cam = Camera(.36)
                tim = 0
                
            elif self.state['state'] == 'run':
                mn = self.state['group']
                left = len(alive[mn])
                curgroup = mn
                MainDis.delete('all')
                op = 0
                hurg = [-2000.0, 0]
                playerlevels = [0,0]
                lowestchunk = 0
                highestchunk = 0
                for qr in range(left):
                    a = alive[mn][op]
                    a.load()
                    temp = run(spd.get(), hurg, best)
                    hurg = temp[0]
                    best = temp[1]
                    was = temp[2]
                    if spelare.state != 'alive':
                        del alive[mn][op]
                        av += arti.fitness / float(pz)
                        kork.append(arti)
                        left -= 1
                    else:
                        a.set(was, best)
                        if arti.fitness >= hurg[0]:
                            hurg = [arti.fitness, a]
                        op += 1
                tim += spd.get()
                
                if left != 0:
                    for ab in alive[mn]: cam.move(ab.s_.x, ab.s_.y, .25)
                    a = hurg[1]
                    spelare = a.s_
                    cam.move(spelare.x, spelare.y, .5)
                    try:
                        temp = render(False, lasttime, frames, fps, mn)
                        blv = playerlevels[0]
                        lasttime = temp[0]
                        frames = temp[1]
                        fps = temp[2]
                    except Exception as Error:
                        RendObj.write('Error\n' + str(Error.args), 0, 0, '#ffff99', ('Arial', 25, 'bold'))
                        raise NameError('HiThere')
                else:
                    self.state['group'] += 1
                    tim = 0
                    if self.state['group'] >= len(alive): self.state = 'start'
                    
if __name__ == '__main__':

    filemaster = files('Darnet/')
    iconfiles = files('Icons/', parent = filemaster)
    iconfiles.create('DarnetIcon.png')
    datafiles = files('Data/', parent = filemaster)
    trackfiles = files('Tracks/', parent = datafiles)
    try: trackfiles.fetch('EditMade.txt')
    except:
        trackfiles.create('EditMade.txt')
        trackfiles['EditMade.txt'] = [[{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: -1}, {1: -1}], [{1: -1}, {1: -1}, {1: 1}, {1: 1}, {1: 1, 8: -1, 10: -1, 12: -1, 14: -1, 16: -1, 18: -1, 20: -1, 22: -1, 24: -1, 26: -1, 28: -1, 9: -1, 11: -1, 13: -1, 15: -1, 17: -1, 19: -1, 21: -1, 23: -1, 25: -1, 27: -1, 29: -1}, {1: 1, 7: -1, 9: -1, 11: -1, 13: -1, 15: -1, 17: -1, 19: -1, 21: -1, 23: -1, 25: -1, 27: -1, 29: -1, 8: -1, 10: -1, 12: -1, 14: -1, 16: -1, 18: -1, 20: -1, 22: -1, 24: -1, 26: -1, 28: -1}, {1: 1, 8: -1, 10: -1, 12: -1, 14: -1, 16: -1, 18: -1, 20: -1, 22: -1, 24: -1, 26: -1, 28: -1, 9: -1, 11: -1, 13: -1, 15: -1, 17: -1, 19: -1, 21: -1, 23: -1, 25: -1, 27: -1, 29: -1}, {1: 1}], [{1: 1}, {1: 1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: -2}, {1: -2}], [{1: -2}, {1: -2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}], [{1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}], [{1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}, {1: 2, 3: -2}], [{1: 2}, {1: 2}, {1: -3}, {1: 1, 2: 1, 3: 1, 4: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1, 3: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1, 3: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 2}, {1: 2}, {1: 2}, {1: 2}], [{1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}], [{1: 2}, {1: 2}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 3: -1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 15: -1, 6: -1, 4: -1, 10: -1, 8: -1, 12: -1, 14: -1}, {1: 1, 3: -1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 15: -1, 6: -1, 4: -1, 10: -1, 8: -1, 12: -1, 14: -1}, {1: 1, 3: -1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 15: -1, 6: -1, 4: -1, 10: -1, 8: -1, 12: -1, 14: -1}, {1: 1, 3: -1}], [{1: 1, 3: -1}, {1: 1, 3: -1}, {1: 1, 3: -1}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}], [{1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1, 3: -2}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: -1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1, 4: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 2: 1}, {1: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 3: 1, 2: 1}, {1: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 4: 1, 3: 1, 2: 1}, {1: 1, 6: 1, 7: 1, 8: 1, 9: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 7: 1, 8: 1, 9: 1, 6: 1, 5: 1, 4: 1, 2: 1, 3: 1}, {1: 1, 8: 1, 9: 1, 7: 1, 6: 1, 5: 1, 3: 1, 2: 1, 4: 1}, {1: 1, 9: -1}], [{1: 1, 9: -1}, {1: 1, 9: -1}, {1: 1, 9: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 2}], [{1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}], [{1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}, {1: 2}], [{1: 2}, {1: 1, 2: -1, 4: -1, 3: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1, 3: 1, 4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}], [{4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: -1}, {4: -1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: -1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: -1}, {1: -1}, {1: -1}, {1: -1, 5: 1}, {1: -1, 5: 1}, {1: -1, 5: 1}, {1: -1, 5: 1}, {1: -1}], [{1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}], [{1: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {}, {}, {}, {}], [{}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {2: -1, 1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 5: -1}, {1: 1, 5: -1}], [{1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}], [{1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 6: -1}, {1: 1, 6: -1}, {1: 1, 2: 1, 6: -1}, {1: 1, 2: 1, 6: -1}, {1: 1, 2: 1, 6: -1}, {1: 1, 2: 1, 6: -1}], [{1: 1, 2: 1, 6: -1}, {1: 1, 2: 1, 6: -1}, {1: 1, 2: 1, 7: -1}, {1: 1, 2: 1, 7: -1}, {1: 1, 2: 1, 3: -1, 8: -1}, {1: 1, 2: 1, 3: -1, 8: -1}, {1: 1, 2: 1, 3: 1, 7: -1}, {1: 1, 2: 1, 3: 1, 7: -1}], [{1: 1, 2: 1, 3: 1, 7: -1}, {1: 1, 2: 1, 3: 1, 7: -1}, {1: 1, 2: 1, 3: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 8: -1}], [{1: 1, 2: 1, 3: 1, 4: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: -1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: -1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}], [{1: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: -1}], [{1: -1}, {1: -1}, {1: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 4: -1, 6: -1, 8: -1, 10: -1, 12: -1, 14: -1}, {1: 1, 4: -1, 6: -1, 8: -1, 10: -1, 12: -1, 14: -1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: -1}, {1: -1}, {1: -1}, {1: -1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {}, {}, {}, {}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1}, {1: 1}, {}], [{}, {}, {}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1, 2: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}], [{1: 1, 2: 1, 3: 1, 4: 1}, {1: 1, 2: 1, 3: 1, 4: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}], [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {4: 1}], [{4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}], [{4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1}], [{4: 1}, {4: 1}, {4: 1, 5: -1}, {4: 1}, {4: 1}, {4: 1}, {4: 1, 7: -1}, {4: 1, 7: -1}], [{4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1}, {4: 1}, {4: 1}, {4: 1, 5: 1}], [{4: 1}, {4: 1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}, {4: 1, 7: -1}], [{4: 1, 7: -1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: -1}], [{4: -1}, {4: -1}, {4: -1}, {4: 1}, {4: 1}, {4: 1, 7: -1, 9: -1, 11: -1, 8: -1, 10: -1}, {4: 1, 7: -1, 9: -1, 11: -1, 8: -1, 10: -1}, {4: 1}], [{4: 1}, {4: -1}, {4: -1}, {4: -1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}], [{4: 1}, {}, {}, {}, {4: 1}, {4: 1}, {4: 1}, {4: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}], [{4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}], [{4: 1}, {4: 1, 5: -1}, {4: 1}, {4: 1}, {4: 1}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{}, {}, {}, {}, {}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}], [{1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}], [{1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}], [{1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 5: -1, 7: -1, 6: -1}, {1: 1, 6: -1, 8: -1, 7: -1}, {7: -1, 9: -1, 8: -1}, {7: -1, 9: -1, 8: -1}, {7: -1, 9: -1, 8: -1}, {7: -1, 9: -1, 8: -1}], [{7: -1, 9: -1, 8: -1}, {1: 1, 6: -1, 8: -1, 7: -1}, {1: 1, 5: -1, 7: -1, 6: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}], [{1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}], [{1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1, 4: -1, 6: -1, 5: -1}, {1: 1}, {1: 1}, {1: 1}, {}], [{}, {}, {3: 1}, {3: 1}, {}, {}, {}, {5: 1}], [{5: 1}, {}, {}, {}, {6: 1, 9: -1}, {6: 1, 9: -1}, {9: -1}, {9: -1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{6: -1, 8: -1, 10: -1, 12: -1, 7: -1, 9: -1, 11: -1}, {6: -1}, {6: -1}, {6: -1}, {6: -1, 8: -1, 10: -1, 12: -1, 11: -1, 7: -1, 9: -1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {}, {}, {}, {}], [{}, {1: 1}, {1: 1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}], [{1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1, 4: -1}, {1: 1}, {1: 1}, {}], [{}, {}, {3: 1}, {3: 1}, {}, {}, {}, {5: 1}], [{5: 1}, {}, {}, {}, {6: 1, 9: -1}, {6: 1, 9: -1}, {9: -1}, {9: -1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{}, {}, {}, {}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1, 2: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {}], [{}, {1: 1, 2: 1}, {1: 1}, {1: 1}, {1: 1, 4: -1, 6: -1, 8: -1, 10: -1, 12: -1, 14: -1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {}, {}], [{}, {4: 1}, {4: 1}, {}, {}, {}, {5: 1}, {5: 1}], [{}, {}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 12: -1, 10: -1, 8: -1, 6: -1}, {1: 1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 12: -1, 10: -1, 8: -1, 6: -1}, {1: 1}], [{1: 1}, {1: -1}, {1: -1}, {1: -1, 3: -1, 4: -1, 2: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: -1}, {1: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1, 3: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {}, {}, {}, {1: 1}, {1: 1, 5: -1, 7: -1, 9: -1, 11: -1, 13: -1, 6: -1, 8: -1, 10: -1, 12: -1}, {1: 1}, {1: 1}], [{1: 1}, {1: -1}, {1: -1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1}, {1: 1}, {1: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1, 2: 1, 3: 1}, {1: 1}, {1: 1}, {1: 1}], [{1: 1}, {}, {}, {}, {}, {}, {1: 1}, {1: 1}], [{1: 1}, {1: 1, 2: -1}, {1: 1, 6: 1}, {1: 1, 6: 1}, {1: 1}, {1: 1}, {1: 1}, {4: 1}], [{1: 1, 2: 1, 3: 1, 4: 1}, {1: 1, 4: 1, 5: 1}, {1: 1}, {1: 1}, {1: 1, 4: 1}, {4: 1}, {4: 1}, {5: 1}], [{5: 1}, {5: 1}, {}, {}, {}, {9: -1}, {9: -1}, {9: -1}], [{1: 1, 9: -1}, {1: 1}, {1: 1}, {1: 1}, {}, {}, {3: 1}, {3: 1}], [{}, {}, {5: 1}, {5: 1}, {}, {}, {}, {}], [{}, {}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {}, {4: 1}], [{4: 1}, {}, {}, {1: 1, 6: 1}, {1: 1, 6: 1}, {1: 1}, {1: 1}, {1: -1, 3: -1, 5: -1, 7: 1, 2: -1, 4: -1, 6: -1}], [{}, {}, {7: 1}, {7: 1}, {7: 1}, {}, {}, {}], [{}, {}, {5: 1}, {5: 1}, {}, {}, {}, {3: 1}], [{3: 1}, {3: 1, 6: 1}, {3: 1, 4: -3, 5: -3, 6: 1}, {}, {}, {}, {4: 1}, {4: 1}], [{1: 1}, {1: 1}, {1: 1}, {}, {}, {3: 1}, {3: 1}, {3: 1}], [{3: 1, 4: 1, 5: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1, 5: 1}, {}, {1: 1}, {1: 1}], [{1: 1, 6: 1}, {6: 1}, {6: 1}, {3: -1}, {3: -1}, {}, {}, {}], [{4: 1}, {4: 1}, {4: 1, 5: 1}, {4: 1}, {4: 1}, {4: 1}, {4: 1}, {7: 1}], [{4: 1, 5: 1, 6: 1, 7: 1}, {7: 1, 8: 1}, {}, {}, {6: 1}, {6: 1}, {}, {}], [{}, {6: 1}, {6: 1}, {}, {}, {6: -1}, {6: -1}, {}], [{}, {6: 1}, {6: 1}, {}, {}, {}, {3: 1}, {3: 1}], [{3: 1}, {}, {}, {4: 1}, {4: 1}, {4: 1, 5: -1}, {}, {}], [{}, {3: 1}, {3: 1}, {3: 1}, {3: 1}, {}, {}, {3: 1}], [{3: 1}, {3: 1}, {3: 1}, {3: 1, 4: 1, 5: 1, 6: 1}, {}, {}, {3: 1}, {3: 1}], [{}, {}, {}, {3: 1}, {3: 1}, {5: 1}, {5: 1}, {5: 1, 6: -1, 7: -1}], [{5: 1}, {5: 1}, {5: 1}, {5: 1}, {5: 1, 6: 1}, {}, {}, {}], [{4: 1}, {4: 1}, {4: 1, 7: 1}, {4: 1, 5: 1, 6: 1, 7: 1}, {}, {}, {6: 1}, {6: 1}], [{1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: 1}, {1: -1, 5: 1}, {1: 1, 2: 1, 3: 1, 4: 1}], [{}, {}, {}, {4: 1}, {4: 1}, {7: 1}, {7: 1}, {}], [{}, {}, {}, {4: 1}, {4: 1}, {}, {}, {}], [{2: 1}, {2: 1}, {2: 1}, {2: 1}, {2: 1}, {2: 1}, {}, {}], [{1: 1}, {1: 1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: -1}, {1: 1, 5: 1}], [{1: 1, 6: 1}, {1: -1, 7: 1}, {1: -1, 7: 1}, {1: -1, 7: 1}, {1: 1, 6: 1}, {1: 1, 5: 1}, {1: 1, 5: 1}, {1: 1}], [{1: 1}, {}, {}, {}, {3: 1}, {3: 1}, {}, {}], [{}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}], [{}, {}, {}, {}, {}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1, 7: -1, 9: -1, 8: -1}], [{1: 1, 2: 1, 3: 1, 7: -1, 9: -1, 8: -1}, {1: 1, 2: 1, 3: 1, 7: -1, 9: -1, 8: -1}, {1: 1, 2: 1, 3: 1, 7: -1, 9: -1, 8: -1}, {1: 1, 2: 1, 3: 1, 7: -1, 9: -1, 8: -1}, {1: 1, 2: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, {}, {}], [{}, {}, {}, {}, {1: 1, 2: 1}, {1: 1, 2: 1}, {1: 1, 2: 1}, {1: 1, 2: 1}], [{1: 1, 2: 1}, {1: 1, 2: 1}, {}, {}, {}, {}, {}, {}], [{1: 1}, {1: 1}, {1: 1, 5: -1}, {1: 1, 2: 1, 6: -1}, {1: 1, 2: 1, 3: 1, 7: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 8: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 9: -1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}], [{}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}]]
    seedfiles = files('Seeds/', parent = datafiles)
    tk = Tk()
    try:
        open('data/index.txt')
        saved_seeds = filemaster.fetch('index.txt')
    except:
        saved_seeds = {}
        filemaster.create('index.txt')
        filemaster['index.txt'] = saved_seeds

    screen_width, screen_height = tk.winfo_screenwidth(), tk.winfo_screenheight()
    scrw = (screen_width / 5) * 4 - 6
    scrh = screen_height - 203
    orient = HORIZONTAL

    def resetpalette(event = None):
        global palette, darktolight, palettetheme, Guipal
        palette = pal(colors = {'white': '#ffffff', 'lightgrey': '#d8d8e6', 'grey': '#a4a4c3', 'darkgrey': '#222244', 'dark': '#111122', \
                                'darkred': '#660066', 'red' : '#990033', 'lightred': '#dd0000', 'darkorange': '#dd6600', 'orange': '#ff9900', 'yellow': '#ffdd00', \
                                'middlered': '#ff0080', 'purple': '#cc0077', 'pink': '#ff0099', \
                                'green': '#00ff66', 'darkgreen': '#00aa00', 'extradarkgreen': '#006600', 'blue': '#00aaff', \
                                'middleblue': '#0080ff', 'darkblue': '#0052a4', 'black': '#000022', \
                                'pink': '#ff00ff', 'purple': '#bb00bb'})
        Guipal = pal()
        palcolor(Guipal, 'dark', '', bound = palette.all['darkblue'])
        palcolor(Guipal, 'light', '', bound = palette.all['darkorange'])
        palettetheme = palswitch(palette)
        palettetheme.white.append(palcolor(palettetheme, 'bg', '', bound = palette.all['dark']))
        palettetheme.black.append(palcolor(palettetheme, 'contrast', '', bound = palette.all['white']))
        palettetheme.white.append(palcolor(palettetheme, 'bgshade', '', bound = palette.all['darkgrey']))
        palettetheme.black.append(palcolor(palettetheme, 'contrastshade', '', bound = palette.all['white']))
        palettetheme.white.append(palcolor(palettetheme, 'bgshshade', '', bound = palette.all['grey']))
        palettetheme.black.append(palcolor(palettetheme, 'contrastshshade', '', bound = palette.all['grey']))
        palettetheme.white.append(palcolor(palettetheme, 'bgorange', '', bound = palette.all['orange']))
        palettetheme.black.append(palcolor(palettetheme, 'contrastorange', '', bound = palette.all['yellow']))
        palettetheme.white.append(palcolor(palettetheme, 'blackwhite', '', bound = palette.all['black']))
        palettetheme.black.append(palcolor(palettetheme, 'whiteblack', '', bound = palette.all['white']))
        #palettetheme.extend(savedi, n = palettetheme.black, colors = {'bg': '#ffffff', 'bgshade': '#dfdfef'})
        #'contrast': '#ffffff', 'contrastshade': '#dfdfef', 'bg': '#ffffff', 'bgshade': '#dfdfef'})
        darktolight = {'red': 'lightred', 'darkblue': 'blue', 'darkgreen': 'green', \
                       'orange': 'yellow', 'purple': 'pink', 'grey': 'lightgrey'}
        try:
            for ab in palette:
                total = 0
                for cd in range(1, 7, 2):
                    total += int(palette[ab][cd: cd + 2], base = 16)
                if total < 192:
                    fg = '#ffffff'
                else:
                    fg = '#000000'
                changecolors[ab].configure(bg = palette[ab], fg = fg)
            savetopalettefile(palette, 'palettearti.txt')
        except: pass


    def savetopalettefile(array, f):
        pickle.dump(array, open(f, 'wb'))

    try:
        resetpalette()
        dictionary = pickle.load(open('palettearti.txt', 'rb'))
        if len(palette) == len(dictionary):
            palette = dictionary
    except:
        resetpalette()
        savetopalettefile(palette, 'palettearti.txt')

    def createimage(coords, name):
        iconfiles.create(name)
        img = Image.new('RGBA', (9, 11), color = (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        coordinates = coords
        for color in coordinates:
            for point in coordinates[color]:
                draw.point(point, fill = color)
        img.save(iconfiles.path(name))
        
    createimage({'#ffffff': set([(0, 10), (1, 10), (2, 9), (3, 8), (3, 7), (4, 6), (4, 5), (4, 4), \
                                       (5, 3), (5, 2), (6, 1), (7, 0), (8, 0)])}, 'Hyperbolic.png')
    createimage({'#ffffff': set([(8, 0), (7, 0), (6, 0), (5, 1), (4, 2), (4, 3), (3, 4), (2, 5), (1, 5), (0, 5)])}, 'Sigmoid.png')
    createimage({'#ffffff': set([(0, 5), (10, 0), (1, 5), (9, 0), (2, 5), (8, 0), (3, 5), (7, 0), \
                                 (4, 5), (6, 0), (5, 5), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)])}, 'Treshold.png')

    tk.configure(background = Guipal['light'])
    tk.option_add('*background', Guipal['light'])
    tk.option_add('*Button.background', '#f0f0f0')
    tk.option_add('*Button.highlightbackground', '#f0f0f0')
    tk.option_add('*Button.relief', FLAT)
    space = scrw
    
    TopBar = Frame(tk)
    TopBar.grid(row = 0, column = 0, sticky = W + E + S + N)
    LowBar = Frame(tk)
    LowBar.grid(row = 1, column = 0, sticky = W + E + S + N)

    #TopCNF = {'activebackground': palette['grey']}
    newseed = Button(TopBar, text = 'New', command = restart)#, cnf = TopCNF)
    newseed.grid(row = 0, column = 1, sticky = W + S + N)
    savebutton = Button(TopBar, text = 'Options', command = savecommand)
    savebutton.grid(row = 0, column = 2, sticky = E + S + N)
    TrackEdit = Button(TopBar, text = 'Edit Track')
    TrackEdit.grid(row = 0, column = 3, sticky = E + S + N)

    def switchpalette():
        palettetheme.switch()
        darkcheck.configure(fg = palettetheme['blackwhite'])
        for ab in palette:
            total = 0
            for cd in range(1, 7, 2):
                total += int(palette[ab][cd: cd + 2], base = 16)
            if total < 128:
                fg = '#ffffff'
            else:
                fg = '#000000'
            changecolors[ab].configure(bg = palette[ab], fg = fg)
        savetopalettefile(palette, 'palettearti.txt')

    MainDis = Canvas(LowBar, width = scrw, height = scrh, background = palettetheme['bg'])
    MainDis.grid(row = 0, column = 1, sticky = N + S, columnspan = 5)
    MainDis.bind('<Control-MouseWheel>', Scroll)
    MainDis.width, MainDis.height = scrw, scrh

    inputspace = LabelFrame(LowBar, text = 'Ingame Options', fg = palette['white'])
    buttonsspace = LabelFrame(inputspace, text = 'Buttons', fg = palette['white'])
    showstats = IntVar()
    showstatscheck = Checkbutton(buttonsspace, text = 'Show graph?', variable = showstats, activebackground = Guipal['light'], cursor = 'hand2')
    darkbool = IntVar()
    darkcheck = Checkbutton(buttonsspace, text = 'Theme', variable = darkbool, activebackground = Guipal['light'], cursor = 'hand2', command = switchpalette)
    namesbool = IntVar()
    namescheck = Checkbutton(buttonsspace, text = 'Show player names?', variable = namesbool, activebackground = Guipal['light'], cursor = 'hand2')
    namescheck.select()
    neurrendmode = IntVar()
    neurrendcheck = Checkbutton(buttonsspace, text = 'Show Network?', variable = neurrendmode, activebackground = Guipal['light'], cursor = 'hand2')
    sliderspace = LabelFrame(inputspace, text = 'Sliders', fg = palette['white'])
    spd = Scale(sliderspace, from_ = 0, to = 150, orient = orient, length = space / 4, highlightbackground = Guipal['light'], troughcolor = palette['dark'], activebackground = palette['lightred'], cursor = 'hand2')
    zoom = Scale(sliderspace, from_ = .05, to = 1, orient = orient, resolution = -1, length = space / 4, highlightbackground = Guipal['light'], troughcolor = palette['dark'], activebackground = palette['lightred'], cursor = 'hand2')
    zoom.set(.5)
    spdlabel = Label(sliderspace, text = 'speed')
    zoomlabel = Label(sliderspace, text = 'zoom')
    otherbuttonsspace = LabelFrame(inputspace, text = 'Palette', fg = palette['white'])

    def changecolor(event):
        global palette
        a = askcolor(color = palette[event.widget.mytag])[1]
        if a != None:
            palette[event.widget.mytag] = a
            total = 0
            for cd in range(1, 7, 2):
                total += int(a[cd: cd + 2], base = 16)
            if total < 192:
                fg = '#ffffff'
            else:
                fg = '#000000'
            event.widget.config(bg = a, fg = fg)
            savetopalettefile(palette, 'palettearti.txt')
            changecolors[ab].flash()

    changecolors = dict()
    for ab in palette:
        total = 0
        for cd in range(1, 7, 2):
            total += int(palette[ab][cd: cd + 2], base = 16)
        if total < 192:
            fg = '#ffffff'
        else:
            fg = '#000000'
        #changecolors[ab] = Button(otherbuttonsspace, width = 11, height = 1, font = ('Arial', 7, 'bold'), text = ab, fg = fg, bg = palette[ab], cursor = 'hand2')
        changecolors[ab] = Label(otherbuttonsspace, width = 11, height = 1, relief = FLAT, font = ('Arial', 7, 'bold'), text = ab, fg = fg, bg = palette[ab], cursor = 'hand2')
        changecolors[ab].mytag = ab
        changecolors[ab].bind('<Button-1>', changecolor)

    neurrendcheck.grid(row = 0, column = 0, sticky = S + W)
    showstatscheck.grid(row = 1, column = 1, sticky = S)
    darkcheck.grid(row = 0, column = 1, sticky = S + W)
    namescheck.grid(row = 1, column = 0, sticky = S)
    spdlabel.grid(row = 1, column = 2, sticky = S)
    zoomlabel.grid(row = 0, column = 2, sticky = S)
    spd.grid(row = 1, column = 1, sticky = S)
    zoom.grid(row = 0, column = 1, sticky = S)
    for ab, cd in enumerate(changecolors):
        changecolors[cd].grid(row = int(ab // 5), column = ab % 5, sticky = S + N)
    resetcolors = Button(otherbuttonsspace, width = 7, bg = palette['lightred'], relief = GROOVE, height = 1, font = ('Arial', 12, 'bold'), text = 'Reset', cursor = 'hand2')
    resetcolors.bind('<Button-1>', resetpalette)
    resetcolors.grid(row = 0, column = 5, sticky = N + S, rowspan = 5)
    for ab in range(5):
        otherbuttonsspace.grid_rowconfigure(ab, minsize = 21)
    sliderspace.grid(row = 0, column = 1, rowspan = 1, sticky = S + N + W + E)
    buttonsspace.grid(row = 0, column = 0, rowspan = 1, sticky = S + N + W + E)
    otherbuttonsspace.grid(row = 0, column = 2, rowspan = 1, sticky = S + N + W + E)

    tk.wm_state('zoomed')

    pick_player_space = LabelFrame(LowBar, text = 'Pick previewed player', width = screen_width / 5, height = screen_height - 160, bg = palette['white'])
    pick_player_space.option_add('*background', palette['white'])
    pick_player_space.grid_propagate(False)
    pick_player_container = Frame(pick_player_space)
    pick_player_container.place(relx = 0, rely = 0, anchor = NW)
    pick_player_scrolly = Scrollbar(pick_player_container)
    pick_player_field = Listbox(pick_player_container, yscrollcommand = pick_player_scrolly.set, font = \
                                ('Arial', int(((screen_width / 5) - 20) / 19)), selectbackground = '#ffff00', selectforeground = '#2020ff', \
                                bg = '#ff9900', width = 25, height = 10)
    pick_player_scrolly.config(command = pick_player_field.yview)
    pick_player_field.grid(row = 0, column = 0, sticky = E + W)
    pick_player_scrolly.grid(row = 0, column = 1, sticky = S + N)
    f = Frame(pick_player_container)
    score_graph = Canvas(f, width = screen_width / 5 - 30, height = screen_height / 4)
    score_graph.grid()
    score_graph.width, score_graph.height = screen_width / 5 - 30, screen_height / 4
    f.grid(row = 1, columnspan = 2)

    inputspace.grid(row = 1, column = 1, sticky = S + N + E + W, columnspan = 5)
    pick_player_space.grid(row = 0, rowspan = 3, sticky = N + S)

    chunksforward = 4
    lasttime = copy.deepcopy(time.time())
    starttime = lasttime
    frames = 0
    fps = 0
    lastalive = 'gfycwunc3'

    player_names = (
                    'That Guy From Titanic', 'Darth Vader', 'Terminator', 'Toyota', 'Dakota', \
                    'Ethan', 'Gwen', 'Robin Debank', 'Calvin', 'Clyde', 'Yoda', 'Phoenix', \
                    'Harry Potter')
    tk.title('Darnet')
    runobj = rungame()
    runobj.initialise(int(time.time() * 65189) % 571874)
    runobj.loop()

    # layout:
    #
    # {*tag*: *children*}
    # om widget inte är någon sorts frame är children
    # istället id'n
