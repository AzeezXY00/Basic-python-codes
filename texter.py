import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os

class Texter:
    def __init__(self, root):
        self.root = root
        self.root.title("Texter")
        self.root.geometry("1000x680")
        self.root.configure(bg="#1E1E2E")

        self.current_file = None
        self.is_modified = False
        self.dark_mode = False
        self.font_size = 14

        self.dark_theme = {
            "bg": "#1E1E2E",
            "sidebar": "#181825",
            "editor": "#1E1E2E",
            "text": "#CDD6F4",
            "muted": "#6C7086",
            "accent": "#CBA6F7",
            "accent2": "#89B4FA",
            "success": "#A6E3A1",
            "warning": "#F9E2AF",
            "danger": "#F38BA8",
            "border": "#313244",
            "selection": "#45475A",
            "lineno": "#45475A",
            "statusbar": "#181825",
            "menubar": "#181825",
            "button_bg": "#313244",
            "button_fg": "#CDD6F4",
            "button_active": "#45475A",
        }

        self.light_theme = {
            "bg": "#EFF1F5",
            "sidebar": "#E6E9EF",
            "editor": "#FFFFFF",
            "text": "#4C4F69",
            "muted": "#9CA0B0",
            "accent": "#8839EF",
            "accent2": "#1E66F5",
            "success": "#40A02B",
            "warning": "#DF8E1D",
            "danger": "#D20F39",
            "border": "#CCD0DA",
            "selection": "#DCE0E8",
            "lineno": "#ACB0BE",
            "statusbar": "#E6E9EF",
            "menubar": "#E6E9EF",
            "button_bg": "#DCE0E8",
            "button_fg": "#4C4F69",
            "button_active": "#CCD0DA",
        }

        self.theme = self.light_theme
        self._build_ui()
        self._bind_shortcuts()
        self._update_status()

    def t(self):
        return self.theme

    def _build_ui(self):
        self._build_menubar()
        self._build_toolbar()
        self._build_main()
        self._build_statusbar()

    def _build_menubar(self):
        self.menubar = tk.Menu(self.root, bg=self.t()["menubar"], fg=self.t()["text"],
                               activebackground=self.t()["accent"], activeforeground="#FFFFFF",
                               borderwidth=0, relief="flat")
        self.root.config(menu=self.menubar)

        file_menu = tk.Menu(self.menubar, tearoff=0, bg=self.t()["menubar"], fg=self.t()["text"],
                            activebackground=self.t()["accent"], activeforeground="#FFFFFF")
        file_menu.add_command(label="New              Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...          Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save             Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As...  Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        self.menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menubar, tearoff=0, bg=self.t()["menubar"], fg=self.t()["text"],
                            activebackground=self.t()["accent"], activeforeground="#FFFFFF")
        edit_menu.add_command(label="Undo             Ctrl+Z", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo             Ctrl+Y", command=lambda: self.text_area.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut              Ctrl+X", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy             Ctrl+C", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste            Ctrl+V", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All       Ctrl+A", command=self.select_all)
        edit_menu.add_command(label="Find & Replace   Ctrl+F", command=self.open_find)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(self.menubar, tearoff=0, bg=self.t()["menubar"], fg=self.t()["text"],
                            activebackground=self.t()["accent"], activeforeground="#FFFFFF")
        view_menu.add_command(label="Toggle Theme     Ctrl+T", command=self.toggle_theme)
        view_menu.add_command(label="Increase Font    Ctrl+=", command=self.increase_font)
        view_menu.add_command(label="Decrease Font    Ctrl+-", command=self.decrease_font)
        view_menu.add_command(label="Word Wrap", command=self.toggle_wrap)
        self.menubar.add_cascade(label="View", menu=view_menu)

    def _build_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg=self.t()["sidebar"], height=44, pady=4)
        self.toolbar.pack(fill="x", side="top")

        btn_style = dict(bg=self.t()["button_bg"], fg=self.t()["button_fg"],
                         activebackground=self.t()["button_active"], activeforeground=self.t()["text"],
                         relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
                         font=("Helvetica", 12))

        buttons = [
            ("⊕ New", self.new_file),
            ("⊙ Open", self.open_file),
            ("⊘ Save", self.save_file),
            ("|", None),
            ("⊟ Cut", lambda: self.text_area.event_generate("<<Cut>>")),
            ("⊞ Copy", lambda: self.text_area.event_generate("<<Copy>>")),
            ("⊛ Paste", lambda: self.text_area.event_generate("<<Paste>>")),
            ("|", None),
            ("⌕ Find", self.open_find),
            ("|", None),
            ("◑ Theme", self.toggle_theme),
        ]

        for label, cmd in buttons:
            if label == "|":
                sep = tk.Frame(self.toolbar, bg=self.t()["border"], width=1)
                sep.pack(side="left", fill="y", padx=6, pady=4)
            else:
                b = tk.Button(self.toolbar, text=label, command=cmd, **btn_style)
                b.pack(side="left", padx=2)

        font_frame = tk.Frame(self.toolbar, bg=self.t()["sidebar"])
        font_frame.pack(side="right", padx=10)
        tk.Button(font_frame, text="A+", command=self.increase_font,
                  bg=self.t()["button_bg"], fg=self.t()["accent"], relief="flat",
                  bd=0, padx=8, pady=4, cursor="hand2", font=("Helvetica", 12, "bold")).pack(side="right", padx=2)
        tk.Button(font_frame, text="A-", command=self.decrease_font,
                  bg=self.t()["button_bg"], fg=self.t()["accent"], relief="flat",
                  bd=0, padx=8, pady=4, cursor="hand2", font=("Helvetica", 12, "bold")).pack(side="right", padx=2)

    def _build_main(self):
        self.main_frame = tk.Frame(self.root, bg=self.t()["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.line_frame = tk.Frame(self.main_frame, bg=self.t()["sidebar"], width=52)
        self.line_frame.pack(side="left", fill="y")
        self.line_frame.pack_propagate(False)

        self.line_numbers = tk.Text(self.line_frame, width=4, padx=8,
                                    bg=self.t()["sidebar"], fg=self.t()["lineno"],
                                    state="disabled", relief="flat", bd=0,
                                    font=("Courier New", self.font_size),
                                    selectbackground=self.t()["sidebar"],
                                    cursor="arrow")
        self.line_numbers.pack(fill="both", expand=True)

        editor_frame = tk.Frame(self.main_frame, bg=self.t()["editor"])
        editor_frame.pack(side="left", fill="both", expand=True)

        scrollbar_y = ttk.Scrollbar(editor_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(editor_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.text_area = tk.Text(
            editor_frame,
            bg=self.t()["editor"], fg=self.t()["text"],
            insertbackground=self.t()["accent"],
            selectbackground=self.t()["selection"],
            selectforeground=self.t()["text"],
            relief="flat", bd=0,
            font=("Courier New", self.font_size),
            undo=True, maxundo=-1,
            wrap="word",
            padx=16, pady=12,
            spacing1=2, spacing3=2,
            yscrollcommand=self._sync_scroll,
            xscrollcommand=scrollbar_x.set,
        )
        self.text_area.pack(fill="both", expand=True)

        scrollbar_y.config(command=self._on_scrollbar)
        scrollbar_x.config(command=self.text_area.xview)

        self.text_area.bind("<<Modified>>", self._on_modified)
        self.text_area.bind("<KeyRelease>", self._on_key)
        self.text_area.bind("<ButtonRelease>", self._update_status)

        self._update_line_numbers()

    def _build_statusbar(self):
        self.status_bar = tk.Frame(self.root, bg=self.t()["statusbar"], height=26)
        self.status_bar.pack(fill="x", side="bottom")

        self.status_file = tk.Label(self.status_bar, text="Untitled", bg=self.t()["statusbar"],
                                    fg=self.t()["accent"], font=("Helvetica", 11), padx=12)
        self.status_file.pack(side="left")

        self.status_modified = tk.Label(self.status_bar, text="", bg=self.t()["statusbar"],
                                        fg=self.t()["warning"], font=("Helvetica", 11))
        self.status_modified.pack(side="left")

        self.status_pos = tk.Label(self.status_bar, text="Ln 1, Col 1", bg=self.t()["statusbar"],
                                   fg=self.t()["muted"], font=("Helvetica", 11), padx=12)
        self.status_pos.pack(side="right")

        self.status_words = tk.Label(self.status_bar, text="0 words", bg=self.t()["statusbar"],
                                     fg=self.t()["muted"], font=("Helvetica", 11), padx=12)
        self.status_words.pack(side="right")

        self.status_encoding = tk.Label(self.status_bar, text="UTF-8", bg=self.t()["statusbar"],
                                        fg=self.t()["muted"], font=("Helvetica", 11), padx=12)
        self.status_encoding.pack(side="right")

    def _bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_as())
        self.root.bind("<Control-f>", lambda e: self.open_find())
        self.root.bind("<Control-t>", lambda e: self.toggle_theme())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        self.root.bind("<Control-equal>", lambda e: self.increase_font())
        self.root.bind("<Control-minus>", lambda e: self.decrease_font())

    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])

    def _on_scrollbar(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def _on_modified(self, event=None):
        if self.text_area.edit_modified():
            self.is_modified = True
            self.status_modified.config(text="● unsaved")
            self.text_area.edit_modified(False)

    def _on_key(self, event=None):
        self._update_line_numbers()
        self._update_status()

    def _update_line_numbers(self):
        content = self.text_area.get("1.0", "end-1c")
        line_count = content.count("\n") + 1
        numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", numbers)
        self.line_numbers.config(state="disabled")

    def _update_status(self, event=None):
        pos = self.text_area.index("insert")
        line, col = pos.split(".")
        self.status_pos.config(text=f"Ln {line}, Col {int(col)+1}")
        content = self.text_area.get("1.0", "end-1c")
        words = len(content.split()) if content.strip() else 0
        chars = len(content)
        self.status_words.config(text=f"{words} words  {chars} chars")
        fname = os.path.basename(self.current_file) if self.current_file else "Untitled"
        self.status_file.config(text=fname)

    def new_file(self):
        if self.is_modified:
            if not messagebox.askyesno("Unsaved changes", "Discard unsaved changes?"):
                return
        self.text_area.delete("1.0", "end")
        self.current_file = None
        self.is_modified = False
        self.status_modified.config(text="")
        self.root.title("Texter")
        self._update_line_numbers()
        self._update_status()

    def open_file(self):
        if self.is_modified:
            if not messagebox.askyesno("Unsaved changes", "Discard unsaved changes?"):
                return
        path = filedialog.askopenfilename(filetypes=[
            ("Text files", "*.txt"), ("Python files", "*.py"),
            ("Markdown", "*.md"), ("All files", "*.*")
        ])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", content)
            self.current_file = path
            self.is_modified = False
            self.status_modified.config(text="")
            self.root.title(f"Texter — {os.path.basename(path)}")
            self._update_line_numbers()
            self._update_status()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self.is_modified = False
            self.status_modified.config(text="")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
            ("Text files", "*.txt"), ("Python files", "*.py"),
            ("Markdown", "*.md"), ("All files", "*.*")
        ])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self.current_file = path
            self.is_modified = False
            self.status_modified.config(text="")
            self.root.title(f"Texter — {os.path.basename(path)}")
            self._update_status()

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", "end")
        return "break"

    def toggle_wrap(self):
        current = self.text_area.cget("wrap")
        self.text_area.config(wrap="none" if current == "word" else "word")

    def increase_font(self):
        self.font_size = min(self.font_size + 2, 40)
        self._apply_font()

    def decrease_font(self):
        self.font_size = max(self.font_size - 2, 8)
        self._apply_font()

    def _apply_font(self):
        f = ("Courier New", self.font_size)
        self.text_area.config(font=f)
        self.line_numbers.config(font=f)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme = self.dark_theme if self.dark_mode else self.light_theme
        self._refresh_theme()

    def _refresh_theme(self):
        t = self.t()
        self.root.configure(bg=t["bg"])
        self.toolbar.configure(bg=t["sidebar"])
        self.main_frame.configure(bg=t["bg"])
        self.line_frame.configure(bg=t["sidebar"])
        self.line_numbers.configure(bg=t["sidebar"], fg=t["lineno"], selectbackground=t["sidebar"])
        self.text_area.configure(bg=t["editor"], fg=t["text"], insertbackground=t["accent"],
                                  selectbackground=t["selection"])
        self.status_bar.configure(bg=t["statusbar"])
        self.status_file.configure(bg=t["statusbar"], fg=t["accent"])
        self.status_modified.configure(bg=t["statusbar"], fg=t["warning"])
        self.status_pos.configure(bg=t["statusbar"], fg=t["muted"])
        self.status_words.configure(bg=t["statusbar"], fg=t["muted"])
        self.status_encoding.configure(bg=t["statusbar"], fg=t["muted"])
        for widget in self.toolbar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=t["button_bg"], fg=t["button_fg"], activebackground=t["button_active"])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=t["border"] if widget.cget("width") == 1 else t["sidebar"])

    def open_find(self):
        win = tk.Toplevel(self.root)
        win.title("Find & Replace")
        win.geometry("380x140")
        win.configure(bg=self.t()["bg"])
        win.resizable(False, False)

        t = self.t()
        lbl_style = dict(bg=t["bg"], fg=t["text"], font=("Helvetica", 12))
        entry_style = dict(bg=t["sidebar"], fg=t["text"], insertbackground=t["accent"],
                           relief="flat", bd=0, font=("Courier New", 12))
        btn_style = dict(bg=t["button_bg"], fg=t["button_fg"], relief="flat", bd=0,
                         padx=10, pady=4, cursor="hand2", font=("Helvetica", 11))

        tk.Label(win, text="Find:", **lbl_style).grid(row=0, column=0, padx=12, pady=10, sticky="e")
        find_entry = tk.Entry(win, width=26, **entry_style)
        find_entry.grid(row=0, column=1, padx=6, pady=10)
        find_entry.focus()

        tk.Label(win, text="Replace:", **lbl_style).grid(row=1, column=0, padx=12, sticky="e")
        replace_entry = tk.Entry(win, width=26, **entry_style)
        replace_entry.grid(row=1, column=1, padx=6)

        def do_find():
            self.text_area.tag_remove("found", "1.0", "end")
            term = find_entry.get()
            if not term:
                return
            idx = "1.0"
            count = 0
            while True:
                idx = self.text_area.search(term, idx, nocase=True, stopindex="end")
                if not idx:
                    break
                end = f"{idx}+{len(term)}c"
                self.text_area.tag_add("found", idx, end)
                self.text_area.tag_config("found", background=t["warning"], foreground="#1E1E2E")
                idx = end
                count += 1
            messagebox.showinfo("Find", f"{count} match(es) found.", parent=win)

        def do_replace():
            term = find_entry.get()
            replacement = replace_entry.get()
            content = self.text_area.get("1.0", "end-1c")
            new_content = content.replace(term, replacement)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", new_content)
            self._update_line_numbers()

        btn_frame = tk.Frame(win, bg=t["bg"])
        btn_frame.grid(row=2, column=0, columnspan=2, pady=12)
        tk.Button(btn_frame, text="Find", command=do_find, **btn_style).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Replace All", command=do_replace, **btn_style).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Close", command=win.destroy, **btn_style).pack(side="left", padx=6)

    def quit_app(self):
        if self.is_modified:
            if not messagebox.askyesno("Unsaved changes", "Quit without saving?"):
                return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Texter(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()
