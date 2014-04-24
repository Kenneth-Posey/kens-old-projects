using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace TurboHost
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            UpdateCheck check = new UpdateCheck();
            Application.Run(check);

            if (check.checkSwitch == true)
            {
                TurboHost main = new TurboHost();
                Application.Run(main);
            }
            else
                Application.Exit();
        }
    }
}
