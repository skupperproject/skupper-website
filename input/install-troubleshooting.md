# Troubleshooting

## Some install directories are not writable

Make sure your current user has permission to write to the
`$HOME/.local/bin` directory:

~~~ console
$ ls -ld $HOME/.local/bin
drwxrwxr-x. 1 fritz fritz 264 Dec 20 09:01 /home/fritz/.local/bin
~~~

## Some required programs are not available

Use your OS package manager to install the required packages.

For example, this is how you find and install `awk` on Fedora:

~~~ console
$ dnf whatprovides awk
gawk-5.1.1-5.fc38.x86_64 : The GNU version of the AWK text processing utility
Repo        : fedora
Matched from:
Filename    : /usr/bin/awk
Provide    : /bin/awk

$ sudo dnf install gawk
~~~

## Some required network resources are not available

Make sure you can reach github.com:

~~~ console
$ ping github.com
PING github.com (140.82.113.4) 56(84) bytes of data.
64 bytes from lb-140-82-113-4-iad.github.com (140.82.113.4): icmp_seq=1 ttl=51 time=34.3 ms
~~~

Use `traceroute` to find out where connectivity falters:

~~~ console
$ traceroute github.com
~~~

<!-- ## The checksum does not match the downloaded release archive -->
<!-- - Try blowing away the cached download. -->
