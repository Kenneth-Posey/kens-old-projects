using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using System.Net;
using System.IO;
using System.Diagnostics;

namespace TurboKeys
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
            Application.SetCompatibleTextRenderingDefault(true);

            UpdateCheck check = new UpdateCheck();
            Application.Run(check);

            if (check.checkSwitch == false)
            {
                //Login login = new Login();
                MainInterface main = new MainInterface();
                Application.Run(main);

                //Application.Run(login);

                //if (login.switches == true)
                //{
                //}
            }
            else
                Application.Exit();
        }
    }
}
