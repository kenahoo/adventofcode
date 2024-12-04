#!/usr/bin/perl

open my($fh), '<', 'data/3.txt';
my $sum = 0;

my $chunk = qr{(mul|do|don't)\((?:(\d+),(\d+))?\)};

$doing = 1;
while (<$fh>) {
    while (m/$chunk/g) {
        if ($1 eq 'do') {
            $doing = 1;
        } elsif ($1 eq 'don\'t') {
            $doing = 0;
        } else {
            $sum += $2 * $3 if $doing;
        }
    }
}
print "$sum\n";
