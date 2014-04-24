using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net;
using System.IO;
using System.Diagnostics;

namespace TurboKeys
{
    public partial class UpdateCheck : Form
    {
        public bool checkSwitch { get; set; }

        public UpdateCheck()
        {
            InitializeComponent();
        }

        private void UpdateCheck_Load(object sender, EventArgs e)
        {
            this.Visible = false;
            checkSwitch = false;
            string url1 = @"http://www.turbo-keys.com/mousekeys_rs_update.php?version=25";
            HttpWebRequest WebRequestObject1 = (System.Net.HttpWebRequest)HttpWebRequest.Create(url1);
            WebResponse Response1 = WebRequestObject1.GetResponse();

            Stream WebStream1 = Response1.GetResponseStream();
            StreamReader Reader1 = new StreamReader(WebStream1);
            string urlContent1 = Reader1.ReadToEnd();

            Reader1.Close();
            WebStream1.Close();
            Response1.Close();

            if (urlContent1 == "0")
            {
                DialogResult result = MessageBox.Show("There's an update! \nGo to http://www.turbo-keys.com to download.", "Turbo-Keys is Updated!", MessageBoxButtons.OKCancel);
                //Application.Exit();
                if (result == System.Windows.Forms.DialogResult.OK)
                {
                    Process.Start(getBrowser.GetDefaultBrowserPath(), "http://www.turbo-keys.com/");
                    Application.Exit();
                }
                else if (result == System.Windows.Forms.DialogResult.Cancel)
                { Application.Exit(); }
                else
                { Application.Exit(); }
            }
            else if (urlContent1 == null)
            { Application.Exit(); }
            else if (urlContent1 == "1")
            {
                checkFunction();
            }
            else
            { Application.Exit(); }
            this.Close();
        }

        private void checkFunction()
        {
            checkSwitch = true;
        }

    }
}

