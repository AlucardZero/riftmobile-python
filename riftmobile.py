# Rift Mobile API
import requests
import json
import sys

class Shard:
        def __init__(self, name, shardId):
                self.name = name
                self.shardId = shardId

class Zone:
        def __init__(self, name, zoneId, event=None, started=None):
                self.name = name
                self.zoneId = zoneId
                self.started = started
                self.event = event

class RiftClient:
        def __init__(self, dc):
                if dc != "us" and dc != "eu":
                        sys.exit("Invalid DC\n");
                self.url = "http://chat-" + dc + ".riftgame.com:8080/chatservice"
                self.headers = { 'UserAgent': 'trion/mobile', 'Accept': 'application/json' }

        def sendRequest(self, path, payload=None):
                r = requests.get(self.url + path, params=payload, headers=self.headers)
                if r.status_code != requests.codes.ok:
                        r.raise_for_status()

                return r.json['data']

        def listShards(self):
                shards = self.sendRequest("/shard/list")
                return map(lambda shard: Shard(shard['name'], shard['shardId']), shards)
                
        def listZones(self, shardId):
                zones = self.sendRequest("/zoneevent/list", { 'shardId': shardId })
                return map(lambda zone: Zone(zone['zone'], zone['zoneId']), zones)
