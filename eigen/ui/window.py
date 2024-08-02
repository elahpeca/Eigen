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

from eigen.constants import rootdir, app_id

@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class EigenWindow(Adw.Window):
    __gtype_name__ = "EigenWindow"

    decompositions_dropdown = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()
    matrix_flowbox = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.settings = Gio.Settings.new(app_id)

        self.connect("unrealize", self.save_window_props)

        self.provider = self.create_css_provider()

        self.decompositions_chooser_init()

        self.size_chooser_init()

        self.get_current_size()

        self.matrix_init()

        self.rows_dropdown.connect("notify::selected", self.matrix_init)
        self.cols_dropdown.connect("notify::selected", self.matrix_init)

    def save_window_props(self, *args):
        win_size = self.get_default_size()

        self.settings.set_int("window-width", win_size.width)
        self.settings.set_int("window-height", win_size.height)

    def create_css_provider(self):
        provider = Gtk.CssProvider()
        provider.load_from_resource(f"{rootdir}/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        return provider
    
    def decompositions_chooser_init(self):
        decomposition_model = Gtk.StringList.new(["Eigen", "SVD", "LU", "QR", "Cholesky"])
        self.decompositions_dropdown.set_model(decomposition_model)

    def size_chooser_init(self):
        size_model = Gtk.StringList.new([str(i) for i in range(1, 8)])

        self.rows_dropdown.set_model(size_model)
        self.cols_dropdown.set_model(size_model)

        self.rows_dropdown.set_selected(1)
        self.cols_dropdown.set_selected(1)

    def get_current_size(self):
        self.current_rows = self.rows_dropdown.get_selected() + 1
        self.current_cols = self.cols_dropdown.get_selected() + 1

    def create_entry(self, row, col):
        entry = Gtk.Entry()
        entry.set_max_length(7)
        entry.set_placeholder_text(f"({row + 1}, {col + 1})")
        entry.set_halign(Gtk.Align.START)
        entry.set_valign(Gtk.Align.START)
        entry.set_alignment(0.5)

        style_context = entry.get_style_context()
        style_context.add_provider(self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_context.add_class("narrow-entry")
        return entry

    def matrix_init(self, *args):
        self.matrix_flowbox.remove_all()

        self.get_current_size()

        self.matrix_flowbox.set_min_children_per_line(self.current_cols)
        self.matrix_flowbox.set_max_children_per_line(self.current_cols)
        
        def set_matrix_flowbox_margin(cols):
            default_margin = 164
            self.matrix_flowbox.set_margin_start(default_margin - 25*(cols-1))
            self.matrix_flowbox.set_margin_end(default_margin - 25*(cols-1))

        set_matrix_flowbox_margin(self.current_cols)
        for row in range(self.current_rows):
            for col in range(self.current_cols):
                entry = self.create_entry(row, col)
                self.matrix_flowbox.append(entry)