using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Text;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;
using System.Net;
using System.IO;
using System.Threading;
using System.Runtime.InteropServices;
using System.Reflection;

namespace TurboKeys
{
    public partial class Login : Form
    {
        public bool switches { get; set; }

        public Login()
        {
            InitializeComponent();
        }

        private void Login_Load(object sender, EventArgs e)
        {
            textBox1.MaxLength = 15;
            textBox2.PasswordChar = '*';
            textBox2.MaxLength = 4;

            pictureBox1.Cursor = Cursors.Hand;

            ToolTip toolTip = new ToolTip();

            toolTip.AutoPopDelay = 10000;
            toolTip.InitialDelay = 500;
            toolTip.ReshowDelay = 500;
            toolTip.ShowAlways = true;

            toolTip.SetToolTip(pictureBox1, "Click to Log In");

            string inipath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\Turbo-Keys\";
            string userInfoLocation = inipath + @"user_info.ini";

            if (File.Exists(userInfoLocation))
            {
                IniParser parser = new IniParser(userInfoLocation);
                textBox1.Text = parser.GetSetting("user_info", "facebook_id");
                textBox2.Text = parser.GetSetting("user_info", "pin_number");
            }
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            switches = false;
            StringBuilder urlBuilder = new StringBuilder();
            urlBuilder.Append(@"http://www.turbo-keys.com/mousekeys.php?fbid=");
            urlBuilder.Append(textBox1.Text);
            urlBuilder.Append(@"&pin=");
            urlBuilder.Append(textBox2.Text);

            string url1 = urlBuilder.ToString();

            StringBuilder urlBuilder2 = new StringBuilder();
            urlBuilder2.Append(@"http://www.turbo-keys.com/mousekeys_check.php?fbid=");
            urlBuilder2.Append(textBox1.Text);
            urlBuilder2.Append(@"&pin=");
            urlBuilder2.Append(textBox2.Text);

            string url2 = urlBuilder2.ToString();

            HttpWebRequest WebRequestObject1 = (System.Net.HttpWebRequest)HttpWebRequest.Create(url1);

            WebRequestObject1.UserAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13";

            WebResponse Response1 = WebRequestObject1.GetResponse();
            Stream WebStream1 = Response1.GetResponseStream();
            StreamReader Reader1 = new StreamReader(WebStream1);
            string urlContent1 = Reader1.ReadToEnd();

            Reader1.Close();
            WebStream1.Close();
            Response1.Close();

            HttpWebRequest WebRequestObject2 = (System.Net.HttpWebRequest)HttpWebRequest.Create(url2);

            WebRequestObject2.UserAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13";

            WebResponse Response2 = WebRequestObject2.GetResponse();
            Stream WebStream2 = Response2.GetResponseStream();
            StreamReader Reader2 = new StreamReader(WebStream2);
            string urlContent2 = Reader2.ReadToEnd();

            Reader2.Close();
            WebStream2.Close();
            Response2.Close();

            if (urlContent1 == "0")
            {
                DialogResult result = MessageBox.Show("Your Account Balance is Empty.\nGo to http://apps.facebook.com/turbokeys-points/ to recharge", "Empty Account", MessageBoxButtons.YesNo);
                if (result == System.Windows.Forms.DialogResult.Yes)
                {
                    ProcessStartInfo sInfo = new ProcessStartInfo("http://apps.facebook.com/turbokeys-points");
                    Process.Start(sInfo);
                    Application.Exit();
                }
                else
                {
                    Application.Exit();
                }
            }
            else if (urlContent1 == "1")
            {
                DialogResult result = MessageBox.Show("There was a problem or mistake with your PIN or facebook ID. \nPlease update it at http://apps.facebook.com/turbokeys-points/", "ID or PIN Error", MessageBoxButtons.YesNo);
                if (result == System.Windows.Forms.DialogResult.Yes)
                {
                    ProcessStartInfo sInfo = new ProcessStartInfo("http://apps.facebook.com/turbokeys-points");
                    Process.Start(sInfo);
                    Application.Exit();
                }
                else
                {
                    Application.Exit();
                }
            }
            else if (urlContent1 != null)
            {
                long content1Length = urlContent1.Length;
                long content2Length = urlContent2.Length;

                long balanceCode1 = Convert.ToInt64(urlContent1.Substring(6));
                long balanceCode2 = Convert.ToInt64(urlContent2.Substring(6));

                long random1 = Convert.ToInt64(urlContent1.Remove(6));
                long random2 = Convert.ToInt64(urlContent2.Remove(6));

                long fbid = Convert.ToInt64(textBox1.Text);
                long pin = Convert.ToInt64(textBox2.Text);

                long fbidpin = fbid * pin;

                long modfbidpin1 = fbidpin % random1;
                long modfbidpin2 = fbidpin % random2;

                long balance1 = balanceCode1 / modfbidpin1;

                if (balanceCode2 == modfbidpin2)
                {
                    if (balanceCode2 > 0)
                    {
                        if (checkBox1.Checked == true)
                        {
                            string inipath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\Turbo-Keys\";
                            if (!File.Exists(inipath + "user_info.ini"))
                            {
                                System.IO.Directory.CreateDirectory(inipath);
                            }
                            string userInfoLocation = inipath + @"user_info.ini";

                            StreamWriter write = new StreamWriter(userInfoLocation);
                            write.Write("");
                            write.Flush();
                            write.Dispose();

                            IniParser parser = new IniParser(userInfoLocation);
                            parser.AddSetting("user_info", "facebook_id", textBox1.Text.ToString());
                            parser.AddSetting("user_info", "pin_number", textBox2.Text.ToString());

                            parser.SaveSettings();

                        }
                        switches = true;
                    }
                    this.Close();
                }
                else
                {
                    MessageBox.Show("There was an error contacting the server. Please try again later.");
                    Application.Exit();
                }
            }
            else
            {
                MessageBox.Show("There was an error contacting the server. Please try again later.");
                Application.Exit();
            }

        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            ProcessStartInfo sInfo = new ProcessStartInfo("http://apps.facebook.com/turbokeys-points");
            Process.Start(sInfo);
        }

        private void pictureBox1_Click_1(object sender, EventArgs e)
        {

        }

        private void linkLabel1_LinkClicked_1(object sender, LinkLabelLinkClickedEventArgs e)
        {
            ProcessStartInfo sInfo = new ProcessStartInfo("http://apps.facebook.com/turbokeys-points");
            Process.Start(sInfo);
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

        }


        
    }
}
