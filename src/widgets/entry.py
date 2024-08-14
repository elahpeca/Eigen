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

        self.current_text = ''

        self.set_default_flags()

        self.connect("changed", self.text_getter)
        self.connect("changed", self.filter_input)

    def text_getter(self, *args):
        self.current_text = self.get_text()

    def filter_input(self, *args):
        """
        Schedules the input filtering process asynchronously.

        This method avoids conflicts between user input and irreversible
        widget modifications by delaying the filtering logic until after
        the user has finished typing. It uses a combination of input filtering
        and visual feedback to guide the user towards valid entries.

        Args:
            *args: Additional arguments passed to the "changed" signal.
        """

        unwritten_floats = ['.', '-', '-.']

        if self._needs_filtering(self.current_text):
            self.add_css_class('error')
            GLib.idle_add(self._apply_numeric_filter, self.current_text)
            self.set_default_flags()
            GLib.timeout_add(300, self._remove_error_class)

        elif self.current_text in unwritten_floats:
            self.add_css_class('error')

        elif self.current_text not in unwritten_floats:
            GLib.timeout_add(300, self._remove_error_class)

    def _needs_filtering(self, text):
        """
        Checks if the given text needs numeric filtering.

        Args:
            text (str): The text to check for filtering needs.

        Returns:
            True if filtering is needed, False otherwise.
        """

        if text.count('.') > 1:
            return True

        if '-' in text and not text.startswith('-'):
            return True

        for index, char in enumerate(text):
            if not char.isdigit() and (char not in '.-' or (char == '-' and index != 0)):
                return True

        return False

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
            elif char == '.' and self.dot_allowed:
                new_text += char
                self.dot_allowed = False
            elif char == '-' and self.minus_allowed and index == 0:
                new_text += char
                self.minus_allowed = False

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

    def _remove_error_class(self):
        """
        Removes the error class if the current text is a valid numeric input.

        Returns:
            False: Returns False to stop the timer callback.
        """

        self.remove_css_class('error')
        return False

    def set_default_flags(self):
        """
        Sets the default flags for dot and minus
        """

        self.dot_allowed = True
        self.minus_allowed = True
