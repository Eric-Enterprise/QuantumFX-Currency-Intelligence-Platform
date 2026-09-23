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
    assert app.compare_tree.item(first, "values")[0] == "Offer 2"
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


def test_reduced_motion(app):
    app.toggle_motion()
    assert not app.animator.enabled
    results = []
    app.animator.run("test", results.append)
    assert results == [1.0]
    assert app.store.prefs["animations"] is False


def test_copy_only_for_current_valid_result(app):
    assert not app.copy_btn.disabled
    app.amount.set("abc")
    assert app.copy_btn.disabled
    app.calculate()
    assert app.copy_btn.disabled
    assert app.amount_entry.cget("style") == "Invalid.TEntry"
    app.amount.set("100")
    app.calculate(save=False)
    assert not app.copy_btn.disabled
    assert app.amount_entry.cget("style") == "TEntry"


def test_search_shortcut_targets_search(app):
    app.focus_search()
    app.root.update()
    assert app.tabs.select() == str(app.markets)
    assert app.root.focus_get() == app.search_entry


def test_disabled_button_does_not_invoke(app):
    invoked = []
    original = app.copy_btn.command
    app.copy_btn.command = lambda: invoked.append(True)
    app.copy_btn.configure(state="disabled")
    app.copy_btn.invoke()
    assert invoked == []
    app.copy_btn.configure(state="normal")
    app.copy_btn.invoke()
    assert invoked == [True]
    app.copy_btn.command = original


def test_collapsed_fees_keep_values_and_show_active_state(app):
    assert not app.fees_expanded
    app.toggle_fees()
    app.percent.set("2")
    app.toggle_fees()
    assert not app.fees_expanded and "active" in app.fee_toggle.text
    app.amount.set("100")
    app.calculate(save=False)
    assert app.last_result[0]["fee"] == 2

@pytest.mark.parametrize('language', ['de', 'ko', 'sv', 'en'])
def test_language_switch_preserves_state_and_translates(app, language):
    from quantumfx.core import Store
    from quantumfx.i18n import LANGUAGES
    # Switch away first so the English case also exercises a rebuild.
    app.change_language('sv' if language == 'en' else 'en')
    app.amount.set('1234.56')
    app.percent.set('2')
    app.fixed.set('1')
    app.calculate()
    rows = list(app.store.rows)
    app.search.set('GBP')
    app.offers[0][0].set('My custom offer')
    app.offers[0][1].set('3')
    app.compare()
    app.chart_key = ('EUR', 'USD', 30)
    app.chart_points = [('2026-01-01', D('1.1')), ('2026-01-02', D('1.2'))]
    app.chart_source = 'cache'
    app.snake.start()
    game = app.snake.game
    app.tabs.select(app.history_tab)
    app.language_choice.set(LANGUAGES[language])
    app.language_box.event_generate('<<ComboboxSelected>>')
    app.root.update()
    assert app.tr.language == language
    assert Store(app.store.folder).prefs['language'] == language
    assert app.store.rows == rows
    assert app.amount.get() == '1234.56' and app.percent.get() == '2' and app.fixed.get() == '1'
    assert app.tabs.select() == str(app.history_tab)
    assert app.page_title.cget('text') == app.tr('History')
    assert app.copy_btn.text == app.tr('Copy') and app.copy_btn.icon_name == 'copy'
    assert app.offers[0][0].get() == 'My custom offer' and app.offers[0][1].get() == '3'
    assert app.offers[1][0].get() == app.tr('Offer {n}', n=2)
    assert len(app.compare_tree.get_children()) == 3
    assert app.snake.game is game and not app.snake.running and app.snake.timer is None
    assert app.search.get() == 'GBP' and len(app.search.trace_info()) == 1
    assert app.chart_key == ('EUR', 'USD', 30) and len(app.chart_points) == 2
    assert app.tr('Cache') in app.chart_status.get()
    assert app.tr('Fees') in app.detail.get()
    assert app.result.get() == app.money(app.last_result[0]['net'], app.target.get()) + ' ' + app.target.get()
    app.tabs.select(app.converter)
    app.root.geometry('980x700')
    app.root.update()
    app.viewport.yview_moveto(1)
    app.root.update()
    assert app.viewport.yview()[1] == 1.0
    for _, _, button in app.nav_buttons:
        text_box = button.bbox(button.find_all()[-1])
        assert text_box[2] <= button.winfo_width(), (language, button.text, text_box)


def test_language_switch_with_pending_work_and_save_failure(app, monkeypatch):
    app.pending.update({'rates', 'chart'})
    def fail_save():
        raise OSError('simulated save failure')
    monkeypatch.setattr(app.store, 'save', fail_save)
    app.change_language('ko')
    assert app.refresh_btn.disabled and app.chart_btn.disabled
    assert app.feedback.get() == app.tr('Language could not be saved.')
    assert app.tr('Loading historical reference rates …') == app.chart_status.get()
    app.events.put(('rates', app.apply_snapshot, app.snapshot, None))
    app.root.after_cancel(app.poll_id)
    app.poll()
    assert not app.refresh_btn.disabled and 'rates' not in app.pending
    assert app.tr('DEMO · Undated sample rates · Do not use for actual conversions') == app.status.get()


def test_saved_language_restored_in_new_window(app):
    import tkinter as tk
    from quantumfx.app import App
    app.change_language('ko')
    window = tk.Toplevel(app.root)
    restored = App(window, app.store.folder, offline=True)
    try:
        window.update()
        assert restored.tr.language == 'ko'
        assert restored.copy_btn.text == '복사'
        assert restored.language_choice.get() == '한국어'
        assert restored.font_family == 'Malgun Gothic'
    finally:
        restored.close()
