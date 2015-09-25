# Rift Mobile API
# License: MIT (see LICENSE)
import requests
#import json
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

class Character:
       def __init__(self, name, playerId, shard, guild=None):
                self.name = name
                self.playerId = playerId
                self.shard = shard
                self.guild = guild

class RiftClient:
        def __init__(self, dc):
                if dc != "us" and dc != "eu":
                        raise ValueError("Invalid DC specified")
                self.url = "http://chat-" + dc + ".riftgame.com:8080/chatservice"
                self.authurl = "https://auth.trionworlds.com/auth"
                self.loginurl = "https://chat-" + dc + ".riftgame.com/chatservice/loginByTicket?os=iOS&osVersion=5.100000&vendor=Apple"
                self.headers = { 'UserAgent': 'trion/mobile', 'Accept': 'application/json' }
                self.session = None

        def sendRequest(self, path, payload=None):
                """ Sends REST request to the API
                Uses a session if you have logged in

                Args:
                        path (string): string to append to the base API URL
                        payload (dict): parameters to append to the GET or POST request

                Returns:
                        The response from the API in JSON format
                """
                r = None
                if self.session != None:
                        r = self.session.post(self.url + path, params=payload, headers=self.headers)
                else:
                        r = requests.post(self.url + path, params=payload, headers=self.headers)

                if r.status_code != requests.codes.ok:
                        r.raise_for_status()

                return r.json

        def listShards(self):
                """ Lists all shards known to the mobile API.

                Returns:
                        A list of Shard objects
                """
                shards = self.sendRequest("/shard/list")
                return map(lambda shard: Shard(shard['name'], shard['shardId']), shards['data'])
                
        def listZones(self, shardId):
                """ Lists all zones known to the mobile API on a shard

                Args:
                        shardId (int): The shard's ID number

                Returns:
                        A list of Zone objects
                """
                zones = self.sendRequest("/zoneevent/list", { 'shardId': shardId })
                return map(lambda zone: Zone(zone['zone'], zone['zoneId'], zone.get('name'), zone.get('started')), zones['data'])

        def login(self, username, password):
                """ Logs in to the mobile API.
                Enables many more features

                Args:
                        username (string): The login userid
                        password (string): The login password
                Returns:
                        A status code indicating the result. 0 = success, other = the HTTP error code
                """
                self.session = requests.Session()
                r = self.session.post(self.authurl, params={'username': username, 'password': password, 'channel': 1}, headers=self.headers)
                if r.status_code != requests.codes.ok:
                        return r.status_code;

                r = self.session.post(self.loginurl, params={'ticket': r.text}, headers=self.headers)
                if r.status_code != requests.codes.ok:
                        return r.status_code
                return 0

        def listCharacters(self):
                """ Gets the list of characters on your account
                Must have logged in

                Returns:
                        a list of Character objects, or None if you have not logged in
                """
                if self.session == None:
                        return None
                characters = self.sendRequest("/chat/characters")
                return map(lambda character: Character(character['name'], character['playerId'], character['shardName'], character.get('guild')), characters['data'])
