import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

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
        self.data = [[None for _ in range(cols)] for _ in range(rows)]

    def update_value(self, row, col, value):
        """
        Updates the value at a specific cell in the matrix.

        Args:
            row (int): Row index.
            col (int): Column index.
            value (str): New value for the cell.
        """

        try:
            self.data[row][col] = float(value)
        except ValueError:
            self.data[row][col] = None

    def resize(self, new_rows, new_cols):
        """
        Resizes the matrix data, preserving existing values.

        Args:
            new_rows (int): New number of rows.
            new_cols (int): New number of columns.
        """

        new_data = [[None for _ in range(new_cols)] for _ in range(new_rows)]

        for i in range(min(self.rows, new_rows)):
            for j in range(min(self.cols, new_cols)):
                new_data[i][j] = self.data[i][j]

        self.data = new_data
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
    
    def filter_entry_text(self, entry):
        text = entry.get_text()
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
            entry.set_text(new_text)
            entry.set_position(-1)
            
        return False

    
    def on_entry_changed(self, entry, row, col):
        """
        Handles changes in text within a cell.
        Updates the matrix data and calls the callback.

        Args:
            entry (Gtk.Entry): The input widget.
            row (int): Row index.
            col (int): Column index.
        """
        GLib.idle_add(self.filter_entry_text, entry)
        self.matrix_data.update_value(row, col, entry.get_text())

        self.update_matrix_data()

    def create_entry(self, row, col):
        """
        Creates an input widget (Gtk.Entry) for a cell.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            Gtk.Entry: The created input widget.
        """

        entry = Gtk.Entry()

        entry.set_max_length(7)
        entry.get_text()

        entry.set_placeholder_text(f"({row + 1},{col + 1})")
        entry.set_alignment(0.5)

        entry.connect("changed", self.on_entry_changed, row, col)

        style_context = entry.get_style_context()
        style_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_context.add_class("narrow-entry")
        return entry

    def set_margins(self, cols):
        """
        Sets margins for the Gtk.Grid.

        Args:
            cols (int): Number of columns.
        """

        DEFAULT_MARGIN = 157
        margin = DEFAULT_MARGIN - 25 * (cols - 1)
        self.grid.set_margin_start(margin)
        self.grid.set_margin_end(margin)

    def initialize_matrix_view(self):
        """
        Initializes the matrix view.
        Adds/updates input widgets within the Gtk.Grid.
        """

        rows = self.matrix_data.rows
        cols = self.matrix_data.cols

        self.set_margins(cols)

        entries_to_remove = []
        for key in self.entries.keys():
            row, col = key
            if row >= rows or col >= cols:
                entries_to_remove.append(key)

        for key in entries_to_remove:
            entry = self.entries.pop(key)
            if self.grid.get_child_at(key[1], key[0]) is entry:
                self.grid.remove(entry)

        for row in range(rows):
            for col in range(cols):
                if (row, col) not in self.entries:
                    entry = self.create_entry(row, col)
                    self.entries[(row, col)] = entry
                    self.grid.attach(entry, col, row, 1, 1)
                else:
                    entry = self.entries[(row, col)]
                    current_position = self.grid.get_child_at(col, row)
                    if current_position is not entry:
                        self.grid.attach(entry, col, row, 1, 1)

    def clear_matrix(self, rows, cols):
        """
        Clears all input widgets within the Gtk.Grid.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
        """
        for row in range(rows):
            for col in range(cols):
                entry = self.grid.get_child_at(col, row)
                entry.delete_text(0, -1)

