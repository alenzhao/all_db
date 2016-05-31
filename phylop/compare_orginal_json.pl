#!/usr/bin/perl
use warnings;
use strict;


#my @ch = c('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','X','Y','M');
open(OUT, ">phylop.comp")||die "$!";
my $infile = "hg38_refgene_72.json";
open(IN, $infile)||die "$!";
my $h = <IN>;
while(<IN>){
	s/\s+$//;
	#s/\s//g;
	my $aline_json = $_;
	my @line = split(/\s/,$aline_json);
	my $chr = $line[9];
	if($chr == 23){$chr = 'X';}
	if($chr == 24){$chr = 'Y';}
	if($chr == 25){$chr = 'M';}
	my $p = $line[6];$p =~ s/,//;
	my @sc = split(',', $line[17]);

#+++++++++++++ debug code ++++++++++
$p = 16512;
$chr = 7;
@sc = c('0.06');

#+++++++++++++++++++++++++++++++++++


## deal with original wigfix file
	open(WIG, "phyloP_files/chr$chr.phyloP100way.wigFix")||die "$!";
	my @block_index = ();
	while(<WIG>){
		if(/^fix/){
			s/\s+$//;
			my $line = $_;
			$line =~ /fixedStep chrom=chr([0-9XYMxym]+) start=(\d+) step=1/;
			push @block_index, $2;
		}
	}
	close WIG;

## find out the block which contains the 1000bp phylop score
	my $block_ancor = -1;
	if($#block_index ==0){
		$block_ancor = 0;
	}else{
		for my $i (1..$#block_index){
			if($p >= $block_index[$i-1] and $p <= $block_index[$i]){
				$block_ancor = $i;
			}
		}
	}

## generate the json format data
	my $in_block = 0;
	my $value_str = '';
	my $full = 0;
	open(WIG, "phyloP_files/chr$chr.phyloP100way.wigFix")||die "$!";
	my $block_count = 0;
	while(<WIG>){
		if(/fixedStep chrom=chr$chr start=(\d+) step=1/){
			$block_count +=1;
			if($block_count == $block_ancor){	
				$in_block = 1;
				next;
			}
		}else{
		    if($in_block ==1){
				$in_block = 0;
				last;
		    }else{
				$in_block = 0;
		    }
		}
	    
	    if($in_block ){
 			s/\s+$//;
			my $p = sprintf("%.2f", $_);
			$value_str .= "$p,";
			$full +=1;
			if($full == ($#sc+1)){
				last;
			}
	    }
	}
	close WIG;

	$value_str =~ s/,$//;
	my $outstr = "\{ \"_id\" : \{ \"p\" : $p, \"c\" : $chr \}, \"f\" : \[ \{ \"sc\" : \"$value_str\" \} \] \}";
	if($outstr ne $aline_json){
	    print OUT "$aline_json\n$outstr\n\n";
	}

}
close IN;

close OUT;
