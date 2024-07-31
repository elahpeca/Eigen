import sys

from gi.repository import Gio, Adw

from eigen.ui.window import EigenWindow
from eigen.constants import rootdir, app_id, version

class EigenApplication(Adw.Application):
    __gtype_name__ = "EigenApplication"

    def __init__(self):
        super().__init__(application_id=app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.set_resource_base_path(rootdir)
        self.style_manager = Adw.StyleManager.get_default()
        self.settings = Gio.Settings.new(app_id)

        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = EigenWindow(
                application=self,
                default_height=self.settings.get_int("window-height"),
                default_width=self.settings.get_int("window-width"),
            )
        self.win.present()

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Eigen',
                                # application_icon=f'{app_icon}',
                                developer_name='elahpeca',
                                version=f'{version}',
                                copyright='© 2024 elahpeca')
        about.present()

    def on_preferences_action(self, widget, _):
        return None

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main():
    app = EigenApplication()
    return app.run(sys.argv)

if __name__ == "__main__":
    main()