# Skupper website

[![main](https://github.com/ssorj/skupper-website/workflows/main/badge.svg)](https://github.com/ssorj/skupper-website/actions?query=workflow%3Amain)

## Project commands

You can use the `./plano` command in the root of the project to
perform project tasks.  It accepts a subcommand.  Use `./plano --help`
to list the available commands.

## Rendering the site

You can use the `./plano render` command in the root of the project to
render the site:

```console
$ ./plano render
--> render
Rendering input files
<-- render
OK (0.21s)
```

For development, you can serve the site locally.  Any changes you make
to the input files are rendered on demand.

```console
$ ./plano serve
--> serve
Rendering input files
Watching for input file changes
Serving at http://localhost:8080
Starting LiveReload v0.9.1 for /home/jross/code/skupper-website-ssorj/output on port 35729.
```

<!-- ## Generating the docs -->

<!-- The docs source is in a distinct repo, skupper-docs -->
<!-- It gets imported here and installed  -->
<!-- You must have antora installed -->
