using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Google.GData.Spreadsheets;
using Google.GData.Extensions;
using Google.Spreadsheets;
using Google.GData.Client;
using TurboHost.UtilityClasses;
using System.Drawing.Imaging;
using System.IO;
using MouseKeyboardActivityMonitor.Controls;
using System.Threading;
using System.Web;
using System.Net;
using System.Runtime.InteropServices;
using MouseKeyboardActivityMonitor;
using MouseKeyboardActivityMonitor.WinApi;

namespace TurboHost
{
    public partial class TurboHost : Form
    {
        [DllImport("user32.dll")]
        static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

        private bool SavedData { get; set; }
        private bool tPaused { get; set; }

        //User Info
        private string tUserName { get; set; }
        private string tPassword { get; set; }
        private string tFacebookId { get; set; }
        private string tFacebookPin { get; set; }
        private string tSheetName { get; set; }
        private string tWorksheetName { get; set; }

        //Bet Info
        private string tCurrentName1 { get; set; }
        private string tCurrentName2 { get; set; }
        private string tCurrentDate { get; set; }
        private int tImageCount { get; set; }
        private int tCurrentCommission { get; set; }
        private string tCurrentBet { get; set; }

        //File Info
        private string tDirectory { get; set; }
        private IniParser tParser;
        private FileIO tFileIO;
        private SpreadsheetsService tService { get; set; }
        private SpreadsheetEntry tDicingSpreadsheet { get; set; }
        private ListEntry tDicingWorksheet { get; set; }
        private WorksheetEntry tWorksheetEntry { get; set; }
        private ListFeed tWorksheetFeed { get; set; }
        private string tCurrentUrl { get; set; }

        //Forms
        public NewBet tBetScreen { get; set; }
        public TextReplacements tTextReplace { get; set; }
        public LoginSetup tLogin;

        //Global Info
        private int tBetScreenKey { get; set; }
        private int tScreenshotKey { get; set; }
        private int tSaveKey { get; set; }
        private bool tBuyinMode { get; set; }
        private int tCurrentAutotypeKey { get; set; }
        private string tTextboxContents { get; set; }
        private bool tUpdateText { get; set; }
        private Dictionary<int, string> tAutoTyperDictionary { get; set; }
        private Dictionary<string, string> tTextReplacementDictionary { get; set; }
        private KeyboardHookListener Listener { get; set; }

        //Net Bet Window Info
        private int tBetX { get; set; }
        private int tBetY { get; set; }

        Thread GetBalanceThread;
        Thread AutotypeThread;

        public TurboHost()
        {
            InitializeComponent();
            tImageCount = 0;
            tCurrentName1 = "";
            tCurrentName2 = "";
            tCurrentBet = "";
            tCurrentDate = "";
            tCurrentName1 = "";
            tCurrentName2 = "";
            tCurrentBet = "";
            label7.Text = "";
            label10.Text = "";

            tUserName = "";
            tPassword = "";
            tFacebookPin = "";
            tFacebookId = "";
            tSheetName = "";
            tWorksheetName = "";

            tTextboxContents = "";

            tBuyinMode = false;
        }

        private void TurboHost_Load(object sender, EventArgs e)
        {
            tAutoTyperDictionary = new Dictionary<int, string>();
            tFileIO = new FileIO();
            tParser = new IniParser(tFileIO.GetSettingsFilePath());
            tService = new SpreadsheetsService("TurboHost");
            tTextReplacementDictionary = new Dictionary<string, string>();

            tCurrentDate = GetFormattedDate();
            tDirectory = tFileIO.FolderPath;

            tBetX = 150;
            tBetY = 150;

            SavedData = CheckSettingsFile();
            if (SavedData == false)
            {
                this.Hide();
                tLogin = new LoginSetup();
                tLogin.FormClosed += new FormClosedEventHandler(tLogin_FormClosed);
                tLogin.TopMost = true;
                tLogin.ShowDialog();
            }
            else
            {
                Listener = new KeyboardHookListener(new GlobalHooker());
                Listener.Enabled = true;

                try
                {
                    HookManager.KeyPress += HookManager_KeyPress;
                }
                catch
                {
                    Console.WriteLine("error");
                }
                FinishLoading();
            }
        }

        void tLogin_FormClosed(object sender, FormClosedEventArgs e)
        {
            tParser = new IniParser(tFileIO.GetSettingsFilePath());
            tParser.AddSetting("UserSettings", "GmailAddress", tLogin.tGmailAddress);
            tParser.AddSetting("UserSettings", "GmailPassword", tLogin.tGmailPassword);
            tParser.AddSetting("UserSettings", "FacebookId", tLogin.tFacebookId);
            tParser.AddSetting("UserSettings", "FacebookPin", tLogin.tFacebookPIN);
            tParser.AddSetting("UserSettings", "SpreadsheetName", tLogin.tSpreadsheetName);
            tParser.SaveSettings();

            HookManager.KeyPress += new KeyPressEventHandler(HookManager_KeyPress);
            tUserName = tLogin.tGmailAddress;
            tPassword = tLogin.tGmailPassword;
            tFacebookId = tLogin.tFacebookId;
            tFacebookPin = tLogin.tFacebookPIN;
            tSheetName = tLogin.tSpreadsheetName;

            LoadComboBoxValues(comboBox1);
            LoadComboBoxValues(comboBox2);
            LoadComboBoxValues(comboBox3);
            try
            {
                tService.setUserCredentials(tUserName, tPassword);

                tDicingSpreadsheet = GetDicingSheet();
                tWorksheetEntry = GetWorksheet(tDicingSpreadsheet);
                tWorksheetFeed = GetWorksheetFeed(tWorksheetEntry);
            }
            catch {
                MessageBox.Show("There was an error logging you into Google or loading your spreadsheets. Check the info.", 
                    "Google Error", MessageBoxButtons.OK);
            }

            tTextReplacementDictionary.Add("{player1}", "");
            tTextReplacementDictionary.Add("{player2}", "");
            tTextReplacementDictionary.Add("{bet}", "");
            tTextReplacementDictionary.Add("{pot}", "");
            this.Show();
        }

        private void FinishLoading()
        {
            tUserName = GetGmailUserName();
            tPassword = GetGmailPassword();
            tFacebookId = GetFacebookId();
            tFacebookPin = GetFacebookPin();
            tSheetName = GetSpreadsheetName();
            tWorksheetName = GetWorksheetName();

            LoadComboBoxValues(comboBox1);
            LoadComboBoxValues(comboBox2);
            LoadComboBoxValues(comboBox3);

            try
            {
                this.tService.setUserCredentials(tUserName, tPassword);

                this.tDicingSpreadsheet = GetDicingSheet();
                this.tWorksheetEntry = GetWorksheet(tDicingSpreadsheet);
                this.tWorksheetFeed = GetWorksheetFeed(tWorksheetEntry);
            }
            catch
            {
                MessageBox.Show("There was an error logging you into Google or loading your spreadsheets. Check the info.",
                    "Google Error", MessageBoxButtons.OK);
            }

            tTextReplacementDictionary.Add("{player1}", "");
            tTextReplacementDictionary.Add("{player2}", "");
            tTextReplacementDictionary.Add("{bet}", "");
            tTextReplacementDictionary.Add("{pot}", "");
        }

        private void HookManager_KeyPress(object sender, KeyPressEventArgs e)
        {
            string tActiveWindowTitle = GetActiveWindowTitle();
            //int tValue = ReturnMatchedKeyCode(e.KeyValue.ToString());
            KeysConverter tConverter = new KeysConverter();
            string tKey = tConverter.ConvertToString(e.KeyChar);
            int tValue = ReturnMatchedKeyCode(tKey);

            if (tValue == tBetScreenKey)
            {
                e.Handled = true;
                HookManager.KeyPress -= new KeyPressEventHandler(HookManager_KeyPress);
                tBetScreen = new NewBet();
                tBetScreen.TopMost = true;
                tBetScreen.FormClosed += new FormClosedEventHandler(tBetScreen_FormClosed);
                tBetScreen.tX = tBetX;
                tBetScreen.tY = tBetY;
                tBetScreen.Show();
            }

            if (tValue == tScreenshotKey)
            {
                e.Handled = true;
                ScreenShot();
            }

            if (tValue == tSaveKey)
            {
                e.Handled = true;
                InsertRow(tCurrentName1, tCurrentName2, tCurrentBet, tWorksheetFeed);
                SubmitCommission();
            }

            if (tActiveWindowTitle.Contains("RuneScape"))
            {
                if (tAutoTyperDictionary.ContainsKey(tValue))
                {
                    e.Handled = true;
                    tCurrentAutotypeKey = tValue;
                    //if (AutotypeThread != null)
                    //{
                    //    AutotypeThread.Abort();
                    //}
                    //AutotypeThread = new Thread(new ThreadStart(AutoType));
                    //AutotypeThread.Start();
                    AutoType();
                }
            }
            if (tValue != tBetScreenKey && tValue != tScreenshotKey && tValue != tSaveKey)
                return;
            e.Handled = true;
            
        }

        private void AutoType()
        {
            int tCount = 0;
            string tLine = tAutoTyperDictionary[tCurrentAutotypeKey];
            foreach (string tKey in tTextReplacementDictionary.Keys)
            {
                tLine = tLine.Replace(tKey, tTextReplacementDictionary[tKey]);
            }
            Random tRandomGenerator = new Random();
            HookManager.KeyPress -= new KeyPressEventHandler(HookManager_KeyPress);
            while (tCount < tLine.Length)
            {
                SendKeys.Send(tLine[tCount].ToString());
                Thread.Sleep(tRandomGenerator.Next(10));
                tCount++;
            }
            HookManager.KeyPress += new KeyPressEventHandler(HookManager_KeyPress);
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.Checked == true)
                this.TopMost = true;
            else
                this.TopMost = false;
        }

        void tBetScreen_FormClosed(object sender, FormClosedEventArgs e)
        {
            if (tBetScreen.tPlayerOne != null && tBetScreen.tPlayerOne.Trim().Length > 0)
            {
                tCurrentName1 = tBetScreen.tPlayerOne;
                tTextReplacementDictionary["{player1}"] = tCurrentName1;
            }
            if (tBetScreen.tPlayerTwo != null && tBetScreen.tPlayerTwo.Trim().Length > 0)
            {
                tCurrentName2 = tBetScreen.tPlayerTwo;
                tTextReplacementDictionary["{player2}"] = tCurrentName2;
            }
            if (tBetScreen.tBet != null && tBetScreen.tBet.Trim().Length > 0)
            {
                tCurrentBet = tBetScreen.tBet;
                string tGp = GetReturnedGp(tCurrentBet);
                string tCommission = GetCommission(tCurrentBet);
                tTextReplacementDictionary["{bet}"] = tCurrentBet;
                tTextReplacementDictionary["{pot}"] = tGp;
                tCommission = IntToBet(tCommission);
                tGp = IntToBet(tGp);
                label7.Text = tCommission;
                label10.Text = tGp;
            }
            tBetX = tBetScreen.tX;
            tBetY = tBetScreen.tY;
            HookManager.KeyPress += new KeyPressEventHandler(HookManager_KeyPress);
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            tBetScreenKey = ReturnMatchedKeyCode(comboBox1.SelectedItem.ToString().ToLowerInvariant());
        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            tScreenshotKey = ReturnMatchedKeyCode(comboBox2.SelectedItem.ToString().ToLowerInvariant());
        }

        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {
            tSaveKey = ReturnMatchedKeyCode(comboBox3.SelectedItem.ToString().ToLowerInvariant());
        }

        private void label8_Click(object sender, EventArgs e)
        {
            if (!tPaused)
            {
                HookManager.KeyPress -= new KeyPressEventHandler(HookManager_KeyPress);
                label8.Text = "Resume";
                tPaused = true;
            }
            else
            {
                HookManager.KeyPress += new KeyPressEventHandler(HookManager_KeyPress);
                label8.Text = "Pause";
                tPaused = false;
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            ProcessAutotyper(textBox1.Text);
        }

        private void SubmitCommission(){

            string tBaseUrl = @"http://www.turbo-keys.com/facebook/process_commission.php?";
            tBaseUrl += "facebookid=" + System.Web.HttpUtility.UrlEncode(tFacebookId.ToString());
            tBaseUrl += "&pin=" + System.Web.HttpUtility.UrlEncode(tFacebookPin.ToString());
            tBaseUrl += "&wager=" + System.Web.HttpUtility.UrlEncode(tCurrentBet.ToString());
            tBaseUrl += "&player1=" + System.Web.HttpUtility.UrlEncode(tCurrentName1.ToString());
            tBaseUrl += "&player2=" + System.Web.HttpUtility.UrlEncode(tCurrentName2.ToString());
            tCurrentUrl = tBaseUrl;

            GetBalanceThread = new Thread(new ThreadStart(GetBalance));
            GetBalanceThread.Start();
        }

        private void GetBalance()
        {
            string pUrl = tCurrentUrl;
            Uri tUri = new Uri(pUrl);
            HttpWebRequest tRequest = (HttpWebRequest) HttpWebRequest.Create(tUri);
            WebResponse tResult = tRequest.GetResponse();
            Stream tStream = tResult.GetResponseStream();
            StreamReader tStreamReader = new StreamReader(tStream);
            string tContent = tStreamReader.ReadToEnd();

            tStreamReader.Close();
            tStream.Close();
            tResult.Close();
            try
            {
                float tCurrentBalance = float.Parse(tContent);

                if (tCurrentBalance <= 0)
                {
                    DialogResult tBoxResult = MessageBox.Show("Your balance is empty, please restock!", "No Balance", MessageBoxButtons.OK);
                    System.Windows.Forms.Application.Exit();
                }
            }
            catch { }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            HookManager.KeyPress -= new KeyPressEventHandler(HookManager_KeyPress);
            tTextReplace = new TextReplacements();
            tTextReplace.tTextboxContents = tTextboxContents;
            tTextReplace.FormClosed += new FormClosedEventHandler(tTextReplace_FormClosed);
            tTextReplace.TopMost = true;
            tTextReplace.Show();
        }

        void tTextReplace_FormClosed(object sender, FormClosedEventArgs e)
        {
            if (tTextReplace.tUpdateText)
            {
                tTextboxContents = tTextReplace.tTextboxContents;
                ProcessReplacements(tTextboxContents);
            }
            HookManager.KeyPress += new KeyPressEventHandler(HookManager_KeyPress);
        }

        private void checkBox2_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox2.Checked == true)
            {
                tBuyinMode = true;
            }
            else
            {
                tBuyinMode = false;
            }
        }
    }
}

