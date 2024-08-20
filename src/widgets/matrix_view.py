import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
from .numeric_entry import NumericEntry

class MatrixView(Gtk.Grid):
    """
    Represents the matrix view in the interface.

    Handles the visual representation of the matrix,
    using a grid to display cells.
    """
    def __init__(self, on_data_change_callback):
        """
        Initializes a MatrixView object.

        Args:
            on_data_change_callback (callable): Called when the matrix data changes.
        """
        super().__init__()
        self.on_data_change_callback = on_data_change_callback
        self.matrix_data = None
        self.entries = {}

    def set_matrix(self, matrix_data):
        """
        Sets the matrix data and refreshes the view.

        Args:
            matrix_data (MatrixData): The matrix data.
        """
        self.matrix_data = matrix_data
        self.refresh_matrix()

    def refresh_matrix(self):
        """
        Updates the MatrixView to match the current matrix data.
        """
        rows, cols = self.matrix_data.rows, self.matrix_data.cols
        self.set_margins(cols)
        self.remove_old_entries(rows, cols)
        self.update_existing_entries(rows, cols)
        self.add_new_entries(rows, cols)

    def set_margins(self, cols, window_width=420, element_width=58):
        """
        Sets margins for the MatrixView such that the size of elements remains fixed.

        Args:
        cols (int): Number of columns in the MatrixView.
        window_width (int, optional): Total width of the window.
        element_width (int, optional): Fixed width of each MatrixView element.
        """
        margin = (window_width - cols * element_width) / 2
        self.set_margin_start(margin)
        self.set_margin_end(margin)

    def remove_old_entries(self, rows, cols):
        """
        Removes entries from the MatrixView that are no longer needed.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
        """
        entries_to_remove = [key for key in self.entries if key[0] >= rows or key[1] >= cols]
        for key in entries_to_remove:
            entry = self.entries.pop(key)
            if self.get_child_at(key[1], key[0]) is entry:
                entry.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
                entry.set_transition_duration(500)
                self.remove(entry)
                entry.set_reveal_child(True)

    def update_existing_entries(self, rows, cols):
        """
        Reattaches existing entries if they are not already in the correct position.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
        """
        for row in range(rows):
            for col in range(cols):
                current_entry = self.entries.get((row, col))
                if current_entry and self.get_child_at(col, row) != current_entry:
                    self.attach(current_entry, col, row, 1, 1)

    def add_new_entries(self, rows, cols):
        """
        Adds new entries with animation to the MatrixView for any new matrix cells.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
        """
        for row in range(rows):
            for col in range(cols):
                if (row, col) not in self.entries:
                    entry = self.create_entry(row, col)
                    self.entries[(row, col)] = entry
                    entry.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
                    entry.set_transition_duration(500)
                    self.entries[(row, col)] = entry
                    self.attach(entry, col, row, 1, 1)
                    entry.set_reveal_child(True)

    def update_matrix_data(self):
        """
        Updates the matrix data and calls the data change callback.
        """
        self.on_data_change_callback(self.matrix_data.data)

    def create_entry(self, row, col):
        """
        Creates an input widget (NumericEntry) inside Gtk.Revealer container for a cell.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            revealer (Gtk.Revealer): The created widget.
        """
        entry = NumericEntry()
        entry.set_max_length(10)
        entry.set_placeholder_text('0')
        entry.set_alignment(0.5)
        entry.connect('changed', self.on_entry_changed, row, col)
        entry.set_size_request(40, 40)

        revealed_entry = Gtk.Revealer()
        revealed_entry.set_child(entry)
        return revealed_entry

    def on_entry_changed(self, entry, row, col):
        """
        Handles changes in text within a cell.
        Updates the matrix data and calls the callback.

        Args:
            entry (NumericEntry): The input widget.
            row (int): Row index.
            col (int): Column index.
        """
        self.matrix_data.update_value(row, col, entry.get_text())
        self.update_matrix_data()

    def clear_matrix(self, rows, cols):
        """
        Clears all input widgets within the MatrixView.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
        """
        for row in range(rows):
            for col in range(cols):
                entry = self.get_child_at(col, row).get_child()
                if entry is not None:
                    entry.delete_text(0, -1)

