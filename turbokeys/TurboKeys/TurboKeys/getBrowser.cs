using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.Win32;

namespace TurboKeys
{
    class getBrowser
    {
        public static string GetDefaultBrowserPath()
        {
            string key = @"htmlfile\shell\open\command";
            RegistryKey registryKey =
            Registry.ClassesRoot.OpenSubKey(key, false);
            // get default browser path
            return ((string)registryKey.GetValue(null, null)).Split('"')[1];
        }
    }
}
