#!/usr/bin/env python
import riftmobile
rc = riftmobile.RiftClient("us")
# Deepwood in this long list
shards = rc.listShards()
print shards[45].name
# First zone of Deepwood
zones = rc.listZones(1704)
print zones[0].name
