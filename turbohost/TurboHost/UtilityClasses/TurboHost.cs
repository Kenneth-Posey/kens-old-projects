using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using TurboHost.UtilityClasses;
using System.Drawing.Imaging;
using Google.GData.Spreadsheets;
using Google.GData.Client;
using System.Text.RegularExpressions;

namespace TurboHost
{
    public partial class TurboHost : Form
    {
        private string GetFormattedDate()
        {
            return DateTime.Today.Day + "-" + DateTime.Today.Month + "-" + DateTime.Now.Year;
        }

        private void CheckScreenshotDirectory()
        {
            bool tDirectoryExists = Directory.Exists(tDirectory);
            if (!tDirectoryExists)
                Directory.CreateDirectory(tDirectory);
        }

        private bool ScreenShot()
        {
            bool tSuccessful;
            string tFileName = tCurrentName1 + "-" + tCurrentName2 + "-" +
                                tCurrentBet + "-" + GetFormattedDate() + "-" + tImageCount.ToString() + ".png";
            tFileName = tDirectory + tFileName;
            try
            {
                ScreenCapture tScreenCapture = new ScreenCapture();
                tScreenCapture.CaptureScreenToFile(tFileName, ImageFormat.Png);
                tImageCount++;
                return tSuccessful = true;
            }
            catch
            {
                return tSuccessful = false;
            }
        }

        private string GetWorksheetName()
        {
            if (tWorksheetName == null || tWorksheetName.Length == 0)
            {
                tWorksheetName = tParser.GetSetting("UserSettings", "Spreadsheet");   
            }

            if (tWorksheetName == null || tWorksheetName.Length == 0)
            {
                tWorksheetName = "Smokin Dices";
            }
            
            return tWorksheetName;
        }

        private string GetGmailUserName()
        {
            if (tUserName.Length == 0 || tUserName == null)
                tUserName = tParser.GetSetting("UserSettings", "GmailAddress");
            return tUserName;
        }

        private string GetGmailPassword()
        {
            if (tPassword.Length == 0 || tPassword == null)
                tPassword = tParser.GetSetting("UserSettings", "GmailPassword");
            return tPassword;
        }

        private string GetFacebookId()
        {
            if (tFacebookId.Length == 0 || tFacebookId == null)
                tFacebookId = tParser.GetSetting("UserSettings", "FacebookId");
            return tFacebookId;

        }

        private string GetFacebookPin()
        {
            if (tFacebookPin.Length == 0 || tFacebookPin == null)
                tFacebookPin = tParser.GetSetting("UserSettings", "FacebookPin");
            return tFacebookPin;

        }

        private string GetSpreadsheetName()
        {
            if (tSheetName.Length == 0 || tSheetName == null)
                tSheetName = tParser.GetSetting("UserSettings", "SpreadsheetName");
            return tSheetName;
        }

        private SpreadsheetEntry GetDicingSheet()
        {
            SpreadsheetQuery tSpreadsheetQuery = new SpreadsheetQuery();
            SpreadsheetFeed tSpreadsheetFeed = tService.Query(tSpreadsheetQuery);

            foreach (SpreadsheetEntry tEntry in tSpreadsheetFeed.Entries)
            {
                if (tEntry.Title.Text == tWorksheetName)
                    return tEntry;
            }
            return new SpreadsheetEntry();
        }

        private WorksheetEntry GetWorksheet(SpreadsheetEntry pSpreadsheetEntry)
        {
            AtomLink link = tDicingSpreadsheet.Links.FindService(GDataSpreadsheetsNameTable.WorksheetRel, null);
            string tLink = link.HRef.ToString();

            WorksheetQuery tWorksheetQuery = new WorksheetQuery(tLink);
            tWorksheetQuery.Title = tSheetName;

            WorksheetFeed wfeed = tService.Query(tWorksheetQuery);
            WorksheetEntry wentry = wfeed.Entries.FirstOrDefault() as WorksheetEntry;
            return wentry;

        }

        private ListFeed GetWorksheetFeed(WorksheetEntry pWorksheetEntry)
        {
            AtomLink wListFeedLink = pWorksheetEntry.Links.FindService(GDataSpreadsheetsNameTable.ListRel, null);
            ListQuery wquery = new ListQuery(wListFeedLink.HRef.ToString());
            ListFeed w2feed = tService.Query(wquery);
            return w2feed;
        }

        private void InsertRow(string pPlayerOne, string pPlayerTwo, string pBetAmount, ListFeed pFeed)
        {
            DateTime tDateTime = DateTime.Today;

            string tDate = tDateTime.Day + "/" + tDateTime.Month + "/" + tDateTime.Year;
            int tBetAmount = ConvertBetToInt(pBetAmount);
            int tCommission = (int)(tBetAmount * 0.10);
            int tAdminFee;
            if (tBuyinMode == true)
            {
                tAdminFee = (int)(tCommission * 0.10);
            }
            else
            {
                tAdminFee = (int)(tCommission * 0.30);
            }

            ListEntry tNewRow = new ListEntry();

            ListEntry.Custom tElementDate = new ListEntry.Custom();
            tElementDate.LocalName = "date";
            tElementDate.Value = tDate;

            ListEntry.Custom tElementPlayer1 = new ListEntry.Custom();
            tElementPlayer1.LocalName = "nameofplayer1";
            tElementPlayer1.Value = pPlayerOne;

            ListEntry.Custom tElementPlayer2 = new ListEntry.Custom();
            tElementPlayer2.LocalName = "nameofplayer2";
            tElementPlayer2.Value = pPlayerTwo;

            ListEntry.Custom tElementPlayer1Bet = new ListEntry.Custom();
            tElementPlayer1Bet.LocalName = "player1bet";
            tElementPlayer1Bet.Value = tBetAmount.ToString();

            ListEntry.Custom tElementPlayer2Bet = new ListEntry.Custom();
            tElementPlayer2Bet.LocalName = "player2bet";
            tElementPlayer2Bet.Value = tBetAmount.ToString();

            ListEntry.Custom tElementCommission = new ListEntry.Custom();
            tElementCommission.LocalName = "commission";
            tElementCommission.Value = tCommission.ToString();

            ListEntry.Custom tElementAdminFee = new ListEntry.Custom();
            tElementAdminFee.LocalName = "commisionforadmin";
            tElementAdminFee.Value = tAdminFee.ToString();

            tNewRow.Elements.Add(tElementAdminFee);
            tNewRow.Elements.Add(tElementCommission);
            tNewRow.Elements.Add(tElementDate);
            tNewRow.Elements.Add(tElementPlayer1);
            tNewRow.Elements.Add(tElementPlayer1Bet);
            tNewRow.Elements.Add(tElementPlayer2);
            tNewRow.Elements.Add(tElementPlayer2Bet);

            var tResult = pFeed.Insert(tNewRow) as ListEntry;
        }

        private int ConvertBetToInt(string pBetAmount)
        {
            double tBetAmountFloat;
            int tBetAmountInt = 0;
            string tBet = pBetAmount.Substring(0, pBetAmount.Length - 1);
            tBet = tBet.Replace(",", "");

            int tMultiplier = GetMultiplier(pBetAmount);
            //Int32.TryParse(tBet, out tBetAmount);
            double.TryParse(tBet, out tBetAmountFloat);
            tBetAmountInt = (int)(tBetAmountFloat * (double)tMultiplier);
            return tBetAmountInt;
        }

        private string GetCommission(string pBetAmount)
        {
            double tBetAmount;
            string tBet;
            string tBetTest = pBetAmount.Substring(pBetAmount.Length - 1, 1);
            if (tBetTest != "b" && tBetTest != "B" &&
                tBetTest != "k" && tBetTest != "K" &&
                tBetTest != "m" && tBetTest != "M")
            {
                tBet = pBetAmount.Replace(",", "");
            }
            else
            {
                tBet = pBetAmount.Substring(0, pBetAmount.Length - 1);
                tBet = tBet.Replace(",", "");
            }

            int tMultiplier = GetMultiplier(pBetAmount);
            double.TryParse(tBet, out tBetAmount);

            tBetAmount = Convert.ToInt32(tBetAmount * 0.1 * tMultiplier);
            return tBetAmount.ToString("###,###,###,###");
        }

        private string GetReturnedGp(string pBetAmount)
        {
            double tBetAmount;
            string tBet;
            string tBetTest = pBetAmount.Substring(pBetAmount.Length - 1, 1);
            if (tBetTest != "b" && tBetTest != "B" &&
                tBetTest != "k" && tBetTest != "K" &&
                tBetTest != "m" && tBetTest != "M")
            {
                tBet = pBetAmount.Replace(",", "");
            }
            else
            {
                tBet = pBetAmount.Substring(0, pBetAmount.Length - 1);
                tBet = tBet.Replace(",", "");
            }

            int tMultiplier = GetMultiplier(pBetAmount);
            double.TryParse(tBet, out tBetAmount);

            tBetAmount = Convert.ToInt64(tBetAmount * 0.95 * 2 * tMultiplier);
            return tBetAmount.ToString("###,###,###,###");
        }

        private int GetMultiplier(string pBetAmount)
        {
            string tUnit = pBetAmount.Substring(pBetAmount.Length - 1, 1);
            int tMultiplier;
            switch (tUnit)
            {
                case "b":
                case "B":
                    tMultiplier = 1000000000;
                    break;
                case "m":
                case "M":
                    tMultiplier = 1000000;
                    break;
                case "k":
                case "K":
                    tMultiplier = 1000;
                    break;
                default:
                    tMultiplier = 1;
                    break;
            }
            return tMultiplier;
        }

        public string IntToBet(string pBetAmount)
        {
            int tLength = 0;
            string tBet = pBetAmount;
            string tFirstHalf = "";
            string tLastHalf = "";
            string tRemainder = "";
            string tBetWord = "";
            bool tZeros = true;

            tBet = tBet.Replace(",", "");
            tLength = tBet.Length;
            if (tLength > 3 && tLength <= 6) {
                tLastHalf = tBet.Substring(tLength - 3, 3);
                while (tZeros)
                {
                    if (tLastHalf.Length > 0 && tLastHalf.Substring(tLastHalf.Length - 1, 1) == "0")
                    {
                        tLastHalf = tLastHalf.Substring(0, tLastHalf.Length - 1);
                    }
                    else
                    {
                        tRemainder = tLastHalf;
                        tZeros = false;
                    }
                }
                //tRemainder = Regex.Replace(tLastHalf, "[0]", "");
                tFirstHalf = tBet.Substring(0, tLength - 3);
                if (tRemainder.Length == 0)
                    tBetWord = tFirstHalf + "k";
                else
                    tBetWord = tFirstHalf + "." + tRemainder + "k";
            } else if (tLength > 6 && tLength <= 9) {
                tLastHalf = tBet.Substring(tLength - 6, 6);
                while (tZeros)
                {
                    if (tLastHalf.Length > 0 && tLastHalf.Substring(tLastHalf.Length - 1, 1) == "0")
                    {
                        tLastHalf = tLastHalf.Substring(0, tLastHalf.Length - 1);
                    }
                    else
                    {
                        tRemainder = tLastHalf;
                        tZeros = false;
                    }
                }
                //tRemainder = Regex.Replace(tLastHalf, "[0]", "");
                tFirstHalf = tBet.Substring(0, tLength - 6);
                if (tRemainder.Length == 0)
                    tBetWord = tFirstHalf + "m";
                else
                    tBetWord = tFirstHalf + "." + tRemainder + "m";
            } else if (tLength > 9 && tLength <= 12) {
                tLastHalf = tBet.Substring(tLength - 9, 9);
                while (tZeros)
                {
                    if (tLastHalf.Length > 0 && tLastHalf.Substring(tLastHalf.Length - 1, 1) == "0")
                    {
                        tLastHalf = tLastHalf.Substring(0, tLastHalf.Length - 1);
                    }
                    else
                    {
                        tRemainder = tLastHalf;
                        tZeros = false;
                    }
                }
                //tRemainder = Regex.Replace(tLastHalf, "[0]", "");
                tFirstHalf = tBet.Substring(0, tLength - 9);
                if (tRemainder.Length == 0)
                    tBetWord = tFirstHalf + "b";
                else
                    tBetWord = tFirstHalf + "." + tRemainder + "b";
            } else {
                tBetWord = tBet;
            }

            return tBetWord;
        }

        private int ReturnMatchedKeyCode(string pCharacter)
        {
            char tCharacter = pCharacter.ToLowerInvariant()[0];
            int tConvertedCharacter = Convert.ToInt32(tCharacter);
            return tConvertedCharacter;
        }

        private void LoadComboBoxValues(ComboBox pComboBox)
        {
            pComboBox.Items.Add("A");
            pComboBox.Items.Add("B");
            pComboBox.Items.Add("C");
            pComboBox.Items.Add("D");
            pComboBox.Items.Add("E");
            pComboBox.Items.Add("F");
            pComboBox.Items.Add("G");
            pComboBox.Items.Add("H");
            pComboBox.Items.Add("I");
            pComboBox.Items.Add("J");
            pComboBox.Items.Add("K");
            pComboBox.Items.Add("L");
            pComboBox.Items.Add("M");
            pComboBox.Items.Add("N");
            pComboBox.Items.Add("O");
            pComboBox.Items.Add("P");
            pComboBox.Items.Add("Q");
            pComboBox.Items.Add("R");
            pComboBox.Items.Add("S");
            pComboBox.Items.Add("T");
            pComboBox.Items.Add("U");
            pComboBox.Items.Add("V");
            pComboBox.Items.Add("W");
            pComboBox.Items.Add("X");
            pComboBox.Items.Add("Y");
            pComboBox.Items.Add("Z");
            pComboBox.Items.Add("0");
            pComboBox.Items.Add("1");
            pComboBox.Items.Add("2");
            pComboBox.Items.Add("3");
            pComboBox.Items.Add("4");
            pComboBox.Items.Add("5");
            pComboBox.Items.Add("6");
            pComboBox.Items.Add("7");
            pComboBox.Items.Add("8");
            pComboBox.Items.Add("9");
            pComboBox.Items.Add("`");
            pComboBox.Items.Add("-");
            pComboBox.Items.Add("=");
            pComboBox.Items.Add("[");
            pComboBox.Items.Add("]");
            pComboBox.Items.Add(@"\");
            pComboBox.Items.Add(";");
            pComboBox.Items.Add("'");
            pComboBox.Items.Add(",");
            pComboBox.Items.Add(".");
            pComboBox.Items.Add("/");
        }

        private void ProcessAutotyper(string pAutotypedText)
        {
            tAutoTyperDictionary = new Dictionary<int, string>();
            char[] tLineDelimiters = new char[] { '\r', '\n' };
            char[] tCommandDelimiters = new char[] { '|' };
            string[] tAutoTyperRows = pAutotypedText.Split(tLineDelimiters, StringSplitOptions.RemoveEmptyEntries);
            foreach (string tRow in tAutoTyperRows)
            {
                try
                {
                    string[] tSplitRow = tRow.Split(tCommandDelimiters);
                    int tCommand = ReturnMatchedKeyCode(tSplitRow[0]);
                    string tLine = tSplitRow[1];
                    tAutoTyperDictionary.Add(tCommand, tLine);
                }
                catch { }
            }
        }

        private void ProcessReplacements(string pReplacementText)
        {
            tTextReplacementDictionary = new Dictionary<string, string>();
            char[] tLineDelimiters = new char[] { '\r', '\n' };
            char[] tCommandDelimiters = new char[] { '|' };
            string[] tAutoTyperRows = pReplacementText.Split(tLineDelimiters, StringSplitOptions.RemoveEmptyEntries);
            foreach (string tRow in tAutoTyperRows)
            {
                try
                {
                    string[] tSplitRow = tRow.Split(tCommandDelimiters);
                    string tCommand = tSplitRow[0];
                    string tLine = tSplitRow[1];
                    tTextReplacementDictionary.Add(tCommand, tLine);
                }
                catch { }
            }
        }

        private bool CheckSettingsFile()
        {
            string tFileName = tFileIO.GetSettingsFilePath();
            if (File.Exists(tFileName))
            {
                string tGmailPasswordCheck = GetGmailPassword();
                string tGmailUsernameCheck = GetGmailUserName();
                string tFacebookIdCheck = GetFacebookId();
                string tFacebookPinCheck = GetFacebookPin();
                string tSpreadsheetNameCheck = GetSpreadsheetName();

                if (tGmailPasswordCheck == "" || tGmailPasswordCheck == null) return false;
                if (tGmailUsernameCheck == "" || tGmailUsernameCheck == null) return false;
                if (tFacebookIdCheck == "" || tFacebookIdCheck == null) return false;
                if (tFacebookPinCheck == "" || tFacebookPinCheck == null) return false;
                if (tSpreadsheetNameCheck == "" || tSpreadsheetNameCheck == null) return false;

                return true;
            }
            else
                return false;
        }

        private string GetActiveWindowTitle()
        {
            const int nChars = 256;
            IntPtr handle = IntPtr.Zero;
            StringBuilder Buff = new StringBuilder(nChars);
            handle = GetForegroundWindow();

            if (GetWindowText(handle, Buff, nChars) > 0)
            {
                return Buff.ToString();
            }
            return null;
        }
    }
}
