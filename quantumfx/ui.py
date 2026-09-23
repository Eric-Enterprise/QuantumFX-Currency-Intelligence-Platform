"""Small native UI primitives; animations never block the Tk event loop."""
from .i18n import Translator, font_family
import time
import tkinter as tk
import math
from tkinter import font as tkfont

BG = "#0b1021"
CARD = "#17233a"
TEXT = "#edf2fc"
MUTED = "#acbad3"
ACCENT = "#b9adff"
MINT = "#60e8c2"
SIDEBAR = "#111a2e"


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


def glass(canvas, x1, y1, x2, y2, radius=20, top="#303c60", bottom="#17233a", glow=0):
    """Opaque layered glass appearance; no OS transparency or readability loss."""
    if x2 <= x1 or y2 <= y1:
        return
    rounded(canvas, x1+1, y1+5, x2-1, y2+5, radius, fill="#080e1d", outline="")
    radius = min(radius, (x2-x1)/2, (y2-y1)/2)
    height = y2-y1
    for dy in range(0, int(height), 2):
        inset = 0
        if dy < radius:
            inset = radius-math.sqrt(max(0, radius**2-(radius-dy)**2))
        elif dy > height-radius:
            inset = radius-math.sqrt(max(0, radius**2-(dy-(height-radius))**2))
        canvas.create_line(x1+inset, y1+dy, x2-inset, y1+dy,
                           fill=blend(top, bottom, dy/height), width=2)
    rounded(canvas, x1, y1, x2, y2, radius, fill="", outline=blend("#4b5b80", "#abbbec", glow), width=1)
    canvas.create_line(x1+radius, y1+1, x2-radius, y1+1, fill=blend("#7484ad", "#cddaff", glow), width=1)


def icon(canvas, name, x, y, color=TEXT, size=18):
    """Resolution-independent line icons, not font-dependent emoji."""
    s = size / 24
    def line(*coords):
        canvas.create_line(*[x+v*s if i%2 == 0 else y+v*s for i,v in enumerate(coords)], fill=color, width=1.6, capstyle="round", joinstyle="round")
    def oval(a,b,c,d):
        canvas.create_oval(x+a*s,y+b*s,x+c*s,y+d*s,outline=color,width=1.6)
    def rect(a,b,c,d):
        canvas.create_rectangle(x+a*s,y+b*s,x+c*s,y+d*s,outline=color,width=1.6)
    if name == "swap":
        line(3,7,21,7,17,3); line(21,17,3,17,7,21)
    elif name == "chart":
        line(3,3,3,21,22,21); line(6,15,11,10,15,13,21,5)
    elif name == "globe":
        oval(2,2,22,22); oval(7,2,17,22); line(2,12,22,12)
    elif name == "compare":
        line(4,4,4,21,10,21); line(14,21,14,4,20,4); line(1,7,4,4,7,7); line(17,18,20,21,23,18)
    elif name == "history":
        oval(3,3,21,21); line(12,6,12,12,17,15)
    elif name == "game":
        line(3,7,21,7,23,19,18,19,15,15,9,15,6,19,1,19,3,7); line(5,10,5,14); line(3,12,7,12); oval(16,10,18,12)
    elif name == "help":
        oval(2,2,22,22); line(9,8,10,6,14,6,16,8,15,11,12,13,12,14); oval(11.5,17,12.5,18)
    elif name == "refresh":
        line(20,8,17,4,9,3,4,7,3,13,6,18,13,21,20,17); line(20,3,20,8,15,8)
    elif name == "expand":
        line(3,9,3,3,9,3); line(15,3,21,3,21,9); line(21,15,21,21,15,21); line(9,21,3,21,3,15)
    elif name == "close":
        line(5,5,19,19); line(19,5,5,19)
    elif name == "copy":
        rect(8,8,21,21); line(4,16,3,16,3,3,16,3,16,4)
    elif name == "star":
        points=[]
        for i in range(11):
            angle=-math.pi/2+i*math.pi/5; r=10 if i%2 == 0 else 4.5
            points += [12+math.cos(angle)*r,12+math.sin(angle)*r]
        line(*points)
    elif name == "download":
        line(12,2,12,16); line(7,11,12,16,17,11); line(3,16,3,21,21,21,21,16)
    elif name == "trash":
        line(3,6,21,6); line(8,6,8,3,16,3,16,6); line(5,6,6,21,18,21,19,6); line(10,10,10,17); line(14,10,14,17)
    elif name == "check":
        line(4,12,9,17,20,5)
    elif name == "play":
        line(7,3,21,12,7,21,7,3)
    elif name == "pause":
        line(8,4,8,20); line(16,4,16,20)
    elif name == "sparkles":
        line(11,2,13,9,20,11,13,13,11,20,9,13,2,11,9,9,11,2); line(20,1,20,5); line(18,3,22,3)


def infer_icon(text):
    text = getattr(text, "source", text)
    for word, name in [("copy", "copy"), ("refresh", "refresh"), ("Fullscreen", "expand"),
                       ("Window", "expand"), ("Close", "close"), ("CSV", "download"),
                       ("export", "download"), ("remove", "trash"), ("clear", "trash"),
                       ("save pair", "star"), ("convert", "swap"), ("Convert", "swap"),
                       ("compare", "compare"), ("load", "refresh"), ("Animation", "sparkles"),
                       ("New game", "play"), ("Pause", "pause"), ("⇄", "swap")]:
        if word.casefold() in text.casefold():
            return name
    return None


class Tooltip:
    def __init__(self, widget, text):
        self.widget, self.text, self.job, self.popup = widget, text, None, None
        widget.bind("<Enter>", self.schedule, add=True)
        widget.bind("<FocusIn>", self.schedule, add=True)
        for event in ("<Leave>", "<FocusOut>", "<ButtonPress>", "<Destroy>"):
            widget.bind(event, self.hide, add=True)

    def schedule(self, event=None):
        self.hide()
        self.job = self.widget.after(650, self.show)

    def show(self):
        self.job = None
        if not self.widget.winfo_exists():
            return
        self.popup = tk.Toplevel(self.widget)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        tk.Label(self.popup, text=self.text, bg="#31405f", fg=TEXT, padx=12, pady=9,
                 wraplength=290, justify="left", font=(font_family(getattr(self.text, "language", "en")), 10)).pack()
        self.popup.update_idletasks()
        x = min(self.widget.winfo_rootx(), self.widget.winfo_screenwidth()-self.popup.winfo_reqwidth()-12)
        y = min(self.widget.winfo_rooty()+self.widget.winfo_height()+6, self.widget.winfo_screenheight()-self.popup.winfo_reqheight()-12)
        self.popup.geometry(f"+{max(0,x)}+{max(0,y)}")

    def hide(self, event=None):
        if self.job:
            self.widget.after_cancel(self.job)
            self.job = None
        if self.popup:
            self.popup.destroy()
            self.popup = None


class MotionButton(tk.Canvas):
    """Rounded button with pointer, focus, keyboard and disabled states."""
    def __init__(self, parent, text, command, animator, accent=False, background=BG, icon_name=None, align="center", hint=None):
        self.text, self.command, self.animator = text, command, animator
        self.icon_name = icon_name or infer_icon(text)
        self.align = align
        self.accent = accent
        self.disabled = False
        self.hover = 0.0
        self.focused = False
        self.pressed = False
        self.face = tkfont.Font(family=font_family(getattr(text, "language", "en")), size=10, weight="bold" if accent else "normal")
        width = self.face.measure(text) + (64 if self.icon_name else 32)
        super().__init__(parent, width=width, height=48, bg=background, highlightthickness=0,
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
        self.tooltip = Tooltip(self, hint or text)

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
            kwargs["width"] = self.face.measure(self.text) + (64 if self.icon_name else 32)
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
        fill = blend("#7164c7" if self.accent else "#273957", "#9884ea" if self.accent else "#3a5279", self.hover)
        if self.disabled:
            fill = "#192132"
        inset = 3 if self.pressed else 1
        glass(self, inset, inset, max(inset+1, width-inset), height-5-inset, radius=13,
              top=fill, bottom=blend(fill, BG, .30), glow=1 if self.focused else self.hover*.65)
        color = MUTED if self.disabled else TEXT
        label = self.text.replace("★ ", "").replace("  ↗", "")
        if self.text == "⇄":
            label = ""
        text_width = self.face.measure(label)
        start = 16 if self.align == "left" else max(12, (width-text_width-(28 if self.icon_name else 0))/2)
        if self.icon_name:
            icon(self, self.icon_name, start, height/2-12, color, 18)
            start += 28
        self.create_text(start, height/2-2 + int(self.pressed), anchor="w", text=label, font=self.face, fill=color)


class Hero(tk.Canvas):
    def __init__(self, parent, translator=None):
        self.tr = translator or Translator()
        super().__init__(parent, bg=BG, height=96, highlightthickness=0)
        self.bind("<Configure>", lambda e: self.draw())

    def draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        glass(self, 1, 1, w-2, h-7, radius=24, top="#39466b", bottom="#1b2c47")
        if w > 720:
            for i in range(12):
                self.create_oval(w-290+i*5, -90+i*5, w+70-i*5, 215-i*5,
                                 outline=blend("#5c6095", "#23354e", i/12), width=2)
            icon(self, "sparkles", w-130, 29, "#c2b9ff", 46)
        self.create_text(25, 30, anchor="w", text=self.tr("Your money. In any currency."), fill=TEXT, font=(font_family(self.tr.language), 23, "bold"))
        self.create_text(25, 66, anchor="w", text=self.tr("Enter an amount. Choose currencies. Get clarity."), fill="#d3dcee", font=(font_family(self.tr.language), 10))


class GlassResult(tk.Canvas):
    def __init__(self, parent, result, detail, translator=None):
        self.tr = translator or Translator()
        super().__init__(parent, bg=BG, height=225, highlightthickness=0)
        self.result, self.detail = result, detail
        self.glow = 0
        self.face = tkfont.Font(family=font_family(self.tr.language), size=30, weight="bold")
        self.traces = [(v, v.trace_add("write", lambda *args: self.draw())) for v in (result, detail)]
        self.bind("<Configure>", lambda e: self.draw())
        self.bind("<Destroy>", self.dispose)

    def draw(self):
        self.delete("all")
        w, h = max(100, self.winfo_width()), self.winfo_height()
        glass(self, 1, 1, w-2, h-7, radius=24, top="#294959", bottom="#1b293f", glow=self.glow)
        icon(self, "check", 24, 23, MINT, 19)
        self.create_text(52, 33, anchor="w", text=self.tr("Your result · after fees"), fill="#c4dfdc", font=(font_family(self.tr.language), 10))
        value = self.result.get()
        face = self.face
        face.configure(size=30)
        while face.measure(value) > w-48 and face.cget("size") > 12:
            face.configure(size=face.cget("size")-1)
        self.create_text(24, 88, anchor="w", text=value, fill=MINT, font=face)
        self.create_line(24, 122, w-24, 122, fill="#3b5866")
        self.create_text(24, 142, anchor="nw", text=self.detail.get(), fill=TEXT, font=(font_family(self.tr.language), 10), width=w-48)

    def pulse(self, value):
        self.glow = value
        self.draw()

    def dispose(self, event):
        if event.widget == self:
            for variable, handle in self.traces:
                variable.trace_remove("write", handle)
