#!/usr/bin/perl

line:
while (<>) {
  s/Game (\d+): // or die "Bad format: $_";
  $game = $1;
  @draws = split ';';
  %min = (red=>0, green=>0, blue=>0);
  for my $d (@draws) {
    $d =~ s/(\d+) ([a-z]+)/$2=>$1/g;
    %d = eval "($d)";
    while (($color, $n) = each %d) {
      $min{$color} = $n if $n > $min{$color};
    }
  }
  print +($min{red}*$min{green}*$min{blue}), "\n";
}
