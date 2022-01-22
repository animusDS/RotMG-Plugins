using Lib_K_Relay;
using Lib_K_Relay.Interface;
using Lib_K_Relay.Networking;
using Lib_K_Relay.Networking.Packets;
using Lib_K_Relay.Networking.Packets.Client;
using Lib_K_Relay.Networking.Packets.Server;

namespace TutorialMode
{
    public class TutorialMode : IPlugin
    {
        public string GetAuthor()
        {
            return "Animus";
        }

        public string GetName()
        {
            return "Tutorial Mode";
        }

        public string GetDescription()
        {
            return "Enables Tutorial Mode." +
                   "\nAllows you to connect only to tutorial." +
                   "\nUseful for avoiding nexus / Realmeye";
        }

        public string[] GetCommands()
        {
            return new[]
            {
                "/tutorialmode [on | off] - enables or disables tutorial mode"
            };
        }

        public void Initialize(Proxy proxy)
        {
            proxy.HookPacket(PacketType.RECONNECT, OnReconnect);
            proxy.HookPacket(PacketType.HELLO, OnHello);
            proxy.HookCommand("tutorialmode", OnCommand);
        }

        private void OnCommand(Client client, string command, string[] args)
        {
            if (args.Length == 0)
            {
                client.OryxMessage("Tutorial Mode is {0}.", Config.Default.Enabled ? "enabled" : "disabled");
            }
            else
            {
                switch (args[0])
                {
                    case "on":
                        Config.Default.Enabled = true;
                        Config.Default.Save();
                        client.OryxMessage("Tutorial Mode is now enabled");
                        break;

                    case "off":
                        Config.Default.Enabled = false;
                        Config.Default.Save();
                        client.OryxMessage("Tutorial Mode is now disabled");
                        break;
                }
            }
        }

        private void OnReconnect(Client client, Packet packet)
        {
            if (!Config.Default.Enabled) return;
            var reconnect = (ReconnectPacket) packet;
            reconnect.GameId = -1;
        }

        private void OnHello(Client client, Packet packet)
        {
            if (!Config.Default.Enabled) return;
            var hello = (HelloPacket) packet;
            hello.GameId = -1;
        }
    }
}