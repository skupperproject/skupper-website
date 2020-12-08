# Skupper website

## Setting up the project

This project uses Git submodules.  After you clone this repo, load the
submodules using the following command:

```sh
git submodule update --init
```

## Rendering the site

Once you have set up the project, you can use the `./plano` command in
the root of the project to render the site:

```sh
./plano render
```

For development, you can serve the site locally.  Any changes you make
to the input files are rendered on demand.

```sh
$ ./plano serve
--> serve
Rendering input files
Watching for input file changes
Serving at http://localhost:8080
Starting LiveReload v0.9.1 for /home/jross/code/skupper-website-ssorj/output on port 35729.
```

## Project targets

Use `./plano --help` to see the options.
