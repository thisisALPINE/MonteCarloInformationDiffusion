# Gnuplot script file for plotting data in file "diffusion.dat"
# This file is called graphs_probabilities.p

set title "Results for Graph with 1000 Nodes"
set ylabel "Expected Infection as percentage of Nodes"
set xlabel "Probability that an Agent will change its Mind"
set xtics 0.1
set ytics 10
set yrange [0:100]

   plot "diffusion.dat" using 1:2:4:5 title 'Unbalanced Start' w yerrorlines , \
   "diffusion.dat" using 1:3:6:7 title 'Balanced Start' w yerrorlines

