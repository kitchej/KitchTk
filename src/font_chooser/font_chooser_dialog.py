import tkinter as tk

from font_chooser_widget import FontChooserWidget

class FontChooserDialog:
    """Dialog window for find and replace operations"""
    def __init__(self, current_font=None, font_list=None):
        self.window = None
        self.font_chooser_widget = None
        self.current_font = current_font
        self.font_list = font_list

    def get_font(self):
        self.window = tk.Toplevel()
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.lift()
        self.window.title("Choose a Font")
        self.font_chooser_widget = FontChooserWidget(self.window, self.current_font, self.font_list)
        self.window.wait_window()
        return self.font_chooser_widget.chosen_font.get()


if __name__ == '__main__':

    class SimpleEditor(tk.Frame):
        def __init__(self, *args, **kwargs):
            tk.Frame.__init__(self, *args, **kwargs)
            self.allowed_fonts = ['Arial', 'Cambria', 'Courier', 'Lucida Console', 'Nirmala Text']
            self.font_family = 'Arial'
            self.editor = tk.Text(root, wrap=tk.WORD, font=(self.font_family, 14))
            self.scrollbar = tk.Scrollbar(root, command=self.editor.yview, cursor='arrow')
            self.editor.configure(yscrollcommand=self.scrollbar.set, relief=tk.FLAT)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
            self.editor.pack(fill=tk.BOTH, expand=True)
            with open("../DOI.txt", 'r') as file:
                self.editor.insert(tk.END, file.read())

        def change_font(self):
            find_rep_dialog = FontChooserDialog(current_font=self.font_family, font_list=self.allowed_fonts)
            new_font = find_rep_dialog.get_font()
            self.editor.configure(font=(new_font, 14))

    root = tk.Tk()
    editor = SimpleEditor(root)
    menubar = tk.Menu(root)
    menubar.add_command(label="Change Font", command=editor.change_font)
    editor.pack()
    root.configure(menu=menubar)

    root.mainloop()
