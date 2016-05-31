#!/usr/bin/perl
use warnings;

my $file1 = $ARGV[0];## Json file dumped from MongoDB
my $file2 = $ARGV[1];

open(FL1, $file1)||die "$!";
open(FL2, $file2)||die "$!";
my $h = <FL2>;
my $lc = 1;
open(OUT, ">diff_$file1 vs $file2.out")||die "$!";
while(<FL1>){
    s/\s+$//;
    #my $lc = 1;
    my $visited = 0;
    my @cont_1 = split('\s+',$_);
    my $cmp = <FL2>;
    chomp($cmp);
    my @cont_2 = split('\s+', $cmp);
    if($#cont_1 == $#cont_2){
        foreach my $i (0..$#cont_1){
	    if($cont_1[$i] ne $cont_2[$i]){
		if(!$visited){
		    print OUT "$lc:\t$cont_1[$i] <--> $cont_2[$i]\t";
		    $visited = 1;
		}else{
		    print OUT "$cont_1[$i] <--> $cont_2[$i]\t";
		}
	    }
	}
	if($visited){print OUT "\n";}
    }else{
	print OUT "+----------different number of fields:\n";
	foreach my $j (0..$#cont_1){
	    if($cont_1[$j] ne $cont_2[$j]){
		my $str1 = join(' ', @cont_1[$j..$#cont_1]);
		my $str2 = join(' ', @cont_2[$j..$#cont_2]);
		print OUT "$str1\n$str2\n+----------\n";
		last;
	    }
	}
    }
    #print OUT "\n";
    $lc++;
}

close FL1;
close FL2;
close OUT;
