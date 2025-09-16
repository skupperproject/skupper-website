man -Thtml 5 skrouterd.conf   | sed -n '/<hr>/,$p' > input/skrouterd/skrouterd.conf.html.in

man -Thtml skrouterd   | sed -n '/<hr>/,$p' > input/skrouterd/skrouterd.html.in


