import tkinter as tk
from .. import ShiftingBloomFilter
from collections import OrderedDict
class COLOR_PALLETTE:
    GREEN = "#baffc9"
    BLUE = "#b8f1fd"
    ORANGE = "#ffe2be"
    PINK = "#fbbdff"
    PURPLE = "#bbbcfd"
    RED = "#ffa1a1"
    BIGHT_GREEN = "#8ec127"
    YELLOW = "#fbb40c"

class DLabel(tk.Label):
    def __init__(self,*args,**kwargs):
        self.strvar = tk.StringVar()
        if "initial_value" in kwargs:
            self.set(kwargs["initial_value"])
            kwargs.pop("initial_value")
        super().__init__(*args,**kwargs)
        self["textvariable"] = self.strvar

    def set(self,s):
        self.strvar.set(str(s))

    def get(self):
        self.strvar.get()

class Info(tk.Frame):
        def __init__(self,master,
                     color_description=OrderedDict([
                        (COLOR_PALLETTE.GREEN , "Empty field"),
                        #(COLOR_PALLETTE.BLUE  , "Empty field"),
                        (COLOR_PALLETTE.RED   , "Field occupied"),
                        (COLOR_PALLETTE.ORANGE, "Field occupied by offset bit"),
                        (COLOR_PALLETTE.YELLOW, "Field set"),
                        (COLOR_PALLETTE.PURPLE, "Field set by offset bit")
                        ])):
            super().__init__(master,borderwidth=2,relief="groove")
            for row,key in enumerate(color_description):
                l = DLabel(self,background=key,
                                initial_value=color_description[key])
                l.grid(row=row,sticky=tk.W+tk.E)

class Out(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.output_label = DLabel(self)
        self.output_label.grid(row=0, sticky=tk.W+tk.E)

    def set_out(self,out_s):
        self.output_label.set(out_s)

class Filter(tk.Frame):
    def __init__(self,master,out=None,length=25):
        super().__init__(master, borderwidth=2, relief="sunken")
        self.length = length
        self.bloom = ShiftingBloomFilter(length=length)
        self.cells = []
        self.entry = tk.Entry(self)
        self.out = out
        self.entry.grid(row=1,columnspan=length,sticky=tk.S+tk.N)
        self.insert = tk.Button(self,text="Insert",command=self._insert)
        self.check = tk.Button(self,text="Check",command=self._check)
        self.clear = tk.Button(self,text="Clear",command=self._clear)
        self.insert.grid(row=2,columnspan=length//3,sticky=tk.S)
        self.check.grid(row=2,column=length//3,columnspan=length//3,sticky=tk.S)
        self.clear.grid(row=2,column=2*length//3,columnspan=length//3,
                                                                sticky=tk.S)
        for i in range(length):
            color = COLOR_PALLETTE.GREEN
            #if i > self.bloom.cut_off:
            #    color = COLOR_PALLETTE.BLUE
            label = DLabel(self, background=color,initial_value=0)
            label.grid(row=0,column=i)
            self.cells.append(label)

    def refresh(self):
        for i in range(self.length):
            if self.bloom.filter[i] == 1:
                self._set_cell(i)

    def _set_cell(self,cell_id,to=1,
                  bg=(COLOR_PALLETTE.RED,COLOR_PALLETTE.ORANGE)):
        bg, aftercut = bg
        if cell_id > self.bloom.cut_off:
            bg = aftercut
        self.cells[cell_id].set(to)
        self.cells[cell_id].config(bg=bg)

    def _insert(self):
        self.bloom.insert(self.entry.get())
        self.refresh()

    def _clear(self):
        self.bloom = ShiftingBloomFilter(self.length)
        for i in range(self.length):
            self._set_cell(i,to=0,bg=(COLOR_PALLETTE.GREEN,COLOR_PALLETTE.BLUE))

    def _check(self):
        self.refresh()
        is_in, sets = self.bloom.check(self.entry.get())
        self.out.set_out("Item is %sin the set" % ("" if is_in else "not "))
        if is_in:
            hash_func = self.bloom.hashfunc
            cut_off = self.bloom.cut_off
            for h in hash_func[:cut_off]:
                self._set_cell(self.bloom._get_hash(h,self.entry.get(),0),
                           bg=(COLOR_PALLETTE.YELLOW,COLOR_PALLETTE.YELLOW))
            for h in hash_func[cut_off:]:
                for i in range(self.bloom.max_set+1):
                    self._set_cell(self.bloom._get_hash(h,self.entry.get(),i),
                           bg=(COLOR_PALLETTE.PURPLE,COLOR_PALLETTE.PURPLE))


class Main(tk.Tk):
    def __init__(self,title="ShiftingBloomFilter Visualiser",length=25):
        super().__init__()
        self.title(title)
        self.out = Out(self)
        self.filter = Filter(self,out=self.out,length=length)
        self.info = Info(self)
        self.filter.grid(row=0,column=1,sticky=tk.N+tk.S)
        self.info.grid(row=0,column=0)
        self.out.grid(row=1,columnspan=2)
        self.resizable(False,False)

    @staticmethod
    def run(title="ShiftingBloomFilter Visualiser",length=25):
        window = Main(title,length)
        window.mainloop()

