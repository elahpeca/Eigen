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
        """

        GLib.idle_add(self._apply_numeric_filter)

    def _apply_numeric_filter(self):
        """
        Applies numeric input filtering to the entry's text.

        This method ensures that the entry's text only contains digits, a
        single decimal point (.), and optionally a minus sign (-) at the
        beginning.
        """

        text = self.get_text()
        new_text = ''
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
            self.set_position(-1)
