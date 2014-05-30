#! /usr/bin/python
import sys

if ( len(sys.argv) < 6 ) :
  print "Usage : Enter client log and relay log, start time, end time and percentile \n";
  exit;

client_log = sys.argv[ 1 ];
relay_log  = sys.argv[ 2 ];
start_time = int(sys.argv[ 3 ])*1000000;
end_time   = int(sys.argv[ 4 ])*1000000;
percentile = int(sys.argv[ 5 ]);

uplink_arrivals = dict()
uplink_departures = dict()
downlink_arrivals = dict()
downlink_departures = dict()
pkt_sizes=dict();

fh_client = open( client_log, "r" );
for line in fh_client.readlines():
  line.strip();
  records=line.split()
  if ( len(records) == 11 ) :
    action = records[ 2 ];
    hash_str = records[ 10 ];
    ts = int(records[ 4 ].split(",")[0]);
    size = int( records[ 7 ]);
    if ( ( ts < start_time ) or ( ts > end_time ) ) :
      continue;
    elif ( action == "RECEIVED" ):
      # Receive packet at client, will be forwarded out by relay
      uplink_arrivals[ hash_str ] = int(records[4].split(",")[0]);
    elif ( action == "SENT" ):
      # Downlink departure for packet that arrived from relay
      downlink_departures[ hash_str ] = int(records[4].split(",")[0]);
      pkt_sizes[ hash_str ] = size;

fh_relay = open( relay_log, "r" );
for line in fh_relay.readlines():
  line.strip();
  records=line.split()
  if ( len(records) == 11 ) :
    action = records[ 2 ];
    hash_str = records[10];
    ts = int(records[ 4 ].split(",")[0]);
    size = int( records[ 7 ]);
    if ( ( ts < start_time ) or ( ts > end_time ) ) :
      continue;
    elif ( action == "RECEIVED" ):
      # Receive packet at relay, will be forwarded out by client
      downlink_arrivals[ hash_str ] = int(records[4].split(",")[0]);
    elif ( action == "SENT" ):
      # Uplink departure for packet that arrived from client
      uplink_departures[ hash_str ] = int(records[4].split(",")[0]);
      pkt_sizes[ hash_str ] = size;

# print uplink departures :
uplink_delays=[]
uplink_bytes=0
for hash_str in uplink_departures :
  if ( hash_str not in uplink_arrivals ) :
    print "Did not see ", hash_str, "arriving on uplink "
  else :
    print hash_str,"UPLINK  ",(uplink_departures[ hash_str ] - uplink_arrivals[ hash_str ])/1000.0," ms ",pkt_sizes[ hash_str ]," bytes ";
    delay =  (uplink_departures[ hash_str ] - uplink_arrivals[ hash_str ])/1000.0
    assert( delay > 0 );
    uplink_delays += [ delay ];
    uplink_bytes += pkt_sizes[ hash_str ]

# print downlink departures :
downlink_delays=[]
downlink_bytes=0
for hash_str in downlink_departures :
  if ( hash_str not in downlink_arrivals ) :
    print "Did not see ",hash_str, "arriving on downlink "
  else :
    print hash_str,"DOWNLINK  ",(downlink_departures[ hash_str ] - downlink_arrivals[ hash_str ])/1000.0," ms ",pkt_sizes[ hash_str ]," bytes ";
    delay = (downlink_departures[ hash_str ] - downlink_arrivals[ hash_str ])/1000.0
    assert( delay > 0 );
    downlink_delays += [ delay  ];
    downlink_bytes += pkt_sizes[ hash_str ]

uplink_delays.sort()
downlink_delays.sort()

print>>sys.stderr, percentile,"th percentile DOWNLINK ", downlink_delays [ int( (percentile/100.0) * len( downlink_delays ) ) ], "ms"
print>>sys.stderr," Downlink datarate ", (downlink_bytes*1000.0)/ (end_time-start_time ), " KB per second "
