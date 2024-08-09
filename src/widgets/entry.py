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
        self.connect("changed", self.filter_input)

    def filter_input(self, *args):
        """
        Schedules the input filtering process asynchronously.

        This method avoids conflicts between user input and irreversible
        widget modifications by delaying the filtering logic until after
        the user has finished typing.

        Args:
            *args: Additional arguments passed to the "changed" signal.
        """

        text = self.get_text()
        if self._needs_filtering(text):
            GLib.idle_add(self._apply_numeric_filter, text)

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
        if '-' in text and not text.startswith('-') or text.count('-') > 1:
            return True
        for char in text:
            if not char.isdigit() and char not in '.-':
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
        dot_present = False
        minus_present = False

        for index, char in enumerate(text):
            if char.isdigit():
                new_text += char
            elif char == '.' and not dot_present:
                new_text += char
                dot_present = True
            elif char == '-' and not minus_present and index == 0:
                new_text += char
                minus_present = True

        if new_text != text:
            self.set_text(new_text)
            self._update_text_and_cursor(new_text, cursor_position, text)

    def _update_text_and_cursor(self, new_text, old_position, old_text):
        """
        Updates the text and adjusts the cursor position to maintain its relative location.

        Args:
            new_text (str): : The filtered text.
            old_position (int): The original cursor position.
            old_text (str): The text before filtering.
        """

        self.set_text(new_text)
        new_position = old_position
        chars_removed_before = sum(1 for i in range(min(old_position,  len(old_text)))
                                   if i < len(new_text) and old_text[i] != new_text[i])

        new_position -= chars_removed_before
        new_position = max(0, new_position)

        self.set_position(new_position)
