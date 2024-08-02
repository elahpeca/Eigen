gnome = import('gnome')

subdir('ui')
subdir('icons')

desktop_file = i18n.merge_file(
        input: APPLICATION_ID+'.desktop.in',
       output: APPLICATION_ID+'.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: APPLICATION_ID+'.metainfo.xml.in',
       output: APPLICATION_ID+'.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

configure_file(
  input: '@0@.gresource.xml.in'.format(meson.project_name()),
  output: '@0@.gresource.xml'.format(meson.project_name()),
  configuration: conf,
)

gnome.compile_resources(meson.project_name(),
  join_paths(meson.current_build_dir(), meson.project_name()+'.gresource.xml'),
  gresource_bundle: true,
  source_dir: meson.current_build_dir(),
  install: true,
  install_dir: PKGDATA_DIR,
  dependencies: blueprints
)

configure_file(
  input: '@0@.gschema.xml.in'.format(APPLICATION_ID),
  output: '@0@.gschema.xml'.format(APPLICATION_ID),
  configuration: conf,
  install: true,
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif
