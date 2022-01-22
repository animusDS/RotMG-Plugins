
from mimetypes import init
from Plugins.AutoNexus import AutoNexus
from Plugins.DamageBoost import DamageBoost
from Plugins.Godmode import Godmode
from Plugins.NoDebuff import NoDebuff
from Plugins.NoProjectile import NoProjectile
from Plugins.Panic import Panic
from Plugins.PluginInterface import PluginInterface
from Plugins.Speedy import Speedy
from Plugins.Swiftness import Swiftness
from Plugins.TQ import TQ
from valorlib.Packets.Packet import *
from client import Client

class CommandHandler(PluginInterface):

    hooks = {PacketTypes.PlayerText}
    load = True  # true because why wouldn't you want to activate this
    defaultState = True

    # add your own plugins / remove the ones you don't have
    plugins = {"an": AutoNexus, "db": DamageBoost, "gm": Godmode, "nb": NoDebuff,
               "np": NoProjectile, "pn": Panic, "sp": Speedy, "sw": Swiftness, "tq": TQ}

    def getAuthor(self) -> str:
        return "animus"

    def onPlayerText(self, client: Client, packet: PlayerText, send: bool) -> (PlayerText, bool):
        if packet.text[0:3] == "/p " and packet.text[3:5] in self.plugins:
            p = self.plugins[packet.text[3:5]]
            plugin = client.pluginManager.findClass(p.__name__)
            if client.pluginManager.plugins[plugin]:
                if p.__name__ == Swiftness.__name__ or Speedy.__name__:
                    client.disableSwiftness = True
                    client.disableSpeedy = True
                client.pluginManager.plugins[plugin] = False
            else:
                if p.__name__ == Swiftness.__name__ or Speedy.__name__:
                    client.disableSwiftness = False
                    client.disableSpeedy = False
                client.pluginManager.plugins[plugin] = True
            client.createNotification(
                "CommandHandler", "Set to {}".format(client.pluginManager.plugins[plugin]))
            send = False
        elif packet.text[0:1] == "/help":
            client.createNotification(
                "CommandHandler", "Use the following command '/p an' (AutoNexus), '/p db' (DamageBoost), '/p gm' (GodMode), '/p nb' (NoDebuff), '/p np' (NoProjectile), '/p pn' (Panic), '/p sp' (Speedy), '/p sw' (Swiftness),")
            send = False
        return (packet, send)
