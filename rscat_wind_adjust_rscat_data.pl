#!/usr/bin/perl -w
#
#==-FNMOC/N38DI PERL SCRIPT DEFINITION-==========================================
#
#  NAME: rscat_wind_adjust_rscat_data.pl
#  
#        A.K.A: SMS RSCAT_WIND_Adjust_RapidScat_ASCII_Data_files.pl
#
#  SCRIPT OVERVIEW: This script (in LINUX O/S) finds data entries with a + (plus)
#                   character & REPLACES with the SPACE (" ") character. 
#                   This program will find also al occurances of the String "---99"
#                   and replace with "___99" [3 spaces and '99'].
#
#                   EXAMPLE:
#
#
#------------------------------------------------------------------------------
# PARAMETER TABLE:
#------------------------------------------------------------------------------
#
# I/O           NAME              TYPE         FUNCTION
#------------------------------------------------------------------------------
#  I           RSCAT DATA         ASCII files  input file name
#  O           Output Data        ASCII File   output file
#  $i          index variable     integer
#_______________________________________________________________________________
#==============================================================================
#
#==============================================================================
#-
#
# Programmer: Mr. Paul McCrone      15 May 2015
#
#==============================================================================
#  NOTES: THIS SCRIPT ASSUMES THE USE OF PERL version 5.8 for Redhat Linux 5+.
#	  It is designed to run on a variant of Microsoft Windows only
#
#------------------------------------------------------------------------------
#
# A simple perl script
#
#
#
#------------------------------------------------------------------------------
#

use strict;
use diagnostics;
use Net::FTP;
use File::Copy;
#use Win32;
#use Win32::File;
#use Win32::File qw/GetAttributes SetAttributes/;
#use Win32::Internet;

#
# As a rule, the letter 'O' or 'o' (as in 'oscar') can be confused with a zero.
# I generally define variables $o and $O (the letter 'o') as zero to eliminate confusion.
# "$o" means lower case "o" and "$O" means capital "O", which are different variables in 
# PERL. FYI: I now put this in all my PERL scripts.
#

my $o=0;
my $O=0;


###### This is an example of a UNIX/LINUX Spawn in PERL
###### Note the backtick quotes ``
#
#my @deleteJPEGUPPER = `/bin/rm -f /metsat04/tropical/MarkIVB/JPEG/*.JPG`;
#


system("date");



my $renameitnow = `echo Renaming files now.`;
my $renameSTATUS = 0;

my $rename_string = "echo Renaming files now.";

#
#########################################
#########################################
# This is the location where I want to search for files.
#my $search_dir_name  =  "/opt/global/webservices/apache/app/tcweb/dynamic/products/tc08/SHEM/";

#### LINUX ONLY ##### my $search_dir_name  =  -/gpfs3/home/mccronep/idl/pmc-projects/-;

#### FOR WINDOWS

my $search_dir_name='D:/m4b_data/SATFOCUS/alpha/Taiwain/';
$search_dir_name='/home/mccronep/data/RapidScat/ascii_test/';
$search_dir_name='/satdat/m4b/RapidScat/nrt/ascii/';


# This is my home dir
#

my $home                   = "D:/perl/";
$home                   = "/home/mccronep/";

# This is the path where the perl prgm is located
#

my $perlhome               = "D:/perl/alpha/";
   $perlhome               = "/home/mccronep/python/src/RapidScat/";

my $garbage_indicator      =  "/xxx---xxx/";
my $old_file_name          =  "/xxx---xxx/";
my $blank_space            =  " ";
my $bspc            	   =  " ";
my $under_score            =  "_";
my $uscor                  =  "_";

my $plus_sign              =  "+";
my $plus                   =  "+";
my $psign                  =  "+";

my $dir                    =  $garbage_indicator;

my $datafile               =  $garbage_indicator;

# This is the pattern you want to search by
my $pattern             = $blank_space ;

# THIS IS WHAT YOU WILL CHANGE THE OLD PATTERN INTO.
my $newpattern          =  $under_score;

# These are the files that you want to change

my $pattern_for_search  =  "*";


my $length_of_pattern      =  length($pattern);

my $length_of_newpattern   =  length($newpattern);

my $manual_entry           =  $garbage_indicator;
   $manual_entry           =  $ARGV[0];
my $length_manual_entry    =  $o;
   $length_manual_entry    =  length($manual_entry), if exists $ARGV[0];

my $cmd_line_pattern       =  $garbage_indicator;
   $cmd_line_pattern       =  $ARGV[1];
my $length_c_l_pattern     =  $o;
   $length_c_l_pattern     =  length($cmd_line_pattern), if exists $ARGV[1];

my $cmd_line_newpattern    =  $garbage_indicator;
   $cmd_line_newpattern    =  $ARGV[2];
my $length_c_l_newpattern  =  $o;
   $length_c_l_newpattern  =  length($cmd_line_newpattern), if exists $ARGV[2];


#------------------------------------
# rscat_wind_adjust_rscat_data.pl
#------------------------------------
#

print "\n\n ------------------------------------\n";
print " START PERL SCRIPT: -rscat_wind_adjust_rscat_data.pl-  \n";
print " ------------------------------------\n";



#------------------------------------
# NOTE regarding the previous line:
#------------------------------------
# If you get an ":Use of uninitialized value:" error from PERL, just ignore it.
# This is not a problem, as the PERL code written here does account for this
# possibility and it will not prevent this code from running correctly.
#

print "\n\n ------------------------------------\n";
print " NOTE :\n";
print " ------------------------------------\n";
print " If you get an :Use of uninitialized value: error \n";
print " from PERL, just ignore it. This is not a problem, \n";
print " as the PERL code written here does account for this\n";
print " possibility and it will not prevent this code from \n";
print " running correctly.\n\n";
print " ------------------------------------\n";

print "\n\nThe length of the ARGV0 is $length_manual_entry.\n\n";
print "The length of the ARGV1 is $length_c_l_pattern.\n\n";
print "The length of the ARGV2 is $length_c_l_newpattern.\n\n";
print " ------------------------------------\n";

####################################################################

####################################################################

if ($length_manual_entry != 0) {
        $dir                 =  $ARGV[0];
        $datafile            =  $ARGV[0];
        print "\nThe manually entered top directory is ----.\n";
        print "-->$dir.\n";
        print " ------------------------------------\n";

}

if ($length_c_l_pattern != 0) {
        ######$pattern             =  $ARGV[1];
        print "\nThis script does not accept this second entry----.\n";
        ######print "--> $pattern.\n";
        print " ------------------------------------\n";

        #### These are the files that you want to change
        #####$pattern_for_search  =  $pattern . -*-;
        #####$length_of_pattern   =  length($pattern);

}

if ($length_c_l_newpattern != 0) {
        #####$newpattern          =  $ARGV[2];
        print "\nThis script does not accept this third entry----.\n";
        #####print "--> $newpattern.\n";
        print " ------------------------------------\n";
        #####$length_of_newpattern   =  length($newpattern);

}


####################################################################

if (-e $dir) {
     print "File or directory $dir exists and is valid.\n\n";

}
else {
       print "***File or directory $dir ***DOES NOT *** exist.\n\n";
       $dir                 =  $garbage_indicator;
       $datafile            =  $garbage_indicator;

}

####################################################################
if ($dir eq $garbage_indicator) {
        $dir                 =  $search_dir_name;
        $datafile            =  $search_dir_name;
        die ("Theres nothing to convert! Quitting...NOW...\n\n");

}

####################################################################
###
###	my @dir_array      =  `dir`;
###
###	my @target_array   =  `dir`;
###	   @target_array   =  @dir_array;
###
###	my $length_of_dir     =  $#dir_array    + 1;
###	print "The Length of directory array is...$length_of_dir\n\n";
###	
###	my $length_of_tgtdir  =  $#target_array + 1;
###	print "The Length of target array is...$length_of_tgtdir\n\n";
###
####################################################################
###
###
###	if ($length_of_dir eq $length_of_tgtdir) {
###	       print "The Length of directory matched.\n\n";
###	       print "............CONTINUING.....................\n\n";
###	}
###	else {
###	       print "***The Length of directory ***DOES NOT *** match.\n\n";
###	       die ("Theres nothing to modify! Quitting...\n\n");
###	}
###
###
###	print "\n\n\n...TargetArray -2- is :\n @target_array.....\n\n";
####################################################################

print "...................................................................\n";
print "___________________________________________________________________\n";
print "...................................................................\n";

print "\n\nThe TargetArarray contents:";
print "\n\n---------------------------\n\n";

my $iii               = 0 ;
my $ii                = 0 ;
my $i                 = 0 ;

open(FILE, $datafile) || die("FAILURE--Data file could not be opened by Perl script: $!\n");

my @datafile_lines = <FILE>; #### Slurp file into array

my $len_1line         = 0 ;
my $currchar          = '0';
my $dashdashdash99    = '---99';
my $dashdashdash      = '---';
my $spcspcspc_a       = '                          ';
my $spcspcspc         = $spcspcspc_a.$spcspcspc_a.$spcspcspc_a.$spcspcspc_a.'   ';
my $space2dash99      = '  -99';
my $testddd99         = 0 ;
my $testddd           = 0 ;
my $oneline           = '0';
my $ctrctrctr         = 0;

################################################## START FOREACH-1-

foreach $oneline (@datafile_lines) {
        #
        #
	#	#-----------------------------------------------------------------------
        #	# This the beginning of the CTR IF Block
        #	# - - - - - - - - - - - - - - - - - - - - 
        #	# This block is meant only from the very first line in the ascii file.
        #	# PYTHON has the tendency to place a literal line with just 3 dashes
        #	# in the very first line. I want to get rid of these 3 dashes.
	#	#-----------------------------------------------------------------------
	#	#
        #	if ($ctrctrctr == 0 ) {
	#		#
	#		$testddd=index($oneline,$dashdashdash);
       	#	        if ($testddd99 != -1) { 
       	#	             substr($oneline,$testddd99,3)=$spcspcspc;
       	#	        }
       	#	#
       	#	}
	#	#END OF CTR IF BLOCK
	#	#	
      	#	$ctrctrctr = $ctrctrctr + 1;
	#----------------------------------------------------------
	#
	#
	#
        $testddd99=index($oneline,$dashdashdash99);
	#
	if ($testddd99 != -1) {
	           substr($oneline,$testddd99,5)=$space2dash99;
	}
	#
        # START i loop -1-
	$len_1line = length($oneline);
	for ($i=0; $i<=$len_1line-1; $i++){
            #
            $currchar= substr($oneline,$i,1);
            #             
	    if ($currchar eq $plus_sign) {
	           substr($oneline,$i,1)=$blank_space;
	    }
            #
        }
        # END OF i loop -1-
	#
        $testddd99=index($oneline,$dashdashdash99);
	#
	if ($testddd99 != -1) {
	           substr($oneline,$testddd99,5)=$space2dash99;
	}
	#-----------------
	#
        $testddd99=index($oneline,$dashdashdash99);
	#
	if ($testddd99 != -1) {
	           substr($oneline,$testddd99,5)=$space2dash99;
	}

	#-----------------
	#
}
############################ END OF FOREACH LOOP [[ONELINE]]

close FILE;

print "\n\n ------------------------------------\n";
print " --Total number of lines processed:-- $ctrctrctr  \n";
print " ------------------------------------\n";
#
#


##################################################

###my $ddatafile = CHOMP($datafile);
my $ddatafile = $datafile;

###my $newfilename = $ddatafile.".txt";
my $newfilename = $ddatafile;

system("rm -rf ".$datafile);


open(OUT,">$newfilename")|| die("FAILURE-- Unable to open output file: $!\n");

foreach $oneline (@datafile_lines) {
	#
	print OUT "$oneline";
	#print "$oneline";

	#
}
############################ END OF FOREACH LOOP [[ONELINE]]

close OUT;

#
##------------------------------------
## rscat_wind_adjust_rscat_data.pl 
##------------------------------------
##

print "\n\n ------------------------------------\n";
print " END PERL SCRIPT: -rscat_wind_adjust_rscat_data.pl-  \n";
print " ------------------------------------\n";
#
#

system("date");


##########################################################################################################
####### UNIX VERSION!!!!!############################################
##########################################################################################################


END_OF_THE_PROGRAM:
#######################################################################
#
# END OF THE PROGRAM
#
#######################################################################
