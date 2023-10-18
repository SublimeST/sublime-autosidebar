from typing import List, Optional
import sublime
import sublime_plugin
import inspect
import logging

DEFERRED_WINDOWS: List[sublime.Window] = []

logger = logging.getLogger(__name__)


def add_deferred(window: Optional[sublime.Window]):
    logger.info("Defer from: %s", inspect.stack()[1][3])
    if not window:
        logger.warn("Windows is None, not adding")
        return

    DEFERRED_WINDOWS.append(window)


def check_deferred():
    logger.info("Apply deferred from: %s", inspect.stack()[1][3])
    logger.info("Applying to: %s", DEFERRED_WINDOWS)

    while len(DEFERRED_WINDOWS) > 0:
        internal_apply_sidebar_status(DEFERRED_WINDOWS.pop())


def apply_sidebar_status(window: Optional[sublime.Window]):
    logger.info("Apply from: %s", inspect.stack()[1][3])
    add_deferred(window)
    check_deferred()


def internal_apply_sidebar_status(window: sublime.Window):
    sidebar_visible = False

    logger.info("Views: %s", window.views())
    logger.info("Folders: %s", window.folders())

    if not window.get_tabs_visible() and len(window.views()) > 1:
        sidebar_visible = True

    if len(window.folders()) > 0:
        sidebar_visible = True

    logger.info("Show sidebar?: %s", sidebar_visible)

    window.set_sidebar_visible(sidebar_visible, animate=True)


class AutoSidebar(sublime_plugin.EventListener):
    def on_init(self, views):
        for view in views:
            apply_sidebar_status(view.window())

    def on_new(self, view):
        apply_sidebar_status(view.window())

    def on_associate_buffer(self, buffer):
        apply_sidebar_status(buffer.window())

    def on_clone(self, view):
        apply_sidebar_status(view.window())

    def on_load(self, view):
        apply_sidebar_status(view.window())

    def on_reload(self, view):
        apply_sidebar_status(view.window())

    def on_pre_move(self, view):
        add_deferred(view.window())

    def on_post_move(self, view):
        check_deferred()

    def on_pre_close(self, view):
        add_deferred(view.window())

    def on_close(self, view):
        check_deferred()

    def on_activated(self, view):
        apply_sidebar_status(view.window())

    def on_deactivated(self, view):
        apply_sidebar_status(view.window())

    def on_new_project(self, window):
        apply_sidebar_status(window)

    def on_load_project(self, window):
        apply_sidebar_status(window)

    def on_post_save_project(self, window):
        apply_sidebar_status(window)

    def on_pre_close_project(self, window):
        add_deferred(window)
