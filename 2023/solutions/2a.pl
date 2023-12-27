#!/usr/bin/perl

%max = (red=>12, green=>13, blue=>14);

line:
while (<>) {
  s/Game (\d+): // or die "Bad format: $_";
  $game = $1;
  @draws = split ';';
  for my $d (@draws) {
    $d =~ s/(\d+) ([a-z]+)/$2=>$1/g;
    %d = eval "($d)";
    while (($color, $n) = each %d) {
      next line if ($n > $max{$color});
    }
  }
  print "$game\n";
}
