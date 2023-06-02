from tkinter import filedialog as fido
import os
import json
import tkinter as tk
from enum import Enum
# from tkinter import tix
import tkinter.font as tkFont
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText as sc
from tkinter import messagebox as mb
frameIdMax = 1000
EntryWidth = 20


class States (Enum):
    Empty = 0
    Choice = 1


class ChoiceFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__()  # borderwidth=1,highlightbackground="black",highlightthickness=1)
        self.title(master.strvars['id'].get())
        ft = master.ft
        self.content = {}
        mapGrid = {'label'    : [1, 1], 
                'id_lb'    : [0, 2],
                'id'       : [1, 2],
                'speech_lb': [0, 3],
                'speech'   : [1, 3],
                'to_lb'    : [0, 4],
                'to'       : [1, 4]
                }
        mapLabel ={'label': "phrase: "+master.master.id,
                'id_lb': "name: ",
                'speech_lb': "speech: ",
                'to_lb': "to: "
                }
        mapEntry =['id', 'to']
        for q in mapLabel:
            self.content[q] = tk.Label(self, text=mapLabel[q], font=ft)
        for q in mapEntry:
            self.content[q] = tk.Entry(self, width=EntryWidth, textvariable=master.strvars[q], font=ft, )
        self.content['speech'] = sc(
            self, wrap=tk.WORD, height=3, width=EntryWidth, font=ft)  # int(10*scale))
        self.content['speech'].insert(tk.INSERT, master.str['speech'])
        for q in mapGrid:
            self.content[q].grid(column=mapGrid[q][0], row=mapGrid[q][1])

        # self.apply = tk.Button(self, font=ft)
        # self.apply.grid(column=0, row=5)
        # self.apply['text']='apply'
        self.remove = tk.Button(self, font=ft)
        self.remove.grid(column=0, row=5)
        self.remove['text'] = '-'
        self.remove['command'] = master.remove

        self.ok = tk.Button(self, font=ft)
        self.ok.grid(column=1, row=5)
        self.ok['text'] = 'ok'
        self.ok['command'] = master.check_and_close

        self.protocol("WM_DELETE_WINDOW", master.close_frame)


class Choice:
    def __init__(self, master, ft):
        self.button = tk.Button(master, font=ft)
        self.master = master
        self.ft = ft
        self.frame = None
        self.str = {}
        self.str['speech'] = ""
        self.strvars = {}
        self.strvars['id'] = tk.StringVar()
        self.strvars['id'].set('...')
        # self.speech = tk.StringVar()
        self.strvars['to'] = tk.StringVar()
        self.button.grid(row=3, column=len(master.choices))
        self.button['text'] = self.strvars['id'].get()
        self.button['command'] = self.open_frame
        # master.master = States.Choice

        self.open_frame()

    def unpack_data(self, data: dict):
        for k, v in data['ScrolledText'].items():
            self.content[k].insert(tk.INSERT, v)
        for k, v in data['strvars'].items():
            self.strvars[k].set(v)
        for k, v in data['str'].items():
            self.str[k] = v
        self.close_frame()

    def pack_data(self):
        data = {}
        # data.update(self.strvars)
        data['strvars'] = {}
        data['ScrolledText'] = {}
        data['str'] = {}

        for k, v in self.strvars.items():
            if isinstance(v, tk.StringVar):
                data['strvars'][k] = v.get()
            if isinstance(v, sc):
                data['ScrolledText'][k] = v.get("1.0", tk.END)

        for k, v in self.str.items():
            if isinstance(v, str):
                data['str'][k] = v
        return data

    def open_frame(self):
        if self.frame == None:
            self.frame = ChoiceFrame(self)

    def check_and_close(self):
        self.check_choice()
        self.close_frame()

    def close_frame(self):
        # self.save_frame()
        # self.check_choice()
        self.button['text'] = self.strvars['id'].get()
        self.master.master.DrawArrows()
        self.frame.destroy()
        self.frame = None

    def remove(self):
        if mb.askyesno('Warning', 'Are you sure to delete this choice?'):
            self.close_frame()
            self.button.destroy()
            self.master.choices.remove(self)
            self.master.master.DrawFrames()

    def check_choice(self):
        self.str['speech'] = self.frame.content['speech'].get("1.0", tk.END)
        tostr = self.strvars['to'].get()
        to = None
        for w1 in self.master.master.frames:
            if w1.id == tostr:
                to = w1
                break
        if to == None:
            mb.showwarning(
                'Error!', f'The choice {tostr} of the phrase {self.master.id} refers to non-existing phrase!')
            return -1
            # continue
        elif to == self.master:
            mb.showwarning(
                'Error!', f'The choice {tostr} of the phrase {self.master.id} refers to itself!')
            return -2
            # continue
        return 0
    # def save_frame(self):
    #     pass

        self.frame.destroy()


class MyFrame(tk.Frame):
    nrows = 4
    ncols = 3

    def __init__(self, id, xpos, ypos):
        super().__init__(borderwidth=1, highlightbackground="black", highlightthickness=1)
        self.empty = True
        self.id = id
        # self.phrase = ""
        # self.orator = ""
        self.choices = []
        self.xpos = xpos
        self.ypos = ypos
        self.arrows = []
        self.size = self.winfo_width()
        ft = self.master.ft
        self.scale = 1  # self.master.fontsize/10
        self.content = {}
        self.strvars = {}
        # self.stringvars['speech'    ]=tk.StringVar
        self.strvars['orator'] = tk.StringVar()
        # self.config(yscrollcommand = self.master.vscroll.set)
        # self.config(xscrollcommand = self.master.hscroll.set)

        # self.canvas = tk.Canvas(self)
        # self.canvas.pack()
        self.content['label'] = tk.Label(
            self, text="phrase " + self.id, font=ft)
        self.content['label'].grid(column=1, row=0)
        self.content['speech_lb'] = tk.Label(self, text="speech: ", font=ft)
        self.content['speech_lb'].grid(column=0, row=1)
        self.content['speech'] = sc(
            self, wrap=tk.WORD, height=3, font=ft, width=EntryWidth,)  # int(10*scale))
        self.content['speech'].grid(column=1, row=1)
        self.content['orator_lb'] = tk.Label(self, text="orator: ", font=ft)
        self.content['orator_lb'].grid(column=0, row=2)
        self.content['orator'] = tk.Entry(
            self, font=ft, width=EntryWidth, textvariable=self.strvars['orator'])  # int(10*scale))
        self.content['orator'].grid(column=1, row=2)
        self.content['destructor'] = tk.Button(self, font=ft, text='⨷')
        # self.content['destructor'].img=tk.PhotoImage(file='close.png',width=20,height=20)
        # self.content['destructor'].config(image=self.content['destructor'].img)
        self.content['destructor'].grid(column=0, row=0)
        self.content['destructor']["command"] = self.remove

        self.content['addbutton'] = tk.Button(self, font=ft)
        self.content['addbutton']['text'] = '+'

        self.choices = []
        self.addchoice = None

        self.add_choice_button()

        # self.create_line
    def unpack_data(self, data: dict):
        self.xpos = data['x']
        self.ypos = data['y']
        for k, v in data['strvars'].items():
            self.strvars[k].set(v)
        for k, v in data['ScrolledText'].items():
            self.content[k].insert(tk.INSERT, v)
        for k, v in data['choices'].items():
            self.add_choice()
            self.choices[-1].unpack_data(v)

    def pack_data(self):
        data = {}
        data['x'] = self.xpos
        data['y'] = self.ypos
        data['strvars'] = {}
        for k, v in self.strvars.items():
            data['strvars'][k] = v.get()
        data['ScrolledText'] = {}
        for k, v in self.content.items():
            # if isinstance(v, tk.Entry):
            #     data[k]=v.get()
            if isinstance(v, sc):
                data['ScrolledText'][k] = v.get('1.0', tk.END)
        data['choices'] = {}
        for c in self.choices:
            data['choices'][c.strvars['id'].get()] = c.pack_data()
        return data

    def resize(self):
        if len(self.content) > 0:
            for key, val in self.content.items():
                try:
                    val.configure(font=self.master.ft)
                except:
                    pass
        self.addchoice.configure(font=self.master.ft)
        for c in self.choices:
            c.button.configure(font=self.master.ft)
        self.redraw_choices()
        self.add_choice_button()
        mousex = self.master.winfo_pointerx()-self.master.winfo_rootx()
        mousey = self.master.winfo_pointery()-self.master.winfo_rooty()
        self.xpos = self.xpos*self.scale
        self.ypos = self.ypos*self.scale
        # self.xpos = (mousex-self.xpos)*(self.scale-1)+self.xpos
        # self.ypos = (mousey-self.ypos)*(self.scale-1)+self.ypos

    def redraw_choices(self):
        for i, ch in enumerate(self.choices):
            ch.button.grid(row=3, column=i)

    def add_choice_button(self):
        if self.addchoice != None:
            self.addchoice.destroy()
        self.addchoice = tk.Button(self, font=self.master.ft)
        self.addchoice.grid(column=len(self.choices), row=3)
        self.addchoice['command'] = self.add_choice
        self.addchoice['text'] = 'choice +'

    def add_choice(self):
        self.choices.append(Choice(self, self.master.ft))
        self.add_choice_button()

    def remove(self):
        if mb.askyesno(title='Warning', message="Do you wish to delete 'phrase "+self.id+"'?"):
            self.master.finalize_dragging()
            self.master.frames.remove(self)
            for ar in self.arrows:
                self.master.canvas.delete(ar)
            self.master.DrawArrows()
            self.destroy()

    def get_speech(self):
        return self.speech.get('1.0', tk.END)

    def get_orator(self):
        return self.orator.get()

    def place_frame(self, x, y):
        tmp = self.location(x, y)
        self.xpos = tmp[0]
        self.ypos = tmp[1]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # setting title
        self.title("undefined")
        # setting window size
        self.width = 1000
        self.height = 500
        self.frames = []
        self.state = States.Empty
        self.dragged_widget = None
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height,
                                    (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.geometry(alignstr)
        self.resizable(width=True, height=True)
        self.drawarrows = True
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # self.attributes("-fullscreen", False)

        self.fontsize = 12
        self.fontname = 'Calibri'

        self.canvas = tk.Canvas(self, width=screenwidth, height=screenheight,
                                scrollregion=f"0 0 {screenwidth} {screenheight}")
        self.canvas.height = self.canvas.winfo_reqheight()
        self.canvas.width = self.canvas.winfo_reqwidth()
        # pack(side=tk.LEFT, fill = tk.BOTH)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        # self.makescroll(self, self.canvas )
        self.makescroll(self, self.canvas)

        # self.vscroll = tk.Scrollbar(self, orient= tk.VERTICAL,command = self.canvas.yview)
        # self.vscroll.grid(row = 0, column = 1, sticky = tk.NS)#pack(side=tk.RIGHT, fill = tk.Y)

        # self.canvas.configure(yscrollcommand = self.vscroll.set)

        self.menu_init()
        self.keybinds()

        # self.canvas.create_line(0, 0, 200, 100, arrow=tk.LAST)
        # self.state('zoomed')

        # GButton_457=tk.Button(self)
        # GButton_457["bg"] = "#e9e9ed"
        self.font_init()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # GButton_457["font"] = ft
        # GButton_457["fg"] = "#000000"
        # GButton_457["justify"] = "center"
        # GButton_457["text"] = "Button"
        # GButton_457.place(x=170,y=100,width=70,height=25)
        # GButton_457["command"] = self.AddFrame

    def on_closing(self):
        if mb.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def makescroll(self, parent, thing):
        self.vscroll = tk.Scrollbar(
            parent, orient=tk.VERTICAL, command=thing.yview)
        self.vscroll.grid(row=0, column=1, sticky=tk.NS)
        thing.config(yscrollcommand=self.vscroll.set)
        self.vscroll.bind('<ButtonPress-1>', self.DrawFrames)

        self.hscroll = tk.Scrollbar(
            parent, orient=tk.HORIZONTAL, command=thing.xview)
        self.hscroll.grid(row=1, column=0, sticky=tk.EW)
        thing.config(xscrollcommand=self.hscroll.set)
        self.hscroll.bind('<ButtonPress-1>', self.DrawFrames)

    def menu_init(self):
        self.menubar = tk.Menu()
        self.config(menu=self.menubar)
        self.file_bar = tk.Menu(self.menubar)
        self.file_bar.add_command(
            label='save', command=self.save_file, accelerator="Ctrl+S")
        self.file_bar.add_command(
            label='load', command=self.open_file, accelerator="Ctrl+O")
        self.file_bar.add_command(
            label='export', command=self.export_file, accelerator="Ctrl+E")
        self.file_bar.add_command(
            label='import', command=self.import_file, accelerator="Ctrl+I")
        self.menubar.add_cascade(
            label='File ⬇', menu=self.file_bar, underline=0)
        self.menubar.add_command(
            label='hide/show arrows', command=self.show_arrows)
        self.menubar.add_command(label='new phrase', command=self.AddFrame)

        self.font_bar = tk.Menu(self.menubar)
        self.font_bar.add_command(label='+', command=self.font_increase)
        self.font_bar.add_command(label='-', command=self.font_decrease)
        self.menubar.add_cascade(
            label='Font ⬇', menu=self.font_bar, underline=0)
        # self.font_bar.add_cascade(label='Fonts...', menu=self.fonts_choice_bar)

        # self.fonts_choice_bar = tk.Menu(self.font_bar)
        # self.menubar.add_command(label='Exit',command=self.destroy)
    def keybinds(self):
        self.event_add('<<Drag>>', '<B1-Motion>')
        self.event_add('<<DragInit>>', '<ButtonPress-1>')
        self.event_add('<<DragFinal>>', '<ButtonRelease-1>')
        self.bind('<<DragInit>>', self.drag_init)
        self.bind('<<Drag>>', self.drag_widget)
        self.bind('<<DragFinal>>', self.finalize_dragging)
        self.bind('<Double-Button-1>', self.AddFrame)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.bind("<Key>", self.shortcuts)
        self.bind("<Control-O>", self.open_file)
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-S>", self.save_file)
        self.bind("<Control-s>", self.save_file)
        # self.bind('<MouseWheel>', self.OnMouse)

        # self.canvas.event_add('<<Toggle>>>', '<ButtonPress-1>')
        # self.canvas.bind('<<Toggle>>', self.line_pressed)
        # self.canvas.bind('<Double-Button-1>', self.line_pressed)
        # self.height = self.winfo_reqheight()
        # self.width = self.winfo_reqwidth()

    def shortcuts(self, event=None):
        if event == None:
            return
        else:
            c = event.char
            if c == 'a' and c == 'A' and c == 'Ф' and c == 'ф':
                self.show_arrows()
            elif c == '-':
                fsize = self.fontsize
                self.font_decrease()
                scale = float(self.fontsize)/float(fsize)
                for f in self.frames:
                    f.scale = scale
                    f.resize()
                    f.scale = 1
                # self.resize_canvas(scale=scale)
                self.DrawFrames()
            elif c == '+':
                fsize = self.fontsize
                self.font_increase()
                scale = float(self.fontsize)/float(fsize)
                for f in self.frames:
                    f.scale = scale
                    f.resize()
                    f.scale = 1
                # self.resize_canvas(scale=scale)
                self.DrawFrames()

    def font_choice(self):
        pass

    def show_arrows(self, event=None):
        self.drawarrows = not self.drawarrows
        self.DrawFrames()

    def resize_canvas(self, event=None, scale=1):
        # determine the ratio of old width/height to new width/height
        # print('here')
        if event == None:
            wscale = scale
            hscale = scale
            self.canvas.width = self.canvas.winfo_width()*scale
            self.canvas.height = self.canvas.winfo_height()*scale
        else:
            wscale = float(event.width)/self.canvas. winfo_width()
            hscale = float(event.height)/self.canvas.winfo_height()
        # print(f"event {event.width}, {event.height}")
        # print(f"canvas {self.canvas.width}, {self.canvas.height}")
            self.canvas.width = event.width
            self.canvas.height = event.height
        # resize the canvas
        self.canvas.config(width=self.canvas.width, height=self.canvas.height)
        # rescale all the objects tagged with the "all" tag
        self.canvas.scale("all", 0, 0, wscale, hscale)
        self.adjust_frames_position()
        self.DrawFrames()

    def OnMouse(self, event=None):
        self.hscroll.yview("scroll", event.delta, "units")

    def font_increase(self, event=None):
        self.fontsize += 2
        self.font_init()

    def font_decrease(self, event=None):
        if self.fontsize > 2:
            self.fontsize -= 2
        self.font_init()

    def font_init(self, event=None):
        self.ft = tkFont.Font(family=self.fontname, size=self.fontsize)
        self.DrawFrames()

    def save_file(self, event=None):
        filetypes = (('dialogues', '*.kds'), ('All files', '*.*'))
        filename = fd.asksaveasfilename(
            filetypes=filetypes, defaultextension='.kds')
        data = self.pack_data()
        # file,ext = os.path.splitext(filename)
        # if ext == '':
        #     filename=file+'.kds'
        # if os.path.isfile(filename):
        #     if not mb.askokcancel('Rewrite',f"Ok to rewrite the file {filename}?"):
        #         return
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent='\t', ensure_ascii=False)

    def open_file(self, event=None):
        filetypes = (('dialogues', '*.kds'), ('All files', '*.*'))
        filename = fd.askopenfilename(filetypes=filetypes)
        with open(filename) as f:
            data = json.load(f)
        self.unpack_data(data)
        self.DrawFrames()

    def unpack_data(self, data: dict):
        self.fontname = data['fontname']
        self.fontsize = data['fontsize']
        self.width = data['width']
        self.height = data['height']
        for id, f in data['frames'].items():
            self.frames.append(MyFrame(id, f['x'], f['y']))
            self.frames[-1].unpack_data(f)

    def pack_data(self):
        data = {}
        data['fontname'] = self.fontname
        data['fontsize'] = self.fontsize
        data['width'] = self.width
        data['height'] = self.height
        data['frames'] = {}
        for f in self.frames:
            data['frames'][f.id] = f.pack_data()
        return data

    def export_file(self, event=None):
        filetypes = (('dialogues', '*.json'), ('All files', '*.*'))
        filename = fd.asksaveasfilename(filetypes=filetypes)

    def import_file(self, event=None):
        filetypes = (('dialogues', '*.json'), ('All files', '*.*'))
        filename = fd.askopenfilename(filetypes=filetypes)

    def line_pressed(self, e):
        print("click")

    def drag_init(self, event):
        wid_drag = None
        if isinstance(event.widget.master, MyFrame):
            wid_drag = event.widget.master
        elif isinstance(event.widget, MyFrame):
            wid_drag = event.widget
        if wid_drag != None:
            # store the widget that is clicked
            self.dragged_widget = wid_drag
            # ensure dragged widget is ontop
            wid_drag.lift()
            # store the currently mouse position
            self.marked_pointx = self.winfo_pointerx()
            self.marked_pointy = self.winfo_pointery()
        else:
            self.finalize_dragging(event)

    def drag_widget(self, event):
        if (w := self.dragged_widget):  # walrus assignment
            cx, cy = w.winfo_x(), w.winfo_y()  # current x and y
            # deltaX and deltaY to mouse position stored
            dx = self.marked_pointx - self.winfo_pointerx()
            dy = self.marked_pointy - self.winfo_pointery()
            # adjust widget by deltaX and deltaY
            w.place(x=cx-dx, y=cy-dy)
            # update the marked for next iteration
            self.marked_pointx = self.winfo_pointerx()
            self.marked_pointy = self.winfo_pointery()

    def finalize_dragging(self, event=None):
        # default setup
        if isinstance(self.dragged_widget, MyFrame):
            # self.winfo
            # x=self.winfo_x()-self.winfo_rootx()
            # y=self.winfo_y()-self.winfo_rooty()
            self.adjust_frames_position()
            # print(f'mouse coordinates: {event.x}, {event.y}\nglobal coordinates: {x}, {y}')
            # x=event.x
            # y=event.y
            # self.dragged_widget.place(x=x, y=y)
            self.DrawFrames()
            # self.dragged_widget.place_frame(x,y)
        self.dragged_widget = None

    def adjust_frames_position(self, event=None):
        for f in self.frames:
            v = self.vscroll.get()
            h = self.hscroll.get()
            x = self.winfo_pointerx()-self.winfo_rootx() + \
                h[0]*self.winfo_screenwidth()
            y = self.winfo_pointery()-self.winfo_rooty() + \
                v[0]*self.winfo_screenheight()
            x = x - (f.winfo_pointerx()-f.winfo_rootx())
            y = y - (f.winfo_pointery()-f.winfo_rooty())
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            # if x+f.winfo_width() >self.winfo_width() :x=self.winfo_width() -f.winfo_width()
            # if y+f.winfo_height()>self.winfo_height():y=self.winfo_height()-f.winfo_height()
            f.xpos = x
            f.ypos = y

    def DrawFrames(self, e=None):
        for i, w in enumerate(self.frames):
            v = self.vscroll.get()
            h = self.hscroll.get()
            w.offsetx = h[0]*self.winfo_screenwidth()
            w.offsety = v[0]*self.winfo_screenheight()
            w.resize()
            w.place(x=w.xpos-w.offsetx, y=w.ypos-w.offsety)
        self.DrawArrows()
        self.hscroll.lift()
        self.vscroll.lift()

    def DrawArrows(self):
        for i, w in enumerate(self.frames):
            for ar in w.arrows:
                self.canvas.delete(ar)
            w.arrows = []
            if self.drawarrows:
                for j, ch in enumerate(w.choices):
                    tostr = ch.strvars['to'].get()
                    to = None
                    for w1 in self.frames:
                        if w1.id == tostr:
                            to = w1
                            break
                    if to == None:
                        # mb.showwarning('Error!', f'The choice {tostr} of the phrase {w.id} refers to non-existing phrase!')
                        continue
                    elif to == w:
                        # mb.showwarning('Error!', f'The choice {tostr} of the phrase {w.id} refers to itself!')
                        continue
                    else:
                        self.DrawArrow(w, j, to)

    def DrawArrow(self, w1: MyFrame, Choice: int, w2: MyFrame):
        button = w1.choices[Choice].button
        # x1 = w1.xpos+w1.winfo_width()//2
        # y1 = w1.ypos+w1.winfo_height()
        x1 = w1.xpos+button.winfo_x()+button.winfo_width()//2
        y1 = w1.ypos+button.winfo_y()+button.winfo_height()
        x2 = w2.xpos+w2.winfo_width()//2
        y2 = w2.ypos
        # w2.winfo_
        # tmp=""
        tmp = w1.choices[Choice].str['speech']
        tmp = tmp.replace('\n', '')
        tmp = tmp.replace(' ', '')
        if tmp != "":
            dash = None
            width = 1
        else:
            width = 3
            dash = 1
        w1.arrows.append(self.canvas.create_line(
            x1, y1, x2, y2, arrow=tk.LAST, dash=dash, width=width))

        # if w != self.frames[-1]:
        #     w1 = self.frames[i+1]
        #     # x1 = w.winfo_pointerx()-w.winfo_rootx()#+w.winfo_reqwidth()//4
        #     # y1 = w.winfo_pointery()-w.winfo_rooty()+w.winfo_reqheight()
        #     x1 = w.xpos+w.winfo_width()//2
        #     y1 = w.ypos+w.winfo_height()
        #     x2 = w1.xpos+w1.winfo_width()//2
        #     y2 = w1.ypos
        #     w.arrows.append(self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST))
        # self.canvas.lift(w.arrows[-1])

        # w.grid(row=w.ypos*w.nrows, column=w.xpos*w.ncols, rowspan=w.nrows, columnspan=w.ncols)#, sticky='nsew')

    def AddFrame(self, event=None):
        if event == None:
            xpos = 0
            ypos = 0
        else:
            v = self.vscroll.get()
            h = self.hscroll.get()
            offsetx = h[0]*self.winfo_screenwidth()
            offsety = v[0]*self.winfo_screenheight()
            xpos = event.x+offsetx
            ypos = event.y+offsety
        # coords = [[],[]]
        # if len(self.frames) != 0:
        #     for w in self.frames:
        #         coords[0].append(w.xpos)
        #         coords[1].append(w.ypos)
        #     if not 0 in coords[1]:
        #         xpos=0
        #         ypos=0
        #     else:
        #         xmax = 0
        #         for i in range(len(coords[1])):
        #             y=coords[1][i]
        #             x=coords[0][i]
        #             if y == 0 and x>xmax:
        #                 xmax=x
        #         xpos = xmax+1
        frameId = 0
        for frameId in range(frameIdMax):
            IdFound = False
            for f in self.frames:
                if f.id == str(frameId):
                    IdFound = True
            if not IdFound:
                break

        self.frames.append(MyFrame(str(frameId), xpos, ypos))
        self.DrawFrames()
        # print("command")


if __name__ == "__main__":

    app = App()
    app.mainloop()

# def drag_widget(event):
#     if (w:=root.dragged_widget): #walrus assignment
#         cx,cy = w.winfo_x(), w.winfo_y() #current x and y
#         #deltaX and deltaY to mouse position stored
#         dx = root.marked_pointx - root.winfo_pointerx()
#         dy = root.marked_pointy - root.winfo_pointery()
#         #adjust widget by deltaX and deltaY
#         w.place(x=cx-dx, y=cy-dy)
#         #update the marked for next iteration
#         root.marked_pointx = root.winfo_pointerx()
#         root.marked_pointy = root.winfo_pointery()

# def drag_init(event):
#     if event.widget is not root:
#         #store the widget that is clicked
#         root.dragged_widget = event.widget
#         #ensure dragged widget is ontop
#         event.widget.lift()
#         #store the currently mouse position
#         root.marked_pointx = root.winfo_pointerx()
#         root.marked_pointy = root.winfo_pointery()

# def finalize_dragging(event):
#     #default setup
#     root.dragged_widget = None

# root = tk.Tk()
# #name and register some events to some sequences
# root.event_add('<<Drag>>', '<B1-Motion>')
# root.event_add('<<DragInit>>', '<ButtonPress-1>')
# root.event_add('<<DragFinal>>', '<ButtonRelease-1>')
# #bind named events to the functions that shall be executed
# root.bind('<<DragInit>>', drag_init)
# root.bind('<<Drag>>', drag_widget)
# root.bind('<<DragFinal>>', finalize_dragging)
# #fire the finalizer of dragging for setup
# root.event_generate('<<DragFinal>>')
# #populate the window
# for color in ['yellow','red','green','orange']:
#     tk.Label(root, text="test",bg=color).pack()

# root.mainloop()


class TestFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        list_of_options = ["first option", "second option",
                           "third option", "forth option"]
        first_option = tk.StringVar(self)
        first_option.set(list_of_options[0])

        tk.Label(self, text="Test Label 1").grid(row=0, column=0)
        tk.Entry(self, bd=5).grid(row=0, column=1)
        tk.Label(self, text="Test Label 2").grid(row=0, column=2)
        tk.Entry(self, bd=5).grid(row=0, column=3)
        tk.Label(self, text="Test check button 1").grid(row=2, column=0)
        tk.Checkbutton(self, bd=5).grid(row=2, column=1)
        tk.Label(self, text="Test check button 2").grid(row=2, column=2)
        tk.Checkbutton(self, bd=5).grid(row=2, column=3)
        tk.Label(self, text="Test drop down 1").grid(row=3, column=0)
        tk.OptionMenu(self, first_option, *
                      list_of_options).grid(row=3, column=1)


class TestMainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Application")

        for r in range(3):
            self.rowconfigure(r, weight=1)
        for c in range(8):
            self.columnconfigure(c, weight=1)

        self.testFrame1 = TestFrame()
        self.testFrame2 = TestFrame()
        self.testFrame3 = TestFrame()
        self.testFrame4 = TestFrame()
        self.testFrame1.grid(row=0, column=0, rowspan=3,
                             columnspan=3, sticky='nsew')
        self.testFrame1.pack()
        self.testFrame2.grid(row=3, column=0, rowspan=3,
                             columnspan=3, sticky='nsew')
        self.testFrame3.grid(row=0, column=3, rowspan=2,
                             columnspan=3, sticky='nsew')
        self.testFrame4.grid(row=2, column=3, rowspan=4,
                             columnspan=3, sticky='nsew')
        self.testFrame4.pack()


# TestMainApplication().mainloop()


class BigScreen:

    def __init__(self):
        self.root = tk.Tk()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, scrollregion=f"0 0 {w*2} {h*2}")
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.makescroll(self.root, self.canvas)

        self.imagename = fido.askopenfilename(title="Pick Image to View")
        if self.imagename:
            self.photo = tk.PhotoImage(file=self.imagename).zoom(2, 2)
            self.window = self.canvas.create_image(
                (0, 0), anchor=tk.NW, image=self.photo)

        self.root.bind("<Escape>", self.closer)
        # self.root.wm_attributes("-fullscreen", 1)
        # self.root.wm_attributes("-top", 1)

    def makescroll(self, parent, thing):
        v = tk.Scrollbar(parent, orient=tk.VERTICAL, command=thing.yview)
        v.grid(row=0, column=1, sticky=tk.NS)
        thing.config(yscrollcommand=v.set)
        h = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=thing.xview)
        h.grid(row=1, column=0, sticky=tk.EW)
        thing.config(xscrollcommand=h.set)

    def closer(self, ev):
        self.root.destroy()


if __name__ == "____":
    Big = BigScreen()
    Big.root.mainloop()
