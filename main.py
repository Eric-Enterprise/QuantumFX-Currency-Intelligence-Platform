"""Windows entry point; --smoke-test validates the packaged GUI without network."""
import argparse
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import tkinter as tk
from pathlib import Path
from quantumfx.core import data_dir, atomic_json
from quantumfx.app import App


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--windowed", action="store_true", help="Start in a resizable window")
    parser.add_argument("--smoke-test", type=Path)
    args = parser.parse_args()
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass
    folder = data_dir()
    temp = tempfile.TemporaryDirectory() if args.smoke_test else None
    if temp:
        folder = Path(temp.name)
    try:
        folder.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(handlers=[RotatingFileHandler(folder / "QuantumFX.log", maxBytes=1_000_000, backupCount=2, encoding="utf-8")], level=logging.WARNING,
                            format="%(asctime)s %(levelname)s %(message)s")
    except OSError:
        logging.basicConfig(level=logging.WARNING)
    root = tk.Tk()
    app = App(root, folder, offline=args.offline or bool(args.smoke_test))
    if not args.windowed and not args.smoke_test:
        app.toggle_fullscreen()
    if args.smoke_test:
        def smoke():
            try:
                app.amount.set("1234,56")
                app.percent.set("2")
                app.fixed.set("1")
                app.calculate()
                assert app.last_result and len(app.store.rows) == 1
                app.swap()
                app.favorite()
                app.compare()
                assert len(app.compare_tree.get_children()) == 3
                app.tabs.select(app.snake_tab)
                root.update_idletasks()
                app.snake.start()
                app.snake.pause()
                assert len(app.snake.game.body) == 3
                app.chart_points = [("2026-01-01", __import__("decimal").Decimal("1.10")),
                                    ("2026-01-02", __import__("decimal").Decimal("1.15"))]
                app.draw_chart()
                for frame in (app.markets, app.compare_tab, app.history_tab, app.help_tab, app.converter):
                    app.tabs.select(frame)
                    root.update_idletasks()
                for language in ("de", "ko", "sv", "en"):
                    app.change_language(language)
                    root.update_idletasks()
                    assert app.tr.language == language
                    assert app.last_result and len(app.store.rows) == 1
                atomic_json(args.smoke_test, {"ok": True, "result": app.result.get(), "rows": len(app.store.rows),
                                             "languages": ["en", "de", "ko", "sv"]})
            except Exception as exc:
                atomic_json(args.smoke_test, {"ok": False, "error": str(exc)})
            finally:
                app.close()
        root.after(700, smoke)
    root.mainloop()
    logging.shutdown()
    if temp:
        temp.cleanup()


if __name__ == "__main__":
    main()
