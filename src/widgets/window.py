from gi.repository import Gtk, Gdk, Adw, Gio
from .matrix_view import MatrixView
from .matrix_data import MatrixData

@Gtk.Template(resource_path='/com/github/elahpeca/Eigen/gtk/window.ui')
class EigenWindow(Adw.ApplicationWindow):
    """
    Main application window for Eigen.

    Handles the user interface and interaction with matrix data.
    """
    __gtype_name__ = 'EigenWindow'

    main_content = Gtk.Template.Child()
    decompositions_dropdown = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()
    matrix_copy_button = Gtk.Template.Child()
    matrix_cleanup_button = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        """
        Initializes the EigenWindow.

        Args:
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        self.settings = Gio.Settings.new('com.github.elahpeca.Eigen')
        self.connect('unrealize', self.save_window_properties)

        self.setup_dropdowns()
        self.update_matrix_size()
        self.setup_matrix_view()

        self.rows_dropdown.connect('notify::selected', self.on_size_changed)
        self.cols_dropdown.connect('notify::selected', self.on_size_changed)
        self.matrix_cleanup_button.connect('clicked', self.on_matrix_cleanup_clicked)
        self.matrix_copy_button.connect('clicked', self.on_matrix_copy_clicked)

    def save_window_properties(self, *args):
        """
        Save window size to settings when it is unrealized (closed).

        Args:
            *args: Positional arguments passed by the signal.
        """
        window_size = self.get_default_size()
        self.settings.set_int('window-width', window_size.width)
        self.settings.set_int('window-height', window_size.height)

    def setup_dropdowns(self):
        """
        Setups the dropdown menus for matrix decomposition and size selection.
        """
        self.initialize_dropdown(self.decompositions_dropdown, ['Eigen', 'SVD', 'LU', 'QR', 'Cholesky'])
        size_options = [str(i) for i in range(1, 8)]
        self.initialize_dropdown(self.rows_dropdown, size_options, 2)
        self.initialize_dropdown(self.cols_dropdown, size_options, 2)

    def setup_matrix_view(self):
        """
        Creates a MatrixView instance, configures its appearance
        and binds it to the matrix data.
        """
        self.matrix_view = MatrixView()
        self.matrix_view.set_row_homogeneous(True)
        self.matrix_view.set_column_homogeneous(True)
        self.matrix_view.set_row_spacing(5)
        self.matrix_view.set_column_spacing(5)
        self.main_content.insert_child_after(self.matrix_view, self.decompositions_dropdown)

        self.matrix_data = MatrixData(self.current_rows, self.current_cols)
        self.matrix_view.set_matrix(self.matrix_data)

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

    def on_matrix_copy_clicked(self, button):
        """
        Handle the event when the matrix copy button is clicked.

        Args:
            button: The button that triggered the event.
        """
        display = Gdk.Display.get_default()
        clipboard = display.get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(str(self.matrix_data.data))
        clipboard.set_content(content_provider)

    def on_matrix_cleanup_clicked(self, button):
        """
        Clear the matrix when cleanup button is clicked.

        Args:
            button: The button that triggered the event.
        """
        self.matrix_view.clear_matrix(self.current_rows, self.current_cols)

    @staticmethod
    def initialize_dropdown(dropdown, options, selected=0):
        """
        Initializes a dropdown menu with a list of options and selects a default option.

        Args:
            dropdown (Gtk.Dropdown): The Gtk.Dropdown widget to be initialized.
            options (list of str): A list of options to populate the dropdown menu.
            selected (int, optional): The index of the option to be selected by default.
        """
        dropdown.set_model(Gtk.StringList.new(options))
        dropdown.set_selected(selected)
