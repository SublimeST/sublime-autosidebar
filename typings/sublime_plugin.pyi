"""
Based on the reference at: https://www.sublimetext.com/docs/api_reference.html
"""

from typing import Tuple, List
from sublime import (
    AutoCompleteFlags,
    Buffer,
    CommandArgs,
    CompletionList,
    CompletionValue,
    Edit,
    HoverZone,
    Html,
    ListInputItem,
    Point,
    QueryOperator,
    Settings,
    TextChange,
    Value,
    View,
    Window,
)

class CommandInputHandler:
    def name(self) -> str:
        """
        The command argument name this input handler is editing. Defaults to foo_bar for an input handler named FooBarInputHandler.
        """
        ...
    def placeholder(self) -> str:
        """
        Placeholder text is shown in the text entry box before the user has entered anything. Empty by default.
        """
        ...
    def initial_text(self) -> str:
        """
        Initial text shown in the text entry box. Empty by default.
        """
        ...
    def initial_selection(self) -> list[tuple[int, int]]:
        """
        (4081) A list of 2-element tuples, defining the initially selected parts of the initial text.
        """
        ...
    def preview(self, text: str) -> str | Html:
        """
        Called whenever the user changes the text in the entry box. The returned value (either plain text or HTML) will be shown in the preview area of the Command Palette.
        """
        ...
    def validate(self, text: str) -> bool:
        """
        Called whenever the user presses enter in the text entry box. Return False to disallow the current value.
        """
        ...
    def cancel(self):
        """
        Called when the input handler is canceled, either by the user pressing backspace or escape.
        """
        ...
    def confirm(self, text: str):
        """
        Called when the input is accepted, after the user has pressed enter and the text has been validated.
        """
        ...
    def next_input(self, args) -> CommandInputHandler | None:
        """
        Return the next input after the user has completed this one. May return None to indicate no more input is required, or sublime_plugin.BackInputHandler() to indicate that the input handler should be popped off the stack instead.
        """
        ...
    def want_event(self) -> bool:
        """
        (4096) Whether the validate() and confirm() methods should received a second Event parameter. Returns False by default.
        """

class BackInputHandler(CommandInputHandler): ...

class TextInputHandler(CommandInputHandler):
    """
    TextInputHandlers can be used to accept textual input in the Command Palette. Return a subclass of this from Command.input().

    For an input handler to be shown to the user, the command returning the input handler MUST be made available in the Command Palette by adding the command to a Default.sublime-commands file.
    """

    def description(self, text: str) -> str:
        """
        The text to show in the Command Palette when this input handler is not at the top of the input handler stack. Defaults to the text the user entered.
        """
        ...

class ListInputHandler(CommandInputHandler):
    """
    ListInputHandlers can be used to accept a choice input from a list items in the Command Palette. Return a subclass of this from Command.input().

    For an input handler to be shown to the user, the command returning the input handler MUST be made available in the Command Palette by adding the command to a Default.sublime-commands file.
    """

    def list_items(
        self,
    ) -> (
        list[str]
        | tuple[list[str], int]
        | list[tuple[str, Value]]
        | tuple[list[tuple[str, Value]], int]
        | list[ListInputItem]
        | tuple[list[ListInputItem], int]
    ):
        """
        This method should return the items to show in the list.

        The returned value may be a list of item, or a 2-element tuple containing a list of items, and an int index of the item to pre-select.

        The each item in the list may be one of:

            A string used for both the row text and the value passed to the command

            A 2-element tuple containing a string for the row text, and a Value to pass to the command

            A sublime.ListInputItem object (4095)
        """
        ...
    def description(self, value, text: str) -> str:
        """
        The text to show in the Command Palette when this input handler is not at the top of the input handler stack. Defaults to the text of the list item the user selected.
        """
        ...

class Command:
    def name(self) -> str:
        """
        Return the name of the command. By default this is derived from the name of the class.
        """
        ...
    def is_enabled(self) -> bool:
        """
        Return whether the command is able to be run at this time. Command arguments are passed as keyword arguments. The default implementation simply always returns True.
        """
        ...
    def is_visible(self) -> bool:
        """
        Return whether the command should be shown in the menu at this time. Command arguments are passed as keyword arguments. The default implementation always returns True.
        """
        ...
    def is_checked(self) -> bool:
        """
        Return whether a checkbox should be shown next to the menu item. Command arguments are passed as keyword arguments. The .sublime-menu file must have the "checkbox" key set to true for this to be used.
        """
        ...
    def description(self) -> str | None:
        """
        Return a description of the command with the given arguments. Command arguments are passed as keyword arguments. Used in the menu, if no caption is provided. Return None to get the default description.
        """
        ...
    def want_event(self) -> bool:
        """
        Return whether to receive an Event argument when the command is triggered by a mouse action. The event information allows commands to determine which portion of the view was clicked on. The default implementation returns False.
        """
        ...
    def input(self, args: dict) -> CommandInputHandler | None:
        """
        (3154) If this returns something other than None, the user will be prompted for an input before the command is run in the Command Palette.
        """
        ...
    def input_description(self) -> str:
        """
        (3154) Allows a custom name to be show to the left of the cursor in the input box, instead of the default one generated from the command name.
        """
        ...
    def run(self):
        """
        Called when the command is run. Command arguments are passed as keyword arguments.
        """
        ...

class ApplicationCommand(Command):
    """
    A Command instantiated just once.
    """

    ...

class WindowCommand(Command):
    """
    A Command instantiated once per window. The Window object may be retrieved via self.window.
    """

    ...

    window: Window
    """
    The Window this command is attached to.
    """

class TextCommand(Command):
    """
    A Command instantiated once per View. The View object may be retrieved via self.view.
    """

    view: View
    """
    The View this command is attached to.
    """

    def run(self, edit: Edit):
        """
        Called when the command is run. Command arguments are passed as keyword arguments.
        """

class EventListener:
    def on_init(self, views: List[View]):
        """
        (4050) Called once with a list of views that were loaded before the EventListener was instantiated
        """
        ...
    def on_exit(self):
        """
        (4050) Called once after the API has shut down, immediately before the plugin_host process exits
        """
        ...
    def on_new(self, view: View):
        """
        Called when a new file is created.
        """
        ...
    def on_new_async(self, view: View):
        """
        Called when a new buffer is created. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_associate_buffer(self, buffer: View):
        """
        (4084) Called when a buffer is associated with a file. buffer will be a Buffer object.
        """
        ...
    def on_associate_buffer_async(self, buffer: View):
        """
        (4084) Called when a buffer is associated with file. Runs in a separate thread, and does not block the application. buffer will be a Buffer object.
        """
        ...
    def on_clone(self, view: View):
        """
        Called when a view is cloned from an existing one.
        """
        ...
    def on_clone_async(self, view: View):
        """
        Called when a view is cloned from an existing one. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_load(self, view: View):
        """
        Called when the file is finished loading.
        """
        ...
    def on_load_async(self, view: View):
        """
        Called when the file is finished loading. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_reload(self, view: View):
        """
        (4050) Called when the View is reloaded.
        """
        ...
    def on_reload_async(self, view: View):
        """
        (4050) Called when the View is reloaded. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_revert(self, view: View):
        """
        (4050) Called when the View is reverted.
        """
        ...
    def on_revert_async(self, view: View):
        """
        (4050) Called when the View is reverted. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_pre_move(self, view: View):
        """
        (4050) Called right before a view is moved between two windows, passed the View object.
        """
        ...
    def on_post_move(self, view: View):
        """
        (4050) Called right after a view is moved between two windows, passed the View object.
        """
        ...
    def on_post_move_async(self, view: View):
        """
        (4050) Called right after a view is moved between two windows, passed the View object. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_pre_close(self, view: View):
        """
        Called when a view is about to be closed. The view will still be in the window at this point.
        """
        ...
    def on_close(self, view: View):
        """
        Called when a view is closed (note, there may still be other views into the same buffer).
        """
        ...
    def on_pre_save(self, view: View):
        """
        Called just before a view is saved.
        """
        ...
    def on_pre_save_async(self, view: View):
        """
        Called just before a view is saved. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_post_save(self, view: View):
        """
        Called after a view has been saved.
        """
        ...
    def on_post_save_async(self, view: View):
        """
        Called after a view has been saved. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_modified(self, view: View):
        """
        Called after changes have been made to a view.
        """
        ...
    def on_modified_async(self, view: View):
        """
        Called after changes have been made to a view. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_selection_modified(self, view: View):
        """
        Called after the selection has been modified in a view.
        """
        ...
    def on_selection_modified_async(self, view: View):
        """
        Called after the selection has been modified in a view. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_activated(self, view: View):
        """
        Called when a view gains input focus.
        """
        ...
    def on_activated_async(self, view: View):
        """
        Called when a view gains input focus. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_deactivated(self, view: View):
        """
        Called when a view loses input focus.
        """
        ...
    def on_deactivated_async(self, view: View):
        """
        Called when a view loses input focus. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_hover(self, view: View, point: Point, hover_zone: HoverZone):
        """
        Called when the user’s mouse hovers over the view for a short period.

        Parameters:

            view

                The view

            point

                The closest point in the view to the mouse location. The mouse may not actually be located adjacent based on the value of hover_zone.

            hover_zone

                Which element in Sublime Text the mouse has hovered over.
        """
        ...
    def on_query_context(
        self,
        view: View,
        key: str,
        operator: QueryOperator,
        operand: str,
        match_all: bool,
    ) -> bool | None:
        """
        Called when determining to trigger a key binding with the given context key. If the plugin knows how to respond to the context, it should return either True of False. If the context is unknown, it should return None.

        Parameters:

            key

                The context key to query. This generally refers to specific state held by a plugin.

            operator

                The operator to check against the operand; whether to check equality, inequality, etc.

            operand

                The value against which to check using the operator.

            match_all

                This should be used if the context relates to the selections: does every selection have to match(match_all == True), or is at least one matching enough (match_all == False)?

        Returns:

            True or False if the plugin handles this context key and it either does or doesn’t match. If the context is unknown return None.
        """
        ...
    def on_query_completions(
        self, view: View, prefix: str, locations: List[Point]
    ) -> (
        None
        | List[CompletionValue]
        | Tuple[List[CompletionValue], AutoCompleteFlags]
        | CompletionList
    ):
        """
        Called whenever completions are to be presented to the user.

        Parameters:

            prefix

                The text already typed by the user.

            locations

                The list of points being completed. Since this method is called for all completions no matter the syntax, self.view.match_selector(point, relevant_scope) should be called to determine if the point is relevant.

        Returns:

            A list of completions in one of the valid formats or None if no completions are provided.
        """
        ...
    def on_text_command(self, view: View, command_name: str, args: CommandArgs):
        """
        Called when a text command is issued. The listener may return a (command, arguments) tuple to rewrite the command, or None to run the command unmodified.
        """
        ...
    def on_window_command(self, window: Window, command_name: str, args: CommandArgs):
        """
        Called when a window command is issued. The listener may return a (command, arguments) tuple to rewrite the command, or None to run the command unmodified.
        """
        ...
    def on_post_text_command(self, view: View, command_name: str, args: CommandArgs):
        """
        Called after a text command has been executed.
        """
        ...
    def on_post_window_command(
        self, window: Window, command_name: str, args: CommandArgs
    ):
        """
        Called after a window command has been executed.
        """
        ...
    def on_new_window(self, window: Window):
        """
        (4050) Called when a window is created, passed the Window object.
        """
        ...
    def on_new_window_async(self, window: Window):
        """
        (4050) Called when a window is created, passed the Window object. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_pre_close_window(self, window: Window):
        """
        (4050) Called right before a window is closed, passed the Window object.
        """
        ...
    def on_new_project(self, window: Window):
        """
        (4050) Called right after a new project is created, passed the Window object.
        """
        ...
    def on_new_project_async(self, window: Window):
        """
        (4050) Called right after a new project is created, passed the Window object. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_load_project(self, window: Window):
        """
        (4050) Called right after a project is loaded, passed the Window object.
        """
        ...
    def on_load_project_async(self, window: Window):
        """
        (4050) Called right after a project is loaded, passed the Window object. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_pre_save_project(self, window: Window):
        """
        (4050) Called right before a project is saved, passed the Window object.
        """
        ...
    def on_post_save_project(self, window: Window):
        """
        (4050) Called right after a project is saved, passed the Window object.
        """
        ...
    def on_post_save_project_async(self, window: Window):
        """
        (4050) Called right after a project is saved, passed the Window object. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_pre_close_project(self, window: Window):
        """
        Called right before a project is closed, passed the Window object.
        """
        ...

class ViewEventListener:
    """
    A class that provides similar event handling to EventListener, but bound to a specific view. Provides class method-based filtering to control what views objects are created for.
    """

    def on_load(self):
        """
        (3155) Called when the file is finished loading.
        """
        ...
    def on_load_async(self):
        """
        (3155) Same as on_load but runs in a separate thread, not blocking the application.
        """
        ...
    def on_reload(self):
        """
        (4050) Called when the file is reloaded.
        """
        ...
    def on_reload_async(self):
        """
        (4050) Same as on_reload but runs in a separate thread, not blocking the application.
        """
        ...
    def on_revert(self):
        """
        (4050) Called when the file is reverted.
        """
        ...
    def on_revert_async(self):
        """
        (4050) Same as on_revert but runs in a separate thread, not blocking the application.
        """
        ...
    def on_pre_move(self):
        """
        (4050) Called right before a view is moved between two windows.
        """
        ...
    def on_post_move(self):
        """
        (4050) Called right after a view is moved between two windows.
        """
        ...
    def on_post_move_async(self):
        """
        (4050) Same as on_post_move but runs in a separate thread, not blocking the application.
        """
        ...
    def on_pre_close(self):
        """
        (3155) Called when a view is about to be closed. The view will still be in the window at this point.
        """
        ...
    def on_close(self):
        """
        (3155) Called when a view is closed (note, there may still be other views into the same buffer).
        """
        ...
    def on_pre_save(self):
        """
        (3155) Called just before a view is saved.
        """
        ...
    def on_pre_save_async(self):
        """
        (3155) Same as on_pre_save but runs in a separate thread, not blocking the application.
        """
        ...
    def on_post_save(self):
        """
        (3155) Called after a view has been saved.
        """
        ...
    def on_post_save_async(self):
        """
        (3155) Same as on_post_save but runs in a separate thread, not blocking the application.
        """
        ...
    def on_modified(self):
        """
        Called after changes have been made to the view.
        """
        ...
    def on_modified_async(self):
        """
        Same as on_modified but runs in a separate thread, not blocking the application.
        """
        ...
    def on_selection_modified(self):
        """
        Called after the selection has been modified in the view.
        """
        ...
    def on_selection_modified_async(self):
        """
        Called after the selection has been modified in the view. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_activated(self):
        """
        Called when a view gains input focus.
        """
        ...
    def on_activated_async(self):
        """
        Called when the view gains input focus. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_deactivated(self):
        """
        Called when the view loses input focus.
        """
        ...
    def on_deactivated_async(self):
        """
        Called when the view loses input focus. Runs in a separate thread, and does not block the application.
        """
        ...
    def on_hover(self, point: Point, hover_zone: HoverZone):
        """
        Called when the user’s mouse hovers over the view for a short period.

        Parameters:

            point

                The closest point in the view to the mouse location. The mouse may not actually be located adjacent based on the value of hover_zone.

            hover_zone

                Which element in Sublime Text the mouse has hovered over.
        """
        ...
    def on_query_context(
        self, key: str, operator: QueryOperator, operand: str, match_all: bool
    ) -> bool | None:
        """

        Called when determining to trigger a key binding with the given context key. If the plugin knows how to respond to the context, it should return either True of False. If the context is unknown, it should return None.

        Parameters:

            key

                The context key to query. This generally refers to specific state held by a plugin.

            operator

                The operator to check against the operand; whether to check equality, inequality, etc.

            operand

                The value against which to check using the operator.

            match_all

                This should be used if the context relates to the selections: does every selection have to match (match_all == True), or is at least one matching enough (match_all == False)?

        Returns:

            True or False if the plugin handles this context key and it either does or doesn’t match. If the context is unknown return None.
        """
        ...
    def on_query_completions(
        self, prefix: str, locations: List[Point]
    ) -> (
        None
        | List[CompletionValue]
        | Tuple[List[CompletionValue], AutoCompleteFlags]
        | CompletionList
    ):
        """

        Called whenever completions are to be presented to the user.

        Parameters:

            prefix

                The text already typed by the user.

            locations

                The list of points being completed. Since this method is called for all completions no matter the syntax, self.view.match_selector(point, relevant_scope) should be called to determine if the point is relevant.

        Returns:

            A list of completions in one of the valid formats or None if no completions are provided.
        """
        ...
    def on_text_command(
        self, command_name: str, args: CommandArgs
    ) -> Tuple[str, CommandArgs]:
        """
        (3155) Called when a text command is issued. The listener may return a `` (command, arguments)`` tuple to rewrite the command, or None to run the command unmodified.
        """
        ...
    def on_post_text_command(self, command_name: str, args: CommandArgs):
        """
        Called after a text command has been executed.
        """
        ...
    @classmethod
    def is_applicable(cls, settings: Settings) -> bool:
        """
        Returns:

            Whether this listener should apply to a view with the given Settings.
        """
        ...
    @classmethod
    def applies_to_primary_view_only(cls) -> bool:
        """
        Returns:

            Whether this listener should apply only to the primary view for a file or all of its clones as well.
        """
        ...

class TextChangeListener:
    """
    (4081) A class that provides event handling about text changes made to a specific Buffer. Is separate from ViewEventListener since multiple views can share a single buffer.
    """

    def on_text_changed(self, changes: List[TextChange]):
        """
        Called once after changes has been made to a buffer, with detailed information about what has changed.
        """
        ...
    def on_text_changed_async(self, changes: List[TextChange]):
        """
        Same as on_text_changed but runs in a separate thread, not blocking the application.
        """
        ...
    def on_revert(self):
        """

        Called when the buffer is reverted.

        A revert does not trigger text changes. If the contents of the buffer are required here use View.substr.
        """
        ...
    def on_revert_async(self):
        """

        Same as on_revert but runs in a separate thread, not blocking the application.
        """
        ...
    def on_reload(self):
        """

        Called when the buffer is reloaded.

        A reload does not trigger text changes. If the contents of the buffer are required here use View.substr.
        """
        ...
    def on_reload_async(self):
        """

        Same as on_reload but runs in a separate thread, not blocking the application.
        """
        ...
    @classmethod
    def is_applicable(cls, buffer: Buffer):
        """
        Returns:

            Whether this listener should apply to the provided buffer.
        """
    def detach(self):
        """
        Remove this listener from the buffer.

        Async callbacks may still be called after this, as they are queued separately.

        Raises ValueError:

            if the listener is not attached.

        """
    def attach(self, buffer: Buffer):
        """
        Attach this listener to a buffer.

        Raises ValueError:

            if the listener is already attached.
        """
        ...
    def is_attached(self) -> bool:
        """
        Returns:
            whether the listener is receiving events from a buffer. May not be called from __init__.
        """
        ...
