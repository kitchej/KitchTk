import tkinter as tk
import tkinter.ttk as ttk

class FindReplaceWidget:
    """Widget for find and replace operations"""

    def __init__(self, parent, text_widget: tk.Text):
        self.parent = parent
        self.text_widget = text_widget
        self.word_counter = 1
        self.found_word_indexes = []
        self.match_word = tk.IntVar()
        self.match_case = tk.IntVar()
        self.match_case.set(0)
        self.match_word.set(0)
        self.is_find_all = None

        self.find_entry = ttk.Entry(self.parent, width=25)
        self.find_button = ttk.Button(self.parent, text="Find", command=self.find)
        self.find_all_button = ttk.Button(self.parent, text="Find All", command=self.find_all)
        self.match_case_label = ttk.Label(self.parent, text="Match Case")
        self.match_case_check = ttk.Checkbutton(self.parent, variable=self.match_case, command=self.refresh_found_words)
        self.match_case_check.state(['!alternate'])
        self.match_word_label = ttk.Label(self.parent, text="Match Word")
        self.match_word_check = ttk.Checkbutton(self.parent, variable=self.match_word, command=self.refresh_found_words)
        self.match_word_check.state(['!alternate'])
        self.replace_entry = ttk.Entry(self.parent, width=25)
        self.replace_button = ttk.Button(self.parent, text="Replace", command=self.replace)
        self.replace_all_button = ttk.Button(self.parent, text="Replace All", command=self.replace_all)
        self.navigation_frame = tk.Frame(self.parent)
        self.next = ttk.Button(self.navigation_frame, text="Next", command=self.next_instance)
        self.prev = ttk.Button(self.navigation_frame, text="Prev", command=self.previous_instance)
        self.word_count_label = tk.Label(self.navigation_frame)
        self.find_entry.grid(row=0, column=0, padx=10)
        self.find_button.grid(row=0, column=1)
        self.find_all_button.grid(row=0, column=2, padx=(0, 3))
        self.match_case_label.grid(row=0, column=3)
        self.match_case_check.grid(row=0, column=4)
        self.match_word_label.grid(row=0, column=5)
        self.match_word_check.grid(row=0, column=6, padx=(0, 10))
        self.replace_entry.grid(row=1, column=0, padx=5)
        self.replace_button.grid(row=1, column=1)
        self.replace_all_button.grid(row=1, column=2)
        self.navigation_frame.grid(row=2, column=0, columnspan=4, sticky='w', padx=10, pady=10)


    def clear_tags(self, tag):
        old_tags = []
        ranges = self.text_widget.tag_ranges(tag)
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            stop = ranges[i + 1]
            old_tags.append((tag, str(start), str(stop)))
        for old_tag in old_tags:
            self.text_widget.tag_remove(old_tag[0], old_tag[1], old_tag[2])

    @staticmethod
    def get_tags(start, end, text_obj):
        """
        Provided by Bryan Oakley
        https://stackoverflow.com/questions/61661490/how-do-you-get-the-tags-from-text-in-a-tkinter-text-widget
        """
        index = start
        tags = []
        while text_obj.compare(index, "<=", end):
            tags.extend((text_obj.tag_names(index)))
            index = text_obj.index(f"{index}+1c")
        return set(tags)

    def get_first_string_index(self, string, regex=False, no_case=False, start="1.0"):
        """Helper method that finds the first instance of a string in self.text_widget"""
        length = tk.IntVar()
        word_start = self.text_widget.search(string, start, regexp=regex, stopindex=tk.END, nocase=no_case, count=length)
        if word_start == '':
            return None
        word_start_index = word_start.split(".")
        start_row = int(word_start_index[0])
        start_column = int(word_start_index[1])
        end_row = start_row + string.count('\n')
        end_column = start_column + length.get()
        word_end = f"{end_row}.{end_column}"
        return word_start, word_end

    def get_string_indexes(self, string, regex=False, no_case=False, start="1.0"):
        """Helper method that find the all instances of a string in self.text_widget"""
        length = tk.IntVar()
        out = []
        while start != self.text_widget.index(tk.END):
            word_start = self.text_widget.search(string, start, regexp=regex, stopindex=tk.END, nocase=no_case, count=length)
            if word_start == '':
                break
            word_start_index = word_start.split(".")
            start_row = int(word_start_index[0])
            start_column = int(word_start_index[1])
            end_row = start_row + string.count('\n')
            end_column = start_column + length.get()
            word_end = f"{end_row}.{end_column}"
            start = word_end
            out.append((word_start, word_end))
        return out

    def get_word_index(self, start='1.0'):
        """Finds a word within the editor and returns it's index. Returns False if no word was found."""
        word = self.find_entry.get()
        if word == '':
            return False
        if self.match_word.get():
            return self.get_first_string_index(f"\\m{word}\\M",
                                               regex=True,
                                               no_case=not self.match_case.get(),
                                               start=start)
        else:
            return self.get_first_string_index(word,
                                               no_case=not self.match_case.get(),
                                               start=start)

    def get_all_word_indexes(self, start='1.0'):
        """
        Finds all instances of a word within the editor and sets self.found_word_indexes
        Returns False if no words were found.
        Returns True if words were found.
        """
        word = self.find_entry.get()
        if word == '':
            return False
        if self.match_word.get():
            self.found_word_indexes = self.get_string_indexes(f"\\m{word}\\M",
                                                              regex=True,
                                                              no_case=not self.match_case.get(),
                                                              start=start)
        else:
            self.found_word_indexes = self.get_string_indexes(word,
                                                              no_case=not self.match_case.get(),
                                                              start=start)
        if self.found_word_indexes:
            return True
        else:
            return False

    def find(self):
        """GUI action to find all words in self.text_widget and mark the first instance"""
        if self.is_find_all or self.is_find_all is None:
            self.is_find_all = False
            self.word_count_label.pack_forget()
            self.prev.pack(side=tk.LEFT)
            self.word_count_label.pack(side=tk.LEFT, padx=5)
            self.next.pack(side=tk.LEFT)
        self.clear_tags('found')
        result = self.get_all_word_indexes()
        if not result:
            self.word_count_label.configure(text="None")
        else:
            self.word_counter = 1
            self.text_widget.tag_add('found', self.found_word_indexes[self.word_counter - 1][0],
                                    self.found_word_indexes[self.word_counter - 1][1])
            self.word_count_label.configure(text=f"{self.word_counter}/{len(self.found_word_indexes)}")
            self.text_widget.see(self.found_word_indexes[0][0])

    def find_all(self):
        """GUI action to find all words in self.text_widget and show all instances"""
        if not self.is_find_all or self.is_find_all is None:
            self.is_find_all = True
            self.word_count_label.pack_forget()
            self.prev.pack_forget()
            self.next.pack_forget()
            self.word_count_label.pack(padx=45)
            self.word_counter = 1
        self.clear_tags('found')
        result = self.get_all_word_indexes()
        if not result:
            self.word_count_label.configure(text="None")
        else:
            for word in self.found_word_indexes:
                self.text_widget.tag_add('found', word[0], word[1])
            self.word_count_label.configure(text=f"Total: {len(self.found_word_indexes)}")

    def replace(self):
        """GUI action to replace the first selected word. Re-finds all words afterward."""
        if not self.found_word_indexes:
            return
        index = self.found_word_indexes[self.word_counter - 1]
        self.text_widget.delete(index[0], index[1])
        self.text_widget.insert(index[0], self.replace_entry.get())
        result = self.get_all_word_indexes(start=index[1])
        if not result:
            self.word_count_label.configure(text="None")
            return
        self.word_count_label.configure(text=f"{self.word_counter}/{len(self.found_word_indexes)}")
        self.word_counter -= 1
        self.next_instance()

    def replace_all(self):
        """GUI action to replace all found words."""
        if not self.found_word_indexes:
            return
        replace_word = self.replace_entry.get()
        self.clear_tags('found')
        # Since we are constantly changing the text, ignore the
        # indexes in self.found_word_indexes and just find the words as we go
        start = '1.0'
        for i in range(len(self.found_word_indexes)):
            word_start, word_end = self.get_word_index(start=start)
            self.text_widget.delete(word_start, word_end)
            self.text_widget.insert(word_start, replace_word)
            start = word_end
        self.found_word_indexes = []
        self.word_count_label.configure(text=f"None")

    def next_instance(self):
        """GUI action to select the next instance. Wraps to the first instance if last is selected"""
        if self.word_counter + 1 > len(self.found_word_indexes):
            self.word_counter = 1
        else:
            self.word_counter += 1
        if not self.found_word_indexes:
            return
        self.clear_tags('found')
        self.word_count_label.configure(text=f"{self.word_counter}/{len(self.found_word_indexes)}")
        self.text_widget.tag_add('found', self.found_word_indexes[self.word_counter - 1][0],
                                self.found_word_indexes[self.word_counter - 1][1])
        self.text_widget.see(self.found_word_indexes[self.word_counter - 1][0])

    def previous_instance(self):
        """GUI action to select the previous instance. Wraps back to the last instance if first is selected."""
        if self.word_counter == 1:
            self.word_counter = len(self.found_word_indexes)
        else:
            self.word_counter -= 1
        if not self.found_word_indexes:
            return
        else:
            self.clear_tags('found')

            self.word_count_label.configure(text=f"{self.word_counter}/{len(self.found_word_indexes)}")
            self.text_widget.tag_add('found', self.found_word_indexes[self.word_counter - 1][0],
                                    self.found_word_indexes[self.word_counter - 1][1])
            self.text_widget.see(self.found_word_indexes[self.word_counter - 1][0])

    def refresh_found_words(self):
        """Resets the tags and re-finds all words. Useful if options for finding words are changed"""
        if self.is_find_all is None:
            return
        elif self.is_find_all:
            self.find_all()
        else:
            self.find()