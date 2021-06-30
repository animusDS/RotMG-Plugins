using Lib_K_Relay.Networking;
using Lib_K_Relay.Utilities;

namespace TutorialMode
{
    public static class Extensions
    {
        public static void OryxMessage(this Client client, string fmt, params object[] args)
        {
            client.SendToClient(PluginUtils.CreateOryxNotification("Tutorial Mode", string.Format(fmt, args)));
        }
    }
}