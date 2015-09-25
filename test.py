#!/usr/bin/env python
import riftmobile
import sys
import ConfigParser

#Invalid DC
run = False
try:
        rc = riftmobile.RiftClient("zz")
except ValueError as e:
        run = True

assert run, "Invalid DC test did not fail"

#Valid DC
rc = riftmobile.RiftClient("us")
assert rc != None
assert rc.authurl == "https://auth.trionworlds.com/auth"

# Print the 4th shard
shards = rc.listShards()
assert shards[3] == "Asphodel"

# First zone of Deepwood
zones = rc.listZones(1704)
assert zones[0].name == "Shimmersand"

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
