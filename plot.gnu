set xdata time
set timefmt "%H:%M:%S"
set ytics 10 nomirror tc lt 1
set ylabel 'Temperature 1 [C]' tc lt 1
set y2tics 10 nomirror tc lt 2
set y2label 'Temperature 2 [C]' tc lt 2

log_file = system("echo $GNUPLOT_FILE")

plot log_file using 2:3 with lines title 'T1 [C]', '' using 2:5 with lines title 'T2 [C]' axes x1y2
pause 1
reread



