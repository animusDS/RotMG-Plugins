using Lib_K_Relay.Networking;
using Lib_K_Relay.Utilities;

namespace ProjectileMod
{
    internal static class Extensions
    {
        public static void OryxMessage(this Client client, string fmt, params object[] args)
        {
            client.SendToClient(PluginUtils.CreateOryxNotification("Projectile Mod", string.Format(fmt, args)));
        }
    }
}