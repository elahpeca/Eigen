project('eigen',
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2',
		   ],
)

gnome = import('gnome')
i18n = import('i18n')

subdir('data')
subdir('eigen')
subdir('po')

dependencies = [
	dependency('gtk4'),
	dependency('libadwaita-1'),
]

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
