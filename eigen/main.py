import sys

from gi.repository import Gio, Adw

from eigen.ui.window import EigenWindow
from eigen.constants import rootdir, app_id


class EigenApplication(Adw.Application):
    """The main application class."""

    __gtype_name__ = "EigenApplication"

    def __init__(self):
        super().__init__(application_id=app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.set_resource_base_path(rootdir)
        self.style_manager = Adw.StyleManager.get_default()
        self.settings = Gio.Settings.new(app_id)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """

        self.win = self.props.active_window
        if not self.win:
            self.win = EigenWindow(
                application=self,
                default_height=self.settings.get_int("window-height"),
                default_width=self.settings.get_int("window-width"),
            )
            # create app actions
            self.create_action("about", self.on_about)
            self.create_action("preferences", self.on_preferences)
        self.win.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
            activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_about(self, *_args):
        toast = Adw.Toast.new("About was pressed")
        toast.set_timeout(1)
        self.win.toast_overlay.add_toast(toast)

    def on_preferences(self, *_args):
        toast = Adw.Toast.new("Preferences was pressed")
        toast.set_timeout(1)
        self.win.toast_overlay.add_toast(toast)


def main():
    """The application's entry point."""
    app = EigenApplication()
    return app.run(sys.argv)
