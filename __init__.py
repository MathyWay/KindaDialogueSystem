import tkinter as tk
# from tkinter import tix
import tkinter.font as tkFont
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText as sc
from tkinter import messagebox as mb
frameIdMax = 1000
class MyFrame(tk.Frame):
    nrows = 4
    ncols = 3
    def __init__ (self, id, xpos, ypos):
        super().__init__(borderwidth=1,highlightbackground="black",highlightthickness=1)
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
        scale = self.master.fontsize/10
        self.content = {}
        # self.config(yscrollcommand = self.master.vscroll.set)
        # self.config(xscrollcommand = self.master.hscroll.set)

        # self.canvas = tk.Canvas(self)
        # self.canvas.pack()
        self.content['label'     ] = tk.Label(self, text="phrase " + self.id, font=ft)
        self.content['label'     ].grid(column=1, row=0)
        self.content['speech_lb' ] = tk.Label(self, text="speech: ", font=ft)
        self.content['speech_lb' ].grid(column=0, row=1)
        self.content['speech'    ] = sc(self, wrap=tk.WORD, width=int(10*scale), height=3, font=ft)
        self.content['speech'    ].grid(column=1, row=1)
        self.content['orator_lb' ] = tk.Label(self, text="orator: ", font=ft)
        self.content['orator_lb' ].grid(column=0, row=2)
        self.content['orator'    ] = tk.Entry(self,width=int(10*scale), font=ft)  
        self.content['orator'    ].grid(column=1, row=2)
        self.content['destructor'] = tk.Button(self, font=ft)
        self.content['destructor']['text'] = 'x'
        self.content['destructor'].grid(column=0,row=0)
        self.content['destructor']["command"] = self.remove

        self.content['addbutton' ] = tk.Button(self, font=ft)
        self.content['addbutton' ]['text'] = '+'

        # self.create_line
    def resize(self):
        if len(self.content) > 0:
            for key, val in self.content.items():
                val.configure(font=self.master.ft)
    def remove(self):
        if mb.askyesno(title='Warning', message = 'Do you wish to delete phrase '+self.id+'?'):
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
        tmp = self.location(x,y)
        self.xpos = tmp[0]
        self.ypos = tmp[1]
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #setting title
        self.title("undefined")
        #setting window size
        self.width=1000
        self.height=500
        self.frames = []
        self.dragged_widget = None
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.geometry(alignstr)
        self.resizable(width=True, height=True)
        self.drawarrows = True
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        # self.attributes("-fullscreen", False)

        self.fontsize = 12
        self.fontname = 'Calibri'

        self.canvas = tk.Canvas(self, width = screenwidth, height=screenheight, scrollregion =  f"0 0 {screenwidth} {screenheight}")
        self.canvas.height = self.canvas.winfo_reqheight()
        self.canvas.width = self.canvas.winfo_reqwidth()
        self.canvas.grid(row = 0, column = 0, sticky = tk.NSEW)#pack(side=tk.LEFT, fill = tk.BOTH)
        # self.makescroll(self, self.canvas )
        self.makescroll(self,self.canvas)

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
        # GButton_457["font"] = ft
        # GButton_457["fg"] = "#000000"
        # GButton_457["justify"] = "center"
        # GButton_457["text"] = "Button"
        # GButton_457.place(x=170,y=100,width=70,height=25)
        # GButton_457["command"] = self.AddFrame

    def makescroll(self, parent, thing):
        self.vscroll = tk.Scrollbar(parent, orient = tk.VERTICAL, command = thing.yview)
        self.vscroll.grid(row = 0, column = 1, sticky = tk.NS)
        thing.config(yscrollcommand = self.vscroll.set)
        self.vscroll.bind('<ButtonPress-1>', self.DrawFrames)

        self.hscroll = tk.Scrollbar(parent, orient = tk.HORIZONTAL, command = thing.xview)
        self.hscroll.grid(row = 1, column = 0, sticky = tk.EW)
        thing.config(xscrollcommand = self.hscroll.set)
        self.hscroll.bind('<ButtonPress-1>', self.DrawFrames)
    def menu_init(self):
        self.menubar = tk.Menu()
        self.config(menu=self.menubar)
        self.menubar.add_command(label='save',command=self.save_file)
        self.menubar.add_command(label='load',command=self.open_file, accelerator="Ctrl+O")
        self.menubar.add_command(label='hide/show arrows',command=self.show_arrows)
        self.menubar.add_command(label='new phrase',command=self.AddFrame)
        self.font_bar = tk.Menu(self.menubar)
        self.font_bar.add_command(label='+', command=self.font_increase)
        self.font_bar.add_command(label='-', command=self.font_decrease)
        self.menubar.add_cascade(label = 'Font', menu=self.font_bar, underline = 0)
        # self.menubar.add_command(label='Exit',command=self.destroy)
    def keybinds (self):
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
        self.bind('<MouseWheel>', self.OnMouse)
        

        # self.canvas.event_add('<<Toggle>>>', '<ButtonPress-1>')
        # self.canvas.bind('<<Toggle>>', self.line_pressed)
        # self.canvas.bind('<Double-Button-1>', self.line_pressed)
        # self.height = self.winfo_reqheight()
        # self.width = self.winfo_reqwidth()
    def shortcuts(self, event = None):
        if event == None:
            return
        else:
            c=event.char
            if c == 'a' and c == 'A' and c == 'Ф' and c == 'ф':
                self.show_arrows()
            elif c == '-':
                self.font_decrease()
            elif c == '+':
                self.font_increase()
    def show_arrows(self, event=None):
        self.drawarrows=not self.drawarrows
        self.DrawFrames()
    def resize_canvas(self,event):
        # determine the ratio of old width/height to new width/height
        # print('here')
        wscale = float(event.width)/self.canvas.width
        hscale = float(event.height)/self.canvas.height
        # print(f"event {event.width}, {event.height}")
        # print(f"canvas {self.canvas.width}, {self.canvas.height}")
        self.canvas.width = event.width
        self.canvas.height = event.height
        # resize the canvas 
        self.canvas.config(width=self.canvas.width, height=self.canvas.height)
        # rescale all the objects tagged with the "all" tag
        self.canvas.scale("all",0,0,wscale,hscale)
        self.adjust_frames_position()
        self.DrawFrames()
    def OnMouse(self, event=None):
        self.hscroll.yview("scroll", event.delta, "units")
    def font_increase(self,event=None):
        self.fontsize += 2
        self.font_init()
    def font_decrease(self,event=None):
        if self.fontsize > 2:
            self.fontsize -= 2
        self.font_init()
    def font_init(self, event=None):
        self.ft = tkFont.Font(family=self.fontname,size=self.fontsize)
        self.DrawFrames()
    def save_file(self, event = None):
        filetypes = (('dialogues', '*.json'),('All files', '*.*'))
        filename = fd.asksaveasfilename(filetypes=filetypes)
    def open_file(self, event=None):
        filetypes = (('dialogues', '*.json'),('All files', '*.*'))
        filename = fd.askopenfilename(filetypes=filetypes)
    def line_pressed(self, e):
        print("click")
    def drag_init(self, event):
        wid_drag = event.widget.master 
        if wid_drag is not self:
            #store the widget that is clicked
            self.dragged_widget = wid_drag
            #ensure dragged widget is ontop
            if isinstance (wid_drag, MyFrame):
                wid_drag.lift()
                #store the currently mouse position
                self.marked_pointx = self.winfo_pointerx()
                self.marked_pointy = self.winfo_pointery()
            else:
                self.finalize_dragging(event)
    def drag_widget(self, event):
        if (w:=self.dragged_widget): #walrus assignment
            cx,cy = w.winfo_x(), w.winfo_y() #current x and y
            #deltaX and deltaY to mouse position stored
            dx = self.marked_pointx - self.winfo_pointerx()
            dy = self.marked_pointy - self.winfo_pointery()
            #adjust widget by deltaX and deltaY
            w.place(x=cx-dx, y=cy-dy)
            #update the marked for next iteration
            self.marked_pointx = self.winfo_pointerx()
            self.marked_pointy = self.winfo_pointery()
    def finalize_dragging(self, event=None):
        #default setup
        if isinstance (self.dragged_widget, MyFrame):
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
            x=self.winfo_pointerx()-self.winfo_rootx()+h[0]*self.winfo_screenwidth()
            y=self.winfo_pointery()-self.winfo_rooty()+v[0]*self.winfo_screenheight()
            x = x - (f.winfo_pointerx()-f.winfo_rootx())
            y = y - (f.winfo_pointery()-f.winfo_rooty())
            # if x<0:x=0
            # if y<0:y=0
            # if x+f.winfo_width() >self.winfo_width() :x=self.winfo_width() -f.winfo_width()
            # if y+f.winfo_height()>self.winfo_height():y=self.winfo_height()-f.winfo_height()
            f.xpos=x
            f.ypos=y
    def DrawFrames(self, e=None):
        for i, w in enumerate (self.frames):
            v = self.vscroll.get()
            h = self.hscroll.get()
            tmp=self.canvas.winfo_x()
            w.offsetx = h[0]*self.winfo_screenwidth()
            w.offsety = v[0]*self.winfo_screenheight()
            w.resize()
            w.place(x=w.xpos-w.offsetx, y=w.ypos-w.offsety)
        self.DrawArrows()
    def DrawArrows(self):
        for i, w in enumerate (self.frames):
            for ar in w.arrows:
                self.canvas.delete(ar)
            w.arrows = []
            if self.drawarrows:
                if w != self.frames[-1]:
                    w1 = self.frames[i+1]
                    # x1 = w.winfo_pointerx()-w.winfo_rootx()#+w.winfo_reqwidth()//4
                    # y1 = w.winfo_pointery()-w.winfo_rooty()+w.winfo_reqheight()
                    x1 = w.xpos+w.winfo_width()//2
                    y1 = w.ypos+w.winfo_height()
                    x2 = w1.xpos+w1.winfo_width()//2
                    y2 = w1.ypos
                    w.arrows.append(self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST))

            # w.grid(row=w.ypos*w.nrows, column=w.xpos*w.ncols, rowspan=w.nrows, columnspan=w.ncols)#, sticky='nsew')
    def AddFrame(self, event = None):
        if event == None:
            xpos=0
            ypos=0
        else:
            xpos = event.x
            ypos = event.y
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


import tkinter as tk


class TestFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        list_of_options = ["first option", "second option", "third option", "forth option"]
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
        tk.OptionMenu(self, first_option, *list_of_options).grid(row=3, column=1)


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
        self.testFrame1.grid(row=0, column=0, rowspan=3, columnspan=3, sticky='nsew')
        self.testFrame1.pack()
        self.testFrame2.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='nsew')
        self.testFrame3.grid(row=0, column=3, rowspan=2, columnspan=3, sticky='nsew')
        self.testFrame4.grid(row=2, column=3, rowspan=4, columnspan=3, sticky='nsew')
        self.testFrame4.pack()


# TestMainApplication().mainloop()

import tkinter as tk
from tkinter import filedialog as fido

class BigScreen:

    def __init__( self ):
        self.root = tk.Tk()
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, scrollregion = f"0 0 {w*2} {h*2}")
        self.canvas.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.makescroll(self.root, self.canvas )

        self.imagename = fido.askopenfilename( title = "Pick Image to View" )
        if self.imagename:
            self.photo = tk.PhotoImage(file = self.imagename).zoom(2, 2)
            self.window = self.canvas.create_image(
                ( 0, 0 ), anchor = tk.NW, image = self.photo)

        self.root.bind("<Escape>", self.closer)
        # self.root.wm_attributes("-fullscreen", 1)
        # self.root.wm_attributes("-top", 1)

    def makescroll(self, parent, thing):
        v = tk.Scrollbar(parent, orient = tk.VERTICAL, command = thing.yview)
        v.grid(row = 0, column = 1, sticky = tk.NS)
        thing.config(yscrollcommand = v.set)
        h = tk.Scrollbar(parent, orient = tk.HORIZONTAL, command = thing.xview)
        h.grid(row = 1, column = 0, sticky = tk.EW)
        thing.config(xscrollcommand = h.set)

    def closer(self, ev):
        self.root.destroy()

if __name__ == "____":
    Big = BigScreen()
    Big.root.mainloop()