#!/usr/bin/perl
use warnings;

my @var_order = ();
open(IN, "hg38_esp6500_exome.json")||die "$!";
#open(IN, "test.json")||die "$!";
#my $h = <IN>;
while(<IN>){
	s/\s+$//;
	my $l = $_;
	my @line = split(/[,\s]/, $l);
	if($l =~ /"r" : "([ATGCNacgtn\.]+)".*?"o" : \[ "([ACGTNacgtn\.]+)" \]/){
            push  @var_order, "$line[10]:$line[6]:$1:$2";
	}elsif($l =~ /"r" : "([ATGCNacgtn\.]+)".*?"o" : \[ "([ACGTNacgtn\.]+)", "([ACGTNacgtn\.]+)" \]/){
	    push @var_order, "$line[10]:$line[6]:$1:$2,$3";
	    #push @var_order, "$line[10]:$line[6]:$1:$3";
	}elsif($l =~ /"r" : "([ATGCNacgtn\.]+)".*?"o" : \[ "([ACGTNacgtn\.]+)", "([ACGTNacgtn\.]+)", "([ACGTNacgtn\.]+)" \]/){
	    push @var_order, "$line[10]:$line[6]:$1:$2,$3,$4";
	    #push @var_order, "$line[10]:$line[6]:$1:$3";
	    #push @var_order, "$line[10]:$line[6]:$1:$4";
	}
}
close IN;

my %esp = ();
my $infile = 'ESP6500SI-V2-SSA137.GRCh38-liftover.snps_indels.vcf';
#my $infile = "test.vcf";
open(IN, $infile)||die "$!";
while(<IN>){
    s/\s+$//;
    #if(!/^#/ and /GRCh38_POSITION=[0-9xyXYmn]+:\d+/){
    if(!/^#/ and !/GRCh38_POSITION=-1/){
	my @line = split(/\t|\s+/, $_);
	$line[$#line] =~ /GRCh38_POSITION=([0-9a-zA-Z_]+):(\d+)/;
	my $grch38_c = $1;
	if($grch38_c eq 'X'){$grch38_c = 23;}
	if($grch38_c eq 'Y'){$grch38_c = 24;}
	if($grch38_c eq 'M'){$grch38_c = 25;}
	my $grch38_p = $2;
	my @info = split(/;/, $line[$#line]);
	#my @alt = split(/,/, $line[4]);
	#if($#alt >0){
	#   print "multiple alt alleles\n$_\n";
	#}else{
	#foreach my $a (@alt){
	if($grch38_c =~ /_/){
	    $grch38_c =~ s/(\d+)([_a-zA-Z0-9]+)/$1/;
	}
	    my $id = "$grch38_c:$grch38_p:$line[3]:$line[4]";
	    #my $id = "$line[0]:$line[1]";
	    $esp{$id}{'chr'}   = $grch38_c;
	    $esp{$id}{'pos'}   = $grch38_p;
	    $esp{$id}{'dbsnp'} = $line[2];
	    $esp{$id}{'ref'}   = $line[3];
	    $esp{$id}{'alt'}   = $line[4];
	    $esp{$id}{'visited'} = 0;
	    $esp{$id}{'hg19_position'} = "$line[0]:$line[1]";
	    foreach my $i (@info){
		my @pair = split(/=/, $i);
		$esp{$id}{$pair[0]} = $pair[1];
	    }
	#}
    }
}
close IN;

open(ERR, ">unmatched_records_in_mongoDB")||die "$!";
open(OUT, ">xz_esp6500.json")||die "$!";
foreach my $v (@var_order){
	#my @var = split(/\s/, $v);
	if($esp{$v} eq ''){
	    print ERR "$v\n";
	}else{
	my %info = %{$esp{$v}};
	$esp{$v}{'visited'} = 1;
	my @maf = split(/,/, $info{'MAF'});
	$maf[0] = sprintf("%.2f", $maf[0]); $maf[0] *= 0.01;## EMAF
	$maf[1] = sprintf("%.2f", $maf[1]); $maf[1] *= 0.01;## AMAF
	$maf[2] = sprintf("%.2f", $maf[2]); $maf[2] *= 0.01;## GMAF
    
	my @alt_grp = split(',',$info{'alt'});
	my $alt_o = '';
	if($#alt_grp == 1){
	    $alt_o = "\"$alt_grp[0]\", \"$alt_grp[1]\"";
	}elsif($#alt_grp == 2){
	    $alt_o = "\"$alt_grp[0]\", \"$alt_grp[1]\", \"$alt_grp[2]\"";
	}else{
	    $alt_o = "\"$alt_grp[0]\"";
	}
	print OUT "\{ \"_id\" : \{ \"p\" : $info{'pos'}, \"c\" : $info{'chr'} }, \"f\" : \[ \{ \"AMAF\" : $maf[1], \"HGVS_PROTEIN_VAR\" : \"$info{'HGVS_PROTEIN_VAR'}\", \"FG\" : \"$info{'FG'}\", \"EA_GTC\" : \"$info{'EA_GTC'}\", \"GWAS_PUBMED\" : \"$info{'GWAS_PUBMED'}\", \"EMAF\" : $maf[0], \"AA_AC\" : \"$info{'AA_AC'}\", \"GS\" : \"$info{'GS'}\", \"EA_AC\" : \"$info{'EA_AC'}\", \"id\" : \"$info{'dbsnp'}\", \"DP\" : \"$info{'DP'}\", \"CDS_SIZES\" : \"$info{'CDS_SIZES'}\", \"GL\" : \"$info{'GL'}\", \"HGVS_CDNA_VAR\" : \"$info{'HGVS_CDNA_VAR'}\", \"r\" : \"$info{'ref'}\", \"TAC\" : \"$info{'TAC'}\", \"DBSNP\" : \"$info{'DBSNP'}\", \"AA\" : \"$info{'AA'}\", \"GTC\" : \"$info{'GTC'}\", \"hg19_position\" : \"$info{'hg19_position'}\", \"AA_AGE\" : \"$info{'AA_AGE'}\", \"CA\" : \"$info{'CA'}\", \"CG\" : \"$info{'CG'}\", \"GTS\" : \"$info{'GTS'}\", \"EA_AGE\" : \"$info{'EA_AGE'}\", \"AA_GTC\" : \"$info{'AA_GTC'}\", \"GMAF\" : $maf[2], \"CP\" : \"$info{'CP'}\", \"PH\" : \"$info{'PH'}\", \"o\" : \[ $alt_o \], \"EXOME_CHIP\" : \"$info{'EXOME_CHIP'}\" \} \] \}\n";
}
}
close OUT;
close ERR;

open(UNM, ">unvisited_in_original")||die "$!";
foreach my $v (keys %esp){
    if($esp{$v}{'visited'} ==0){
	print UNM "$v\n";
    }
}
close UNM;



#my @fields = ();
#push 
#my @fields = ();



