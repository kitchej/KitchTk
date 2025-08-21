import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tk_font

class FontChooserWidget:
    """Widget for choosing a font"""
    def __init__(self, parent, current_font=None, font_list=None):
        self.parent = parent
        self.chosen_font = tk.StringVar()
        self.chosen_font.set("")
        if font_list is None:
            self.font_list = sorted(set(tk_font.families()))
        else:
            self.font_list = font_list
        self.font_box = tk.Listbox(self.parent, takefocus=1, exportselection=0)
        for font in self.font_list:
            self.font_box.insert(tk.END, font)

        self.scrollbar = ttk.Scrollbar(self.font_box)
        self.scrollbar.configure(command=self.font_box.yview)
        self.font_box.configure(yscrollcommand=self.scrollbar.set)

        self.preview_frame = tk.Frame(self.parent, width=50, height=5)
        self.preview_frame.pack_propagate(False)
        self.preview = tk.Text(self.preview_frame, wrap=tk.WORD)
        self.preview.pack(fill=tk.BOTH, expand=True)
        self.preview.insert(0.0, "Preview text. This box is editable, feel free to type anything.")

        self.confirm = ttk.Button(self.parent, text="Confirm", command=self.get_font)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.confirm.pack(side=tk.BOTTOM, pady=5)
        self.font_box.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.preview_frame.pack(expand=True, fill=tk.BOTH)

        try:
            curr_font_index = self.font_list.index(current_font)
        except ValueError:
            curr_font_index = 0
        self.font_box.select_set(curr_font_index)
        self.font_box.activate(curr_font_index)
        self.font_box.see(curr_font_index)
        self.font_box.focus_set()
        self.preview.configure(font=self.font_box.get(curr_font_index))

        self.parent.bind("<Return>", self.get_font)
        self.font_box.bind('<ButtonRelease-1>', self.change_preview_font)
        self.font_box.bind('<KeyRelease-Up>', self.change_preview_font)
        self.font_box.bind('<KeyRelease-Down>', self.change_preview_font)

    def change_preview_font(self, event):
        preview_font = self.font_box.get(tk.ACTIVE if event.type.name == 'KeyRelease' else tk.ANCHOR)
        self.preview.configure(font=(preview_font, 12))

    def get_font(self, *args):
        self.chosen_font.set(self.font_box.get(self.font_box.curselection()))
        self.parent.destroy()
        return self.font_box.get(self.font_box.curselection())