#!/bin/sh

set -e

echo "Determining your OS and architecture"
echo

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

echo "  Operating system: $OPERATING_SYSTEM"
echo "  Architecture: $ARCHITECTURE"
echo

echo "Looking up the latest release for your environment"
echo

RELEASE_URL=`curl -sL "https://api.github.com/repos/skupperproject/skupper/releases/latest" \
             | grep browser_download_url \
             | cut -d '"' -f 4 \
             | grep "${OPERATING_SYSTEM}-${ARCHITECTURE}"`

echo "  $RELEASE_URL"
echo

mkdir -p "$INSTALL_DIR"

echo "Downloading and installing the Skupper command"
echo

curl -fL "$RELEASE_URL" | tar -C "$INSTALL_DIR" -xzf -

echo
echo "The Skupper command is now installed in ${INSTALL_DIR}"
echo

if [ ! `which skupper` = "$INSTALL_DIR/skupper" ]; then
    echo "Use the following command to place it on your path:"
    echo
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
    echo
fi
