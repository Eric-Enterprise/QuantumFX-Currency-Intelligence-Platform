"""Small native UI primitives; animations never block the Tk event loop."""
import time
import tkinter as tk
from tkinter import font as tkfont

BG = "#090d17"
CARD = "#131b2b"
TEXT = "#edf2fc"
MUTED = "#8e9db6"
ACCENT = "#ab9aff"
MINT = "#60e8c2"
SIDEBAR = "#0f1421"


def blend(a, b, t):
    return "#" + "".join(f"{round(int(a[i:i+2], 16) * (1-t) + int(b[i:i+2], 16) * t):02x}"
                         for i in (1, 3, 5))


class Animator:
    def __init__(self, root, enabled=True):
        self.root, self.enabled, self.jobs = root, enabled, {}

    def cancel(self, key):
        job = self.jobs.pop(key, None)
        if job:
            self.root.after_cancel(job)

    def stop(self):
        for key in list(self.jobs):
            self.cancel(key)

    def run(self, key, update, duration=240):
        self.cancel(key)
        if not self.enabled:
            update(1.0)
            return
        start = time.monotonic()
        def frame():
            self.jobs.pop(key, None)
            t = min(1.0, (time.monotonic() - start) * 1000 / duration)
            update(1 - (1-t) ** 3)
            if t < 1 and self.root.winfo_exists():
                self.jobs[key] = self.root.after(16, frame)
        frame()


def rounded(canvas, x1, y1, x2, y2, radius=12, **kwargs):
    r = min(radius, (x2-x1)/2, (y2-y1)/2)
    return canvas.create_polygon(x1+r,y1, x2-r,y1, x2,y1, x2,y1+r,
        x2,y2-r, x2,y2, x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1,
        smooth=True, splinesteps=24, **kwargs)


class MotionButton(tk.Canvas):
    """Rounded button with pointer, focus, keyboard and disabled states."""
    def __init__(self, parent, text, command, animator, accent=False, background=BG):
        self.text, self.command, self.animator = text, command, animator
        self.accent = accent
        self.disabled = False
        self.hover = 0.0
        self.focused = False
        self.pressed = False
        self.face = tkfont.Font(family="Segoe UI", size=10, weight="bold" if accent else "normal")
        width = self.face.measure(text) + 32
        super().__init__(parent, width=width, height=44, bg=background, highlightthickness=0,
                         bd=0, takefocus=True, cursor="hand2")
        self.bind("<Configure>", lambda e: self.draw())
        self.bind("<Enter>", lambda e: self.transition(1))
        self.bind("<Leave>", lambda e: self.transition(0))
        self.bind("<FocusIn>", lambda e: self.set_focus(True))
        self.bind("<FocusOut>", lambda e: self.set_focus(False))
        self.bind("<ButtonPress-1>", self.press)
        self.bind("<ButtonRelease-1>", self.release)
        self.bind("<space>", self.invoke)
        self.bind("<Return>", self.invoke)
        self.bind("<Destroy>", lambda e: self.animator.cancel(str(self)))

    def set_focus(self, focused):
        self.focused = focused
        self.draw()

    def transition(self, target):
        start = self.hover
        def update(t):
            self.hover = start + (target-start) * t
            self.draw()
        self.animator.run(str(self), update, 150)

    def configure(self, cnf=None, **kwargs):
        if "state" in kwargs:
            self.disabled = kwargs.pop("state") == "disabled"
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            kwargs["width"] = self.face.measure(self.text) + 32
        result = super().configure(cnf, **kwargs)
        if hasattr(self, "face"):
            self.draw()
        return result

    config = configure

    def press(self, event):
        if not self.disabled:
            self.focus_set()
            self.pressed = True
            self.draw()

    def release(self, event):
        pressed = self.pressed
        self.pressed = False
        self.draw()
        if pressed and 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height():
            self.invoke()

    def invoke(self, event=None):
        if not self.disabled:
            self.command()
        return "break"

    def draw(self):
        self.delete("all")
        width, height = self.winfo_width(), self.winfo_height()
        fill = blend(ACCENT if self.accent else "#1b263b", "#c7bbff" if self.accent else "#2b3c57", self.hover)
        if self.disabled:
            fill = "#192132"
        inset = 3 if self.pressed else 1
        rounded(self, inset, inset, max(inset+1, width-inset), height-inset, fill=fill,
                outline=ACCENT if self.focused else (fill if self.accent else "#29364d"), width=1)
        self.create_text(width/2, height/2 + int(self.pressed), text=self.text, font=self.face,
                         fill=MUTED if self.disabled else (BG if self.accent else TEXT))


class Hero(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg=BG, height=140, highlightthickness=0)
        self.bind("<Configure>", lambda e: self.draw())

    def draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        rounded(self, 0, 0, w, h, radius=22, fill="#172137", outline="#2b3653")
        for i in range(5):
            x = w - 190 + i*45
            self.create_oval(x, -110+i*8, x+310, 190+i*8, outline=blend("#38416a", "#172137", i/5), width=1)
        self.create_text(28, 26, anchor="w", text="QUANTUMFX  /  DEIN FINANZÜBERBLICK", fill=ACCENT, font=("Segoe UI", 9, "bold"))
        self.create_text(28, 66, anchor="w", text="Währungen. Einfach klar.", fill=TEXT, font=("Segoe UI", 27, "bold"))
        self.create_text(28, 110, anchor="w", text="Umrechnen, vergleichen und Entwicklungen entdecken.", fill=MUTED, font=("Segoe UI", 11))
