using Lib_K_Relay.Networking;
using Lib_K_Relay.Utilities;

namespace AbilitySpam
{
    internal static class Extensions
    {
        public static void OryxMessage(this Client client, string fmt, params object[] args)
        {
            client.SendToClient(PluginUtils.CreateOryxNotification("Auto Ability", string.Format(fmt, args)));
        }
    }
}