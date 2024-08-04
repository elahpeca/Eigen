from gi.repository import Gio, Gtk, Adw

from .window import EigenWindow

class EigenApplication(Adw.Application):
    __gtype_name__ = "EigenApplication"

    def __init__(self):
        super().__init__(application_id="com.github.elahpeca.Eigen",
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.set_resource_base_path("/com/github/elahpeca/Eigen")
        self.style_manager = Adw.StyleManager.get_default()
        self.settings = Gio.Settings.new("com.github.elahpeca.Eigen")

        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = EigenWindow(
                application=self,
                default_height=self.settings.get_int("window-height"),
                default_width=self.settings.get_int("window-width"),
            )
        win.present()

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name="Eigen",
                                application_icon="com.github.elahpeca.Eigen",
                                developer_name="elahpeca",
                                version="0.1.0",
                                website="https://github.com/elahpeca/Eigen",
                                issue_url = "https://github.com/elahpeca/Eigen/issues",
                                developers=["elahpeca <acephaleee@gmail.com>",
                                            "k0nvulsi0n <charonpersonal@proton.me>"],
                                copyright="© 2024 elahpeca",
                                license_type = Gtk.License.GPL_3_0)
        about.present()

    def on_preferences_action(self, widget, _):
        print("app.preferences action activated")

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
