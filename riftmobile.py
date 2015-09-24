# Rift Mobile API
import requests
import json
import sys

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
                return r.json

        def listShards(self):
                print self.sendRequest("/shard/list")
                
        def listZones(self, shardId):
                print self.sendRequest("/zoneevent/list", { 'shardId': shardId })
