# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
from gi.repository import Gtk, Gdk, Adw, Gio

@Gtk.Template(resource_path="/com/github/elahpeca/Eigen/window.ui")
class EigenWindow(Adw.Window):
    __gtype_name__ = "EigenWindow"

    decompositions_dropdown = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()
    matrix_flowbox = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = Gio.Settings.new('com.github.elahpeca.Eigen')

        self.connect("unrealize", self.save_window_properties)

        self.css_provider = self.create_css_provider()

        self.initialize_decompositions_dropdown()
        self.initialize_size_chooser()

        self.update_matrix_size()
        self.matrix_data = []
        self.initialize_matrix()

        self.rows_dropdown.connect("notify::selected", self.initialize_matrix)
        self.cols_dropdown.connect("notify::selected", self.initialize_matrix)

    def save_window_properties(self, *args):
        window_size = self.get_default_size()

        self.settings.set_int("window-width", window_size.width)
        self.settings.set_int("window-height", window_size.height)

    def create_css_provider(self):
        provider = Gtk.CssProvider()
        provider.load_from_resource('com/github/elahpeca/Eigen/style.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        return provider

    def initialize_decompositions_dropdown(self):
        decomposition_options = Gtk.StringList.new(["Eigen", "SVD", "LU", "QR", "Cholesky"])
        self.decompositions_dropdown.set_model(decomposition_options)

    def initialize_size_chooser(self):
        size_options = Gtk.StringList.new([str(i) for i in range(1, 8)])

        self.rows_dropdown.set_model(size_options)
        self.cols_dropdown.set_model(size_options)

        self.rows_dropdown.set_selected(2)
        self.cols_dropdown.set_selected(2)

    def update_matrix_size(self):
        self.current_rows = self.rows_dropdown.get_selected() + 1
        self.current_cols = self.cols_dropdown.get_selected() + 1

    def on_matrix_entry_changed(self, buffer, gparam, row, col):
        entry_text = buffer.get_text()
        try:
            number = float(entry_text)
            self.matrix_data[row][col] = number
        except ValueError:
            self.matrix_data[row][col] = None
        print(self.matrix_data)

    def create_matrix_entry(self, row, col):
        entry = Gtk.Entry()
        entry.set_max_length(7)
        entry.set_placeholder_text(f"({row + 1}, {col + 1})")
        entry.set_halign(Gtk.Align.START)
        entry.set_valign(Gtk.Align.START)
        entry.set_alignment(0.5)

        entry.get_buffer().connect("notify::text", self.on_matrix_entry_changed, row, col)

        style_context = entry.get_style_context()
        style_context.add_provider(self.css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_context.add_class("narrow-entry")
        return entry

    def set_matrix_flowbox_margins(self, cols):
        DEFAULT_MARGIN = 164
        margin = DEFAULT_MARGIN - 25 * (cols - 1)
        self.matrix_flowbox.set_margin_start(margin)
        self.matrix_flowbox.set_margin_end(margin)

    def initialize_matrix(self, *args):
        self.matrix_flowbox.remove_all()
        self.update_matrix_size()

        self.matrix_data = [[None for _ in range(self.current_cols)] for _ in range(self.current_rows)]

        self.matrix_flowbox.set_min_children_per_line(self.current_cols)
        self.matrix_flowbox.set_max_children_per_line(self.current_cols)

        self.set_matrix_flowbox_margins(self.current_cols)
        for row in range(self.current_rows):
            for col in range(self.current_cols):
                entry = self.create_matrix_entry(row, col)
                self.matrix_flowbox.append(entry)
