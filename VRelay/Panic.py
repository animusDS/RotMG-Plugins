from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from valorlib.Packets.DataStructures import WorldPosData
from ConditionEffect import *
from client import Client

import re
import time
import random


class Panic(PluginInterface):

	hooks = {PacketTypes.PlayerText, PacketTypes.Update, PacketTypes.Hello}
	load = True
	defaultState = True

	unsafeDungeons = ['Garden of Chaos', 'Crypt of the Illusionist', 'Trial of the Illusionist']

	# All valor class ID's
	classTypes = [768, 775, 782, 784, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806,
					 807, 808, 22566, 22570, 24896, 21945, 26306, 26307]
	panicMode = False
	createNotif = False

	def getAuthor(self):
		return "animus"

	def onHello(self, client: Client, packet: Hello, send: bool) -> (Hello, bool):
		if self.createNotif == True:
			client.createNotification("Panic Mode", "Nexused due to player joining you in an unsafe dungeon. Be more carful next time!")
			self.createNotif = False
		return (packet, send)

	def onUpdate(self, client: Client, packet: Update, send: bool) -> (Update, bool):
		for obj in packet.newObjects:
			if obj.objectStatusData.objectID != client.objectID:
				for classType in self.classTypes:
					if obj.objectType == classType:
						for map in self.unsafeDungeons:
							if self.panicMode == True and client.currentMap == map:
								client.SendPacketToServer(CreatePacket(Escape()))
								self.createNotif = True
		return (packet, send)

	def onPlayerText(self, client: Client, packet: PlayerText, send: bool) -> (PlayerText, bool):
		if packet.text[0:7] == "/panic ":
			try:		
				if packet.text.split(" ")[-1] == "on":
					self.panicMode = True
				elif packet.text.split(" ")[-1] == "off":  
					self.panicMode = False
				client.createNotification("Panic Mode", "Set Panic Mode to {}".format(self.panicMode))
			except:
				client.createNotification("Panic Mode", "Incorrect syntax. Use '/panic ON | OFF'.")
			send = False
		return (packet, send)
