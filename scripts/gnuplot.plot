set boxwidth 0.5
set xrange[0:24]
set xlabel 'Hour of day (GMT)'
set ylabel 'Hits'
set style fill solid
set timestamp
set terminal png size 350,262 
set output '/tmp/django/wikicount/introduction.png'
plot '/tmp/output.log' using 1:2 with boxes notitle
