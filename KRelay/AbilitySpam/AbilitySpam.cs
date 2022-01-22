using Lib_K_Relay;
using Lib_K_Relay.Interface;
using Lib_K_Relay.Networking;
using Lib_K_Relay.Networking.Packets;
using Lib_K_Relay.Networking.Packets.Client;
using Lib_K_Relay.Utilities;

namespace AbilitySpam
{
    public class AbilitySpam : IPlugin
    {
        public string GetAuthor()
        {
            return "Animus";
        }

        public string GetName()
        {
            return "Ability Spam";
        }

        public string GetDescription()
        {
            return "Multiplies how many abilities you send" +
                   "\nYou will dc if you send over 20." +
                   "\nDoes not work on chargable items.";
        }

        public string[] GetCommands()
        {
            return new[]
            {
                "/abilityspam",
                "/abilityspam [amount] - set the number of packets sent.",
                "/abilityspam [on | off] - toggle ability spam on and off.",
                "/abilityspam safemode [on | off] - toggle Safe Mode on and off.",
            };
        }

        public void Initialize(Proxy proxy)
        {
            proxy.HookPacket(PacketType.USEITEM, OnUseItem);
            proxy.HookPacket(PacketType.MAPINFO, OnMap);
            proxy.HookCommand("abilityspam", OnCommand);
        }

        private void OnCommand(Client client, string command, string[] args)
        {
            if (args.Length == 0)
            {
                client.OryxMessage("Ability is {0}.", Config.Default.Enabled ? "enabled." : "disabled.");
                if (Config.Default.Enabled)
                    client.OryxMessage("You will send ability {0} packets.", (int) Config.Default.AbilityCount);
            }
            else
            {
                switch (args[0])
                {
                    case "on":
                        Config.Default.Enabled = true;
                        Config.Default.Save();
                        client.OryxMessage("Ability Spam now enabled.");
                        break;

                    case "off":
                        Config.Default.Enabled = false;
                        Config.Default.Save();
                        client.OryxMessage("Ability Spam now disabled.");
                        break;

                    case "safemode":
                        if (args[1] == "on")
                        {
                            Config.Default.SafeMode = true;
                            Config.Default.Save();
                            client.OryxMessage("Safe Mode enabled.");
                        }
                        else if (args[1] == "off")
                        {
                            Config.Default.SafeMode = false;
                            Config.Default.Save();
                            client.OryxMessage("Safe Mode disabled.");
                        }
                        else
                        {
                            client.OryxMessage("Unrecognized argument: {0}", args[0]);
                            client.OryxMessage("Usage:");
                            client.OryxMessage("'/abilityspam safemode [on | off]' - enable or disable safemode");
                        }

                        break;

                    default:
                        if (int.TryParse(args[0], out var count))
                        {
                            if (count > 10000 || count < 1)
                            {
                                client.OryxMessage("Number should be between 1 and 10000.");
                            }
                            else
                            {
                                Config.Default.AbilityCount = count;
                                Config.Default.Save();
                                client.OryxMessage("Ability Spam count set to {0}.", count);
                            }
                        }
                        else
                        {
                            client.OryxMessage("Unrecognized argument: {0}", args[0]);
                            client.OryxMessage("Usage:");
                            client.OryxMessage("'/abilityspam [on | off]' - enable or disable Ability Spam");
                            client.OryxMessage("'/abilityspam [amount]' - set the ability count");
                        }

                        break;
                }
            }
        }

        private int _timeCount;

        private void OnUseItem(Client client, Packet packet)
        {
            var useItem = (UseItemPacket) packet;
            if (!Config.Default.Enabled) return;
            if ((_timeCount * 500 >= 8000) & Config.Default.SafeMode)
            {
                client.SendToClient(
                    PluginUtils.CreateOryxNotification("Ability Spam", "Safe Mode is on! Sent normal amount."));
                return;
            }

            for (var index = 0; index < Config.Default.AbilityCount; ++index)
            {
                useItem.Time = client.Time + 500 * index;
                client.SendToServer(useItem);
                _timeCount++;
            }

            useItem.Send = false;
            client.SendToClient(PluginUtils.CreateOryxNotification("Ability Spam",
                "Sent " + Config.Default.AbilityCount + " Ability Packets"));
        }

        private void OnMap(Client client, Packet packet)
        {
            _timeCount = 0;
        }
    }
}