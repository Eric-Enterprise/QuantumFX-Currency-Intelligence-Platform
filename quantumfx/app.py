"""Responsive Tk desktop interface. Network workers communicate via a queue."""
import logging
import queue
import threading
import tkinter as tk
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from tkinter import ttk, filedialog, messagebox
from .core import RateService, Store, convert, number, money, export_csv
from .ui import BG, CARD, TEXT, MUTED, ACCENT, MINT, SIDEBAR, Animator, MotionButton, Hero, GlassResult, Tooltip, blend
from .snake import SnakePanel
from .i18n import Translator, LANGUAGES
from . import __version__


class App:
    def __init__(self, root, folder=None, offline=False):
        self.root = root
        self.service = RateService(folder)
        self.store = Store(folder)
        self.tr = Translator(self.store.prefs.get("language", "en"))
        self.animator = Animator(root, self.store.prefs.get("animations", True) is not False)
        self.fullscreen = False
        self.snapshot = self.service.cached()
        self.events = queue.Queue()
        self.pending = set()
        self.chart_points = []
        self.chart_key = None
        self.last_result = None
        self.root.title("QuantumFX · Currency Intelligence")
        self.root.geometry("1180x820")
        self.root.minsize(980, 700)
        self.root.configure(bg=BG)
        try:
            self.root.iconbitmap(str(Path(__file__).resolve().parents[1] / "assets" / "quantumfx.ico"))
        except tk.TclError:
            pass
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.report_callback_exception = self.callback_error
        self.style()
        self.amount = tk.StringVar(value="1000")
        self.base = tk.StringVar(value=self.store.prefs.get("base", "EUR"))
        self.target = tk.StringVar(value=self.store.prefs.get("target", "USD"))
        self.percent = tk.StringVar(value="0")
        self.fixed = tk.StringVar(value="0")
        self.days = tk.StringVar(value="90")
        self.search = tk.StringVar()
        self.status = tk.StringVar()
        self.result = tk.StringVar(value=self.tr("Ready to convert"))
        self.detail = tk.StringVar()
        self.feedback = tk.StringVar()
        self.chart_status = tk.StringVar(value=self.tr("Choose a currency pair and load its rate history."))
        self.build()
        for variable in (self.amount, self.percent, self.fixed):
            variable.trace_add("write", lambda *args: self.invalidate_result())
        self.apply_snapshot(self.snapshot)
        self.fill_history()
        self.root.bind("<Return>", self.enter_action)
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self.leave_fullscreen())
        self.root.bind("<Control-r>", lambda e: self.refresh())
        self.root.bind("<Control-s>", lambda e: self.swap())
        self.root.bind("<Control-f>", self.focus_search)
        self.poll_id = self.root.after(100, self.poll)
        if not offline:
            self.root.after(150, self.refresh)

    def style(self):
        self.font_family = "Malgun Gothic" if self.tr.language == "ko" else "Segoe UI"
        self.root.option_add("*Font", (self.font_family, 10))
        self.root.option_add("*TCombobox*Listbox.background", CARD)
        self.root.option_add("*TCombobox*Listbox.foreground", TEXT)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Muted.TLabel", foreground=MUTED)
        style.configure("TButton", background=CARD, foreground=TEXT, padding=(14, 9), borderwidth=0)
        style.map("TButton", background=[("active", "#28415d"), ("disabled", "#192538")],
                  foreground=[("disabled", "#66778e")])
        style.configure("Accent.TButton", background=ACCENT, foreground=BG, font=(self.font_family, 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#81efd4")])
        style.configure("TEntry", fieldbackground=CARD, foreground=TEXT, insertcolor=TEXT, padding=12,
                        bordercolor="#4b5b80", lightcolor=CARD, darkcolor=CARD)
        style.map("TEntry", bordercolor=[("focus", ACCENT)])
        style.configure("Invalid.TEntry", bordercolor="#ffa99c")
        style.configure("TCombobox", fieldbackground=CARD, background=CARD, foreground=TEXT, padding=10, arrowcolor=TEXT,
                        bordercolor="#4b5b80", lightcolor=CARD, darkcolor=CARD)
        style.map("TCombobox", fieldbackground=[("readonly", CARD)], foreground=[("readonly", TEXT)])
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.layout("TNotebook", [("Notebook.client", {"sticky": "nswe"})])
        style.layout("TNotebook.Tab", [])
        style.configure("TNotebook.Tab", background=CARD, foreground=MUTED, padding=(20, 12))
        style.map("TNotebook.Tab", background=[("selected", "#223952")], foreground=[("selected", ACCENT)])
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT, rowheight=34, borderwidth=0)
        style.configure("Treeview.Heading", background="#22334c", foreground=TEXT, padding=8)
        style.map("Treeview", background=[("selected", "#28556a")])
        style.configure("Vertical.TScrollbar", background="#3b4e70", troughcolor=BG, bordercolor=BG,
                        arrowcolor=MUTED, lightcolor=BG, darkcolor=BG)

    def label(self, parent, text, size=10, muted=False):
        w = ttk.Label(parent, text=text, font=(self.font_family, size, "bold" if size >= 18 else "normal"),
                      style="Muted.TLabel" if muted else "TLabel")
        w.pack(anchor="w", pady=(0, 8))
        parent.bind("<Configure>", lambda e: w.configure(wraplength=max(200, e.width-16)), add=True)
        return w

    def button(self, parent, text, fn, accent=False):
        hints = {"⇄": self.tr("Swap source and target currencies · Ctrl+S"),
                 self.tr("Convert & save  ↗"): self.tr("Convert using the displayed rates and save the result to history · Enter"),
                 self.tr("Fullscreen  F11"): self.tr("Toggle fullscreen · F11. Press Escape to return to a window."),
                 self.tr("Refresh"): self.tr("Refresh daily reference rates in the background · Ctrl+R")}
        return MotionButton(parent, text, fn, self.animator, accent, hint=hints.get(text))

    def build(self):
        sidebar = tk.Frame(self.root, bg=SIDEBAR, width=224, padx=16, pady=26)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="QuantumFX", bg=SIDEBAR, fg=TEXT, font=(self.font_family, 16, "bold")).pack(anchor="w")
        tk.Label(sidebar, text=f"VERSION {__version__}", bg=SIDEBAR, fg=ACCENT, font=(self.font_family, 9)).pack(anchor="w", pady=(8, 28))
        self.nav = tk.Frame(sidebar, bg=SIDEBAR)
        self.nav.pack(fill="x")
        self.motion_btn = MotionButton(sidebar, self.tr("Effects on") if self.animator.enabled else self.tr("Effects off"),
                                       self.toggle_motion, self.animator, background=SIDEBAR, icon_name="sparkles",
                                       hint=self.tr("Turn animations on or off. Your preference is saved."))
        self.motion_btn.pack(side="bottom", fill="x", pady=8)
        language_panel = ttk.Frame(sidebar)
        language_panel.pack(side="bottom", fill="x", pady=(12, 8))
        ttk.Label(language_panel, text=self.tr("Language")).pack(anchor="w", pady=(0, 6))
        self.language_choice = tk.StringVar(value=LANGUAGES[self.tr.language])
        self.language_box = ttk.Combobox(language_panel, textvariable=self.language_choice,
                                         values=list(LANGUAGES.values()), state="readonly", width=16)
        self.language_box.pack(fill="x")
        self.language_box.bind("<<ComboboxSelected>>", self.language_selected)
        outer = ttk.Frame(self.root, padding=(24, 18))
        outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 18))
        self.page_title = ttk.Label(header, text=self.tr("Overview"), font=(self.font_family, 23, "bold"))
        self.page_title.pack(side="left")
        self.button(header, self.tr("Close"), self.close).pack(side="right", padx=(8, 0))
        self.full_btn = self.button(header, self.tr("Fullscreen  F11"), self.toggle_fullscreen)
        self.full_btn.pack(side="right", padx=8)
        self.refresh_btn = self.button(header, self.tr("Refresh"), self.refresh)
        self.refresh_btn.pack(side="right")
        status_line = ttk.Label(outer, textvariable=self.status, foreground=ACCENT, wraplength=1080)
        status_line.pack(fill="x", pady=(0, 15))
        outer.bind("<Configure>", lambda e: status_line.configure(wraplength=max(250, e.width-50)))
        ttk.Label(outer, text=self.tr("Frankfurter / ECB · Daily reference rates · Fees are your own estimates."),
                  style="Muted.TLabel").pack(side="bottom", anchor="w", pady=(12, 0))
        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill="both", expand=True)
        self.converter = ttk.Frame(self.tabs)
        self.markets = ttk.Frame(self.tabs, padding=(0, 22))
        self.history_tab = ttk.Frame(self.tabs, padding=(0, 22))
        self.compare_tab = ttk.Frame(self.tabs, padding=(0, 22))
        self.help_tab = ttk.Frame(self.tabs, padding=(0, 22))
        self.snake_tab = ttk.Frame(self.tabs, padding=(0, 16))
        self.nav_buttons = []
        for frame, title, glyph in [(self.converter, self.tr("Converter"), "swap"), (self.markets, self.tr("Currencies"), "globe"),
                             (self.compare_tab, self.tr("Fees"), "compare"), (self.history_tab, self.tr("History"), "history"),
                             (self.snake_tab, self.tr("Snake"), "game"), (self.help_tab, self.tr("Help"), "help")]:
            self.tabs.add(frame, text=title)
            nav_btn = MotionButton(self.nav, title, lambda f=frame: self.tabs.select(f), self.animator,
                                   background=SIDEBAR, icon_name=glyph, align="left")
            nav_btn.pack(fill="x", pady=5)
            self.nav_buttons.append((str(frame), title, nav_btn))
        self.tabs.bind("<<NotebookTabChanged>>", self.page_changed)
        viewport = tk.Canvas(self.converter, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.converter, orient="vertical", command=viewport.yview)
        viewport.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        viewport.pack(side="left", fill="both", expand=True)
        content = ttk.Frame(viewport, padding=(0, 22))
        content_id = viewport.create_window((0, 0), window=content, anchor="nw")
        content.bind("<Configure>", lambda e: viewport.configure(scrollregion=viewport.bbox("all")))
        viewport.bind("<Configure>", lambda e: viewport.itemconfigure(content_id, width=e.width))
        self.viewport = viewport
        self.root.bind("<MouseWheel>", self.scroll_converter, add=True)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=3)
        hero = Hero(content, translator=self.tr)
        hero.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 24))
        left = ttk.Frame(content, padding=(0, 0, 28, 0))
        left.grid(row=1, column=0, sticky="nsew")
        right = ttk.Frame(content)
        right.grid(row=1, column=1, sticky="nsew")
        def responsive(event):
            viewport.itemconfigure(content_id, width=event.width)
            if event.width < 950:
                left.grid_configure(row=1, column=0, columnspan=2, padx=(0, 0))
                right.grid_configure(row=2, column=0, columnspan=2, pady=(24, 0))
            else:
                left.grid_configure(row=1, column=0, columnspan=1)
                right.grid_configure(row=1, column=1, columnspan=1, pady=0)
        viewport.bind("<Configure>", responsive)
        self.label(left, self.tr("Your currency converter"), 20)
        self.label(left, self.tr("1  Enter an amount"), muted=True)
        self.amount_entry = ttk.Entry(left, textvariable=self.amount, font=(self.font_family, 19))
        self.amount_entry.pack(fill="x", pady=(0, 6))
        self.label(left, self.tr("For example 1234.56 · no thousands separators"), muted=True)
        Tooltip(self.amount_entry, self.tr("Use a dot or comma as the decimal separator, e.g. 1234.56. Enter converts and saves."))
        self.label(left, self.tr("2  Choose currencies"), muted=True)
        pair = ttk.Frame(left)
        pair.pack(fill="x", pady=(0, 16))
        source = ttk.Frame(pair)
        source.pack(side="left", fill="x", expand=True)
        self.label(source, self.tr("From"), muted=True)
        self.base_box = ttk.Combobox(source, textvariable=self.base, width=8, state="readonly")
        self.base_box.pack(fill="x")
        self.button(pair, "⇄", self.swap).pack(side="left", padx=10, pady=(26, 0))
        target = ttk.Frame(pair)
        target.pack(side="left", fill="x", expand=True)
        self.label(target, self.tr("To"), muted=True)
        self.target_box = ttk.Combobox(target, textvariable=self.target, width=8, state="readonly")
        self.target_box.pack(fill="x")
        for box in (self.base_box, self.target_box):
            box.bind("<<ComboboxSelected>>", self.pair_changed)
        self.fees_expanded = False
        self.fee_toggle = MotionButton(left, self.tr("Add fees · optional"), self.toggle_fees,
                                       self.animator, icon_name="compare", hint=self.tr("Show optional percentage and fixed fees. Leave them at zero for no deductions."))
        self.fee_toggle.pack(anchor="w", pady=(0, 10))
        fees = ttk.Frame(left)
        self.fees_container = fees
        ttk.Label(fees, text=self.tr("Percent %")).pack(side="left")
        percent_entry = ttk.Entry(fees, textvariable=self.percent, width=6)
        percent_entry.pack(side="left", padx=(8, 18))
        ttk.Label(fees, text=self.tr("Fixed fee")).pack(side="left")
        fixed_entry = ttk.Entry(fees, textvariable=self.fixed, width=8)
        fixed_entry.pack(side="left", padx=8)
        Tooltip(percent_entry, self.tr("Percentage deducted from the source amount, from 0 to 100."))
        Tooltip(fixed_entry, self.tr("Fixed deduction in the source currency. For example, 2 means EUR 2 when converting from EUR."))
        self.convert_btn = self.button(left, self.tr("Convert & save  ↗"), self.calculate, True)
        self.convert_btn.pack(fill="x")
        result_card = GlassResult(left, self.result, self.detail, translator=self.tr)
        self.result_card = result_card
        result_card.pack(fill="x", pady=18)
        actions = ttk.Frame(left)
        actions.pack(fill="x")
        self.copy_btn = self.button(actions, self.tr("Copy"), self.copy)
        self.copy_btn.pack(side="left")
        self.button(actions, self.tr("★ Save pair"), self.favorite).pack(side="left", padx=8)
        ttk.Label(left, textvariable=self.feedback, foreground="#ffcc80", wraplength=385).pack(fill="x", pady=12)
        self.label(right, self.tr("Rate trends"), 20)
        toolbar = ttk.Frame(right)
        toolbar.pack(fill="x", pady=(0, 12))
        ttk.Label(toolbar, text=self.tr("Period (days)"), style="Muted.TLabel").pack(side="left")
        period = ttk.Combobox(toolbar, textvariable=self.days, values=(30, 90, 365), width=5, state="readonly")
        period.pack(side="left", padx=12)
        period.bind("<<ComboboxSelected>>", self.pair_changed)
        self.chart_btn = self.button(toolbar, self.tr("Load history"), self.load_chart)
        self.chart_btn.pack(side="right")
        self.button(right, self.tr("Export chart CSV"), self.export_chart).pack(anchor="e", pady=(0, 8))
        self.canvas = tk.Canvas(right, bg=CARD, highlightthickness=0, height=280)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart())
        self.canvas.bind("<Motion>", self.chart_hover)
        ttk.Label(right, textvariable=self.chart_status, wraplength=540, style="Muted.TLabel").pack(fill="x", pady=12)
        self.label(right, self.tr("Favorites · double-click to open"), muted=True)
        self.favorites = tk.Listbox(right, bg=CARD, fg=TEXT, selectbackground="#28556a", height=3,
                                   relief="flat", highlightthickness=0, activestyle="none")
        self.favorites.pack(fill="x")
        self.favorites.bind("<Double-Button-1>", self.open_favorite)
        self.button(right, self.tr("Remove selected pair"), self.remove_favorite).pack(anchor="e", pady=8)
        self.fill_favorites()
        self.build_markets()
        self.build_history()
        self.build_compare()
        self.build_help()
        self.snake = SnakePanel(self.snake_tab, self.store, self.animator, translator=self.tr)
        self.snake.pack(fill="both", expand=True)

    def money(self, value, currency):
        return self.tr.amount(money(value, currency))

    def language_selected(self, event=None):
        code = next((code for code, label in LANGUAGES.items() if label == self.language_choice.get()), "en")
        self.change_language(code)

    def change_language(self, code):
        if code not in LANGUAGES or code == self.tr.language:
            return
        selected = self.tabs.index(self.tabs.select())
        expanded = self.fees_expanded
        offers = [[v.get() for v in row] for row in self.offers]
        for i, row in enumerate(offers):
            if row[0] == self.tr("Offer {n}", n=i+1):
                row[0] = None
        had_comparison = bool(self.compare_tree.get_children())
        self.snake.pause()
        game, started, highscore = self.snake.game, self.snake.started, self.snake.highscore
        speed = next((k for k in ("Relaxed", "Normal", "Fast") if self.tr(k) == self.snake.speed.get()), "Normal")
        self.animator.stop()
        self.search.trace_remove("write", self.search_trace)
        self.root.unbind("<MouseWheel>")
        for child in self.root.winfo_children():
            child.destroy()
        self.tr = Translator(code)
        self.store.prefs["language"] = code
        self.style()
        self.build()
        self.apply_snapshot(self.snapshot)
        self.fill_history()
        for i, (variables, values) in enumerate(zip(self.offers, offers)):
            for variable, value in zip(variables, values):
                variable.set(self.tr("Offer {n}", n=i+1) if value is None else value)
        if had_comparison:
            self.compare()
        if expanded:
            self.toggle_fees()
        self.snake.game, self.snake.started, self.snake.highscore = game, started, highscore
        self.snake.speed.set(self.tr(speed))
        self.snake.update_caption()
        self.snake.draw()
        self.tabs.select(selected)
        self.full_btn.configure(text=self.tr("Window  Esc" if self.fullscreen else "Fullscreen  F11"))
        if self.chart_points:
            self.describe_chart()
        else:
            self.chart_status.set(self.tr("Choose a currency pair and load its rate history."))
        self.draw_chart()
        if "rates" in self.pending:
            self.refresh_btn.configure(state="disabled")
            self.status.set(self.tr("Loading rates in the background …"))
        if "chart" in self.pending:
            self.chart_btn.configure(state="disabled")
            self.chart_status.set(self.tr("Loading historical reference rates …"))
        try:
            self.store.save()
        except OSError:
            self.feedback.set(self.tr("Language could not be saved."))

    def enter_action(self, event=None):
        if self.tabs.select() == str(self.converter):
            self.calculate()

    def focus_search(self, event=None):
        self.tabs.select(self.markets)
        self.search_entry.focus_set()
        self.search_entry.selection_range(0, "end")
        return "break"

    def toggle_fees(self):
        self.fees_expanded = not self.fees_expanded
        if self.fees_expanded:
            self.fees_container.pack(fill="x", pady=(0, 16), before=self.convert_btn)
        else:
            self.fees_container.pack_forget()
        self.update_fee_hint()

    def update_fee_hint(self):
        try:
            active = number(self.percent.get()) != 0 or number(self.fixed.get()) != 0
        except ValueError:
            active = True
        self.fee_toggle.configure(text=self.tr("Hide fees") if self.fees_expanded else
                                   (self.tr("Fees active · edit") if active else self.tr("Add fees · optional")))

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        self.full_btn.configure(text=self.tr("Window  Esc") if self.fullscreen else self.tr("Fullscreen  F11"))

    def leave_fullscreen(self):
        if hasattr(self, "snake"):
            self.snake.pause()
        if self.fullscreen:
            self.toggle_fullscreen()

    def toggle_motion(self):
        self.animator.enabled = not self.animator.enabled
        self.animator.stop()
        self.motion_btn.configure(text=self.tr("Effects on") if self.animator.enabled else self.tr("Effects off"))
        self.store.prefs["animations"] = self.animator.enabled
        try:
            self.store.save()
        except OSError:
            self.feedback.set(self.tr("Could not save display preferences."))
        self.draw_chart()

    def page_changed(self, event=None):
        selected = self.tabs.select()
        for frame, title, button in self.nav_buttons:
            button.accent = frame == selected
            button.draw()
            if frame == selected:
                self.page_title.configure(text=title)
        if hasattr(self, "snake"):
            self.snake.pause()
        self.animator.run("page", lambda t: self.page_title.configure(foreground=blend(MUTED, TEXT, t)), 300)

    def table(self, parent, columns):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=12)
        tree = ttk.Treeview(frame, columns=[x[0] for x in columns], show="headings")
        for key, title, width in columns:
            tree.heading(key, text=title)
            tree.column(key, width=width, minwidth=80, anchor="w", stretch=True)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        horizontal = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scroll.set, xscrollcommand=horizontal.set)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        scroll.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        tree.grid(row=0, column=0, sticky="nsew")
        tree.tag_configure("even", background="#17233a")
        tree.tag_configure("odd", background="#1c2a43")
        return tree

    def build_markets(self):
        self.label(self.markets, self.tr("All available currencies"), 20)
        self.label(self.markets, self.tr("Rates per 1 unit of the converter's source currency. Double-click to select a target currency."), muted=True)
        bar = ttk.Frame(self.markets)
        bar.pack(fill="x")
        ttk.Label(bar, text=self.tr("Find currency")).pack(side="left", padx=(0, 12))
        self.search_entry = ttk.Entry(bar, textvariable=self.search)
        self.search_entry.pack(side="left")
        Tooltip(self.search_entry, self.tr("Search by currency code, e.g. EUR or USD · Ctrl+F"))
        self.button(bar, self.tr("Reset"), lambda: self.search.set("")).pack(side="left", padx=8)
        self.search_trace = self.search.trace_add("write", lambda *args: self.fill_markets())
        self.button(self.markets, self.tr("Export rates as CSV"), self.export_rates).pack(anchor="e", pady=(10, 0))
        self.market_tree = self.table(self.markets, [("code", self.tr("Currency"), 120), ("rate", self.tr("Rate"), 220),
                                                     ("base", self.tr("Base"), 120), ("date", self.tr("Rate date / source"), 350)])
        self.market_tree.bind("<Double-Button-1>", self.open_market)

    def build_history(self):
        self.label(self.history_tab, self.tr("Your recent conversions"), 20)
        bar = ttk.Frame(self.history_tab)
        bar.pack(fill="x")
        self.button(bar, self.tr("Export CSV"), self.export_history).pack(side="right")
        self.button(bar, self.tr("Clear history"), self.clear_history).pack(side="right", padx=8)
        self.history_tree = self.table(self.history_tab, [("time", self.tr("Time"), 150), ("amount", self.tr("Amount"), 120),
            ("pair", self.tr("Currency pair"), 130), ("net", self.tr("Result"), 150), ("fee", self.tr("Fee (source)"), 120),
            ("date", self.tr("Rate date"), 110), ("source", self.tr("Source"), 110)])
        self.label(self.history_tab, self.tr("Up to 1,000 entries are stored locally. CSV decimal values are not rounded."), muted=True)

    def build_help(self):
        self.label(self.help_tab, self.tr("Understanding your numbers and data"), 22)
        text = self.tr("help_body", folder=self.store.folder, version=__version__)
        box = tk.Text(self.help_tab, bg=CARD, fg=TEXT, relief="flat", wrap="word", padx=22, pady=18)
        box.pack(fill="both", expand=True)
        box.insert("1.0", text)
        box.configure(state="disabled")

    def build_compare(self):
        self.label(self.compare_tab, self.tr("What is left after fees?"), 20)
        self.label(self.compare_tab, self.tr("Compare three offers using the amount and currency pair from the converter."), muted=True)
        self.label(self.compare_tab, self.tr("Assumes the same reference rate. Percentage and fixed fees are deducted in the source currency."), muted=True)
        grid = ttk.Frame(self.compare_tab)
        grid.pack(fill="x", pady=12)
        for col, title in enumerate((self.tr("Offer"), self.tr("Fee %"), self.tr("Fixed fee (source)"))):
            ttk.Label(grid, text=title, style="Muted.TLabel").grid(row=0, column=col, sticky="w", padx=(0, 24), pady=8)
        self.offers = []
        for i in range(3):
            variables = [tk.StringVar(value=self.tr("Offer {n}", n=i+1)), tk.StringVar(value="0"), tk.StringVar(value="0")]
            for col, var in enumerate(variables):
                ttk.Entry(grid, textvariable=var, width=18 if col == 0 else 10).grid(row=i+1, column=col, padx=(0, 16), pady=6, sticky="ew")
                var.trace_add("write", lambda *args: self.invalidate_comparison())
            self.offers.append(variables)
        self.button(self.compare_tab, self.tr("Compare offers"), self.compare, True).pack(anchor="w", pady=10)
        self.compare_status = tk.StringVar(value=self.tr("Enter your own fees and compare offers."))
        ttk.Label(self.compare_tab, textvariable=self.compare_status, foreground=ACCENT, wraplength=1000).pack(fill="x")
        self.compare_tree = self.table(self.compare_tab, [("name", self.tr("Offer"), 220), ("fee", self.tr("Fees (source)"), 180),
            ("net", self.tr("Payout (target)"), 220), ("difference", self.tr("Difference from best offer"), 240)])

    def invalidate_comparison(self):
        if hasattr(self, "compare_tree"):
            self.compare_tree.delete(*self.compare_tree.get_children())
            self.compare_status.set(self.tr("Inputs or rates changed · compare offers again."))

    def compare(self):
        self.invalidate_comparison()
        try:
            amount = number(self.amount.get())
            base, target = self.base.get(), self.target.get()
            results = []
            for i, (name, percent, fixed) in enumerate(self.offers):
                label = name.get().strip()[:60] or self.tr("Offer {n}", n=i+1)
                result = convert(amount, base, target, self.snapshot.rates, number(percent.get()), number(fixed.get()))
                results.append((label, result))
            results.sort(key=lambda item: item[1]["net"], reverse=True)
            best = results[0][1]["net"]
            for label, result in results:
                self.compare_tree.insert("", "end", values=(label, self.money(result["fee"], base) + " " + base,
                    self.money(result["net"], target) + " " + target, self.money(best-result["net"], target) + " " + target))
            self.compare_status.set(self.tr("{amount} {base} → {target} · Rate date {date} · Sorted by payout. Individual exchange-rate markups are not included.", amount=self.money(amount, base), base=base, target=target, date=self.snapshot.day or "DEMO"))
        except ValueError as exc:
            self.compare_status.set(self.tr.error(exc))

    def submit(self, key, fn, done):
        if key in self.pending:
            return
        self.pending.add(key)
        def work():
            try:
                self.events.put((key, done, fn(), None))
            except Exception as exc:
                self.events.put((key, done, None, exc))
        threading.Thread(target=work, daemon=True).start()

    def poll(self):
        while True:
            try:
                key, done, result, error = self.events.get_nowait()
            except queue.Empty:
                break
            self.pending.discard(key)
            if key == "rates":
                self.refresh_btn.configure(state="normal")
            if key == "chart":
                self.chart_btn.configure(state="normal")
            if error:
                if key == "chart":
                    self.chart_status.set(self.tr.error(error))
                else:
                    self.feedback.set(self.tr.error(error))
            else:
                done(result)
        self.poll_id = self.root.after(100, self.poll)

    def refresh(self):
        if "rates" in self.pending:
            return
        self.refresh_btn.configure(state="disabled")
        self.status.set(self.tr("Loading rates in the background …"))
        self.submit("rates", self.service.latest, self.apply_snapshot)

    def apply_snapshot(self, snapshot):
        self.snapshot = snapshot
        self.invalidate_comparison()
        codes = sorted(snapshot.rates)
        for var, box in ((self.base, self.base_box), (self.target, self.target_box)):
            box.configure(values=codes)
            if var.get() not in codes:
                var.set("EUR" if "EUR" in codes else codes[0])
        if snapshot.source == "demo":
            self.status.set(self.tr("DEMO · Undated sample rates · Do not use for actual conversions"))
        else:
            source = self.tr("Retrieved online") if snapshot.source == "online" else self.tr("Offline / saved rates")
            self.status.set(self.tr("{source} · Rate date {date} · {count} currencies · Frankfurter / ECB", source=source, date=snapshot.day, count=len(codes)))
        self.feedback.set(self.tr.error(snapshot.warning))
        self.calculate(save=False)
        self.fill_markets()

    def calculate(self, save=True):
        try:
            amount, percent, fixed = number(self.amount.get()), number(self.percent.get()), number(self.fixed.get())
            base, target = self.base.get(), self.target.get()
            result = convert(amount, base, target, self.snapshot.rates, percent, fixed)
        except ValueError as exc:
            self.last_result = None
            self.copy_btn.configure(state="disabled")
            try:
                number(self.amount.get())
            except ValueError:
                self.amount_entry.configure(style="Invalid.TEntry")
            self.result.set(self.tr("Check your input"))
            self.detail.set("")
            self.feedback.set(self.tr.error(exc))
            return
        self.last_result = (result, target)
        self.copy_btn.configure(state="normal")
        self.amount_entry.configure(style="TEntry")
        self.result.set(f"{self.money(result['net'], target)} {target}")
        self.detail.set(self.tr("1 {base} = {rate} {target}\nFees: {fee} {base}\nBefore fees: {gross} {target}",
                                base=base, target=target, rate=f"{result['rate']:.6f}",
                                fee=self.money(result['fee'], base), gross=self.money(result['gross'], target)))
        if save:
            self.animator.run("result", lambda t: self.result_card.pulse(1-t), 650)
            try:
                self.store.add({"time": datetime.now().isoformat(timespec="seconds"), "amount": str(amount),
                    "base": base, "target": target, "net": str(result["net"]), "rate": str(result["rate"]),
                    "fee": str(result["fee"]), "date": self.snapshot.day or "DEMO", "source": self.snapshot.source})
                self.feedback.set(self.tr("Conversion saved locally.") + (self.tr(" DEMO rates used.") if self.snapshot.source == "demo" else ""))
                self.fill_history()
            except OSError:
                self.feedback.set(self.tr("Converted, but history could not be saved."))

    def invalidate_result(self):
        self.update_fee_hint()
        self.invalidate_comparison()
        self.last_result = None
        self.copy_btn.configure(state="disabled")
        self.amount_entry.configure(style="TEntry")
        self.result.set(self.tr("Recalculate"))
        self.detail.set("")
        self.feedback.set("")

    def scroll_converter(self, event):
        if self.tabs.select() == str(self.converter) and event.widget != self.favorites:
            self.viewport.yview_scroll(int(-event.delta / 120), "units")

    def pair_changed(self, event=None):
        self.animator.cancel("chart")
        self.invalidate_comparison()
        self.chart_points = []
        self.chart_key = None
        self.chart_status.set(self.tr("Pair changed · reload the chart."))
        self.draw_chart()
        self.calculate(save=False)
        self.fill_markets()

    def swap(self):
        a, b = self.base.get(), self.target.get()
        self.base.set(b)
        self.target.set(a)
        self.pair_changed()

    def copy(self):
        if self.last_result:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.result.get())
            self.feedback.set(self.tr("Result copied."))

    def fill_favorites(self):
        self.favorites.delete(0, "end")
        pairs = self.store.prefs.get("favorites", ["EUR/USD", "EUR/GBP", "EUR/CHF"])
        if not isinstance(pairs, list):
            pairs = []
        for pair in pairs[:30]:
            if isinstance(pair, str) and len(pair) == 7 and pair[3] == "/":
                self.favorites.insert("end", pair)

    def save_favorites(self):
        self.store.prefs["favorites"] = list(self.favorites.get(0, "end"))
        try:
            self.store.save()
        except OSError:
            self.feedback.set(self.tr("Could not save favorites."))

    def favorite(self):
        pair = self.base.get() + "/" + self.target.get()
        if pair not in self.favorites.get(0, "end") and self.favorites.size() < 30:
            self.favorites.insert("end", pair)
            self.save_favorites()

    def remove_favorite(self):
        if self.favorites.curselection():
            self.favorites.delete(self.favorites.curselection()[0])
            self.save_favorites()

    def open_favorite(self, event=None):
        if not self.favorites.curselection():
            return
        base, target = self.favorites.get(self.favorites.curselection()[0]).split("/")
        if base not in self.snapshot.rates or target not in self.snapshot.rates:
            self.feedback.set(self.tr("This pair is not available in the current rate snapshot."))
            return
        self.base.set(base)
        self.target.set(target)
        self.pair_changed()

    def market_rows(self):
        rates, base = self.snapshot.rates, self.base.get()
        return [{"code": code, "rate": str(rates[code] / rates[base]), "base": base,
                 "date": self.snapshot.day or "DEMO", "source": self.snapshot.source}
                for code in sorted(rates) if self.search.get().upper().strip() in code]

    def fill_markets(self):
        self.market_tree.delete(*self.market_tree.get_children())
        for i, row in enumerate(self.market_rows()):
            self.market_tree.insert("", "end", tags=("odd" if i%2 else "even",), values=(row["code"], f"{Decimal(row['rate']):.6f}", row["base"], row["date"] + " / " + self.source_label(row["source"])))

    def open_market(self, event=None):
        if self.market_tree.selection():
            self.target.set(self.market_tree.item(self.market_tree.selection()[0], "values")[0])
            self.pair_changed()
            self.tabs.select(self.converter)

    def source_label(self, source):
        return self.tr({"online": "Retrieved online", "cache": "Cache", "demo": "DEMO"}.get(source, source))

    def fill_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        for i, row in enumerate(self.store.rows):
            self.history_tree.insert("", "end", tags=("odd" if i%2 else "even",), values=(row["time"].replace("T", " "), row["amount"],
                row["base"] + "/" + row["target"], row["net"], row["fee"], row["date"], self.source_label(row["source"])))

    def save_csv(self, rows, fields, name):
        path = filedialog.asksaveasfilename(parent=self.root, title=self.tr("Export CSV"), defaultextension=".csv",
                                          initialfile=name, filetypes=[("CSV", "*.csv")])
        if path:
            try:
                export_csv(path, rows, fields)
                messagebox.showinfo(self.tr("Export"), self.tr("CSV file saved."), parent=self.root)
            except OSError as exc:
                messagebox.showerror(self.tr("Export failed"), self.tr.error(exc), parent=self.root)

    def export_rates(self):
        self.save_csv(self.market_rows(), ["code", "rate", "base", "date", "source"], "QuantumFX-Rates.csv")

    def export_history(self):
        self.save_csv(self.store.rows, ["time", "amount", "base", "target", "net", "rate", "fee", "date", "source"], "QuantumFX-History.csv")

    def export_chart(self):
        if not self.chart_points or not self.chart_key:
            self.chart_status.set(self.tr("Load a rate history first."))
            return
        base, target, _ = self.chart_key
        self.save_csv([{"date": day, "base": base, "target": target, "rate": str(rate)} for day, rate in self.chart_points],
                      ["date", "base", "target", "rate"], f"QuantumFX-{base}-{target}.csv")

    def clear_history(self):
        if messagebox.askyesno(self.tr("Clear history"), self.tr("Permanently delete all saved conversions?"), parent=self.root):
            try:
                self.store.clear()
                self.fill_history()
            except OSError as exc:
                messagebox.showerror(self.tr("Deletion failed"), self.tr.error(exc), parent=self.root)

    def load_chart(self):
        if "chart" in self.pending:
            return
        key = (self.base.get(), self.target.get(), int(self.days.get()))
        self.chart_key = key
        self.chart_points = []
        self.draw_chart()
        self.chart_status.set(self.tr("Loading historical reference rates …"))
        self.chart_btn.configure(state="disabled")
        def done(result):
            if self.chart_key != key or key != (self.base.get(), self.target.get(), int(self.days.get())):
                self.chart_status.set(self.tr("Selection changed · reload the chart."))
                return
            self.chart_points, source = result
            self.chart_source = source
            self.describe_chart()
            self.animator.run("chart", lambda t: self.draw_chart(t), 700)
        self.submit("chart", lambda: self.service.history(*key), done)

    def describe_chart(self):
        first, last = self.chart_points[0][1], self.chart_points[-1][1]
        change = (last / first - 1) * 100
        key = self.chart_key or (self.base.get(), self.target.get(), int(self.days.get()))
        self.chart_status.set(self.tr("{pair} · {change} % over the available period · {count} data points · {source}",
                                     pair=f"{key[0]}/{key[1]}", change=self.tr.amount(f"{change:+.2f}"),
                                     count=len(self.chart_points),
                                     source=self.tr("Cache" if getattr(self, "chart_source", None) == "cache" else "Reference rates")))

    def draw_chart(self, progress=1.0):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if not self.chart_points:
            c.create_text(w / 2, h / 2, text=self.tr("Load rate history to see the trend"), fill=MUTED, width=max(180, w - 60))
            return
        values = [float(p[1]) for p in self.chart_points]
        low, high = min(values), max(values)
        pad = (high - low) * .12 or max(high * .01, .001)
        low, high = low - pad, high + pad
        left, right, top, bottom = 78, max(100, w - 24), 28, max(90, h - 40)
        for i in range(5):
            y = top + (bottom - top) * i / 4
            c.create_line(left, y, right, y, fill="#263951")
            c.create_text(left - 9, y, anchor="e", text=f"{high - (high-low)*i/4:.4f}", fill=MUTED, font=(self.font_family, 9))
        ordinals = [datetime.fromisoformat(p[0]).toordinal() for p in self.chart_points]
        span = max(1, ordinals[-1] - ordinals[0])
        self.chart_coords = [(left + (right-left) * (day-ordinals[0]) / span,
                              bottom - (v-low)/(high-low)*(bottom-top)) for day, v in zip(ordinals, values)]
        visible = self.chart_coords[:max(1, int(len(self.chart_coords)*progress))]
        flat = [v for point in visible for v in point]
        if len(flat) >= 4:
            c.create_polygon(*flat, visible[-1][0], bottom, visible[0][0], bottom, fill="#1b303a", outline="")
            c.create_line(*flat, fill="#204e48", width=7)
            c.create_line(*flat, fill=MINT, width=2)
        else:
            x, y = self.chart_coords[0]
            c.create_oval(x-3, y-3, x+3, y+3, fill=ACCENT, outline="")
        c.create_text(left, h-18, anchor="w", text=self.chart_points[0][0], fill=MUTED)
        c.create_text(right, h-18, anchor="e", text=self.chart_points[-1][0], fill=MUTED)

    def chart_hover(self, event):
        if not self.chart_points or not hasattr(self, "chart_coords"):
            return
        i = min(range(len(self.chart_coords)), key=lambda j: abs(self.chart_coords[j][0] - event.x))
        self.canvas.delete("hover")
        x, y = self.chart_coords[i]
        day, rate = self.chart_points[i]
        self.canvas.create_oval(x-4, y-4, x+4, y+4, fill=TEXT, outline=ACCENT, tags="hover")
        self.canvas.create_text(self.canvas.winfo_width()/2, 12, text=f"{day}   ·   {rate}", fill=TEXT, tags="hover")

    def callback_error(self, kind, value, tb):
        logging.error("UI error", exc_info=(kind, value, tb))
        messagebox.showerror("QuantumFX", self.tr("This action failed. See the local log file for details."), parent=self.root)

    def close(self):
        self.animator.stop()
        self.snake.pause()
        self.root.after_cancel(self.poll_id)
        self.store.prefs.update(base=self.base.get(), target=self.target.get())
        try:
            self.store.save()
        except OSError:
            pass
        self.root.destroy()
