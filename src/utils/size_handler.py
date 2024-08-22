from gi.repository import Gtk

class SizeHandler:
    def __init__(self, *dropdowns, selected=2):
        """
        Initializes the SizeHandler for managing matrix size selection.

        Args:
            *dropdowns (Gtk.DropDown): The dropdown widgets.
            selected (int, optional): The default selected index. Defaults to 2.
        """
        self.dropdowns = dropdowns
        self.selected = selected
        self._setup_dropdowns()

    def _setup_dropdowns(self):
        """
        Sets up the dropdowns for matrix size selection.
        """
        options = [str(i) for i in range(1, 8)]
        model = Gtk.StringList.new(options)

        for dropdown in self.dropdowns:
            dropdown.set_model(model)
            dropdown.set_selected(self.selected)

    def get_selected_size(self):
        """
        Returns a tuple of selected values from each dropdown.

        Returns:
            tuple of int: The selected values of each dropdown, if any, otherwise None.
        """
        selected_size = tuple(dropdown.get_selected() + 1 for dropdown in self.dropdowns)
        return tuple(item if item else None for item in selected_size)

