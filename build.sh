#!/usr/bin/bash

echo "Cleaning current builddir directory..."
rm -r builddir

echo "Rebuilding project..."
meson setup builddir
meson configure builddir -Dprefix="$(pwd)/builddir" -Dbuildtype=debug
ninja -C builddir install

echo "Running project..."
ninja -C builddir run
