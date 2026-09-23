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


class App:
    def __init__(self, root, folder=None, offline=False):
        self.root = root
        self.service = RateService(folder)
        self.store = Store(folder)
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
        self.result = tk.StringVar(value="Bereit zum Umrechnen")
        self.detail = tk.StringVar()
        self.feedback = tk.StringVar()
        self.chart_status = tk.StringVar(value="Währungspaar wählen und Kursverlauf laden.")
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
        self.root.option_add("*Font", "{Segoe UI} 10")
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
        style.configure("Accent.TButton", background=ACCENT, foreground=BG, font=("Segoe UI", 10, "bold"))
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
        w = ttk.Label(parent, text=text, font=("Segoe UI", size, "bold" if size >= 18 else "normal"),
                      style="Muted.TLabel" if muted else "TLabel")
        w.pack(anchor="w", pady=(0, 8))
        parent.bind("<Configure>", lambda e: w.configure(wraplength=max(200, e.width-16)), add=True)
        return w

    def button(self, parent, text, fn, accent=False):
        hints = {"⇄": "Ausgangs- und Zielwährung tauschen · Strg+S",
                 "Umrechnen & speichern  ↗": "Berechnet mit den angezeigten Kursen und speichert das Ergebnis im Verlauf · Enter",
                 "Vollbild  F11": "Vollbild ein- oder ausschalten · F11. Escape führt zurück ins Fenster.",
                 "Kurse aktualisieren": "Tagesreferenzkurse im Hintergrund aktualisieren · Strg+R"}
        return MotionButton(parent, text, fn, self.animator, accent, hint=hints.get(text))

    def build(self):
        sidebar = tk.Frame(self.root, bg=SIDEBAR, width=224, padx=16, pady=26)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="QuantumFX", bg=SIDEBAR, fg=TEXT, font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(sidebar, text="VERSION 2.2", bg=SIDEBAR, fg=ACCENT, font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 28))
        self.nav = tk.Frame(sidebar, bg=SIDEBAR)
        self.nav.pack(fill="x")
        self.motion_btn = MotionButton(sidebar, "Effekte an" if self.animator.enabled else "Effekte aus",
                                       self.toggle_motion, self.animator, background=SIDEBAR, icon_name="sparkles",
                                       hint="Animationen ein- oder ausschalten. Die Einstellung bleibt gespeichert.")
        self.motion_btn.pack(side="bottom", fill="x", pady=8)
        outer = ttk.Frame(self.root, padding=(24, 18))
        outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 18))
        self.page_title = ttk.Label(header, text="Übersicht", font=("Segoe UI", 23, "bold"))
        self.page_title.pack(side="left")
        self.button(header, "Schließen", self.close).pack(side="right", padx=(8, 0))
        self.full_btn = self.button(header, "Vollbild  F11", self.toggle_fullscreen)
        self.full_btn.pack(side="right", padx=8)
        self.refresh_btn = self.button(header, "Aktualisieren", self.refresh)
        self.refresh_btn.pack(side="right")
        status_line = ttk.Label(outer, textvariable=self.status, foreground=ACCENT, wraplength=1080)
        status_line.pack(fill="x", pady=(0, 15))
        outer.bind("<Configure>", lambda e: status_line.configure(wraplength=max(250, e.width-50)))
        ttk.Label(outer, text="Frankfurter / EZB · Tagesreferenzkurse · Gebühren sind eigene Annahmen.",
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
        for frame, title, glyph in [(self.converter, "Rechner", "swap"), (self.markets, "Währungen", "globe"),
                             (self.compare_tab, "Gebühren", "compare"), (self.history_tab, "Verlauf", "history"),
                             (self.snake_tab, "Snake", "game"), (self.help_tab, "Hilfe", "help")]:
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
        hero = Hero(content)
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
        self.label(left, "Dein Währungsrechner", 20)
        self.label(left, "1  Betrag eingeben", muted=True)
        self.amount_entry = ttk.Entry(left, textvariable=self.amount, font=("Segoe UI", 19))
        self.amount_entry.pack(fill="x", pady=(0, 6))
        self.label(left, "Zum Beispiel 1234,56 · ohne Tausendertrennzeichen", muted=True)
        Tooltip(self.amount_entry, "Komma oder Punkt als Dezimaltrennzeichen, z. B. 1234,56. Enter berechnet und speichert.")
        self.label(left, "2  Währungen wählen", muted=True)
        pair = ttk.Frame(left)
        pair.pack(fill="x", pady=(0, 16))
        source = ttk.Frame(pair)
        source.pack(side="left", fill="x", expand=True)
        self.label(source, "Von", muted=True)
        self.base_box = ttk.Combobox(source, textvariable=self.base, width=8, state="readonly")
        self.base_box.pack(fill="x")
        self.button(pair, "⇄", self.swap).pack(side="left", padx=10, pady=(26, 0))
        target = ttk.Frame(pair)
        target.pack(side="left", fill="x", expand=True)
        self.label(target, "Nach", muted=True)
        self.target_box = ttk.Combobox(target, textvariable=self.target, width=8, state="readonly")
        self.target_box.pack(fill="x")
        for box in (self.base_box, self.target_box):
            box.bind("<<ComboboxSelected>>", self.pair_changed)
        self.fees_expanded = False
        self.fee_toggle = MotionButton(left, "Gebühren hinzufügen · optional", self.toggle_fees,
                                       self.animator, icon_name="compare", hint="Optionale Prozent- und Fixgebühren öffnen. Ohne Eingabe wird keine Gebühr abgezogen.")
        self.fee_toggle.pack(anchor="w", pady=(0, 10))
        fees = ttk.Frame(left)
        self.fees_container = fees
        ttk.Label(fees, text="Prozent %").pack(side="left")
        percent_entry = ttk.Entry(fees, textvariable=self.percent, width=6)
        percent_entry.pack(side="left", padx=(8, 18))
        ttk.Label(fees, text="Fixbetrag").pack(side="left")
        fixed_entry = ttk.Entry(fees, textvariable=self.fixed, width=8)
        fixed_entry.pack(side="left", padx=8)
        Tooltip(percent_entry, "Prozentualer Abzug vom Ausgangsbetrag, zwischen 0 und 100.")
        Tooltip(fixed_entry, "Fester Abzug in der Von-Währung. Beispiel: 2 bedeutet 2 EUR bei Ausgangswährung EUR.")
        self.convert_btn = self.button(left, "Umrechnen & speichern  ↗", self.calculate, True)
        self.convert_btn.pack(fill="x")
        result_card = GlassResult(left, self.result, self.detail)
        self.result_card = result_card
        result_card.pack(fill="x", pady=18)
        actions = ttk.Frame(left)
        actions.pack(fill="x")
        self.copy_btn = self.button(actions, "Kopieren", self.copy)
        self.copy_btn.pack(side="left")
        self.button(actions, "★ Paar merken", self.favorite).pack(side="left", padx=8)
        ttk.Label(left, textvariable=self.feedback, foreground="#ffcc80", wraplength=385).pack(fill="x", pady=12)
        self.label(right, "Kursentwicklung", 20)
        toolbar = ttk.Frame(right)
        toolbar.pack(fill="x", pady=(0, 12))
        ttk.Label(toolbar, text="Zeitraum (Tage)", style="Muted.TLabel").pack(side="left")
        period = ttk.Combobox(toolbar, textvariable=self.days, values=(30, 90, 365), width=5, state="readonly")
        period.pack(side="left", padx=12)
        period.bind("<<ComboboxSelected>>", self.pair_changed)
        self.chart_btn = self.button(toolbar, "Verlauf laden", self.load_chart)
        self.chart_btn.pack(side="right")
        self.button(right, "Diagrammdaten als CSV", self.export_chart).pack(anchor="e", pady=(0, 8))
        self.canvas = tk.Canvas(right, bg=CARD, highlightthickness=0, height=280)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart())
        self.canvas.bind("<Motion>", self.chart_hover)
        ttk.Label(right, textvariable=self.chart_status, wraplength=540, style="Muted.TLabel").pack(fill="x", pady=12)
        self.label(right, "Favoriten · Doppelklick zum Öffnen", muted=True)
        self.favorites = tk.Listbox(right, bg=CARD, fg=TEXT, selectbackground="#28556a", height=3,
                                   relief="flat", highlightthickness=0, activestyle="none")
        self.favorites.pack(fill="x")
        self.favorites.bind("<Double-Button-1>", self.open_favorite)
        self.button(right, "Ausgewähltes Paar entfernen", self.remove_favorite).pack(anchor="e", pady=8)
        self.fill_favorites()
        self.build_markets()
        self.build_history()
        self.build_compare()
        self.build_help()
        self.snake = SnakePanel(self.snake_tab, self.store, self.animator)
        self.snake.pack(fill="both", expand=True)

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
        self.fee_toggle.configure(text="Gebühren ausblenden" if self.fees_expanded else
                                   ("Gebühren aktiv · bearbeiten" if active else "Gebühren hinzufügen · optional"))

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        self.full_btn.configure(text="Fenster  Esc" if self.fullscreen else "Vollbild  F11")

    def leave_fullscreen(self):
        if hasattr(self, "snake"):
            self.snake.pause()
        if self.fullscreen:
            self.toggle_fullscreen()

    def toggle_motion(self):
        self.animator.enabled = not self.animator.enabled
        self.animator.stop()
        self.motion_btn.configure(text="Effekte an" if self.animator.enabled else "Effekte aus")
        self.store.prefs["animations"] = self.animator.enabled
        try:
            self.store.save()
        except OSError:
            self.feedback.set("Darstellung konnte nicht gespeichert werden.")
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
        self.label(self.markets, "Alle verfügbaren Währungen", 20)
        self.label(self.markets, "Kurse je 1 Einheit der Ausgangswährung im Rechner. Doppelklick übernimmt die Zielwährung.", muted=True)
        bar = ttk.Frame(self.markets)
        bar.pack(fill="x")
        ttk.Label(bar, text="Währung suchen").pack(side="left", padx=(0, 12))
        self.search_entry = ttk.Entry(bar, textvariable=self.search)
        self.search_entry.pack(side="left")
        Tooltip(self.search_entry, "Nach Währungskürzel suchen, z. B. EUR oder USD · Strg+F")
        self.button(bar, "Zurücksetzen", lambda: self.search.set("")).pack(side="left", padx=8)
        self.search.trace_add("write", lambda *args: self.fill_markets())
        self.button(self.markets, "Kurse als CSV exportieren", self.export_rates).pack(anchor="e", pady=(10, 0))
        self.market_tree = self.table(self.markets, [("code", "Währung", 120), ("rate", "Kurs", 220),
                                                     ("base", "Basis", 120), ("date", "Kursdatum / Quelle", 350)])
        self.market_tree.bind("<Double-Button-1>", self.open_market)

    def build_history(self):
        self.label(self.history_tab, "Deine letzten Umrechnungen", 20)
        bar = ttk.Frame(self.history_tab)
        bar.pack(fill="x")
        self.button(bar, "CSV exportieren", self.export_history).pack(side="right")
        self.button(bar, "Verlauf löschen", self.clear_history).pack(side="right", padx=8)
        self.history_tree = self.table(self.history_tab, [("time", "Zeit", 150), ("amount", "Betrag", 120),
            ("pair", "Währungspaar", 130), ("net", "Ergebnis", 150), ("fee", "Gebühr (Basis)", 120),
            ("date", "Kursdatum", 110), ("source", "Quelle", 110)])
        self.label(self.history_tab, "Bis zu 1.000 Einträge werden lokal gespeichert. Dezimalwerte im CSV bleiben ungerundet.", muted=True)

    def build_help(self):
        self.label(self.help_tab, "Klarheit über Zahlen und Daten", 22)
        text = (
            "SO FUNKTIONIERT ES\n"
            "Betrag und Währungspaar wählen. Komma oder Punkt als Dezimaltrennzeichen verwenden; "
            "keine Tausendertrennzeichen. Prozentuale und fixe Gebühren werden vor der Umrechnung "
            "vom Ausgangsbetrag abgezogen. Erst die Anzeige wird gerundet.\n\n"
            "KURSQUELLEN\n"
            "Online: zuletzt abgerufene Frankfurter-Tagesreferenzkurse der EZB. An Wochenenden und Feiertagen "
            "kann das Kursdatum zurückliegen. Cache: gespeicherte Kurse mit ursprünglichem Kursdatum. "
            "DEMO: undatierte Beispielwerte aus dem Originalprojekt, nur zum Ausprobieren. "
            "Diagramme enthalten ausschließlich abgerufene oder gespeicherte historische Daten.\n\n"
            "BEDIENUNG\n"
            "Enter: umrechnen und speichern. Strg+R: Kurse aktualisieren. Strg+S: Währungen tauschen. "
            "Im Diagramm zeigt die Maus einzelne Datenpunkte. Ein Paarwechsel erfordert einen neuen Diagrammabruf.\n\n"
            "DATENSCHUTZ\n"
            "Beträge, Gebühren und Umrechnungsverlauf bleiben auf diesem Computer. Der Kursdienst erhält "
            "nur Währungspaar, Zeitraum und die üblichen Verbindungsdaten. Keine Anmeldung, keine Telemetrie. "
            "CSV-Dateien werden ausschließlich am gewählten Speicherort angelegt.\n\n"
            "LOKALE DATEN\n" + str(self.store.folder) + "\n\n"
            "QuantumFX 2.2\n"
            "F11: Vollbild wechseln. Escape: Vollbild verlassen und Snake pausieren. "
            "Animationen lassen sich in der Seitenleiste abschalten.\n"
            "Strg+F öffnet die Währungssuche. Hinweise erscheinen bei Mauszeiger oder Tastaturfokus auf Schaltflächen.\n"
            "Originalprojekt: oneiric-hammer/QuantumFX-Currency-Intelligence-Platform. "
            "Die Original-Lizenz liegt der Lieferung unverändert bei."
        )
        box = tk.Text(self.help_tab, bg=CARD, fg=TEXT, relief="flat", wrap="word", padx=22, pady=18)
        box.pack(fill="both", expand=True)
        box.insert("1.0", text)
        box.configure(state="disabled")

    def build_compare(self):
        self.label(self.compare_tab, "Was bleibt nach den Gebühren?", 20)
        self.label(self.compare_tab, "Vergleiche drei eigene Angebote mit dem Betrag und Währungspaar aus dem Rechner.", muted=True)
        self.label(self.compare_tab, "Annahme: gleicher Referenzkurs. Prozent und Fixbetrag werden in der Ausgangswährung abgezogen.", muted=True)
        grid = ttk.Frame(self.compare_tab)
        grid.pack(fill="x", pady=12)
        for col, title in enumerate(("Angebot", "Gebühr in %", "Fixgebühr (Basis)")):
            ttk.Label(grid, text=title, style="Muted.TLabel").grid(row=0, column=col, sticky="w", padx=(0, 24), pady=8)
        self.offers = []
        for i in range(3):
            variables = [tk.StringVar(value=f"Angebot {i+1}"), tk.StringVar(value="0"), tk.StringVar(value="0")]
            for col, var in enumerate(variables):
                ttk.Entry(grid, textvariable=var, width=18 if col == 0 else 10).grid(row=i+1, column=col, padx=(0, 16), pady=6, sticky="ew")
                var.trace_add("write", lambda *args: self.invalidate_comparison())
            self.offers.append(variables)
        self.button(self.compare_tab, "Angebote vergleichen", self.compare, True).pack(anchor="w", pady=10)
        self.compare_status = tk.StringVar(value="Eigene Gebühren eintragen und vergleichen.")
        ttk.Label(self.compare_tab, textvariable=self.compare_status, foreground=ACCENT, wraplength=1000).pack(fill="x")
        self.compare_tree = self.table(self.compare_tab, [("name", "Angebot", 220), ("fee", "Gebühren (Basis)", 180),
            ("net", "Auszahlung (Ziel)", 220), ("difference", "Abstand zum besten Angebot", 240)])

    def invalidate_comparison(self):
        if hasattr(self, "compare_tree"):
            self.compare_tree.delete(*self.compare_tree.get_children())
            self.compare_status.set("Eingaben oder Kurse geändert · Vergleich erneut berechnen.")

    def compare(self):
        self.invalidate_comparison()
        try:
            amount = number(self.amount.get())
            base, target = self.base.get(), self.target.get()
            results = []
            for i, (name, percent, fixed) in enumerate(self.offers):
                label = name.get().strip()[:60] or f"Angebot {i+1}"
                result = convert(amount, base, target, self.snapshot.rates, number(percent.get()), number(fixed.get()))
                results.append((label, result))
            results.sort(key=lambda item: item[1]["net"], reverse=True)
            best = results[0][1]["net"]
            for label, result in results:
                self.compare_tree.insert("", "end", values=(label, money(result["fee"], base) + " " + base,
                    money(result["net"], target) + " " + target, money(best-result["net"], target) + " " + target))
            self.compare_status.set(f"{money(amount, base)} {base} → {target} · Kursdatum {self.snapshot.day or 'DEMO'} · "
                                    "Sortiert nach Auszahlung. Individuelle Wechselkursaufschläge sind nicht enthalten.")
        except ValueError as exc:
            self.compare_status.set(str(exc))

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
                    self.chart_status.set(str(error))
                else:
                    self.feedback.set(str(error))
            else:
                done(result)
        self.poll_id = self.root.after(100, self.poll)

    def refresh(self):
        if "rates" in self.pending:
            return
        self.refresh_btn.configure(state="disabled")
        self.status.set("Kurse werden im Hintergrund geladen …")
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
            self.status.set("DEMO · Beispielkurse ohne Kursdatum · Nicht für tatsächliche Umrechnungen verwenden")
        else:
            source = "Online abgerufen" if snapshot.source == "online" else "Offline / gespeicherte Kurse"
            self.status.set(f"{source} · Kursdatum {snapshot.day} · {len(codes)} Währungen · Frankfurter / EZB")
        self.feedback.set(snapshot.warning)
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
            self.result.set("Eingabe prüfen")
            self.detail.set("")
            self.feedback.set(str(exc))
            return
        self.last_result = (result, target)
        self.copy_btn.configure(state="normal")
        self.amount_entry.configure(style="TEntry")
        self.result.set(f"{money(result['net'], target)} {target}")
        self.detail.set(f"1 {base} = {result['rate']:.6f} {target}\n"
                        f"Gebühren: {money(result['fee'], base)} {base}\n"
                        f"Ohne Gebühren: {money(result['gross'], target)} {target}")
        if save:
            self.animator.run("result", lambda t: self.result_card.pulse(1-t), 650)
            try:
                self.store.add({"time": datetime.now().isoformat(timespec="seconds"), "amount": str(amount),
                    "base": base, "target": target, "net": str(result["net"]), "rate": str(result["rate"]),
                    "fee": str(result["fee"]), "date": self.snapshot.day or "DEMO", "source": self.snapshot.source})
                self.feedback.set("Umrechnung lokal gespeichert." + (" DEMO-Kurse verwendet." if self.snapshot.source == "demo" else ""))
                self.fill_history()
            except OSError:
                self.feedback.set("Berechnet; Verlauf konnte nicht gespeichert werden.")

    def invalidate_result(self):
        self.update_fee_hint()
        self.invalidate_comparison()
        self.last_result = None
        self.copy_btn.configure(state="disabled")
        self.amount_entry.configure(style="TEntry")
        self.result.set("Neu berechnen")
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
        self.chart_status.set("Paar geändert · Verlauf erneut laden.")
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
            self.feedback.set("Ergebnis kopiert.")

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
            self.feedback.set("Favoriten konnten nicht gespeichert werden.")

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
            self.feedback.set("Dieses Paar ist im aktuellen Kursstand nicht verfügbar.")
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
            self.market_tree.insert("", "end", tags=("odd" if i%2 else "even",), values=(row["code"], f"{Decimal(row['rate']):.6f}", row["base"], row["date"] + " / " + row["source"]))

    def open_market(self, event=None):
        if self.market_tree.selection():
            self.target.set(self.market_tree.item(self.market_tree.selection()[0], "values")[0])
            self.pair_changed()
            self.tabs.select(self.converter)

    def fill_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        for i, row in enumerate(self.store.rows):
            self.history_tree.insert("", "end", tags=("odd" if i%2 else "even",), values=(row["time"].replace("T", " "), row["amount"],
                row["base"] + "/" + row["target"], row["net"], row["fee"], row["date"], row["source"]))

    def save_csv(self, rows, fields, name):
        path = filedialog.asksaveasfilename(parent=self.root, title="CSV exportieren", defaultextension=".csv",
                                          initialfile=name, filetypes=[("CSV", "*.csv")])
        if path:
            try:
                export_csv(path, rows, fields)
                messagebox.showinfo("Export", "CSV-Datei gespeichert.", parent=self.root)
            except OSError as exc:
                messagebox.showerror("Export fehlgeschlagen", str(exc), parent=self.root)

    def export_rates(self):
        self.save_csv(self.market_rows(), ["code", "rate", "base", "date", "source"], "QuantumFX-Kurse.csv")

    def export_history(self):
        self.save_csv(self.store.rows, ["time", "amount", "base", "target", "net", "rate", "fee", "date", "source"], "QuantumFX-Verlauf.csv")

    def export_chart(self):
        if not self.chart_points or not self.chart_key:
            self.chart_status.set("Zuerst einen Kursverlauf laden.")
            return
        base, target, _ = self.chart_key
        self.save_csv([{"date": day, "base": base, "target": target, "rate": str(rate)} for day, rate in self.chart_points],
                      ["date", "base", "target", "rate"], f"QuantumFX-{base}-{target}.csv")

    def clear_history(self):
        if messagebox.askyesno("Verlauf löschen", "Alle gespeicherten Umrechnungen unwiderruflich löschen?", parent=self.root):
            try:
                self.store.clear()
                self.fill_history()
            except OSError as exc:
                messagebox.showerror("Löschen fehlgeschlagen", str(exc), parent=self.root)

    def load_chart(self):
        if "chart" in self.pending:
            return
        key = (self.base.get(), self.target.get(), int(self.days.get()))
        self.chart_key = key
        self.chart_points = []
        self.draw_chart()
        self.chart_status.set("Historische Referenzkurse werden geladen …")
        self.chart_btn.configure(state="disabled")
        def done(result):
            if self.chart_key != key or key != (self.base.get(), self.target.get(), int(self.days.get())):
                self.chart_status.set("Auswahl geändert · Verlauf erneut laden.")
                return
            self.chart_points, source = result
            first, last = self.chart_points[0][1], self.chart_points[-1][1]
            change = (last / first - 1) * 100
            self.chart_status.set(f"{key[0]}/{key[1]} · {change:+.2f} % im verfügbaren Zeitraum · "
                                  f"{len(self.chart_points)} Datenpunkte · {'Cache' if source == 'cache' else 'Referenzkurse'}")
            self.animator.run("chart", lambda t: self.draw_chart(t), 700)
        self.submit("chart", lambda: self.service.history(*key), done)

    def draw_chart(self, progress=1.0):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if not self.chart_points:
            c.create_text(w / 2, h / 2, text="Kursverlauf laden, um die Entwicklung zu sehen", fill=MUTED, width=max(180, w - 60))
            return
        values = [float(p[1]) for p in self.chart_points]
        low, high = min(values), max(values)
        pad = (high - low) * .12 or max(high * .01, .001)
        low, high = low - pad, high + pad
        left, right, top, bottom = 78, max(100, w - 24), 28, max(90, h - 40)
        for i in range(5):
            y = top + (bottom - top) * i / 4
            c.create_line(left, y, right, y, fill="#263951")
            c.create_text(left - 9, y, anchor="e", text=f"{high - (high-low)*i/4:.4f}", fill=MUTED, font=("Segoe UI", 9))
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
        messagebox.showerror("QuantumFX", "Diese Aktion ist fehlgeschlagen. Details stehen in der lokalen Protokolldatei.", parent=self.root)

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
