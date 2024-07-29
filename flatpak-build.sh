#!/usr/bin/bash

echo "Rebuilding project..."
flatpak-builder --force-clean .flatpak/repo build-aux/flatpak/com.github.elahpeca.Eigen.yml

echo "Running project..."
flatpak-builder --run .flatpak/repo build-aux/flatpak/com.github.elahpeca.Eigen.yml eigen