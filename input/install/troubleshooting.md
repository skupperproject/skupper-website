# Troubleshooting

## Some install directories are not writable

Change directory permissions.  Make sure your current user has
permission to write to the `~/bin` directory.

## Some required programs are not available

Use your OS's package manager to install the required packages.

~~~
$ dnf whatprovides <program>
$ sudo dnf install <package>
~~~

## Some required network resources are not available

Check your network.  Use traceroute to find out where connectivity
falters.

<!-- ## The checksum does not match the downloaded release archive -->
<!-- - Try blowing away the cached download. -->
