import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

from .entry import NumericEntry

class MatrixData:
    """
    Represents matrix data.

    Stores the matrix in a 2D list and provides methods
    for updating cell values.
    """

    def __init__(self, rows, cols):
        """
        Initializes a MatrixData object.

        Args:
            rows (int): Number of rows in the matrix.
            cols (int): Number of columns in the matrix.
        """

        self.rows = rows
        self.cols = cols
        self.data = [[None] * cols for _ in range(rows)]

    def update_value(self, row, col, value):
        """
        Updates the value at a specific cell in the matrix.

        Args:
            row (int): Row index.
            col (int): Column index.
            value (str): New value for the cell.
        """

        try:
            self.data[row][col] = float(value) if value else None
        except ValueError:
            pass

    def resize(self, new_rows, new_cols):
        """
        Resizes the matrix data, preserving existing values.

        Args:
            new_rows (int): New number of rows.
            new_cols (int): New number of columns.
        """

        if new_rows > self.rows:
            self.data.extend([[None] * self.cols for _ in range(new_rows - self.rows)])
        elif new_rows < self.rows:
            self.data = self.data[:new_rows]

        for row in self.data:
            if new_cols > self.cols:
                row.extend([None] * (new_cols - self.cols))
            elif new_cols < self.cols:
                row[:] = row[:new_cols]

        self.rows = new_rows
        self.cols = new_cols

class MatrixView:
    """
    Represents the matrix view in the interface.

    Handles the visual representation of the matrix,
    using a Gtk.Grid to display cells.
    """

    def __init__(self, grid, css_provider, on_data_change_callback):
        """
        Initializes a MatrixView object.

        Args:
            grid (Gtk.Grid): The Gtk.Grid widget for displaying cells.
            css_provider (Gtk.CssProvider): The CSS provider for styling.
            on_data_change_callback (callable): Called when the matrix data changes.
        """

        self.grid = grid
        self.css_provider = css_provider
        self.on_data_change_callback = on_data_change_callback
        self.matrix_data = None
        self.entries = {}

    def update_matrix_data(self):
        """
        Updates the matrix data and calls the data change callback.
        """

        self.on_data_change_callback(self.matrix_data.data)

    def set_matrix(self, matrix_data):
        """
        Sets the matrix data and refreshes the view.

        Args:
            matrix_data (MatrixData): The matrix data.
        """

        self.matrix_data = matrix_data
        self.initialize_matrix_view()

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

    def create_entry(self, row, col):
        """
        Creates an input widget (NumericEntry) for a cell.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            NumericEntry: The created input widget.
        """

        entry = NumericEntry()

        entry.set_max_length(10)

        entry.set_placeholder_text(f"({row + 1},{col + 1})")
        entry.set_alignment(0.5)

        entry.connect("changed", self.on_entry_changed, row, col)

        style_context = entry.get_style_context()
        style_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_context.add_class("narrow-entry")
        return entry

    @staticmethod
    def set_margins(grid, cols, window_width=380, element_width=52):
        """
        Sets margins for the Gtk.Grid such that the size of grid elements remains fixed.

        Args:
        grid: The grid widget.
        cols (int): Number of columns in the grid.
        window_width (int, optional): Total width of the window. Defaults to 380.
        element_width (int, optional): Fixed width of each grid element. Defaults to 100.
        """

        total_elements_width = cols * element_width
        total_margin_width = window_width - total_elements_width
        margin = total_margin_width / 2

        grid.set_margin_start(margin)
        grid.set_margin_end(margin)

    def initialize_matrix_view(self):
        """
        Initializes the matrix view.
        Adds/updates input widgets within the Gtk.Grid.
        """

        rows = self.matrix_data.rows
        cols = self.matrix_data.cols

        self.set_margins(self.grid, cols)

        entries_to_remove = [key for key in self.entries if key[0] >= rows or key[1] >= cols]
        for key in entries_to_remove:
            entry = self.entries.pop(key)
            if self.grid.get_child_at(key[1], key[0]) is entry:
                self.grid.remove(entry)

        for row in range(rows):
            for col in range(cols):
                current_entry = self.entries.get((row, col))
                grid_entry = self.grid.get_child_at(col, row)

                if current_entry is None:
                    entry = self.create_entry(row, col)
                    self.entries[(row, col)] = entry
                    self.grid.attach(entry, col, row, 1, 1)

                elif grid_entry is not current_entry:
                    self.grid.attach(current_entry, col, row, 1, 1)

    @staticmethod
    def clear_matrix(grid, rows, cols):
        """
        Clears all input widgets within the Gtk.Grid.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
        """

        for row in range(rows):
            for col in range(cols):
                entry = grid.get_child_at(col, row)
                if entry is not None:
                    entry.delete_text(0, -1)

