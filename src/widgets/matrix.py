import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class MatrixData:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = [[None for _ in range(cols)] for _ in range(rows)]

    def update_value(self, row, col, value):
        try:
            self.data[row][col] = float(value)
        except ValueError:
            self.data[row][col] = None

class MatrixView:
    def __init__(self, flowbox, css_provider, on_data_change_callback):
        self.flowbox = flowbox
        self.css_provider = css_provider
        self.on_data_change_callback = on_data_change_callback
        self.matrix_data = None

    def set_matrix(self, matrix_data):
        self.matrix_data = matrix_data
        self.initialize_matrix_view()

    def on_entry_changed(self, entry, row, col):
        entry_text = entry.get_text()
        self.matrix_data.update_value(row, col, entry_text)
        self.on_data_change_callback(self.matrix_data.data)

    def create_entry(self, row, col):
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
        DEFAULT_MARGIN = 157
        margin = DEFAULT_MARGIN - 25 * (cols - 1)
        self.flowbox.set_margin_start(margin)
        self.flowbox.set_margin_end(margin)

    def initialize_matrix_view(self):
        self.flowbox.remove_all()
        rows = self.matrix_data.rows
        cols = self.matrix_data.cols

        self.flowbox.set_min_children_per_line(cols)
        self.flowbox.set_max_children_per_line(cols)

        self.set_margins(cols)
        for row in range(rows):
            for col in range(cols):
                entry = self.create_entry(row, col)
                self.flowbox.append(entry)

    def clear_matrix(self, rows, cols):
        for index in range(rows*cols):
            entry = self.flowbox.get_child_at_index(index).get_child()
            entry.delete_text(0, -1)

