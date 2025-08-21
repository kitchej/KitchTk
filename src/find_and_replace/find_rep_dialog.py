import tkinter as tk

from find_and_replace_widget import FindReplaceWidget

class FindReplaceDialog:
    """Dialog window for find and replace operations"""
    def __init__(self, text_widget: tk.Text):
        self.window = None
        self.text_widget = text_widget
        self.find_rep_widget = None

    def show(self):
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        self.window.lift()
        self.window.protocol('WM_DELETE_WINDOW', self.destroy)
        self.window.title("Find and Replace")
        self.text_widget.tag_configure('found', foreground='white', background='red')
        self.find_rep_widget = FindReplaceWidget(self.window, self.text_widget)

    def destroy(self):
        self.text_widget.tag_delete('found')
        self.window.destroy()
        self.window = None
        self.find_rep_widget = None


if __name__ == '__main__':
    root = tk.Tk()

    editor = tk.Text(root, wrap=tk.WORD, font=('Arial', 14))
    scrollbar = tk.Scrollbar(root, command=editor.yview, cursor='arrow')
    editor.configure(yscrollcommand=scrollbar.set, relief=tk.FLAT)
    find_rep_dialog = FindReplaceDialog(editor)
    menubar = tk.Menu(root)
    menubar.add_command(label="Find and Replace", command=find_rep_dialog.show)

    root.configure(menu=menubar)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    editor.pack(fill=tk.BOTH, expand=True)
    with open("../DOI.txt", 'r') as file:
        editor.insert(tk.END, file.read())

    root.mainloop()