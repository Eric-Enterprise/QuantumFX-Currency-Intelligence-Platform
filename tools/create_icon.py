"""Generate the application's geometric icon. Build-time only: Pillow required."""
from pathlib import Path
from PIL import Image, ImageDraw

image = Image.new("RGBA", (256, 256), (12, 20, 35, 255))
d = ImageDraw.Draw(image)
d.rounded_rectangle((12, 12, 244, 244), radius=52, fill="#152238", outline="#29435a", width=4)
d.ellipse((49, 42, 205, 198), outline="#56dfbe", width=20)
d.line((151, 161, 211, 219), fill="#56dfbe", width=20)
d.line([(64, 147), (103, 111), (132, 137), (183, 85)], fill="#e6edf7", width=10)
d.polygon([(162, 83), (187, 81), (185, 106)], fill="#e6edf7")
path = Path(__file__).resolve().parents[1] / "assets"
path.mkdir(exist_ok=True)
image.save(path / "quantumfx.ico", sizes=[(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)])
