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
from .matrix import MatrixData, MatrixView

@Gtk.Template(resource_path="/com/github/elahpeca/Eigen/gtk/window.ui")
class EigenWindow(Adw.ApplicationWindow):
    """
    Main application window for Eigen.

    Handles the user interface and interaction with matrix data.
    """

    __gtype_name__ = "EigenWindow"

    decompositions_dropdown = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()
    matrix_grid = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()
    matrix_cleanup_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        """
        Initializes the EigenWindow.

        Args:
            **kwargs: Additional keyword arguments passed to the parent class.
        """

        super().__init__(**kwargs)
        self.settings = Gio.Settings.new('com.github.elahpeca.Eigen')

        self.connect("unrealize", self.save_window_properties)

        self.css_provider = self.create_css_provider()

        self.initialize_decompositions_dropdown()
        self.initialize_size_chooser()

        self.update_matrix_size()
        self.matrix_data = MatrixData(self.current_rows, self.current_cols)
        self.matrix_view = MatrixView(self.matrix_grid, self.css_provider, self.on_matrix_data_changed)
        self.matrix_view.set_matrix(self.matrix_data)

        self.rows_dropdown.connect("notify::selected", self.on_size_changed)
        self.cols_dropdown.connect("notify::selected", self.on_size_changed)
        self.matrix_cleanup_button.connect("clicked", self.on_matrix_cleanup_clicked)

    def save_window_properties(self, *args):
        """
        Save window size to settings when it is unrealized (closed).

        Args:
            *args: Positional arguments passed by the signal.
        """

        window_size = self.get_default_size()

        self.settings.set_int("window-width", window_size.width)
        self.settings.set_int("window-height", window_size.height)

    def create_css_provider(self):
        """
        Create and load a CSS provider for custom styles.

        Returns:
            Gtk.CssProvider: The created CSS provider.
        """

        provider = Gtk.CssProvider()
        provider.load_from_resource('com/github/elahpeca/Eigen/style.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        return provider

    def initialize_decompositions_dropdown(self):
        """Initialize the decompositions dropdown with options."""

        decomposition_options = Gtk.StringList.new(["Eigen", "SVD", "LU", "QR", "Cholesky"])
        self.decompositions_dropdown.set_model(decomposition_options)

    def initialize_size_chooser(self):
        """Initialize the rows and columns dropdowns with options."""

        size_options = Gtk.StringList.new([str(i) for i in range(1, 8)])

        self.rows_dropdown.set_model(size_options)
        self.cols_dropdown.set_model(size_options)

        self.rows_dropdown.set_selected(2)
        self.cols_dropdown.set_selected(2)

    def update_matrix_size(self):
        """Update internal row and column counts based on dropdown selection."""

        self.current_rows = self.rows_dropdown.get_selected() + 1
        self.current_cols = self.cols_dropdown.get_selected() + 1

    def on_size_changed(self, *args):
        """
        Handle changes in matrix size dropdowns.

        Args:
            *args: Positional arguments passed by the signal.
        """

        self.update_matrix_size()
        self.matrix_data.resize(self.current_rows, self.current_cols)
        self.matrix_view.set_matrix(self.matrix_data)
        self.matrix_view.update_matrix_data()

    def on_matrix_cleanup_clicked(self, button):
        """
        Clear the matrix when cleanup button is clicked.

        Args:
            button: The button that triggered the event.
        """

        self.matrix_view.clear_matrix(self.current_rows, self.current_cols)

    #temporary method for further development
    def on_matrix_data_changed(self, matrix_data):
        print(matrix_data)
