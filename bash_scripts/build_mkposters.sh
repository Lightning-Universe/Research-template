#!/bin/bash
echo Running "$0"

# Detect the compute architecture (linux-arm64, macos-arm64, macos-x64) and download the appropriate distribution release of dart-sass
# https://github.com/sass/dart-sass/releases/tag/1.50.1

sass_release="1.50.1"
mkposters_release="0.0.1"
arch=$(uname -m)
kernel=$(uname -s)

echo Detected architecture: $arch and kernel: $kernel

if [[ "$arch" =~ ^(arm64|aarch64)$ ]] && [ "$kernel" = "Linux" ]; then
    curl -sL "https://github.com/sass/dart-sass/releases/download/1.50.1/dart-sass-$sass_release-linux-arm64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
elif [ "$arch" = "x86_64" ] && [ "$kernel" = "Linux" ]; then
    curl -sL "https://github.com/sass/dart-sass/releases/download/1.50.1/dart-sass-${sass_release}-linux-x64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
elif [ "$arch" = "arm64" ] && [ "$kernel" = "Darwin" ]; then
    curl -sL "https://github.com/sass/dart-sass/releases/download/1.50.1/dart-sass-${sass_release}-macos-arm64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
elif [ "$arch" = "x86_64" ] && [ "$kernel" = "Darwin" ]; then
    curl -sL "https://github.com/sass/dart-sass/releases/download/1.50.1/dart-sass-${sass_release}-macos-x64.tar.gz" > dart.tar.gz && tar -xzf dart.tar.gz && rm dart.tar.gz
else
    echo "Unsupported architecture: $arch and kernel: $kernel"
fi

# install mkposters
pip uninstall mkposters -y
pip install mkposters==$mkposters_release --quiet

# move the dart-sass binary to the correct location
mkloc=$(pip show mkposters | grep Location | cut -d ' ' -f 2)
rm -rf $mkloc/mkposters/third_party/dart-sass && mv dart-sass $mkloc/mkposters/third_party
