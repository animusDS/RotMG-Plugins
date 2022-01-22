from socket import create_connection
from typing import _SpecialForm
from .PluginInterface import PluginInterface
from valorlib.Packets.Packet import *
from valorlib.Packets.DataStructures import ObjectData, WorldPosData
from client import Client, ObjectInfo

import re
import time
import random

class TQ(PluginInterface):
    
	hooks = {PacketTypes.PlayerText, PacketTypes.Update, PacketTypes.GotoAck, PacketTypes.UseItem}
	load = True
	defaultState = True

	teleporting = False
	listenToAbility = False
	questPosition = WorldPosData()
	noAck = False
	tpPlayer = False
	players = []
	classTypes = [768, 775, 782, 784, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806,
					 807, 808, 22566, 22570, 24896, 21945, 26306, 26307]

	# Worlds
	gardenFirst = False
	gardenSecond = False

	illuFirst = False
	illuSecond = False
	illuThird = False

	shattersFirst = False
	shattersSecond = False
	shattersThird = False

	rift = False

	def getAuthor(self):
		return "Animus"

	def onUpdate(self, client: Client, packet: Update, send: bool) -> (Update, bool):
		# Never always accurate 
		if client.latestQuest != None:
			try:
				self.questPosition = client.newObjects[client.latestQuest].pos
			except:
				print('TeleportTools: Error, no quest avalible...')
				# Add players that join
		for obj in packet.newObjects:
			for classType in self.classTypes:
				for s in obj.objectStatusData.stats:
					if obj.objectStatusData.objectID != client.objectID and obj.objectType == classType and s.statType == 31:
						self.players.append(obj)

		# Remove players that have left
		for d in packet.drops:
			for p in self.players:
				if d == p.objectStatusData.objectID:
					self.players.remove(p)
		return (packet, send)
	
	def onGotoAck(self, client: Client, packet: GotoAck, send: bool) -> (GotoAck, bool):
		if self.teleporting == True:
			if self.noAck == True:
				self.teleporting = False
				self.noAck = False
				return (packet, False)

			time.sleep(0.1)
			g = Goto()
			g.objectID = client.objectID

			pos = WorldPosData()

			# Garden
			if self.gardenFirst == True:
				pos.x = 406
				pos.y = 248
				g.pos = pos
				self.gardenFirst = False

			elif self.gardenSecond == True:
				pos.x = 406
				pos.y = 325
				g.pos = pos
				self.gardenSecond = False

			# Illu
			elif self.illuFirst == True:
				pos.x = 25
				pos.y = 40
				g.pos = pos
				self.illuFirst = False

			elif self.illuSecond == True:
				pos.x = 130
				pos.y = 20
				g.pos = pos
				self.illuSecond = False

			elif self.illuThird == True:
				pos.x = 180
				pos.y = 116
				g.pos = pos
				self.illuThird = False	

			# Shatters
			elif self.shattersFirst == True:
				pos.x = 205
				pos.y = 200
				g.pos = pos
				self.shattersFirst = False
				
			elif self.shattersSecond == True:
				pos.x = 390
				pos.y = 200
				g.pos = pos
				self.shattersSecond = False	

			elif self.shattersThird == True:
				pos.x = 386
				pos.y = 21
				g.pos = pos
				self.shattersThird = False	

			# Rift
			elif self.rift == True:
				pos.x = 19
				pos.y = 93
				g.pos = pos
				self.rift = False			
			else:
				g.pos = self.questPosition
			client.SendPacketToClient(CreatePacket(g))
			self.noAck = True

		return (packet, send)

	def onUseItem(self, client: Client, packet: UseItem, send: bool) -> (UseItem, bool):
		if self.listenToAbility == True:
			packet.itemUsePos = client.currentpos
			self.listenToAbility = False
			self.teleporting = True
			client.createNotification("TeleportTools", "Teleporting..")

		return (packet, send)	

	def onPlayerText(self, client: Client, packet: PlayerText, send: bool) -> (PlayerText, bool):
		if packet.text.lower() == "/tq":
			if client.latestQuest != None:
				self.listenToAbility = True
				client.createNotification("TeleportTools", "Teleport to quest by using your ability")
			else:
				client.createNotification("TeleportTools", "No quest registered")
			send = False
		
		# Garden
		elif packet.text.lower() == "/garden 1":
			if client.currentMap == "Garden of Chaos":
				self.listenToAbility = True
				self.gardenFirst = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")
			else:
				client.createNotification("TeleportTools", "You can only use this command in a Garden of Chaos!")		
			send = False

		elif packet.text.lower() == "/garden 2":
			if client.currentMap == "Garden of Chaos":
				self.listenToAbility = True
				self.gardenSecond = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")
			else:
				client.createNotification("TeleportTools", "You can only use this command in a Garden of Chaos!")			
			send = False
	
		# Illu
		elif packet.text.lower() == "/illu 1":
			if client.currentMap == "Crypt of the Illusionist":
				self.listenToAbility = True
				self.illuFirst = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")
			else:
				client.createNotification("TeleportTools", "You can only use this command in a Crypt of the Illusionist")
			send = False	

		elif packet.text.lower() == "/illu 2":
			if client.currentMap == "Crypt of the Illusionist":
				self.listenToAbility = True
				self.illuSecond = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")
			else:
				client.createNotification("TeleportTools", "You can only use this command in a Crypt of the Illusionist")	
			send = False			

		elif packet.text.lower() == "/illu 3":
			if client.currentMap == "Crypt of the Illusionist":
				self.listenToAbility = True
				self.illuThird = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")	
			else:
				client.createNotification("TeleportTools", "You can only use this command in a Crypt of the Illusionist")	
			send = False

		# Shatters
		elif packet.text.lower() == "/shatters 1":
			if client.currentMap == "The Shatters":
				self.listenToAbility = True
				self.shattersFirst = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")	
			else:
				client.createNotification("TeleportTools", "You can only use this command in The Shatters")	
			send = False

		elif packet.text.lower() == "/shatters 2":
			if client.currentMap == "The Shatters":
				self.listenToAbility = True
				self.shattersSecond = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")		
			else:
				client.createNotification("TeleportTools", "You can only use this command in The Shatters")	
			send = False

		elif packet.text.lower() == "/shatters 3":
			if client.currentMap == "The Shatters":
				self.listenToAbility = True
				self.shattersThird = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")		
			else:
				client.createNotification("TeleportTools", "You can only use this command in The Shatters")	
			send = False		

		# Rift
		elif packet.text.lower() == "/rift":
			if client.currentMap == "Ascended Rift":
				self.listenToAbility = True
				self.rift = True
				client.createNotification("TeleportTools", "Teleport to position by using your ability")	
			else:
				client.createNotification("TeleportTools", "You can only use this command in an Ascended Rift")	
			send = False												
		
		return (packet, send)
