#!/usr/bin/env python3
"""
    Implements a GUI visualiser for shifting bloom filter

    Subclasses:
    - COLOR_PALLETTE => Constants with hex codes for colors used in visualiser.
    - DLabel => tkinter label bound to tkinter StringVar.
    - Info => Frame for displaying information and descriptions.
    - Out => Frame for displaying output messages
    - Filter => Frame representing the ShiftingBloomFilter
    - Main => Main window of visuliser, contains static method run
"""

import tkinter as tk
from collections import OrderedDict
import copy
from .. import ShiftingBloomFilter
from .. import utils
from .. import MULTIPLE

class COLOR_PALLETTE:
    """
        COLOR PALLETTE for visualiser gui.
        Colors defined as constants using hex color codes
    """

    GREEN = "#baffc9"
    BLUE = "#b8f1fd"
    ORANGE = "#ffe2be"
    PINK = "#fbbdff"
    PURPLE = "#bbbcfd"
    RED = "#ffa1a1"
    BIGHT_GREEN = "#8ec127"
    YELLOW = "#fbb40c"


class DLabel(tk.Label):
    """
        tk.Label bound to StringVar
    """

    def __init__(self, *args, **kwargs):
        """
            DLabel(
                [initial_value] => create a label with this text
            )
        """

        self.strvar = tk.StringVar()
        if "initial_value" in kwargs:
            self.set(kwargs["initial_value"])
            kwargs.pop("initial_value")
        super().__init__(*args, **kwargs)
        self["textvariable"] = self.strvar

    def set(self, value):
        """
            (void) set the value of StringVar to s
            set(
                value => change label to s
            )
        """
        self.strvar.set(str(value))

    def get(self):
        """
           (string) returns string represented in the label
        """
        self.strvar.get()


class Info(tk.Frame):
    """
        Frame for displaying informations and descriptions.
    """

    def __init__(self, master, options,
                 color_description=OrderedDict([
                     (COLOR_PALLETTE.GREEN , "Empty field"),
                     (COLOR_PALLETTE.RED   , "Field occupied by offset bit"),
                     (COLOR_PALLETTE.ORANGE, "Field occupied"),
                     (COLOR_PALLETTE.YELLOW, "Field set"),
                     (COLOR_PALLETTE.PURPLE, "Field set by offset bit")
                 ])):
        """
            Info(
                master => parent window
                options => (tk.BooleanVar) option variables for checkboxes
                color_description => dict of color codes (key) and
                                                        descriptions (values)
            )
        """

        super().__init__(master, borderwidth=2, relief="groove")
        self.options = options

        for row, key in enumerate(color_description):
            label = DLabel(self, background=key, initial_value=color_description[key])
            label.grid(column=1, row=row, sticky=tk.W+tk.E)
            if key == COLOR_PALLETTE.GREEN:
                continue
            check_box = tk.Checkbutton(self, variable=self.options[key],
                                       command=master.filter.refresh)
            check_box.grid(column=0, row=row)


class Out(tk.Frame):
    """
        Output frame for displaying output messages
    """

    def __init__(self, master):
        """
            Out(
                master => parent window
            )
        """
        super().__init__(master)
        self.output_label = DLabel(self)
        self.output_label.grid(row=0, sticky=tk.W+tk.E)

    def set_out(self, out_s):
        """
            (void) sets the output field to display given message
            set_out(
                out_s => message to display
            )
        """
        self.output_label.set(out_s)


class Filter(tk.Frame):
    """
        Frame containg and displaying the filter.
    """

    DEFAULT_BACKGROUND = (COLOR_PALLETTE.RED, COLOR_PALLETTE.ORANGE)

    def __init__(self, master, out, options, length=25, hash_source=None,
                 hash_count=None, bloom=None, deepcopy=True, mode=MULTIPLE,
                 no_sets=10):
        """
            Filter(
                master => parent window
                out    => message output frame
                options => (tk.BooleanVar) variables for options (readonly)
                length => length of the filter to create and display
                hash_source => specify other than default hash source,
                                        requires hash_count to be specifed too
                hash_count => specify amount of hases in the source
                bloom => use existing bloom filter instead, requires
                                            ShiftingBloomFilter object
                deepcopy => when using existing bloom filter, should visualiser
                                                            work on a deepcopy
                mode=> mode of work for ShiftingBloomFilter
                no_sets => if multiple sets, number of sets
            )
        """

        super().__init__(master, borderwidth=2, relief="sunken")
        self.length = length
        self.options = options

        if bloom is not None:
            self.length = len(bloom)
            def _construct_bloom():
                return copy.deepcopy(bloom) if deepcopy else bloom
        elif hash_source and hash_count:
            def _construct_bloom():
                return ShiftingBloomFilter(length=length,
                                           hash_source=hash_source,
                                           hash_count=hash_count,
                                           length_as_power=False,
                                           mode=mode)
        else:
            def _construct_bloom():
                return ShiftingBloomFilter(length=length, length_as_power=False,
                                           mode=mode
                                          )
        columnspan = length//4
        self.mode = mode
        if self.mode:
            self.selection_var = tk.StringVar(self)
            self.selection_var.set(0)
            self.sets = [set() for _ in range(no_sets)]
        else:
            self.sets = []
            columnspan = length//3
        self.no_sets = no_sets
        self._construct_bloom = _construct_bloom
        self.bloom = self._construct_bloom()
        self.cells = []
        self.entry = tk.Entry(self)
        self.out = out
        self.entry.grid(row=1, columnspan=length, sticky=tk.S+tk.N)
        self.controls = []
        self.controls.append(tk.Button(self, text="Insert", command=self._insert))
        if self.mode:
            self.controls.append(tk.OptionMenu(self, self.selection_var,
                                    *[str(i) for i, j in enumerate(self.sets)]
                                ))
        self.controls.append(tk.Button(self, text="Check", command=self._check))
        self.controls.append(tk.Button(self, text="Clear", command=self._clear))
        for i, j in enumerate(self.controls):
            j.grid(row=2, column=i*columnspan, columnspan=columnspan, sticky=tk.S)
        self.string_generator = utils.RandomStringGenerator(string_length=...)
        self.generate_button = tk.Button(self, text="Generate random element",
                                         command=self._generate_string)
        self.generate_button.grid(row=3, columnspan=length)
        for i, value in enumerate(self.bloom):
            color = COLOR_PALLETTE.GREEN
            label = DLabel(self, background=color, initial_value=value)
            label.grid(row=0, column=i)
            self.cells.append(label)
        self.currrent_element = None

    def refresh(self):
        """
            (void) refreshes (resets) the display of the filter
        """
        for i, v in enumerate(self.bloom):
            self._set_cell(i, v, (COLOR_PALLETTE.GREEN, COLOR_PALLETTE.GREEN))
        for i, value in enumerate(self.bloom):
            if value == 1:
                self._set_cell(i)

    def _get_aftercut_hashes(self, element):
        """
            [(int)] returns positions of hash offsets for element
        """
        return [self.bloom._get_hash(func, element,0)
                for func in self.bloom.hashfunc[self.bloom.cut_off:]
               ]

    def _set_cell(self, cell_id, value=1,
                  background=DEFAULT_BACKGROUND):
        """
            (void) sets cell in bloom filter display
            _set_cell(
                cell_id => cell index to change
                value      => value to change the cell to
                background => tuple of color codes to use for highlighting
            )
        """
        acut = None
        if background is Filter.DEFAULT_BACKGROUND:
            acut = []
            for i in self.sets:
                if not self.mode:
                    acut += self._get_aftercut_hashes(i)
                    continue
                for j in i:
                    acut += self._get_aftercut_hashes(j)
        elif self.current_element:
            acut = self._get_aftercut_hashes(self.current_element)
        background, aftercut = background
        if acut and cell_id in acut:
            background = aftercut
        if not self.options[background].get():
            background = COLOR_PALLETTE.GREEN
        self.cells[cell_id].set(value)
        self.cells[cell_id].config(bg=background)

    def _insert(self):
        """
            (callback) (void)
            Insert value from entry field into the bloom filter and refresh
            the display.
        """
        self.current_element = self.entry.get()
        if self.mode:
            set_id = int(self.selection_var.get())
            self.master.sets.var.set(set_id)
            self.sets[set_id].add(self.current_element)
            self.bloom.insert(self.current_element, set_id)
        else:
            self.sets.append(self.current_element)
            self.bloom.insert(self.current_element)
        self.refresh()
        self.master.sets.display_set()

    def _clear(self):
        """
            (callback) (void)
            Clears the Bloom Filter and the display of it.
        """
        if self.mode:
            self.sets = [set() for _ in range(self.no_sets)]
        else:
            self.sets = []
        self.current_element = None
        self.bloom = self._construct_bloom()
        for i, value in enumerate(self.bloom):
            self._set_cell(i, value=value, background=(COLOR_PALLETTE.GREEN,
                                                       COLOR_PALLETTE.GREEN))
        self.master.sets.display_set()

    def _check(self):
        """
            (callback) (void)
            Checks if item stored in entry label is in the set, and if it is
            highlights the bits belonging to the item.
        """

        self.refresh()
        self.current_element = self.entry.get()
        is_in, set_ids = self.bloom.check(self.current_element)
        self.out.set_out("Item is %sin the set. %s" % (("" if is_in else "not "),
                ("" if self.mode else "There are %i copies of element" % set_ids)
        ))
        self.master.sets.highlight(set_ids, self.current_element)
        if is_in:
            hash_func = self.bloom.hashfunc
            cut_off = self.bloom.cut_off
            for hash_fn in hash_func[:cut_off]:
                self._set_cell(self.bloom._get_hash(hash_fn, self.entry.get(), 0),
                               background=(COLOR_PALLETTE.YELLOW, COLOR_PALLETTE.YELLOW))
            for hash_fn in hash_func[cut_off:]:
                for i in range(self.bloom.max_set+1):
                    self._set_cell(self.bloom._get_hash(hash_fn, self.entry.get(), i),
                           background=(COLOR_PALLETTE.PURPLE, COLOR_PALLETTE.PURPLE))

    def _generate_string(self):
        """
            (callback) (void)
            Generates a random string and inserts it into entry field
        """
        self.entry.delete(0, tk.END)
        self.entry.insert(0, next(self.string_generator))

class SetDisplay(tk.Frame):
    """
        Frame containing contents of sets that are represented by filter.
    """
    def __init__(self, master, *args):
        """
            SetDisplay(
                master => parent window
                *args => any other tk.Frame config arguments
            )
        """
        super().__init__(master, *args)
        self.master = master
        self.sets = master.filter.sets
        self.var = tk.StringVar(self)
        self.var.set(0)
        if master.mode:
            self.menu = tk.OptionMenu(self, self.var,
            *[str(i) for i,j in enumerate(self.sets)],command=self.display_set
            )
            self.menu.grid(columnspan=2,sticky=tk.W+tk.E)
        self.list = None

    def highlight(self, set_no, element):
        """
            (void) highlights element in set_no unless MULTISET mode,
            then higlights elements corresponding to element

            highlight(
                set_no => set to display
                element => element to highlight
            )
        """
        if set_no and self.master.mode:
            set_no = set_no[0] if int(self.var.get()) not in set_no else self.var.get()
            self.var.set(set_no)
            self.display_set()
        elif set_no:
            self.display_set()
        else:
            self.clear_selection()
            return
        items = self.list.get(0, self.list.size())
        for i, j in enumerate(items):
            if j == element:
                self.list.selection_set(i)

    def clear_selection(self):
        """
            (void) Clears active selection of element
        """
        if self.list:
            self.list.selection_clear(0, tk.END)
    
    def display_set(self, *args):
        """
            (void) displays elements, that are in currently selected set (if MULIPLE mode)
            or just the MULTISET
        """
        self.sets = self.master.filter.sets
        if self.list:
            self.list.grid_forget()
        self.list = tk.Listbox()
        self.list.bindtags((self.list, self.master, "all"))
        if self.master.mode:
            id = int(self.var.get())
            self.sets = self.sets[id]
        for elem in self.sets:
            self.list.insert(tk.END, elem)
        self.list.grid(columnspan=2, sticky=tk.W+tk.E)

class Main(tk.Tk):
    """
        Main window of Visualiser
    """

    def __init__(self, title="ShiftingBloomFilter Visualiser", length=25,
                 hash_count=None, hash_source=None, bloom=None, deepcopy=True,
                 mode=MULTIPLE, no_sets=10):
        """
            Main(
                title  => title for visualiser window
                length => length of the filter
                hash_count => number of hashing functions to use
                hash_source=> source of hash functions
                bloom => use existing bloom filter instead.
                deepcopy => work on copy of a given bloom filter.
            )
        """

        super().__init__()
        self.options = OrderedDict([(COLOR_PALLETTE.GREEN , tk.BooleanVar()),
                                    (COLOR_PALLETTE.RED   , tk.BooleanVar()),
                                    (COLOR_PALLETTE.ORANGE, tk.BooleanVar()),
                                    (COLOR_PALLETTE.YELLOW, tk.BooleanVar()),
                                    (COLOR_PALLETTE.PURPLE, tk.BooleanVar())
                       ])
        self.title(title)
        self.mode = mode
        self.out = Out(self)
        self.filter = Filter(self, out=self.out, options=self.options,
                             length=length, hash_source=hash_source,
                             hash_count=hash_count, bloom=bloom,
                             deepcopy=deepcopy, mode=mode, no_sets=no_sets)
        self.info = Info(self, options=self.options)
        self.sets = SetDisplay(self)
        self.filter.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.info.grid(row=0, column=0)
        self.out.grid(row=1, columnspan=2)
        self.sets.grid(row=2, columnspan=2, sticky=tk.W+tk.E)
        self.resizable(False, False)

    @staticmethod
    def run(title="ShiftingBloomFilter Visualiser", length=25, mode=MULTIPLE):
        """
            (static) (void)
            Instanciates main window of visualiser and runs it.

        """
        window = Main(title, length, mode=mode)
        window.mainloop()
