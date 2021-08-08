#!/bin/sh

set -e

OPERATING_SYSTEM=`uname -s`
ARCHITECTURE=`uname -m`
INSTALL_DIR="$HOME/bin"

if [ "$OPERATING_SYSTEM" = "Darwin" ]; then
    OPERATING_SYSTEM="mac"
elif [ "$OPERATING_SYSTEM" = "Linux" ]; then
    OPERATING_SYSTEM="linux"
    INSTALL_DIR="$HOME/.local/bin"
else
    echo "Error: Unknown operating system: $OPERATING_SYSTEM"
    exit 1
fi

if [ "$ARCHITECTURE" = "aarch64" ]; then
    ARCHITECTURE="arm64"
elif [ "$ARCHITECTURE" = "armv7l" ]; then
    ARCHITECTURE="arm32"
elif [ "$ARCHITECTURE" = "arm64" ]; then
    ARCHITECTURE="arm64"
elif [ "$ARCHITECTURE" = "i386" ]; then
    ARCHITECTURE="i386"
elif [ "$ARCHITECTURE" = "i686" ]; then
    ARCHITECTURE="i386"
elif [ "$ARCHITECTURE" = "x86_64" ]; then
    ARCHITECTURE="amd64"
else
    echo "Error: Unknown architecture: $ARCHITECTURE"
    exit 1
fi

mkdir -p "$INSTALL_DIR"

LATEST_URL="https://api.github.com/repos/skupperproject/skupper/releases/latest"
# RELEASE_URL=`curl -sL $LATEST_URL | jq -r ".assets[] | select(.browser_download_url | contains(\"${OPERATING_SYSTEM}-${ARCHITECTURE}\")) | .browser_download_url"`

RELEASE_URL=`curl -sL "$LATEST_URL" | grep browser_download_url | cut -d '"' -f 4 | grep "${OPERATING_SYSTEM}-${ARCHITECTURE}"`

curl -fL "$RELEASE_URL" | tar -C "$INSTALL_DIR" -xzf -

echo "The Skupper command is now installed at ${INSTALL_DIR}/skupper"
