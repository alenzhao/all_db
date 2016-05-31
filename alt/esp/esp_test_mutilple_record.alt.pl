#!/usr/bin/perl
use warnings;

my @var_order = ();
open(IN, "hg38_esp6500.json")||die "$!";
#open(IN, "test.json")||die "$!";
my $h = <IN>;
while(<IN>){
	s/\s+$//;
	s/"//g;
	s/\\u003e/\>/g;
	my $l = $_;
	#my @line = split(/[,\s]/, $l);
	my @line = split(/[:,}]/, $l);
	if($l =~ /ct:alt/){
		push @var_order, "$line[2]_$line[6]_$line[4]:$line[8]";
	}else{
		push @var_order, "$line[2]:$line[4]";
	}
}
close IN;

my %esp = ();
my %visited = ();
my $infile = 'ESP6500SI-V2-SSA137.GRCh38-liftover.snps_indels.vcf';
#my $infile = "test.vcf";
open(IN, $infile)||die "$!";
while(<IN>){
    s/\s+$//;
   # s/\\u003e/\>/g;
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
	if($grch38_c =~ /_/){
	    #$grch38_c =~ s/(\d+)([_a-zA-Z0-9]+)/$1/;
		print "$grch38_c\n";
	}
	    #my $id = "$grch38_c:$grch38_p:$line[3]:$line[4]";
	    my $id = "$grch38_c:$grch38_p";
	    my $mut = "$line[3]:$line[4]";
	    my %item = ();
	    $item{'chr'}   = $grch38_c;
	    $item{'pos'}   = $grch38_p;
	    $item{'dbsnp'} = $line[2];
	    $item{'ref'}   = $line[3];
	    my @alt_grp = split(',',$line[4]);
	    foreach my $a (0..$#alt_grp){
	        $alt_grp[$a] = "\"$alt_grp[$a]\"";
	    }
	    $item{'alt'}   = join(", ", @alt_grp);
	    #$item{'visited'} = 0;
	    $visited{$id} = 0;
	    $item{'hg19_position'} = "$line[0]:$line[1]";
	    foreach my $i (@info){
		my @pair = split(/=/, $i);
	        $item{$pair[0]} = $pair[1];
	    }
      	my @maf = split(/,/, $item{'MAF'});
	$item{'HGVS_CDNA_VAR'} =~ s/\>/\\u003e/g;
	$maf[0] = sprintf("%.2f", $maf[0]); $maf[0] *= 0.01;## EMAF
	$maf[1] = sprintf("%.2f", $maf[1]); $maf[1] *= 0.01;## AMAF
	$maf[2] = sprintf("%.2f", $maf[2]); $maf[2] *= 0.01;## GMAF
   	if($maf[0] ==0){
	    $maf[0] = '0.0';
	}
	if ($maf[1] == 0){
	    $maf[1] = '0.0';
	}
	if ($maf[2] ==0){
	    $maf[2] = '0.0';
	}
	    #my $out_str = "\{ \"AMAF\" : $maf[1], \"HGVS_PROTEIN_VAR\" : \"$item{'HGVS_PROTEIN_VAR'}\", \"FG\" : \"$item{'FG'}\", \"EA_GTC\" : \"$item{'EA_GTC'}\", \"GWAS_PUBMED\" : \"$item{'GWAS_PUBMED'}\", \"EMAF\" : $maf[0], \"AA_AC\" : \"$item{'AA_AC'}\", \"GS\" : \"$item{'GS'}\", \"EA_AC\" : \"$item{'EA_AC'}\", \"id\" : \"$item{'dbsnp'}\", \"DP\" : \"$item{'DP'}\", \"CDS_SIZES\" : \"$item{'CDS_SIZES'}\", \"GL\" : \"$item{'GL'}\", \"HGVS_CDNA_VAR\" : \"$item{'HGVS_CDNA_VAR'}\", \"r\" : \"$item{'ref'}\", \"TAC\" : \"$item{'TAC'}\", \"DBSNP\" : \"$item{'DBSNP'}\", \"AA\" : \"$item{'AA'}\", \"GTC\" : \"$item{'GTC'}\", \"hg19_position\" : \"$item{'hg19_position'}\", \"AA_AGE\" : \"$item{'AA_AGE'}\", \"CA\" : \"$item{'CA'}\", \"CG\" : \"$item{'CG'}\", \"GTS\" : \"$item{'GTS'}\", \"EA_AGE\" : \"$item{'EA_AGE'}\", \"AA_GTC\" : \"$item{'AA_GTC'}\", \"GMAF\" : $maf[2], \"CP\" : \"$item{'CP'}\", \"PH\" : \"$item{'PH'}\", \"o\" : \[ $item{'alt'} \], \"EXOME_CHIP\" : \"$item{'EXOME_CHIP'}\" \}";
	#}

	my $out_str="\{\"AA\":\"$item{'AA'}\",\"AA_AC\":\"$item{'AA_AC'}\",\"AA_AGE\":\"$item{'AA_AGE'}\",\"AA_GTC\":\"$item{'AA_GTC'}\",\"AMAF\":$maf[1],\"CA\":\"$item{'CA'}\",\"CDS_SIZES\":\"$item{'CDS_SIZES'}\",\"CG\":\"$item{'CG'}\",\"CP\":\"$item{'CP'}\",\"DBSNP\":\"$item{'DBSNP'}\",\"DP\":\"$item{'DP'}\",\"EA_AC\":\"$item{'EA_AC'}\",\"EA_AGE\":\"$item{'EA_AGE'}\",\"EA_GTC\":\"$item{'EA_GTC'}\",\"EMAF\":$maf[0],\"EXOME_CHIP\":\"$item{'EXOME_CHIP'}\",\"FG\":\"$item{'FG'}\",\"GL\":\"$item{'GL'}\",\"GMAF\":$maf[2],\"GS\":\"$item{'GS'}\",\"GTC\":\"$item{'GTC'}\",\"GTS\":\"$item{'GTS'}\",\"GWAS_PUBMED\":\"$item{'GWAS_PUBMED'}\",\"HGVS_CDNA_VAR\":\"$item{'HGVS_CDNA_VAR'}\",\"HGVS_PROTEIN_VAR\":\"$item{'HGVS_PROTEIN_VAR'}\",\"PH\":\"$item{'PH'}\",\"TAC\":\"$item{'TAC'}\",\"hg19_position\":\"$item{'hg19_position'}\",\"id\":\"$item{'dbsnp'}\",\"o\":\[$item{'alt'}\],\"r\":\"$item{'ref'}\"}";

#{"_id":{"c":9,"p":14816},"f":[{"AA":"C","AA_AC":"28,2736","AA_AGE":".","AA_GTC":"1,26,1355","AMAF":0.0101,"CA":".","CDS_SIZES":"NM_182905.4:1398","CG":"1.2","CP":"1.0","DBSNP":"dbSNP_137","DP":"9","EA_AC":"373,6917","EA_AGE":".","EA_GTC":"20,333,3292","EMAF":0.0512,"EXOME_CHIP":"no","FG":"NM_182905.4:missense","GL":"WASH1","GMAF":0.0399,"GS":"215","GTC":"21,359,4647","GTS":"GG,GC,CC","GWAS_PUBMED":".","HGVS_CDNA_VAR":"NM_182905.4:c.1389G\u003eC","HGVS_PROTEIN_VAR":"NM_182905.4:p.(W463C)","PH":"probably-damaging:1.0","TAC":"401,9653","hg19_position":"9:14816","id":"rs200377821","o":["G"],"r":"C"}]}



	
	push @{$esp{$id}}, $out_str;
	#$esp{$id}{$mut}{'visited'} = 0;
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
    	    my @info = split(':', $v);
	    #foreach my $m (keys %{$esp{$v}{$m}}){
	    $visited{$v} = 1;   
	    
	#my @maf = split(/,/, $info{'MAF'});
	#$maf[0] = sprintf("%.2f", $maf[0]); $maf[0] *= 0.01;## EMAF
	#$maf[1] = sprintf("%.2f", $maf[1]); $maf[1] *= 0.01;## AMAF
	#$maf[2] = sprintf("%.2f", $maf[2]); $maf[2] *= 0.01;## GMAF
    
	#my @alt_grp = split(',',$info{'alt'});
	#my $alt_o = '';
	#if($#alt_grp == 1){
	#    $alt_o = "\"$alt_grp[0]\", \"$alt_grp[1]\"";
	#}elsif($#alt_grp == 2){
	#    $alt_o = "\"$alt_grp[0]\", \"$alt_grp[1]\", \"$alt_grp[2]\"";
	#}else{
	#    $alt_o = "\"$alt_grp[0]\"";
	#}
	#print OUT "\{ \"_id\" : \{ \"p\" : $info{'pos'}, \"c\" : $info{'chr'} }, \"f\" : \[ \{ \"AMAF\" : $maf[1], \"HGVS_PROTEIN_VAR\" : \"$info{'HGVS_PROTEIN_VAR'}\", \"FG\" : \"$info{'FG'}\", \"EA_GTC\" : \"$info{'EA_GTC'}\", \"GWAS_PUBMED\" : \"$info{'GWAS_PUBMED'}\", \"EMAF\" : $maf[0], \"AA_AC\" : \"$info{'AA_AC'}\", \"GS\" : \"$info{'GS'}\", \"EA_AC\" : \"$info{'EA_AC'}\", \"id\" : \"$info{'dbsnp'}\", \"DP\" : \"$info{'DP'}\", \"CDS_SIZES\" : \"$info{'CDS_SIZES'}\", \"GL\" : \"$info{'GL'}\", \"HGVS_CDNA_VAR\" : \"$info{'HGVS_CDNA_VAR'}\", \"r\" : \"$info{'ref'}\", \"TAC\" : \"$info{'TAC'}\", \"DBSNP\" : \"$info{'DBSNP'}\", \"AA\" : \"$info{'AA'}\", \"GTC\" : \"$info{'GTC'}\", \"hg19_position\" : \"$info{'hg19_position'}\", \"AA_AGE\" : \"$info{'AA_AGE'}\", \"CA\" : \"$info{'CA'}\", \"CG\" : \"$info{'CG'}\", \"GTS\" : \"$info{'GTS'}\", \"EA_AGE\" : \"$info{'EA_AGE'}\", \"AA_GTC\" : \"$info{'AA_GTC'}\", \"GMAF\" : $maf[2], \"CP\" : \"$info{'CP'}\", \"PH\" : \"$info{'PH'}\", \"o\" : \[ $alt_o \], \"EXOME_CHIP\" : \"$info{'EXOME_CHIP'}\" \} \] \}\n";
	my $o = join(', ', @{$esp{$v}});
	#print OUT "\{ \"_id\" : \{ \"p\" : $info[1], \"c\" : $info[0] }, \"f\" : \[ $o \] \}\n";
	if ($info[0] =~ /_/){
	#	                     "c":15,"ct":"alt","ncbi":"KI270851v1","p":39190
	    my @id = split('[:_]', $info[0]);
	    print OUT "\{\"_id\":\{\"c\":$id[0],\"ct\":\"$id[2]\",\"ncbi\":\"$id[1]\",\"p\":$info[1]\},\"f\":\[$o\]\}\n";
	}else{
	    print OUT "\{\"_id\":\{\"c\":$info[0],\"p\":$info[1]\},\"f\":\[$o\]\}\n";
	}
    }
}

close OUT;
close ERR;

open(UNM, ">unvisited_in_original")||die "$!";
foreach my $v (keys %visited){
    if($visited{$v} ==0){
	print UNM "$v\n";
    }
}
close UNM;




