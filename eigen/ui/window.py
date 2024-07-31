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

    toast_overlay = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()
    matrix_grid = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.settings = Gio.Settings.new(app_id)

        self.create_css_provider()

        self.dropdowns_init()

        self.set_current_size()

        self.matrix_init()

        self.rows_dropdown.connect("notify::selected", self.matrix_init)
        self.cols_dropdown.connect("notify::selected", self.matrix_init)

    def create_css_provider(self):
        self.provider = Gtk.CssProvider()
        self.provider.load_from_resource(f"{rootdir}/style.css") 
    
    def dropdowns_init(self):
        size_model = Gtk.StringList.new([str(i) for i in range(1, 8)])

        self.rows_dropdown.set_model(size_model)
        self.cols_dropdown.set_model(size_model)

        self.rows_dropdown.set_selected(1)
        self.cols_dropdown.set_selected(1)

    def set_current_size(self, *args):
            self.current_rows = self.rows_dropdown.get_selected() + 1
            self.current_cols = self.cols_dropdown.get_selected() + 1

    def matrix_init(self, *args):
        for row in range(self.current_rows):
            for col in range(self.current_cols):
                child = self.matrix_grid.get_child_at(col, row)
                if child:
                    self.matrix_grid.remove(child)

        self.set_current_size()

        for row in range(self.current_rows):
            for col in range(self.current_cols):
                entry = Gtk.Entry()
                entry.set_max_length(7)
                entry.set_placeholder_text(f"({row + 1}, {col + 1})")
                entry.set_halign(Gtk.Align.START)
                entry.set_valign(Gtk.Align.START)

                self.matrix_grid.attach(entry, col, row, 1, 1)

                style_context = entry.get_style_context()
                style_context.add_provider(self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                style_context.add_class("narrow-entry")


