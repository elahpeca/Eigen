<div align="center">
  <img src="./data/icons/hicolor/scalable/apps/com.github.elahpeca.Eigen.svg" height="128"/><h1>Eigen</h1>
</div>
Nice and simple app for matrix decomposition.

## Dependencies

- gtk4
- libadwaita1
- python-gobject
- python3
- blueprint-compiler
- meson
- flatpak-builder

## Building and running

### Flatpak

Use Gnome Builder or run these commands in your terminal app to install flatpak.

```
flatpak-builder --force-clean --user --install .flatpak/repo build-aux/flatpak/com.github.elahpeca.Eigen.json
```

```
flatpak run com.github.elahpeca.Eigen
```
