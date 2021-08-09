---
title: Installing
---

# Installing Skupper

## Installing the command-line tool

### Download and extract the command

To get the latest release of the Skupper command for your platform,
download it from GitHub and extract the executable using `tar` or
`unzip`.

<div class="code-label">Linux</div>

    curl -fL https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-linux-amd64.tgz | tar -xzf -

<div class="code-label">Mac</div>

    curl -fL https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-mac-amd64.tgz | tar -xzf -

<div class="code-label">Windows</div>

    curl -fLO https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-windows-amd64.zip
    unzip skupper-cli-{{skupper_release}}-windows-amd64.zip

This produces an executable file named `skupper` in your current
directory.

To download artifacts for other operating systems or architectures,
see [Skupper releases](/releases/index.html).

### Place the command on your path

Move the executable file to your preferred location and make it
available on your path.  For example, this is how you might install it
in your home directory:

<div class="code-label">Linux or Mac</div>

    mkdir $HOME/bin
    mv skupper $HOME/bin
    export PATH=$PATH:$HOME/bin

<div class="code-label">Windows</div>

    mkdir %UserProfile%\bin
    move skupper.exe %UserProfile%\bin
    set PATH=%PATH%;%UserProfile%\bin

### Check the command

To test your installation, run the `skupper version` command.  You
should see output like this:

    $ skupper version
    client version                 {{skupper_release}}
    transport version              not-found (no configuration has been provided)
    controller version             not-found (no configuration has been provided)
