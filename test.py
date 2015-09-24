#!/usr/bin/env python
import riftmobile
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
