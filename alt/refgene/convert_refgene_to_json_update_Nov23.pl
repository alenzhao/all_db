#!/usr/bin/perl
use warnings;
use strict;


my %ref_hgnc_id = ();
open(IN, "GENE_HGNCID.txt")||die "$!";
my $h = <IN>;
while(<IN>){
	s/\s+$//;
		my @line = split(/\t/, $_);
		$ref_hgnc_id{$line[0]} = $line[1];	
}
close IN;
my %eng_hgnd_id = ();
open(IN, "ensgene_hgnc.txt")||die "$!";
$h = <IN>;
while(<IN>){
	s/\s+$//;
	my @line = split(/\t/,$_);
	$eng_hgnd_id{$line[0]} = $line[1];
}

open(OUT, ">xz_hg38_refgene.json")||die "$!";

my %json = ();
my $infile = "20151005_hg38_refgene_official.txt";
open(IN, $infile)||die "$!";
$h = <IN>;
while(<IN>){
	s/\s+$//;
	my @line = split(/\t/, $_);
	my $chr = $line[2]; $chr =~ s/chr//;
	if($chr eq 'X'){$chr = 23;}
	if($chr eq 'Y'){$chr = 24;}
	my $ep = $line[5];
	my $p = $line[4];
	my $ecds = $line[7];
	my $ecs = $line[14];
	my $scs = $line[13];
	my $ee = $line[10];
	my $ef = $line[$#line];
	my $se = $line[9];
	my $exons = $line[8];
	my $g = $line[12];
	my $scds = $line[6];
	my $st = $line[3];
	my $t = $line[1];

	my $hid = "";
	my $ehid = "";
	my $outstr = "";
	if($ref_hgnc_id{$g} ne ''){
		$hid = $ref_hgnc_id{$g};
		#$outstr = "\{\"exons\":\"$exons\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"ecs\":\"$ecs\",\"scs\":\"$scs\",\"g\":\"$g\",\"scds\":\"$scds\",\"st\":\"$st\",\"t\":\"$t\",\"ecds\":\"$ecds\",\"hid\":\"$hid\",\"se\":\"$se\"\}";
		$outstr = "\{\"ecds\":\"$ecds\",\"ecs\":\"$ecs\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"exons\":\"$exons\",\"g\":\"$g\",\"hid\":\"$hid\",\"scds\":\"$scds\",\"scs\":\"$scs\",\"se\":\"$se\",\"st\":\"$st\",\"t\":\"$t\"\}";
		
	}else{
		$outstr = "\{\"ecds\":\"$ecds\",\"ecs\":\"$ecs\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"exons\":\"$exons\",\"g\":\"$g\",\"scds\":\"$scds\",\"scs\":\"$scs\",\"se\":\"$se\",\"st\":\"$st\",\"t\":\"$t\"\}";
		#$outstr = "\{\"exons\":\"$exons\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"ecs\":\"$ecs\",\"scs\":\"$scs\",\"g\":\"$g\",\"scds\":\"$scds\",\"st\":\"$st\",\"t\":\"$t\",\"ecds\":\"$ecds\",\"se\":\"$se\"\}";
	}

	my $id = "$chr:$ep:$p"; 
	push @{$json{$id}} , $outstr;

	#print OUT "$outstr\n";
}

close IN;

foreach my $e (sort keys %json){
	my @id = split(':', $e);
	#if($id[0] =~ /^[0-9]+$/){
		if ($e =~ /_/){
			my @alt = split('[:_]', $e);
			if( $alt[0] eq 'X'){
				$alt[0] = 23;
			}
			if ($alt[0] eq 'Un'){
				print OUT "\{\"_id\":\{\"c\":27,\"ep\":$id[1],\"ncbi\":\"$alt[1]\",\"p\":$id[2]\},\"f\":\[";
			}else{
				print OUT "\{\"_id\":\{\"c\":$alt[0],\"ct\":\"$alt[2]\",\"ep\":$id[1],\"ncbi\":\"$alt[1]\",\"p\":$id[2]\},\"f\":\[";
			}
		}else{
			print OUT "\{\"_id\":\{\"c\":$id[0],\"ep\":$id[1],\"p\":$id[2]\},\"f\":\[";
		}
		#print OUT "\{\"_id\":\{\"p\":$id[2],\"c\":$id[0],\"ep\":$id[1]\},\"f\":\[";
		my $o = join(',', @{$json{$e}});
		print OUT "$o\]\}\n";
#	}
}




close OUT;

