perl -nle '@x=m/(\d)/g; $t+="$x[0]$x[-1]"; END{print $t}' data/1a
