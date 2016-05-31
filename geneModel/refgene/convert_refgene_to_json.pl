#!/usr/bin/perl
use warnings;
use strict;


my %ref_hgnc_id = ();
open(IN, "20151008_hg38_gene_HGNCid_final.txt")||die "$!";
my $h = <IN>;
while(<IN>){
	s/\s+$//;
		my @line = split(/\t/, $_);
		$ref_hgnc_id{$line[1]} = $line[0];	
}
close IN;
my %eng_hgnd_id = ();
open(IN, "20151008_hg38_ensgene_hgnc_final.txt")||die "$!";
$h = <IN>;
while(<IN>){
	s/\s+$//;
	my @line = split(/\t/,$_);
	$eng_hgnd_id{$line[1]} = $line[0];
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
		#$outstr = "\{\"_id\":\{\"c\":$chr,\"ep\":$ep,\"p\":$p\},\"f\":\[\{\"ecds\":\"$ecds\",\"ecs\":\"$ecs\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"exons\":\"$exons\",\"g\":\"$g\",\"hid\":\"$hid\",\"scds\":\"$scds\",\"scs\":\"$scs\",\"se\":\"$se\",\"st\":\"$st\",\"t\":\"$t\"\}\]\}";
		$outstr = "\{\"ecds\":\"$ecds\",\"ecs\":\"$ecs\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"exons\":\"$exons\",\"g\":\"$g\",\"hid\":\"$hid\",\"scds\":\"$scds\",\"scs\":\"$scs\",\"se\":\"$se\",\"st\":\"$st\",\"t\":\"$t\"\}";
	}else{
		$outstr = "\{\"ecds\":\"$ecds\",\"ecs\":\"$ecs\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"exons\":\"$exons\",\"g\":\"$g\",\"scds\":\"$scds\",\"scs\":\"$scs\",\"se\":\"$se\",\"st\":\"$st\",\"t\":\"$t\"\}";
		#$outstr = "\{\"_id\":\{\"c\":$chr,\"ep\":$ep,\"p\":$p\},\"f\":\[\{\"ecds\":\"$ecds\",\"ecs\":\"$ecs\",\"ee\":\"$ee\",\"ef\":\"$ef\",\"exons\":\"$exons\",\"g\":\"$g\",\"scds\":\"$scds\",\"scs\":\"$scs\",\"se\":\"$se\",\"st\":\"$st\",\"t\":\"$t\"\}\]\}";
	}

	my $id = "$chr:$ep:$p"; 
	push @{$json{$id}} , $outstr;

	#print OUT "$outstr\n";
}

close IN;

foreach my $e (sort keys %json){
	my @id = split(':', $e);
	if($id[0] =~ /^[0-9]+$/){
		print OUT "\{\"_id\":\{\"c\":$id[0],\"ep\":$id[1],\"p\":$id[2]\},\"f\":\[";
		#my $o = join(',', map {$json{$e}{$_}}  keys %{$json{$e}});
		#	foreach my $e_cds {sort {$b cmp $a} keys %{$json{$e}}}{
		#	print OUT "$json{$e}{$e_cds}";
		my $o = join(',', @{$json{$e}});
		print OUT "$o\]\}\n";
	}
}

close OUT;



