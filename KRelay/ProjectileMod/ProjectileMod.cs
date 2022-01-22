using Lib_K_Relay;
using Lib_K_Relay.Interface;
using Lib_K_Relay.Networking;
using Lib_K_Relay.Networking.Packets;
using Lib_K_Relay.Networking.Packets.Client;
using Lib_K_Relay.Networking.Packets.DataObjects;
using Lib_K_Relay.Networking.Packets.Server;

namespace ProjectileMod
{
    public class ProjectileMode : IPlugin
    {
        public string GetAuthor()
        {
            return "Animus";
        }

        public string GetName()
        {
            return "Projectile Modifier";
        }

        public string GetDescription()
        {
            return "Modifies your projectile's life time and speed multiplier." + 
                   "\nThis means you are multiplying." +
                   "\nProjectile effects take place when you enter a new instance!";
        }

        public string[] GetCommands()
        {
            return new[]
            {
                "/projectilemod",
                "/projectilemod [on | off] - enable or disable the plugin",
                "/projectilemod [speedmult | lifemult] [on | off] - enable or disable the modifier",
                "/projectilemod [speedmult | lifemult] [amount] - set the value for the modifier",
                
                "\n Aliases:",
                "[pmod | pm]",
                "[smult | sm | speedmult]",
                "[lmult | lm | lifemult]"
                
            };
        }


        public void Initialize(Proxy proxy)
        {
            proxy.HookPacket(PacketType.PLAYERSHOOT, OnPlayerShoot);
            proxy.HookPacket(PacketType.UPDATE, OnUpdate);
            proxy.HookCommand("projectilemod", OnCommand);
            proxy.HookCommand("pmod", OnCommand);
            proxy.HookCommand("pm", OnCommand);
        }

        private void OnCommand(Client client, string command, string[] args)
        {
            if (args.Length == 0)
            {
                client.OryxMessage("Projectile Mod is {0}", Config.Default.Enabled ? "enabled" : "disabled");
                if (!Config.Default.Enabled) return;
                if (Config.Default.SpeedMultMod & Config.Default.LifeMultMod)
                    client.OryxMessage(
                        "You are currently modding Projectile Speed and Life by a value of {0}x and {1}x.",
                        Config.Default.SpeedMultCount, Config.Default.SpeedMultCount);
                else if (Config.Default.SpeedMultMod)
                    client.OryxMessage("You are currently modding Projectile Speed by a value of {0}x",
                        Config.Default.SpeedMultCount);
                else if (Config.Default.LifeMultMod)
                    client.OryxMessage("You are currently modding Projectile Life by a value of {0}x",
                        Config.Default.LifeMultCount);
            }
            else
            {
                switch (args[0])
                {
                    case "on":
                        Config.Default.Enabled = true;
                        Config.Default.Save();
                        client.OryxMessage("Projectile Modifier now enabled.");
                        break;

                    case "off":
                        Config.Default.Enabled = false;
                        Config.Default.Save();
                        client.OryxMessage("Projectile Modifier now disabled.");
                        break;

                    case "speedmult":
                    case "smult":
                    case "sm":
                        switch (args[1])
                        {
                            case "on":
                                Config.Default.SpeedMultMod = true;
                                Config.Default.Save();
                                client.OryxMessage("Speed modifier enabled.");
                                break;
                            case "off":
                                Config.Default.SpeedMultMod = false;
                                Config.Default.Save();
                                client.OryxMessage("Speed modifier disabled.");
                                break;
                            default:
                                if (double.TryParse(args[1], out var scount))
                                {
                                    if (scount < 0.001 || scount > 100)
                                    {
                                        client.OryxMessage("Number should be between 0.001 and 100.");
                                    }
                                    else
                                    {
                                        Config.Default.SpeedMultCount = scount;
                                        Config.Default.Save();
                                        client.OryxMessage("Speed Multiplier set to {0}x.", scount);
                                    }
                                }
                                else
                                {
                                    client.OryxMessage("Unrecognized argument: {0}", args[0]);
                                    client.OryxMessage("Usage:");
                                    client.OryxMessage("'/projectilemod speedmult [on | off]' - enable or disable speed modifier");
                                    client.OryxMessage("'/projectilemod speedmult [amount]' - set the value for the speed modifier");
                                }

                                break;
                        }

                        break;

                    case "lifemult":
                    case "lmult":
                    case "lm":
                        switch (args[1])
                        {
                            case "on":
                                Config.Default.LifeMultMod = true;
                                Config.Default.Save();
                                client.OryxMessage("Life Multiplier enabled.");
                                break;
                            case "off":
                                Config.Default.LifeMultMod = false;
                                Config.Default.Save();
                                client.OryxMessage("Life Multiplier disabled.");
                                break;
                            default:
                                if (double.TryParse(args[1], out var lcount))
                                {
                                    if (lcount < 0.001 || lcount > 100)
                                    {
                                        client.OryxMessage("Number should be between 0.001 and 100.");
                                    }
                                    else
                                    {
                                        Config.Default.LifeMultCount = lcount;
                                        Config.Default.Save();
                                        client.OryxMessage("Life modifier set to {0}x.", lcount);
                                    }
                                }
                                else
                                {
                                    client.OryxMessage("Unrecognized argument: {0}", args[0]);
                                    client.OryxMessage("Usage:");
                                    client.OryxMessage("'/projectilemod lifemult [on | off]' - enable or disable life time modifier");
                                    client.OryxMessage("'/projectilemod lifemult [amount]' - set the value for the life time modifier");
                                }

                                break;
                        }

                        break;

                    default:
                        client.OryxMessage("Usage:");
                        client.OryxMessage("'/projectilemod [on | off]' - enable or disable Projectile Mod");
                        client.OryxMessage("'/projectilemod [speedmult | lifemult] [on | off]' - enable Speed Mod");
                        client.OryxMessage("'/projectilemod [speedmult | lifemult] [amount]' - set the value for the modifier");
                        break;
                }
            }
        }

        private void OnPlayerShoot(Client client, Packet packet)
        {
            if (!Config.Default.Enabled) return;
            var shootPacket = (PlayerShootPacket) packet;
            shootPacket.LifeMultiplier = (short) (Config.Default.LifeMultCount * 1000);
            shootPacket.SpeedMultiplier = (short) (Config.Default.SpeedMultCount * 1000);
            client.SendToServer(shootPacket);
            shootPacket.Send = false;
        }

        private void OnUpdate(Client client, Packet packet)
        {
            if (!Config.Default.Enabled) return;
            var update = (UpdatePacket) packet;
            foreach (var en in update.NewObjs)
                if (en.Status.ObjectId == client.ObjectId)
                    foreach (var data in en.Status.Data)
                        switch (data.StatId)
                        {
                            case (int) Stats.ProjectileLifeMult:
                                data.IntValue = (int) (Config.Default.LifeMultCount * 1000);
                                break;
                            case (int) Stats.ProjectileSpeedMult:
                                data.IntValue = (int) (Config.Default.SpeedMultCount * 1000);
                                break;
                        }
        }
    }
}