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

from gi.repository import Gtk, Adw, Gio

from eigen.constants import rootdir, app_id

@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class EigenWindow(Adw.Window):
    __gtype_name__ = "EigenWindow"

    toast_overlay = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.settings = Gio.Settings.new(app_id)

        # save settings on window close
        self.connect("unrealize", self.save_window_props)

    def save_window_props(self, *args):
        """Save windows and column information on window close"""
        win_size = self.get_default_size()

        # Save window size
        self.settings.set_int("window-width", win_size.width)
        self.settings.set_int("window-height", win_size.height)
