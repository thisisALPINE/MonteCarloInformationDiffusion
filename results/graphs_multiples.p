# Gnuplot script file for plotting data in file "diffusion.dat"
# This file is called graphs.p

set lmargin 10
set bmargin 5
set font "Helvetica, 24"
set key font "Helvetica, 24"
set xtics font "Helvetica, 12"
set ytics font "Helvetica, 12"
set title "Results for Graph with 10 Nodes" font "Helvetica, 24"
set ylabel "Expected Infection as percentage of Nodes" font "Helvetica, 24"
set xlabel "Number of Messages as multiple of Nodes"font "Helvetica, 24"
set xtics 1
set ytics 10
set yrange [0:100]

   plot "results10.dat" using 1:2:4:5 title 'Unbalanced Start' w yerrorlines , \
   "results10.dat" using 1:3:6:7 title 'Balanced Start' w yerrorlines

