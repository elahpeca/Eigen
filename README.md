<div align="center">
  <img src="./data/icons/hicolor/scalable/apps/com.github.elahpeca.Eigen.svg" height="128"/><h1>Eigen</h1>
</div>
Nice and simple app for matrix decomposition.

## Dependencies

- gtk4
- libadwaita1

## Building and running
#### Building requirements
- meson
- flatpak-builder

### Flatpak

Use Gnome Builder or run these commands in your terminal app to install flatpak.

```
flatpak-builder --force-clean --user --install .flatpak/repo com.github.elahpeca.Eigen.json
```

```
flatpak run com.github.elahpeca.Eigen
```
