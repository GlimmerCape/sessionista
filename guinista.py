import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import traceback
import json

class BrowserSessionViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Browser Session Viewer")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Create Load Button
        load_button = tk.Button(self, text="Load JSON File", command=self.load_json_file)
        load_button.pack(pady=5)

        # Create Search Entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, padx=5)
        self.search_var.trace_add('write', self.search_treeview)

        # Create Treeview with Scrollbars
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind Events
        self.tree.bind('<Double-1>', self.copy_selected_item)
        self.tree.bind('<Key>', self.on_key_press)
        self.tree.focus_set()

        # Create Menu Bar
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open...", command=self.load_json_file)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

    def load_json_file(self):
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                self.populate_treeview(data)
            except Exception as e:
                error_message = f"Failed to load file:\n{e}\n\nStack trace:\n{traceback.format_exc()}"
                messagebox.showerror("Error", error_message)

    def populate_treeview(self, data):
        self.tree.delete(*self.tree.get_children())  # Clear existing data
        for idx, window in enumerate(data):
            window_id = self.tree.insert('', 'end', text=f"Window {idx+1}")
            for tab_idx, tab in enumerate(window['tabs']):
                tab_id = self.tree.insert(window_id, 'end', text=f"Tab {tab_idx+1}")
                for entry in tab['entries']:
                    url = entry.get('url', 'No URL')
                    title = entry.get('title', 'No Title')
                    self.tree.insert(tab_id, 'end', text=title, values=(url,))

    def search_treeview(self, *args):
        search_term = self.search_var.get().lower()
        for item in self.tree.get_children():
            window_visible = False
            for tab in self.tree.get_children(item):
                tab_visible = False
                for entry in self.tree.get_children(tab):
                    title = self.tree.item(entry, 'text').lower()
                    if search_term in title:
                        self.tree.item(entry, open=True)
                        tab_visible = True
                    else:
                        self.tree.detach(entry)
                if tab_visible:
                    self.tree.item(tab, open=True)
                    window_visible = True
                else:
                    self.tree.detach(tab)
            if window_visible:
                self.tree.item(item, open=True)
            else:
                self.tree.detach(item)

    def copy_selected_item(self, event):
        selected_item = self.tree.focus()
        item_text = self.tree.item(selected_item, 'text')
        item_values = self.tree.item(selected_item, 'values')
        if item_values:
            url = item_values[0]
            clipboard_text = f"Title: {item_text}\nURL: {url}"
            self.clipboard_clear()
            self.clipboard_append(clipboard_text)
            messagebox.showinfo("Copied", "URL and Title copied to clipboard.")
        else:
            messagebox.showwarning("No URL", "This item has no URL to copy.")

    def on_key_press(self, event):
        if event.keysym == 'Up':
            prev_item = self.tree.prev(self.tree.focus())
            if prev_item:
                self.tree.focus(prev_item)
                self.tree.selection_set(prev_item)
        elif event.keysym == 'Down':
            next_item = self.tree.next(self.tree.focus())
            if next_item:
                self.tree.focus(next_item)
                self.tree.selection_set(next_item)
        elif event.keysym == 'Return':
            self.copy_selected_item(None)

if __name__ == "__main__":
    app = BrowserSessionViewer()
    app.mainloop()
