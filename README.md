# Skupper website

[![main](https://github.com/skupperproject/skupper-website/actions/workflows/main.yaml/badge.svg)](https://github.com/skupperproject/skupper-website/actions/workflows/main.yaml)

## Project commands

You can use the `./plano` command in the root of the project to
perform project tasks.  It accepts a subcommand.  Use `./plano --help`
to list the available commands.

## Rendering the site

You can use the `./plano render` command in the root of the project to
render the site:

~~~ console
$ ./plano render
--> render
Rendering input files
<-- render
OK (0.21s)
~~~

For development, you can serve the site locally.  Any changes you make
to the input files are rendered on demand.

~~~ console
$ ./plano serve
--> serve
Rendering input files
Watching for input file changes
Serving at http://localhost:8080
Starting LiveReload v0.9.1 for /home/jross/code/skupper-website-ssorj/output on port 35729.
~~~

If you change any of the files or settings in the `config` or
`includes` directories, you need to use the `--force` option with
`render` or `serve` in order to re-render everything in light of the
changes.

## Generating the docs

The docs source is in a distinct repo, skupper-docs, and are written
in AsciiDoc.

1. Run `./plano update-docs` to retrieve the latest
   version of AsciiDoc files from the `main` branch of `skupper-docs`.
2. Run `./plano test` to run tests and populate the `docs` directory
   of this repo with the HTML files generated from the Markdown files.

## Updating the site for new Skupper releases

The `generate-releases` command fetches release data from GitHub and
updates the site for new releases.

~~~ console
./plano generate-releases
./plano render --force
~~~
