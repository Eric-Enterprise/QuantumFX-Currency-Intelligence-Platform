"""Snake model and a self-contained arcade panel with scoped keyboard controls."""
import random
import tkinter as tk
from tkinter import ttk
from .ui import BG, CARD, TEXT, MUTED, ACCENT, MINT, MotionButton, rounded


class SnakeGame:
    def __init__(self, size=20, rng=None):
        self.size = size
        self.rng = rng or random.Random()
        self.reset()

    def reset(self):
        mid = self.size // 2
        self.body = [(mid, mid), (mid-1, mid), (mid-2, mid)]
        self.direction = (1, 0)
        self.queued = self.direction
        self.turned = False
        self.score = 0
        self.over = False
        self.won = False
        self.spawn()

    def spawn(self):
        free = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) not in self.body]
        self.food = self.rng.choice(free) if free else None
        if not free:
            self.over = self.won = True

    def turn(self, direction):
        if self.turned or direction == (-self.direction[0], -self.direction[1]):
            return
        if direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            self.queued = direction
            self.turned = True

    def step(self):
        if self.over:
            return
        self.direction = self.queued
        self.turned = False
        x, y = self.body[0]
        dx, dy = self.direction
        head = (x+dx, y+dy)
        eat = head == self.food
        occupied = self.body if eat else self.body[:-1]
        if not (0 <= head[0] < self.size and 0 <= head[1] < self.size) or head in occupied:
            self.over = True
            return
        self.body.insert(0, head)
        if eat:
            self.score += 10
            self.spawn()
        else:
            self.body.pop()


class SnakePanel(ttk.Frame):
    def __init__(self, parent, store, animator):
        super().__init__(parent)
        self.store, self.animator = store, animator
        self.game = SnakeGame()
        self.running = False
        self.timer = None
        self.started = False
        self.speed = tk.StringVar(value="Normal")
        saved = store.prefs.get("snake_highscore", 0)
        self.highscore = saved if isinstance(saved, int) and 0 <= saved <= 4000 else 0
        self.caption = tk.StringVar()
        self.notice = tk.StringVar(value="Arrow keys or WASD · Space to pause · Enter to restart")
        head = ttk.Frame(self)
        head.pack(fill="x", pady=(0, 14))
        ttk.Label(head, text="A little break. A longer snake.", font=("Segoe UI", 19, "bold")).pack(anchor="w")
        ttk.Label(head, textvariable=self.caption, foreground=MINT, font=("Segoe UI", 12)).pack(anchor="w", pady=8)
        actions = ttk.Frame(self)
        actions.pack(fill="x")
        MotionButton(actions, "New game", self.start, animator, True).pack(side="left")
        self.pause_btn = MotionButton(actions, "Pause / Resume", self.toggle, animator)
        self.pause_btn.pack(side="left", padx=10)
        speeds = ttk.Combobox(actions, textvariable=self.speed, values=("Relaxed", "Normal", "Fast"), width=12, state="readonly")
        speeds.pack(side="left", padx=8)
        speeds.bind("<<ComboboxSelected>>", lambda e: self.pause())
        self.canvas = tk.Canvas(self, background=BG, highlightthickness=0, takefocus=True, height=460)
        self.canvas.pack(fill="both", expand=True, pady=12)
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.canvas.bind("<Button-1>", lambda e: self.canvas.focus_set())
        self.canvas.bind("<KeyPress>", self.key)
        self.bind("<Destroy>", self.destroyed)
        ttk.Label(self, textvariable=self.notice, style="Muted.TLabel").pack(anchor="w")
        self.update_caption()

    def update_caption(self):
        self.caption.set(f"SCORE  {self.game.score:03d}     /     BEST  {self.highscore:03d}")

    def start(self):
        self.pause()
        self.game.reset()
        self.started = self.running = True
        self.canvas.focus_set()
        self.update_caption()
        self.draw()
        self.schedule()

    def schedule(self):
        if self.running and self.timer is None:
            delay = {"Relaxed": 170, "Normal": 115, "Fast": 75}.get(self.speed.get(), 115)
            self.timer = self.after(delay, self.tick)

    def tick(self):
        self.timer = None
        if not self.running:
            return
        previous = list(self.game.body)
        self.game.step()
        if self.game.score > self.highscore:
            self.highscore = self.game.score
            self.store.prefs["snake_highscore"] = self.highscore
            try:
                self.store.save()
            except OSError:
                self.notice.set("High score is kept for this session; saving failed.")
        if self.game.over:
            self.running = False
        self.update_caption()
        if self.running:
            self.animator.run(str(self)+"-move", lambda t: self.draw(t, previous), 65)
        else:
            self.draw()
        self.schedule()

    def pause(self):
        self.animator.cancel(str(self)+"-move")
        self.running = False
        if self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None
        self.draw()

    def toggle(self):
        if not self.started or self.game.over:
            self.start()
        elif self.running:
            self.pause()
        else:
            self.running = True
            self.canvas.focus_set()
            self.draw()
            self.schedule()

    def key(self, event):
        keys = {"Up": (0,-1), "w": (0,-1), "Down": (0,1), "s": (0,1),
                "Left": (-1,0), "a": (-1,0), "Right": (1,0), "d": (1,0)}
        key = event.keysym
        if key in keys and self.running:
            self.game.turn(keys[key])
        elif key == "space":
            self.toggle()
        elif key == "Return":
            self.start()
        elif key == "Escape":
            self.pause()
            return None
        return "break"

    def draw(self, progress=1.0, previous=None):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        cell = max(1, min(w-24, h-24) / self.game.size)
        side = cell * self.game.size
        ox, oy = (w-side)/2, (h-side)/2
        rounded(c, ox-8, oy-8, ox+side+8, oy+side+8, fill=CARD, outline="#2d3d56")
        for i in range(1, self.game.size):
            c.create_line(ox+i*cell, oy, ox+i*cell, oy+side, fill="#182438")
            c.create_line(ox, oy+i*cell, ox+side, oy+i*cell, fill="#182438")
        if self.game.food:
            x, y = self.game.food
            c.create_oval(ox+x*cell+cell*.2, oy+y*cell+cell*.2,
                          ox+(x+1)*cell-cell*.2, oy+(y+1)*cell-cell*.2, fill=ACCENT, outline="")
        for i, (x, y) in enumerate(self.game.body):
            if previous and i < len(previous):
                px, py = previous[i]
                x, y = px+(x-px)*progress, py+(y-py)*progress
            rounded(c, ox+x*cell+1, oy+y*cell+1, ox+(x+1)*cell-1, oy+(y+1)*cell-1,
                    radius=5, fill=MINT if i == 0 else "#249f85", outline="")
        if not self.running:
            label = "YOU WIN!" if self.game.won else ("GAME OVER" if self.game.over else ("PAUSE" if self.started else "SNAKE ARCADE"))
            rounded(c, w/2-150, h/2-44, w/2+150, h/2+44, fill="#1e2940", outline=ACCENT)
            c.create_text(w/2, h/2-10, text=label, fill=TEXT, font=("Segoe UI", 20, "bold"))
            c.create_text(w/2, h/2+22, text="New game / Space", fill=MUTED, font=("Segoe UI", 10))

    def destroyed(self, event):
        if event.widget == self:
            self.animator.cancel(str(self)+"-move")
            if self.timer is not None:
                self.after_cancel(self.timer)
                self.timer = None
