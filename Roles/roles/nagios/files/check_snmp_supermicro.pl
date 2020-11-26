#!/usr/bin/perl

# author: Patrick Zambelli <patrick.zambelli@wuerth-phoenix.com>
# license: GPL - http://www.fsf.org/licenses/gpl.txt
#
# =========================================================================== #
# Usage: $PROGNAME -H <host> -C <snmp_community> -t <test_name> [-n <ele-num>] [-w <low>:<high>] [-c <low>:<high>] [-o <timeout>] \n"; }
#

use strict;
require 5.6.0;
use lib qw( /opt/nagios/libexec );
use utils qw(%ERRORS $TIMEOUT &print_revision &support &usage);
use Net::SNMP;
use Getopt::Long;
use vars qw/$exit $message $opt_version $test_run $opt_timeout $opt_help $opt_command $opt_host $opt_community $opt_verbose
$opt_warning $opt_critical $opt_port $opt_mountpoint $snmp_session $PROGNAME $TIMEOUT $test_details $test_name $test_num/;

my %ERRORS=('OK'=>0,'WARNING'=>1,'CRITICAL'=>2,'UNKNOWN'=>3);
my %StatusOIDS=('fan1'=>1,'fan2'=>2,'fan3'=>3,'fan4'=>4,'fan5'=>5,'volt1'=>6,'volt2'=>7,'volt3'=>8,'volt4'=>9,'volt5'=>10,'volt6'=>11,'volt7'=>12,'temp1'=>13,'temp2'=>14,'temp3'=>15,'chass_intr'=>16);

$PROGNAME      = "check_snmp_HP_Bladesystem.pl";
$opt_verbose   = undef;
$opt_host      = undef;
$opt_community = 'public';
$opt_command   = undef;
$opt_warning   = undef;
$opt_critical  = undef;
$opt_port      = 161;
$message       = undef;
$exit          = 'OK';
$test_details  = undef;
$test_name     = undef;
$test_num      = 1;

my $oid_prefix = ".1.3.6.1.4.1."; #Enterprises
$oid_prefix .= "10876.2.1.1.1.1."; #Supermicro board

# =========================================================================== #
# =====> MAIN
# =========================================================================== #
process_options();

alarm( $TIMEOUT ); # make sure we don't hang Nagios

my $snmp_error;
($snmp_session,$snmp_error) = Net::SNMP->session(
		-version => 'snmpv2c',
		-hostname => $opt_host,
		-community => $opt_community,
		-port => $opt_port,
		);

  # Parse our the thresholds. and set the result
my ($ow_low,$ow_high,$oc_low,$oc_high) = parse_thres($opt_warning,$opt_critical);
#print("\n ow_low: ".$ow_low." ow_high: ".$ow_high." oc_low: ".$oc_low." oc_high: ".$oc_high."\n");

#?
#$|=1;

my ($res,$data_text, $unit)=('','');

#test procedure
if ( defined($test_run) ) { run_SNMP_test($snmp_session, $oid_prefix, %StatusOIDS); }

# =========================================================================== #
# =====> Temperatures
if($test_name =~ m/^temp1$/i){
	my $oid_label = "2.".$StatusOIDS{"temp1"};
	my $oid_data = "4.".$StatusOIDS{"temp1"};
	my ($data_systemp, $label_systemp);
	$unit = "C.";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);

}
elsif($test_name =~ m/^temp2$/i){
	my $oid_label = "2.".$StatusOIDS{"temp2"};
	my $oid_data = "4.".$StatusOIDS{"temp2"};
	my ($data_systemp, $label_systemp);
	$unit = "C.";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);

}
elsif($test_name =~ m/^temp3$/i){
	my $oid_label = "2.".$StatusOIDS{"temp3"};
	my $oid_data = "4.".$StatusOIDS{"temp3"};
	my ($data_systemp, $label_systemp);
	$unit = "C.";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);
}
# =========================================================================== #
# =====> Chassis
elsif($test_name =~ m/^chass-intr$/i){
	my $oid_label = "2.".$StatusOIDS{"chass_intr"};
	my $oid_data = "4.".$StatusOIDS{"chass_intr"};
	my ($data_cass, $label_cass);

	$data_cass = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_cass = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);
        if ($data_cass == 1 ){
          $res = $ERRORS{"CRITICAL"};
          $data_text .= $label_cass.": Intrusion detected.";
        }else{
          $res = $ERRORS{"OK"};
          $data_text .= $label_cass.": No intrusion detected.";
        }
}
# =========================================================================== #
# =====> Volts 
elsif($test_name =~ m/^volt1$/i){
	my $oid_label = "2.".$StatusOIDS{"volt1"};
	my $oid_data = "4.".$StatusOIDS{"volt1"};
	my ($data_cpuvolt, $label_cpuvolt);

	($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_cpuvolt, $label_cpuvolt, $unit, $res, $data_text);
}

elsif($test_name =~ m/^volt2$/i){
	my $oid_label = "2.".$StatusOIDS{"volt2"};
	my $oid_data = "4.".$StatusOIDS{"volt2"};
	my ($data_volt, $label_volt);

        ($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
}

elsif($test_name =~ m/^volt3$/i){
	my $oid_label = "2.".$StatusOIDS{"volt3"};
	my $oid_data = "4.".$StatusOIDS{"volt3"};
	my ($data_volt, $label_volt);

        ($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
}

elsif($test_name =~ m/^volt4$/i){
	my $oid_label = "2.".$StatusOIDS{"volt4"};
	my $oid_data = "4.".$StatusOIDS{"volt4"};
	my ($data_volt, $label_volt);

        ($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
}

elsif($test_name =~ m/^volt5$/i){
	my $oid_label = "2.".$StatusOIDS{"volt5"};
	my $oid_data = "4.".$StatusOIDS{"volt5"};
	my ($data_volt, $label_volt);

        ($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
}

elsif($test_name =~ m/^volt6$/i){
	my $oid_label = "2.".$StatusOIDS{"volt6"};
	my $oid_data = "4.".$StatusOIDS{"volt6"};
	my ($data_volt, $label_volt);

        ($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
}

elsif($test_name =~ m/^volt7$/i){
	my $oid_label = "2.".$StatusOIDS{"volt7"};
	my $oid_data = "4.".$StatusOIDS{"volt7"};
	my ($data_volt, $label_volt);

        ($res, $data_text) = measure_volts($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
}
# =========================================================================== #
# =====> Fans
elsif($test_name =~ m/^fan1$/i){
	my $oid_label = "2.".$StatusOIDS{"fan1"};
	my $oid_data = "4.".$StatusOIDS{"fan1"};
	my ($data_systemp, $label_systemp);
	$unit = "rpm";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);
}
elsif($test_name =~ m/^fan2$/i){
	my $oid_label = "2.".$StatusOIDS{"fan2"};
	my $oid_data = "4.".$StatusOIDS{"fan2"};
	my ($data_systemp, $label_systemp);
	$unit = "rpm";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);
}
elsif($test_name =~ m/^fan3$/i){
	my $oid_label = "2.".$StatusOIDS{"fan3"};
	my $oid_data = "4.".$StatusOIDS{"fan3"};
	my ($data_systemp, $label_systemp);
	$unit = "rpm";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);
}
elsif($test_name =~ m/^fan4$/i){
	my $oid_label = "2.".$StatusOIDS{"fan4"};
	my $oid_data = "4.".$StatusOIDS{"fan4"};
	my ($data_systemp, $label_systemp);
	$unit = "rpm";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);
}
elsif($test_name =~ m/^fan5$/i){
	my $oid_label = "2.".$StatusOIDS{"fan5"};
	my $oid_data = "4.".$StatusOIDS{"fan5"};
	my ($data_systemp, $label_systemp);
	$unit = "rpm";

	$data_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
	$label_systemp = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

        ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_systemp, $label_systemp, $unit, $res, $data_text);
}
#special check: checking multiple fans and applies limits to each giving worst result
elsif($test_name =~ m/^fan-speeds$/i){

    my @fans_label = ("2.".$StatusOIDS{"fan1"}, "2.".$StatusOIDS{"fan2"}, "2.".$StatusOIDS{"fan3"}, "2.".$StatusOIDS{"fan4"}, "2.".$StatusOIDS{"fan5"});
    my @fans_speed = ("4.".$StatusOIDS{"fan1"}, "4.".$StatusOIDS{"fan2"}, "4.".$StatusOIDS{"fan3"}, "4.".$StatusOIDS{"fan4"}, "4.".$StatusOIDS{"fan5"});

    #Check iterates all fan OIDs: error if one fan is on warning or critical
    my ($data_fan, $label_fan, $fan_result);
    $unit = "rpm";
    $data_text = " Summary: ";
    $res = $ERRORS{"OK"};

    #Iterate through all avalable and registered fans
    for (my $i = 0;$i<@fans_speed;$i++){
        $data_fan = SNMP_getvalue($snmp_session,$oid_prefix.$fans_speed[$i]);
        $label_fan = SNMP_getvalue($snmp_session,$oid_prefix.$fans_label[$i]);

        if (defined(int($data_fan))){
          if (!defined($label_fan)){
            $label_fan = "Fan ".$i;
          }
          #validate monitoring results following passed limits
          ($fan_result, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_fan, $label_fan, $unit, $fan_result, $data_text);

          #Bring highest fan result as final result
          if ($fan_result > $res) { $res = $fan_result; }

        } else {
          $data_text .= "Unable to retrieve SNMP data of fan ".$i."(UNKNOWN)";
          $res = $ERRORS{"UNKNOWN"};
        }
    }
}

#No matching test -t argument
else {
  print("Unknown test argument. \n\n");
  print_help();
  exit $ERRORS{"UNKNOWN"};
}



$snmp_session->close;
alarm( 0 ); # we're not going to hang after this.


my $res_desc = "OK";
#changed to match critial with passed value
$res_desc = "WARNING" if( $res == 1 );
$res_desc = "CRITICAL" if( $res == 2 );
$res_desc = "UNKNOWN" if( $res == 3 );

#print "$ow_low:$ow_high $oc_low:$oc_high\n";
print "$res_desc $data_text\n";
exit $res;


# =========================================================================== #
# =====> Sub-Routines
# =========================================================================== #

sub parse_thres{
	my ($opt_warning,$opt_critical)=@_;
	my ($ow_low,$ow_high) = ('','');
	if($opt_warning){
		if($opt_warning =~ m/^(\d*?):(\d*?)$/){ ($ow_low,$ow_high) = ($1,$2); }
		elsif($opt_warning =~ m/^\d+$/){ ($ow_low,$ow_high)=(-1,$opt_warning); }
		}
	my ($oc_low,$oc_high) = ('','');
	if($opt_critical){
		if($opt_critical =~ m/^(\d*?):(\d*?)$/){ ($oc_low,$oc_high) = ($1,$2); }
		elsif($opt_critical =~ m/^\d+$/){ ($oc_low,$oc_high)=(-1,$opt_critical); }
		}
        return(int($ow_low),int($ow_high),int($oc_low),int($oc_high));
	}

sub result_validation{
  my  ($oc_low, $oc_high, $ow_low, $ow_high, $data_fan, $label_fan, $unit, $result, $data_text)=@_;
  #Validate
  if (((int($oc_low) != 0)&&($data_fan < $oc_low))||((int($oc_high) != 0)&&($data_fan > $oc_high))) {
     $result = $ERRORS{"CRITICAL"};
     $data_text .= $label_fan.": ".$data_fan." ".$unit." (CRIT); ";
  } elsif (((int($ow_low) != 0)&&($data_fan < $ow_low))||((int($ow_high) != 0)&&($data_fan > $ow_high))) {
    $result = $ERRORS{"WARNING"};
    $data_text .= $label_fan.": ".$data_fan." ".$unit." (WARN); ";
  } else {
    $result = $ERRORS{"OK"};
    $data_text .= $label_fan.": ".$data_fan." ".$unit." (OK); ";
  }
  return $result, $data_text;
}

#method for volts checks
sub measure_volts{
  my ($snmp_session,$oid_prefix, $oid_data, $oid_label, $oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text)=@_;
  my $divisor = 1000;
  $unit = "V.";
  $data_volt = SNMP_getvalue($snmp_session,$oid_prefix.$oid_data);
  $label_volt = SNMP_getvalue($snmp_session,$oid_prefix.$oid_label);

  #provide values in decimal position
  $data_volt/=$divisor;
  if ($oc_low != 0) { $oc_low/=$divisor; }
  if ($oc_high != 0) { $oc_high/=$divisor; }
  if ($ow_low != 0) { $ow_low/=$divisor; }
  if ($ow_high != 0) { $ow_high/=$divisor; }
  ($res, $data_text) = result_validation($oc_low, $oc_high, $ow_low, $ow_high, $data_volt, $label_volt, $unit, $res, $data_text);
  return $res, $data_text;
}

# =========================================================================== #
# =====> Support methods
sub process_options {
	Getopt::Long::Configure( 'bundling' );
	GetOptions(
			'V'     => \$opt_version,       'version'     => \$opt_version,
			'v'     => \$opt_verbose,       'verbose'     => \$opt_verbose,
			'h'     => \$opt_help,          'help'        => \$opt_help,
			'H:s'   => \$opt_host,          'hostname:s'  => \$opt_host,
			'p:i'   => \$opt_port,          'port:i'      => \$opt_port,
			'C:s'   => \$opt_community,     'community:s' => \$opt_community,
			'c:s'   => \$opt_critical,          'critical:s'  => \$opt_critical,
			'w:s'   => \$opt_warning,          'warning:s'   => \$opt_warning,
			'o:i'   => \$TIMEOUT,           'timeout:i'   => \$TIMEOUT,
			't:s'	=> \$test_name,		'test:s'      => \$test_name,
			'n:i'	=> \$test_num,		'ele-number:i'      => \$test_num,
			'T'	=> \$test_run,		'test'      => \$test_run
		  );
	if ( defined($opt_version) ) { local_print_revision(); }
	if ( defined($opt_verbose) ) { $SNMP::debugging = 1; }
	if (((!defined($test_name)) || (!defined($opt_host)) || defined($opt_help)
		|| !defined($test_name)) && (!defined($test_run))) {
		
		print_help();
		exit $ERRORS{UNKNOWN};
		}
	}

sub local_print_revision { print_revision( $PROGNAME, '$Revision: 1.0 $ ' ); }

sub print_usage { print "Usage: $PROGNAME -H <host> -C <snmp_community> -t <test_name> [-n <ele-num>] [-w <low>:<high>] [-c <low>:<high>] [-o <timeout>] [-T] \n"; }

sub SNMP_getvalue{
	my ($snmp_session,$oid) = @_;

	my $res = $snmp_session->get_request(
			-varbindlist => [$oid]);

	if(!defined($res)){
		print "ERROR: ".$snmp_session->error."\n";
		exit;
		}
	
	return($res->{$oid});
	}

sub print_help {
	local_print_revision();
	print "Copyright (c) 2008 Patrick Zambelli <patrick.zambelli\@wuerth-phoenix.com> \n\n",
	      "SNMP HP Bladesystem plugin for Nagios\n\n";
	print_usage();
print <<EOT;
	-v, --verbose
		print extra debugging information
	-T, --test
                Perform a test of the current OID sources. Since various supermicro boards provide different oid sources this test scans all available values and provides information for the right check configuration.
	-h, --help
		print this help message
	-H, --hostname=HOST
		name or IP address of host to check
	-C, --community=COMMUNITY NAME
		community name for the host's SNMP agent
	-w, --warning=lower_limit:upper_limit
                define the lower:upper limit of waring level within status value as to stay.
                For voltage status the limits are given as integers in Volts*100 or Volts*1000 (only for +12V and -12V)
                i.e. -w 11600:12500 for 11,6V < x < 12,5V
	-c, --critical=lower_limit:upper_limit
		same as for warning, just for critical values
		-t, --test=TEST NAME
                fan1|fan2|fan3|fan4|fan5|system-temp|cpu-temp|chip-temp|chass-intr|volt_cpu|volt_12|volt_33|volt_15|volt_dimm|volt_5|volt_minus12

EOT
}

sub verbose (@) {
	return if ( !defined($opt_verbose) );
	print @_;
	}

sub run_SNMP_test() {
    my ($snmp_session, $oid_prefix, %StatusOIDS) = @_;
    print("Starting test run....\n");
    my ($oid_test_label, $oid_test_data, $test_run_label, $test_run_data);

    for my $key ( sort (keys %StatusOIDS )) {
      $oid_test_label= $oid_prefix."2.".$StatusOIDS{$key};
      $oid_test_data= $oid_prefix."4.".$StatusOIDS{$key};

      $test_run_label = $snmp_session->get_request(-varbindlist => [$oid_test_label]);
      $test_run_label = ($test_run_label->{$oid_test_label});
      $test_run_data = $snmp_session->get_request(-varbindlist => [$oid_test_data]);
      $test_run_data = ($test_run_data->{$oid_test_data});

      if (defined($test_run_data)){
        print("Status test: \"".$key."\" provides info about: \"".$test_run_label."\" having now value: ".$test_run_data." at OID: ".$oid_test_data."\n");
      } else {
        print ("ERROR: No value at OID: ".$oid_test_data." \nExit now....\n");
        exit 3;
      }
    }
    print("Test run terminated with success!\n");
    exit 0;
}