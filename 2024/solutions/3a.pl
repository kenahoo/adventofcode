#!/usr/bin/perl

open my($fh), '<', 'data/3.txt';
my $sum = 0;
while (<$fh>) {
    while (m/mul\((\d+),(\d+)\)/g) {
        $sum += $1 * $2;
    }
}
print "$sum\n";
