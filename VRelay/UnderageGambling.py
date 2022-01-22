from os import name, remove
from tkinter.constants import FIRST, LAST
from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from valorlib.Packets.DataStructures import ObjectStatusData, WorldPosData
from valorlib.Packets.ConditionEffect import *
from client import Client

import re
import time
import random

''' This plugin is literally for trolling and nothing else. commands are listed in the player text hook on line 65 '''

class UnderageGambling(PluginInterface):

	hooks = {PacketTypes.Update, PacketTypes.PlayerText, PacketTypes.Hello, PacketTypes.Text}
	load = True
	defaultState = False

	pluginName = "Underage Gambling"
	debug = False
	target = None
	players = []
	spamCount = 1
	sleepCount = 0
	classTypes = [768, 775, 782, 784, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806,
					 807, 808, 22566, 22570, 24896, 21945, 26306, 26307]

	def getAuthor(self):
		return "Animus"

	# Clear our list when we change a map.
	def onHello(self, client: Client, packet: Hello, send: bool) -> (Hello, bool):
		self.players.clear()
		return (packet, send)

	# Stop spam command from sending to ourselves ourselves if spam count > 1
	def onText(self, Client: Client, packet: Text, send: bool) -> (Text, bool):
		if self.spamCount > 1 and packet.text[0:22] == "You have sent a gamble":
			send = False
		return (packet, send)

	# Track players that have joined and left the map
	def onUpdate(self, client: Client, packet: Update, send: bool) -> (Update, bool):
		# Add players that join
		for obj in packet.newObjects:
			for classType in self.classTypes:
				for s in obj.objectStatusData.stats:
					if obj.objectStatusData.objectID != client.objectID and obj.objectType == classType and s.statType == 31:
						self.players.append(obj)
						if self.debug:
							print("Added {} to list".format(s.strStatValue))

		# Remove players that have left
		for d in packet.drops:
			for p in self.players:
				if d == p.objectStatusData.objectID:
					self.players.remove(p)
					if self.debug:
						for s in p.objectStatusData.stats:
							if s.statType == 31:
								print("Removed {} from list".format(s.strStatValue))
		if self.debug:						
			print(len(self.players))
		return (packet, send)

	# Few commands for trolling :trollface:
	def onPlayerText(self, client: Client, packet: PlayerText, send: bool) -> (PlayerText, bool):
		if packet.text[0:7] == "/debug ":
			try:		
				if packet.text.split(" ")[-1] == "on":
					self.debug = True
				elif packet.text.split(" ")[-1] == "off":  
					self.debug = False
				client.createNotification(self.pluginName, "Set Debug Mode to {}".format(self.debug))
			except:
				client.createNotification(self.pluginName, "Incorrect syntax. Use '/test ON | OFF'.")
			send = False

		if packet.text[0:8] == "/target ":	
			self.target = packet.text.split(" ")[-1]
			client.createNotification(self.pluginName, "Set Targete to {}".format(self.target))
			send = False

		if packet.text[0:8] == "/scount ":	
			self.spamCount = int(packet.text.split(" ")[-1])
			client.createNotification(self.pluginName, "Set count to {}".format(self.spamCount))
			send = False	

		if packet.text[0:12] == "/sleepcount ":	
			self.sleepCount = float(packet.text.split(" ")[-1])
			client.createNotification(self.pluginName, "Set count to {}".format(self.sleepCount))
			send = False		

		if packet.text[0:8] == "/gamble ":
			g = RequestGamble()	
	
			if packet.text.split(" ")[1] == "spam":
				name = packet.text.split(" ")[-1]
				g.amount = 0
				if name == "all":
					for p in self.players:
						for s in p.objectStatusData.stats:
							if s.statType == 31:
								g.name = s.strStatValue
						for i in range(self.spamCount):
							client.SendPacketToServer(CreatePacket(g))	
							time.sleep(self.sleepCount)
					client.createNotification(self.pluginName, "Sent gamble request to {} players.".format(len(self.players)))	
				else:
					g.name = name
					for i in range(self.spamCount):
						client.SendPacketToServer(CreatePacket(g))
						time.sleep(self.sleepCount)
				client.createNotification(self.pluginName, "Sent gamble request to {} {} times!".format(name, i+1))

			elif packet.text.split(" ")[-1].isnumeric and int(packet.text.split(" ")[-1]) > 0:
				name = packet.text.split(" ")[1]
				amount = int(packet.text.split(" ")[-1])
				g.name = name
				g.amount = amount
				client.createNotification(self.pluginName, "Sent gamble request to {} for {}.".format(g.name, g.amount))
				client.SendPacketToServer(CreatePacket(g))

			send = False	

		return (packet, send)
