"""Opt-in real Windows GUI tests: QUANTUMFX_GUI_TESTS=1 python -m pytest."""
import os
import queue
import time
from decimal import Decimal as D
from datetime import date
import pytest

pytestmark = pytest.mark.skipif(os.environ.get("QUANTUMFX_GUI_TESTS") != "1", reason="Opt-in GUI tests")


@pytest.fixture(scope="module")
def tk_root():
    import tkinter as tk
    root = tk.Tk()
    yield root
    root.destroy()


@pytest.fixture
def app(tmp_path, tk_root):
    from quantumfx.app import App
    root = tk_root
    instance = App(root, tmp_path, offline=True)
    root.update()
    yield instance
    instance.animator.stop()
    instance.snake.pause()
    root.after_cancel(instance.poll_id)
    root.unbind("<MouseWheel>")
    for child in root.winfo_children():
        child.destroy()


def test_fee_calculation_and_invalid_edit(app):
    app.amount.set("100")
    app.percent.set("2")
    app.fixed.set("1")
    app.calculate()
    assert app.last_result[0]["net"] == D("112.52")
    assert len(app.store.rows) == 1
    app.amount.set("abc")
    assert app.last_result is None
    app.calculate()
    assert len(app.store.rows) == 1 and app.last_result is None


def test_swap_does_not_store_implicit_conversion(app):
    app.swap()
    assert (app.base.get(), app.target.get()) == ("USD", "EUR")
    assert len(app.store.rows) == 0


def test_favorites_deduplicated(app):
    app.favorite()
    app.favorite()
    assert list(app.favorites.get(0, "end")).count("EUR/USD") == 1


def test_comparison_sort_and_invalidation(app):
    app.offers[0][1].set("3")
    app.offers[1][1].set("1")
    app.offers[2][1].set("2")
    app.compare()
    first = app.compare_tree.get_children()[0]
    assert app.compare_tree.item(first, "values")[0] == "Angebot 2"
    app.amount.set("50")
    assert app.compare_tree.get_children() == ()


def test_search_and_target_selection(app):
    app.search.set("gbp")
    rows = app.market_tree.get_children()
    assert len(rows) == 1
    app.market_tree.selection_set(rows[0])
    app.open_market()
    assert app.target.get() == "GBP"


def test_chart_stale_response_rejected(app):
    calls = []
    app.submit = lambda key, work, done: calls.append(done)
    app.load_chart()
    app.swap()
    calls[0](([(date.today().isoformat(), D("1.2"))], "online"))
    assert app.chart_points == []


def test_constant_chart_draws(app):
    app.chart_points = [("2026-01-01", D(1)), ("2026-01-04", D(1))]
    app.draw_chart()
    assert len(app.canvas.find_all()) > 0
    assert len(app.chart_coords) == 2


def test_background_queue(app):
    done = []
    app.submit("test", lambda: 42, done.append)
    deadline = time.monotonic() + 2
    while not done and time.monotonic() < deadline:
        app.root.update()
        time.sleep(.01)
    assert done == [42] and "test" not in app.pending


def test_bad_fee_comparison_no_partial_results(app):
    app.offers[2][1].set("101")
    app.compare()
    assert len(app.compare_tree.get_children()) == 0


def test_offline_notice_visible(app):
    assert "DEMO" in app.status.get()
    assert app.snapshot.day is None


def test_scroll_reaches_bottom_at_small_window(app):
    app.root.geometry("980x700")
    app.root.update()
    app.viewport.yview_moveto(1)
    app.root.update()
    assert app.viewport.yview()[1] == 1.0


def test_new_snapshot_invalidates_comparison(app):
    app.compare()
    assert len(app.compare_tree.get_children()) == 3
    app.apply_snapshot(app.snapshot)
    assert app.compare_tree.get_children() == ()


def test_fullscreen_escape(app):
    app.toggle_fullscreen()
    app.root.update()
    assert app.fullscreen and bool(app.root.attributes("-fullscreen"))
    app.leave_fullscreen()
    app.root.update()
    assert not app.fullscreen


def test_snake_pauses_on_navigation(app):
    app.tabs.select(app.snake_tab)
    app.root.update()
    app.snake.start()
    assert app.snake.running and app.snake.timer is not None
    app.tabs.select(app.converter)
    app.root.update()
    assert not app.snake.running and app.snake.timer is None


def test_snake_highscore_persists(app):
    from quantumfx.core import Store
    app.tabs.select(app.snake_tab)
    app.root.update()
    app.snake.start()
    app.snake.after_cancel(app.snake.timer)
    app.snake.timer = None
    x, y = app.snake.game.body[0]
    app.snake.game.food = (x+1, y)
    app.snake.tick()
    app.snake.pause()
    assert Store(app.store.folder).prefs["snake_highscore"] == 10


def test_reduced_motion_and_credit(app):
    app.toggle_motion()
    assert not app.animator.enabled
    assert "Eric" in app.credit.cget("text")
    results = []
    app.animator.run("test", results.append)
    assert results == [1.0]
    assert app.store.prefs["animations"] is False
