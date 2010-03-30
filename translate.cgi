#!/usr/bin/perl

# all external perl modules/files can be found at:
# - http://www.mackers.com/scripts/drunkifier/
# - http://www.mackers.com/scripts/other/
#
# you will also want to change all references to mackers.com to your server.
# sorry for not being neater!

$allowwww=0;

require "/home/mackers/www/alig/HTML/Absolute.pm";
require "drunkifier";

require "/home/mackers/cgi-lib.pl";
&ReadParse;

print "Content-type:text/html\n\n";

# remove/change the next line if you want to run this script on another server.
if ($ENV{'HTTP_HOST'}!~/mackers.com/) { print "Access denied from: $ENV{'HTTP_HOST'}\n"; exit 0; }

$_ = $in{'text'};
if ((/^((http)|(www))/) && ($allowwww || $in{'allowwww'})) {

$in{'text'} =~ s/(\n|\r)//g;
@html = &absolute($in{'text'});

foreach $line (@html) {
  unless ($line=~/(<.*?>)/s) {
    $line = &translate($line);
  } else {
    $line =~ s/((<frame.*?src=")|(href="))http/$1http:\/\/mackers.com\/dunkifier\/translate.cgi?text=http/gi;
  }
  print $line;
}

} else {

unless ($in{'text'}) {
$out = "Please enter plain text or web address" if ($string eq "");
$string = ""
} else {
$out = &translate($in{'text'}."\n");
print "<h1>Drunkifier Input</h1>\n";
print $in{'text'}."<br>\n";
print "<h1>Drunkifier Output</h1>\n";
print $out."<br>\n";
}

}

sub logthis {
$remote_addr = $ENV{'REMOTE_ADDR'};
$remote_addr =~ s/\;/\\\;/;
open (CMD, "nslookup $remote_addr |");
  while (<CMD>) {
    $ns = $_ if (/Name/);
  }
close (CMD);

$ns =~ s/(Name:)|( )|(\t)//g;
$ns =~ s/\n//g;

open (OUT,">>/home/mackers/www/drunkifier/log");
my $log = $_[0] . "\n\n";
$log =~ s/\r//g;
$log =~ s/\n\n/\n/g;
$time = gmtime;
print OUT "--- $time $ns ".$ENV{'HTTP_REFERER'}." ---\n";
print OUT $log;
close (OUT);
}
