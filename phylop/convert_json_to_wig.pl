#!/usr/bin/perl
use warnings;

my $infile = "";
my $chr = $ARGV[0];
chomp($chr);
if($chr eq 'M'){$chr = 25;}
if($chr eq 'X'){$chr = 23;}
if($chr eq 'Y'){$chr = 24;}

my %block = ();
my $cor_now = 0;
my $cor_pre = 0;

#my $in_chr = 0;
open(IN, $infile)||die "$!";
while(<IN>){
	s/\s+$//;
	if(/\"c\" : $chr\s/){
		my $aline_json = $_;
		my @line = split(/\s/,$aline_json);
		#my $chr = $line[9];
		my $p = $line[6];
		$p =~ s/,//;
		my $sc = $line[17];
		$sc =~ s/"//g;
		$block{$chr}{$p} = $sc;
		
		if($cor_now == 0){
			$cor_now = $p;
		}else{
			$cor_pre = $cor_now;
			$cor_now = $cor_pre;
			
			if(($cor_now - $cor_pre) == 1000 ){
				
			}



		}
	}
}
close IN;
