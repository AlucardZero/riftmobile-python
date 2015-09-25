#!/usr/bin/env python
import riftmobile
import sys
import ConfigParser
rc = riftmobile.RiftClient("us")

# Print the 4th shard
shards = rc.listShards()
print shards[3].name
# First zone of Deepwood
zones = rc.listZones(1704)
print zones[0].name
# Find an event anywhere
stop = False
for shard in shards:
        zones = rc.listZones(shard.shardId)
        for zone in zones:
                if zone.event != None:
                        print shard.name, zone.name, zone.event, zone.started
                        stop = True
                        break
        if stop == True:
                break

# Start secured client
config = ConfigParser.RawConfigParser()
config.read('mobile.cfg')
res = rc.login(config.get('Rift','username'), config.get('Rift','password'))
if res != 0:
        print "error:", res
else:
        res = rc.listCharacters()
        # First character
        print res[0].name + "@" + res[0].shard
