using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using TurboHost.UtilityClasses;

namespace TurboHost
{
    public partial class LoginSetup : Form
    {
        public string tGmailAddress { get; set; }
        public string tGmailPassword { get; set; }
        public string tFacebookId { get; set; }
        public string tFacebookPIN { get; set; }
        public string tSpreadsheetName { get; set; }
        IniParser tParser;
        private FileIO tFileIO;

        public LoginSetup()
        {
            InitializeComponent();
        }

        private void LoginSetup_Load(object sender, EventArgs e)
        {
            tFileIO = new FileIO();
            tGmailAddress = "";
            tGmailPassword = "";
            tFacebookId = "";
            tFacebookPIN = "";
            tSpreadsheetName = "";
        }

        private void label5_Click(object sender, EventArgs e)
        {
            tGmailAddress = textBox1.Text.Trim();
            tGmailPassword = textBox2.Text.Trim();
            tFacebookId = textBox3.Text.Trim();
            tFacebookPIN = textBox4.Text.Trim();
            tSpreadsheetName = textBox5.Text.Trim();

            if (tGmailAddress.Length > 0 && tGmailPassword.Length > 0 && tFacebookId.Length > 0 && tFacebookPIN.Length > 0 
                && tSpreadsheetName.Length > 0)
            {
                this.Close();
            }
            else
            {
                DialogResult tResult = MessageBox.Show("For obvious reasons all data is required. Please fill it out to continue.", "All data is required!", MessageBoxButtons.RetryCancel);
                if (tResult == DialogResult.Cancel)
                    Application.Exit();
                else if (tResult == DialogResult.Retry)
                    return;
                else
                    Application.Exit();
            }
        }

    }
}

