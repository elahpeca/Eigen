import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class NumericEntry(Gtk.Entry):
    """
    Represents a text entry widget with built-in numeric input filtering.
    """

    def __init__(self):
        """
        Initializes a NumericEntry object.
        """

        super().__init__()

        self.last_correct_text = ''

        self.connect("changed", self.filter_input)

    def _apply_numeric_filter(self, text):
        """
        Applies numeric input filtering to the entry's text.

        This method ensures that the entry's text only contains digits, a
        single decimal point (.), and optionally a minus sign (-) at the
        beginning.

        Args:
            text (str): The text to filter.
        """

        new_text = ''
        cursor_position = self.get_position()

        for index, char in enumerate(text):
            if char.isdigit():
                new_text += char
            elif char == '.' and '.' not in self.last_correct_text:
                new_text += char
            elif char == '-' and '-' not in self.last_correct_text and index == 0:
                new_text += char

        self.last_correct_text = new_text
        if new_text != text:
            self._update_text_and_cursor(new_text, cursor_position, text)

    def _update_text_and_cursor(self, new_text, cursor_position, old_text):
        """
        Updates the entry text and cursor position.

        Args:
            new_text (str): The new filtered text.
            cursor_position (int): The current cursor position.
            old_text (str): The old text before filtering.
        """

        self.handler_block_by_func(self.filter_input)
        self.set_text(new_text)
        new_cursor_position = max(min(cursor_position - (len(old_text) - len(new_text)), len(new_text)), 0)
        self.set_position(new_cursor_position)
        self.handler_unblock_by_func(self.filter_input)

    @staticmethod
    def is_incorrect(text):
        """
        Checks if the user's input is incorrect.

        Args:
            text (str): The text to check.

        Returns:
            True if text is incorrect, False otherwise.
        """

        if text.count('.') > 1:
            return True

        if '-' in text and not text.startswith('-'):
            return True

        for index, char in enumerate(text):
            if not char.isdigit() and (char not in '.-' or (char == '-' and index != 0)):
                return True

        return False

    @staticmethod
    def error_style(func):
        """
        Decorator to add/remove the "error" class when incorrect data is entered.

        Args:
            func: The function to which the decorator is applied.

        Returns:
            wrapper: A wrapper function that checks the entered data
                     and adds/removes the "error" class.
        """

        def wrapper(self, *args, **kwargs):
            unwritten_floats = ['.', '-', '-.']
            if self.is_incorrect(self.get_text()) or self.get_text() in unwritten_floats:
                self.add_css_class('error')

            func(*args, **kwargs)

            if self.get_text() not in unwritten_floats:
                GLib.timeout_add(300, lambda: self.remove_css_class('error'))
        return wrapper

    @error_style
    def filter_input(self, *args):
        """
        Delays the filtering logic until after the user has finished typing.

        Args:
            *args: Additional arguments passed to the "changed" signal.
        """

        text = self.get_text()
        GLib.idle_add(self._apply_numeric_filter, text)
