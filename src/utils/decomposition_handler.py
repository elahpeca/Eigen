from gi.repository import Gio, GObject, Gtk

class KeyValuePair(GObject.Object):
    key = GObject.Property(
        type=int,
        flags=GObject.ParamFlags.READWRITE,
        default=0
    )
    value = GObject.Property(
        type=str,
        nick="Value",
        blurb="Value",
        flags=GObject.ParamFlags.READWRITE,
        default="",
    )

class DecompositionHandler:
    def __init__(self, dropdown, selected=0):
        """
        Initializes the Dropdown for matrix decomposition selection.

        Args:
            dropdown (Gtk.DropDown): The dropdown widget.
            selected (int, optional): The default selected index. Defaults to 0.
        """
        self.dropdown = dropdown
        self.selected = selected
        self._setup_dropdown()

    def _setup_dropdown(self):
        """
        Sets up the model and expression for the Dropdown.
        """
        model = Gio.ListStore(item_type=KeyValuePair)
        model.splice(
            0,
            0,
            [
                KeyValuePair(key=0, value="Eigen"),
                KeyValuePair(key=1, value="SVD"),
                KeyValuePair(key=2, value="LU"),
                KeyValuePair(key=3, value="QR"),
                KeyValuePair(key=4, value="Cholesky"),
            ],
        )

        list_store_expression = Gtk.PropertyExpression.new(
            KeyValuePair,
            None,
            "value",
        )

        self.dropdown.set_expression(list_store_expression)
        self.dropdown.set_model(model)
        self.dropdown.set_selected(self.selected)

    def get_selected_key(self):
        """
        Returns the key of the selected item.

        Returns:
            str: The key of the selected item, if any, otherwise None.
        """
        selected_item = self.dropdown.get_selected_item()
        return selected_item.key if selected_item else None

    def get_selected_value(self):
        """
        Returns the value of the selected item.

        Returns:
            str: The value of the selected item, if any, otherwise None.
        """
        selected_item = self.dropdown.get_selected_item()
        return selected_item.value if selected_item else None

