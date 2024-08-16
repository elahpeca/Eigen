from gi.repository import Gio, Gtk, Adw

from .window import EigenWindow

class EigenApplication(Adw.Application):
    __gtype_name__ = 'EigenApplication'

    def __init__(self):
        """
        Initializes the EigenApplication instance.
        """
        super().__init__(
            application_id='com.github.elahpeca.Eigen',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

        self.set_resource_base_path('/com/github/elahpeca/Eigen')
        self.style_manager = Adw.StyleManager.get_default()
        self.settings = Gio.Settings.new('com.github.elahpeca.Eigen')

        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        # self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        """
        Activates the application, creating and presenting
        the main window if it doesn't exist.
        """
        win = self.get_property('active-window')

        window_width = self.settings.get_int('window-width')
        window_height = self.settings.get_int('window-height')
        if not win:
            try:
                win = EigenWindow(
                    application=self,
                    default_width=window_width,
                    default_height=window_height
                )
            except Exception as e:
                print(f'Error creating window: {e}')
                return
        win.present()

    def on_about_action(self, *args):
        """
        Handles the 'about' action, displaying the about dialog.

        Args:
            *args: Variable length argument list.
        """
        about = Adw.AboutDialog(
            application_name='Eigen',
            application_icon='com.github.elahpeca.Eigen',
            developer_name='elahpeca',
            version='0.1.0',
            comments=_(
                'Eigen is a nice and simple app for matrix decomposition.',
            ),
            website='https://github.com/elahpeca/Eigen',
            issue_url = 'https://github.com/elahpeca/Eigen/issues',
            developers=[
                'elahpeca <acephaleee@gmail.com>',
                'k0nvulsi0n <charonpersonal@proton.me>',
                ],
            artists=['k0nvulsi0n <charonpersonal@proton.me>'],
            copyright='© 2024 elahpeca',
            license_type = Gtk.License.GPL_3_0
        )
        about.present(self.get_property('active-window'))

    # def on_preferences_action(self, widget, _):
    #     """
    #     Handles the 'preferences' action.

    #     Args:
    #         widget: The widget that triggered the action.
    #         _: Placeholder argument.
    #     """
    #     pass

    def create_action(self, name, callback, shortcuts=None):
        """
        Creates an action with an optional keyboard shortcut.

        Args:
            name (str): The name of the action.
            callback (callable): The function to call when the action is activated.
            shortcuts (list, optional): A list of keyboard shortcuts for the action.
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
