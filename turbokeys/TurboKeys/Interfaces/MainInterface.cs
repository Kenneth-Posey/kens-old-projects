using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Resources;
using System.Reflection;
using System.Drawing.Imaging;
using System.Drawing.Text;
using System.Diagnostics;
using MouseKeyboardLibrary;
using Gma.UserActivityMonitor;
using System.Runtime.InteropServices;

namespace TurboKeys
{
    public partial class MainInterface : Form
    {


        [DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        private static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

        ToolTip testtip = new ToolTip();

        float mouseXstart;
        float mouseYstart;
        float mouseXend;
        float mouseYend;
        float mouseXsend;
        float mouseYsend;
        int clickSwitch;
        bool advanced;

        #region Fetching and Loading Resources into Memory

        Icon mainIcon = global::TurboKeys.Properties.Resources.mainIcon2;
        Icon pauseIcon = global::TurboKeys.Properties.Resources.pauseIcon;
        
        Image black0 = global::TurboKeys.Properties.Resources.black0;
        Image black1 = global::TurboKeys.Properties.Resources.black1;
        Image black2 = global::TurboKeys.Properties.Resources.black2;
        Image black3 = global::TurboKeys.Properties.Resources.black3;
        Image black4 = global::TurboKeys.Properties.Resources.black4;
        Image black5 = global::TurboKeys.Properties.Resources.black5;
        Image black6 = global::TurboKeys.Properties.Resources.black6;
        Image black7 = global::TurboKeys.Properties.Resources.black7;
        Image black8 = global::TurboKeys.Properties.Resources.black8;
        Image black9 = global::TurboKeys.Properties.Resources.black9;
        Image blackA = global::TurboKeys.Properties.Resources.Ablack;
        Image blackB = global::TurboKeys.Properties.Resources.Bblack;
        Image blackC = global::TurboKeys.Properties.Resources.Cblack;
        Image blackD = global::TurboKeys.Properties.Resources.Dblack;
        Image blackE = global::TurboKeys.Properties.Resources.Eblack;
        Image blackF = global::TurboKeys.Properties.Resources.Fblack;
        Image blackG = global::TurboKeys.Properties.Resources.Gblack;
        Image blackH = global::TurboKeys.Properties.Resources.Hblack;
        Image blackI = global::TurboKeys.Properties.Resources.Iblack;
        Image blackJ = global::TurboKeys.Properties.Resources.Jblack;
        Image blackK = global::TurboKeys.Properties.Resources.Kblack;
        Image blackL = global::TurboKeys.Properties.Resources.Lblack;
        Image blackM = global::TurboKeys.Properties.Resources.Mblack;
        Image blackN = global::TurboKeys.Properties.Resources.Nblack;
        Image blackO = global::TurboKeys.Properties.Resources.Oblack;
        Image blackP = global::TurboKeys.Properties.Resources.Pblack;
        Image blackQ = global::TurboKeys.Properties.Resources.Qblack;
        Image blackR = global::TurboKeys.Properties.Resources.Rblack;
        Image blackS = global::TurboKeys.Properties.Resources.Sblack;
        Image blackT = global::TurboKeys.Properties.Resources.Tblack;
        Image blackU = global::TurboKeys.Properties.Resources.Ublack;
        Image blackV = global::TurboKeys.Properties.Resources.Vblack;
        Image blackW = global::TurboKeys.Properties.Resources.Wblack;
        Image blackX = global::TurboKeys.Properties.Resources.Xblack;
        Image blackY = global::TurboKeys.Properties.Resources.Yblack;
        Image blackZ = global::TurboKeys.Properties.Resources.Zblack;

        Image green0 = global::TurboKeys.Properties.Resources.green0;
        Image green1 = global::TurboKeys.Properties.Resources.green1;
        Image green2 = global::TurboKeys.Properties.Resources.green2;
        Image green3 = global::TurboKeys.Properties.Resources.green3;
        Image green4 = global::TurboKeys.Properties.Resources.green4;
        Image green5 = global::TurboKeys.Properties.Resources.green5;
        Image green6 = global::TurboKeys.Properties.Resources.green6;
        Image green7 = global::TurboKeys.Properties.Resources.green7;
        Image green8 = global::TurboKeys.Properties.Resources.green8;
        Image green9 = global::TurboKeys.Properties.Resources.green9;
        Image greenA = global::TurboKeys.Properties.Resources.Agreen;
        Image greenB = global::TurboKeys.Properties.Resources.Bgreen;
        Image greenC = global::TurboKeys.Properties.Resources.Cgreen;
        Image greenD = global::TurboKeys.Properties.Resources.Dgreen;
        Image greenE = global::TurboKeys.Properties.Resources.Egreen;
        Image greenF = global::TurboKeys.Properties.Resources.Fgreen;
        Image greenG = global::TurboKeys.Properties.Resources.Ggreen;
        Image greenH = global::TurboKeys.Properties.Resources.Hgreen;
        Image greenI = global::TurboKeys.Properties.Resources.Igreen;
        Image greenJ = global::TurboKeys.Properties.Resources.Jgreen;
        Image greenK = global::TurboKeys.Properties.Resources.Kgreen;
        Image greenL = global::TurboKeys.Properties.Resources.Lgreen;
        Image greenM = global::TurboKeys.Properties.Resources.Mgreen;
        Image greenN = global::TurboKeys.Properties.Resources.Ngreen;
        Image greenO = global::TurboKeys.Properties.Resources.Ogreen;
        Image greenP = global::TurboKeys.Properties.Resources.Pgreen;
        Image greenQ = global::TurboKeys.Properties.Resources.Qgreen;
        Image greenR = global::TurboKeys.Properties.Resources.Rgreen;
        Image greenS = global::TurboKeys.Properties.Resources.Sgreen;
        Image greenT = global::TurboKeys.Properties.Resources.Tgreen;
        Image greenU = global::TurboKeys.Properties.Resources.Ugreen;
        Image greenV = global::TurboKeys.Properties.Resources.Vgreen;
        Image greenW = global::TurboKeys.Properties.Resources.Wgreen;
        Image greenX = global::TurboKeys.Properties.Resources.Xgreen;
        Image greenY = global::TurboKeys.Properties.Resources.Ygreen;
        Image greenZ = global::TurboKeys.Properties.Resources.Zgreen;

        Image yellow0 = global::TurboKeys.Properties.Resources.yellow0;
        Image yellow1 = global::TurboKeys.Properties.Resources.yellow1;
        Image yellow2 = global::TurboKeys.Properties.Resources.yellow2;
        Image yellow3 = global::TurboKeys.Properties.Resources.yellow3;
        Image yellow4 = global::TurboKeys.Properties.Resources.yellow4;
        Image yellow5 = global::TurboKeys.Properties.Resources.yellow5;
        Image yellow6 = global::TurboKeys.Properties.Resources.yellow6;
        Image yellow7 = global::TurboKeys.Properties.Resources.yellow7;
        Image yellow8 = global::TurboKeys.Properties.Resources.yellow8;
        Image yellow9 = global::TurboKeys.Properties.Resources.yellow9;
        Image yellowA = global::TurboKeys.Properties.Resources.Ayellow;
        Image yellowB = global::TurboKeys.Properties.Resources.Byellow;
        Image yellowC = global::TurboKeys.Properties.Resources.Cyellow;
        Image yellowD = global::TurboKeys.Properties.Resources.Dyellow;
        Image yellowE = global::TurboKeys.Properties.Resources.Eyellow;
        Image yellowF = global::TurboKeys.Properties.Resources.Fyellow;
        Image yellowG = global::TurboKeys.Properties.Resources.Gyellow;
        Image yellowH = global::TurboKeys.Properties.Resources.Hyellow;
        Image yellowI = global::TurboKeys.Properties.Resources.Iyellow;
        Image yellowJ = global::TurboKeys.Properties.Resources.Jyellow;
        Image yellowK = global::TurboKeys.Properties.Resources.Kyellow;
        Image yellowL = global::TurboKeys.Properties.Resources.Lyellow;
        Image yellowM = global::TurboKeys.Properties.Resources.Myellow;
        Image yellowN = global::TurboKeys.Properties.Resources.Nyellow;
        Image yellowO = global::TurboKeys.Properties.Resources.Oyellow;
        Image yellowP = global::TurboKeys.Properties.Resources.Pyellow;
        Image yellowQ = global::TurboKeys.Properties.Resources.Qyellow;
        Image yellowR = global::TurboKeys.Properties.Resources.Ryellow;
        Image yellowS = global::TurboKeys.Properties.Resources.Syellow;
        Image yellowT = global::TurboKeys.Properties.Resources.Tyellow;
        Image yellowU = global::TurboKeys.Properties.Resources.Uyellow;
        Image yellowV = global::TurboKeys.Properties.Resources.Vyellow;
        Image yellowW = global::TurboKeys.Properties.Resources.Wyellow;
        Image yellowX = global::TurboKeys.Properties.Resources.Xyellow;
        Image yellowY = global::TurboKeys.Properties.Resources.Yyellow;
        Image yellowZ = global::TurboKeys.Properties.Resources.Zyellow;

        Image OnBlack = global::TurboKeys.Properties.Resources.OnBlack;
        Image OffBlack = global::TurboKeys.Properties.Resources.OffBlack;
        Image LeftBlack = global::TurboKeys.Properties.Resources.LeftBlack;
        Image NoClickBlack = global::TurboKeys.Properties.Resources.NoClickBlack;
        Image RightBlack = global::TurboKeys.Properties.Resources.RightBlack;

        Image OnGreen = global::TurboKeys.Properties.Resources.OnGreen;
        Image OffGreen = global::TurboKeys.Properties.Resources.OffGreen;
        Image LeftGreen = global::TurboKeys.Properties.Resources.LeftGreen;
        Image NoClickGreen = global::TurboKeys.Properties.Resources.NoClickGreen;
        Image RightGreen = global::TurboKeys.Properties.Resources.RightGreen;

        Image Advanced = global::TurboKeys.Properties.Resources.Advanced;
        Image AdvancedBlue = global::TurboKeys.Properties.Resources.advancedblue;

        #endregion

        #region Declaring Mousekey Classes
        public mousekey key1 = new mousekey();
        public mousekey key2 = new mousekey();
        public mousekey key3 = new mousekey();
        public mousekey key4 = new mousekey();
        public mousekey key5 = new mousekey();
        public mousekey key6 = new mousekey();
        public mousekey key7 = new mousekey();
        public mousekey key8 = new mousekey();
        public mousekey key9 = new mousekey();
        public mousekey key0 = new mousekey();
        public mousekey keyA = new mousekey();
        public mousekey keyB = new mousekey();
        public mousekey keyC = new mousekey();
        public mousekey keyD = new mousekey();
        public mousekey keyE = new mousekey();
        public mousekey keyF = new mousekey();
        public mousekey keyG = new mousekey();
        public mousekey keyH = new mousekey();
        public mousekey keyI = new mousekey();
        public mousekey keyJ = new mousekey();
        public mousekey keyK = new mousekey();
        public mousekey keyL = new mousekey();
        public mousekey keyM = new mousekey();
        public mousekey keyN = new mousekey();
        public mousekey keyO = new mousekey();
        public mousekey keyP = new mousekey();
        public mousekey keyQ = new mousekey();
        public mousekey keyR = new mousekey();
        public mousekey keyS = new mousekey();
        public mousekey keyT = new mousekey();
        public mousekey keyU = new mousekey();
        public mousekey keyV = new mousekey();
        public mousekey keyW = new mousekey();
        public mousekey keyX = new mousekey();
        public mousekey keyY = new mousekey();
        public mousekey keyZ = new mousekey();
        private mousekey currentkey;
        public int mainMouseSpeed { get; set; }
        public int mainClickDistance { get; set; }
        public int mainClickSpeed { get; set; }
        Settings settingsForm = new Settings();
        #endregion

        private Dictionary<mousekey, string> keyList = new Dictionary<mousekey, string>();

        [DllImport("gdi32")]
        public static extern int AddFontResource(string lpFileName); 

        public MainInterface()
        {
            InitializeComponent();
            var f = FontFamily.Families.Where(x => x.Name == "OCR A Extended").FirstOrDefault();
            if (f == null)
            {
                string tFile = Directory.GetCurrentDirectory() + "\\OCRAEXT.TFF";
                AddFontResource(tFile);
            }
            f = f;
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            

            advanced = false;

            textBox1.Hide();
            pictureBox58.Hide();

            //Sets up certain labels and boxes to be invisible
            label5.Text = "";
            label6.Text = "";
            label7.Text = "";

            numericUpDown1.Visible = false;
            pictureBox43.Visible = false;
            pictureBox55.Visible = false;

            numericUpDown2.Visible = false;
            pictureBox44.Visible = false;
            pictureBox56.Visible = false;

            radioButton1.Visible = false;
            radioButton2.Visible = false;

            Random rand = new Random();
            mainMouseSpeed = rand.Next(50, 200);
            mainClickDistance = rand.Next(1, 10);
            mainClickSpeed = rand.Next(5, 20);

            #region Setting Cursors

            pictureBox1.Cursor = Cursors.Hand;
            pictureBox2.Cursor = Cursors.Hand;
            pictureBox3.Cursor = Cursors.Hand;
            pictureBox4.Cursor = Cursors.Hand;
            pictureBox5.Cursor = Cursors.Hand;
            pictureBox6.Cursor = Cursors.Hand;
            pictureBox7.Cursor = Cursors.Hand;
            pictureBox8.Cursor = Cursors.Hand;
            pictureBox9.Cursor = Cursors.Hand;
            pictureBox10.Cursor = Cursors.Hand;
            pictureBox11.Cursor = Cursors.Hand;
            pictureBox12.Cursor = Cursors.Hand;
            pictureBox13.Cursor = Cursors.Hand;
            pictureBox14.Cursor = Cursors.Hand;
            pictureBox15.Cursor = Cursors.Hand;
            pictureBox16.Cursor = Cursors.Hand;
            pictureBox17.Cursor = Cursors.Hand;
            pictureBox18.Cursor = Cursors.Hand;
            pictureBox19.Cursor = Cursors.Hand;
            pictureBox20.Cursor = Cursors.Hand;
            pictureBox21.Cursor = Cursors.Hand;
            pictureBox22.Cursor = Cursors.Hand;
            pictureBox23.Cursor = Cursors.Hand;
            pictureBox24.Cursor = Cursors.Hand;
            pictureBox25.Cursor = Cursors.Hand;
            pictureBox26.Cursor = Cursors.Hand;
            pictureBox27.Cursor = Cursors.Hand;
            pictureBox28.Cursor = Cursors.Hand;
            pictureBox29.Cursor = Cursors.Hand;
            pictureBox30.Cursor = Cursors.Hand;
            pictureBox31.Cursor = Cursors.Hand;
            pictureBox32.Cursor = Cursors.Hand;
            pictureBox33.Cursor = Cursors.Hand;
            pictureBox34.Cursor = Cursors.Hand;
            pictureBox35.Cursor = Cursors.Hand;
            pictureBox36.Cursor = Cursors.Hand;
            pictureBox37.Cursor = Cursors.Hand;
            pictureBox38.Cursor = Cursors.Hand;
            pictureBox39.Cursor = Cursors.Hand;
            pictureBox40.Cursor = Cursors.Hand;
            pictureBox41.Cursor = Cursors.Hand;
            //This is a decoration box
            //pictureBox42.Cursor = Cursors.Hand;
            pictureBox43.Cursor = Cursors.Hand;
            pictureBox44.Cursor = Cursors.Hand;
            numericUpDown1.Cursor = Cursors.Hand;
            numericUpDown2.Cursor = Cursors.Hand;

            label6.Cursor = Cursors.Hand;
            label7.Cursor = Cursors.Hand;

            //Toolbar
            pictureBox45.Cursor = Cursors.Hand;
            pictureBox46.Cursor = Cursors.Hand;
            pictureBox47.Cursor = Cursors.Hand;
            pictureBox48.Cursor = Cursors.Hand;
            pictureBox49.Cursor = Cursors.Hand;
            //pictureBox50.Cursor = Cursors.Hand; Help
            //pictureBox51.Cursor = Cursors.Hand; Box
            pictureBox52.Cursor = Cursors.Hand;
            pictureBox53.Cursor = Cursors.Hand;
            pictureBox54.Cursor = Cursors.Hand;
            pictureBox55.Cursor = Cursors.Hand;
            pictureBox56.Cursor = Cursors.Hand;

            ToolTip toolTip = new ToolTip();

            toolTip.AutoPopDelay = 10000;
            toolTip.InitialDelay = 500;
            toolTip.ReshowDelay = 500;
            toolTip.ShowAlways = true;

            toolTip.SetToolTip(pictureBox50, "Coming Soon: Interactive Help!");

            ToolTip toolTip2 = new ToolTip();

            toolTip2.AutoPopDelay = 10000;
            toolTip2.InitialDelay = 500;
            toolTip2.ReshowDelay = 500;
            toolTip2.ShowAlways = true;

            toolTip2.SetToolTip(pictureBox51, "Coming Soon: Next Key!");

            ToolTip toolTip3 = new ToolTip();

            toolTip3.AutoPopDelay = 10000;
            toolTip3.InitialDelay = 500;
            toolTip3.ReshowDelay = 500;
            toolTip3.ShowAlways = true;

            toolTip3.SetToolTip(pictureBox47, "Global Reset. \nThis resets all your turbo-keys.\nOnly click if you're very sure.");

            ToolTip toolTip4 = new ToolTip();

            toolTip4.AutoPopDelay = 10000;
            toolTip4.InitialDelay = 500;
            toolTip4.ReshowDelay = 500;
            toolTip4.ShowAlways = true;

            toolTip4.SetToolTip(pictureBox49, "Click to Activate your Turbo-Keys");

            ToolTip toolTip5 = new ToolTip();

            toolTip5.AutoPopDelay = 10000;
            toolTip5.InitialDelay = 500;
            toolTip5.ReshowDelay = 500;
            toolTip5.ShowAlways = true;

            toolTip5.SetToolTip(pictureBox52, "Click to Auto-Set Movement \n\nFirst Click where you'll be moving FROM \nThen Click where you'll be moving TO\nThe distance between them will be set\nto the current turbo key");
            
            ToolTip toolTip6 = new ToolTip();

            toolTip6.AutoPopDelay = 10000;
            toolTip6.InitialDelay = 500;
            toolTip6.ReshowDelay = 500;
            toolTip6.ShowAlways = true;

            toolTip6.SetToolTip(pictureBox53, "Click to Auto-Set an Absolute Coordinate \nfor Movement or Clicks.");
            
            ToolTip toolTip7 = new ToolTip();

            toolTip7.AutoPopDelay = 10000;
            toolTip7.InitialDelay = 500;
            toolTip7.ReshowDelay = 500;
            toolTip7.ShowAlways = true;

            toolTip7.SetToolTip(pictureBox54, "Click to Access Mouse Movement Safety Settings.");

            #endregion

            #region Setting Key Properties
            key1.mPictureCurrent = pictureBox1;
            key1.mPictureBlack = black1;
            key1.mPictureGreen = green1;
            key1.mPictureYellow = yellow1;
            key1.mKey = "1";
            keyList.Add(key1, key1.mKey);

            key2.mPictureCurrent = pictureBox2;
            key2.mPictureBlack = black2;
            key2.mPictureGreen = green2;
            key2.mPictureYellow = yellow2;
            key2.mKey = "2";
            keyList.Add(key2, key2.mKey);

            key3.mPictureCurrent = pictureBox3;
            key3.mPictureBlack = black3;
            key3.mPictureGreen = green3;
            key3.mPictureYellow = yellow3;
            key3.mKey = "3";
            keyList.Add(key3, key3.mKey);

            key4.mPictureCurrent = pictureBox4;
            key4.mPictureBlack = black4;
            key4.mPictureGreen = green4;
            key4.mPictureYellow = yellow4;
            key4.mKey = "4";
            keyList.Add(key4, key4.mKey);

            key5.mPictureCurrent = pictureBox5;
            key5.mPictureBlack = black5;
            key5.mPictureGreen = green5;
            key5.mPictureYellow = yellow5;
            key5.mKey = "5";
            keyList.Add(key5, key5.mKey);

            key6.mPictureCurrent = pictureBox6;
            key6.mPictureBlack = black6;
            key6.mPictureGreen = green6;
            key6.mPictureYellow = yellow6;
            key6.mKey = "6";
            keyList.Add(key6, key6.mKey);

            key7.mPictureCurrent = pictureBox7;
            key7.mPictureBlack = black7;
            key7.mPictureGreen = green7;
            key7.mPictureYellow = yellow7;
            key7.mKey = "7";
            keyList.Add(key7, key7.mKey);

            key8.mPictureCurrent = pictureBox8;
            key8.mPictureBlack = black8;
            key8.mPictureGreen = green8;
            key8.mPictureYellow = yellow8;
            key8.mKey = "8";
            keyList.Add(key8, key8.mKey);

            key9.mPictureCurrent = pictureBox9;
            key9.mPictureBlack = black9;
            key9.mPictureGreen = green9;
            key9.mPictureYellow = yellow9;
            key9.mKey = "9";
            keyList.Add(key9, key9.mKey);

            key0.mPictureCurrent = pictureBox10;
            key0.mPictureBlack = black0;
            key0.mPictureGreen = green0;
            key0.mPictureYellow = yellow0;
            key0.mKey = "0";
            keyList.Add(key0, key0.mKey);

            keyA.mPictureCurrent = pictureBox21;
            keyA.mPictureBlack = blackA;
            keyA.mPictureGreen = greenA;
            keyA.mPictureYellow = yellowA;
            keyA.mKey = "A";
            keyList.Add(keyA, keyA.mKey);

            keyB.mPictureCurrent = pictureBox34;
            keyB.mPictureBlack = blackB;
            keyB.mPictureGreen = greenB;
            keyB.mPictureYellow = yellowB;
            keyB.mKey = "B";
            keyList.Add(keyB, keyB.mKey);

            keyC.mPictureCurrent = pictureBox32;
            keyC.mPictureBlack = blackC;
            keyC.mPictureGreen = greenC;
            keyC.mPictureYellow = yellowC;
            keyC.mKey = "C";
            keyList.Add(keyC, keyC.mKey);

            keyD.mPictureCurrent = pictureBox23;
            keyD.mPictureBlack = blackD;
            keyD.mPictureGreen = greenD;
            keyD.mPictureYellow = yellowD;
            keyD.mKey = "D";
            keyList.Add(keyD, keyD.mKey);

            keyE.mPictureCurrent = pictureBox13;
            keyE.mPictureBlack = blackE;
            keyE.mPictureGreen = greenE;
            keyE.mPictureYellow = yellowE;
            keyE.mKey = "E";
            keyList.Add(keyE, keyE.mKey);

            keyF.mPictureCurrent = pictureBox24;
            keyF.mPictureBlack = blackF;
            keyF.mPictureGreen = greenF;
            keyF.mPictureYellow = yellowF;
            keyF.mKey = "F";
            keyList.Add(keyF, keyF.mKey);

            keyG.mPictureCurrent = pictureBox25;
            keyG.mPictureBlack = blackG;
            keyG.mPictureGreen = greenG;
            keyG.mPictureYellow = yellowG;
            keyG.mKey = "G";
            keyList.Add(keyG, keyG.mKey);

            keyH.mPictureCurrent = pictureBox26;
            keyH.mPictureBlack = blackH;
            keyH.mPictureGreen = greenH;
            keyH.mPictureYellow = yellowH;
            keyH.mKey = "H";
            keyList.Add(keyH, keyH.mKey);

            keyI.mPictureCurrent = pictureBox18;
            keyI.mPictureBlack = blackI;
            keyI.mPictureGreen = greenI;
            keyI.mPictureYellow = yellowI;
            keyI.mKey = "I";
            keyList.Add(keyI, keyI.mKey);

            keyJ.mPictureCurrent = pictureBox27;
            keyJ.mPictureBlack = blackJ;
            keyJ.mPictureGreen = greenJ;
            keyJ.mPictureYellow = yellowJ;
            keyJ.mKey = "J";
            keyList.Add(keyJ, keyJ.mKey);

            keyK.mPictureCurrent = pictureBox28;
            keyK.mPictureBlack = blackK;
            keyK.mPictureGreen = greenK;
            keyK.mPictureYellow = yellowK;
            keyK.mKey = "K";
            keyList.Add(keyK, keyK.mKey);

            keyL.mPictureCurrent = pictureBox29;
            keyL.mPictureBlack = blackL;
            keyL.mPictureGreen = greenL;
            keyL.mPictureYellow = yellowL;
            keyL.mKey = "L";
            keyList.Add(keyL, keyL.mKey);

            keyM.mPictureCurrent = pictureBox36;
            keyM.mPictureBlack = blackM;
            keyM.mPictureGreen = greenM;
            keyM.mPictureYellow = yellowM;
            keyM.mKey = "M";
            keyList.Add(keyM, keyM.mKey);

            keyN.mPictureCurrent = pictureBox35;
            keyN.mPictureBlack = blackN;
            keyN.mPictureGreen = greenN;
            keyN.mPictureYellow = yellowN;
            keyN.mKey = "N";
            keyList.Add(keyN, keyN.mKey);

            keyO.mPictureCurrent = pictureBox19;
            keyO.mPictureBlack = blackO;
            keyO.mPictureGreen = greenO;
            keyO.mPictureYellow = yellowO;
            keyO.mKey = "O";
            keyList.Add(keyO, keyO.mKey);

            keyP.mPictureCurrent = pictureBox20;
            keyP.mPictureBlack = blackP;
            keyP.mPictureGreen = greenP;
            keyP.mPictureYellow = yellowP;
            keyP.mKey = "P";
            keyList.Add(keyP, keyP.mKey);

            keyQ.mPictureCurrent = pictureBox11;
            keyQ.mPictureBlack = blackQ;
            keyQ.mPictureGreen = greenQ;
            keyQ.mPictureYellow = yellowQ;
            keyQ.mKey = "Q";
            keyList.Add(keyQ, keyQ.mKey);

            keyR.mPictureCurrent = pictureBox14;
            keyR.mPictureBlack = blackR;
            keyR.mPictureGreen = greenR;
            keyR.mPictureYellow = yellowR;
            keyR.mKey = "R";
            keyList.Add(keyR, keyR.mKey);

            keyS.mPictureCurrent = pictureBox22;
            keyS.mPictureBlack = blackS;
            keyS.mPictureGreen = greenS;
            keyS.mPictureYellow = yellowS;
            keyS.mKey = "S";
            keyList.Add(keyS, keyS.mKey);

            keyT.mPictureCurrent = pictureBox15;
            keyT.mPictureBlack = blackT;
            keyT.mPictureGreen = greenT;
            keyT.mPictureYellow = yellowT;
            keyT.mKey = "T";
            keyList.Add(keyT, keyT.mKey);

            keyU.mPictureCurrent = pictureBox17;
            keyU.mPictureBlack = blackU;
            keyU.mPictureGreen = greenU;
            keyU.mPictureYellow = yellowU;
            keyU.mKey = "U";
            keyList.Add(keyU, keyU.mKey);

            keyV.mPictureCurrent = pictureBox33;
            keyV.mPictureBlack = blackV;
            keyV.mPictureGreen = greenV;
            keyV.mPictureYellow = yellowV;
            keyV.mKey = "V";
            keyList.Add(keyV, keyV.mKey);

            keyW.mPictureCurrent = pictureBox12;
            keyW.mPictureBlack = blackW;
            keyW.mPictureGreen = greenW;
            keyW.mPictureYellow = yellowW;
            keyW.mKey = "W";
            keyList.Add(keyW, keyW.mKey);

            keyX.mPictureCurrent = pictureBox31;
            keyX.mPictureBlack = blackX;
            keyX.mPictureGreen = greenX;
            keyX.mPictureYellow = yellowX;
            keyX.mKey = "X";
            keyList.Add(keyX, keyX.mKey);

            keyY.mPictureCurrent = pictureBox16;
            keyY.mPictureBlack = blackY;
            keyY.mPictureGreen = greenY;
            keyY.mPictureYellow = yellowY;
            keyY.mKey = "Y";
            keyList.Add(keyY, keyY.mKey);

            keyZ.mPictureCurrent = pictureBox30;
            keyZ.mPictureBlack = blackZ;
            keyZ.mPictureGreen = greenZ;
            keyZ.mPictureYellow = yellowZ;
            keyZ.mKey = "Z";
            keyList.Add(keyZ, keyZ.mKey);

            foreach (KeyValuePair<mousekey, string> mousekey in keyList)
            {
                mousekey.Key.mXMovement = label6;
                mousekey.Key.mYMovement = label5;
                mousekey.Key.mCurrentKeyLabel = label7;
                mousekey.Key.relative = true;
            }
            #endregion
            int r = 3;
        }

        void HookManager_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.KeyCode)
            {
                case Keys.D1:
                    if (key1.mActivated == true)
                    {
                        e.Handled = true;
                        key1.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D2:
                    if (key2.mActivated == true)
                    {
                        e.Handled = true;
                        key2.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D3:
                    if (key3.mActivated == true)
                    {
                        e.Handled = true;
                        key3.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D4:
                    if (key4.mActivated == true)
                    {
                        e.Handled = true;
                        key4.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D5:
                    if (key5.mActivated == true)
                    {
                        e.Handled = true;
                        key5.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D6:
                    if (key6.mActivated == true)
                    {
                        e.Handled = true;
                        key6.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D7:
                    if (key7.mActivated == true)
                    {
                        e.Handled = true;
                        key7.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D8:
                    if (key8.mActivated == true)
                    {
                        e.Handled = true;
                        key8.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D9:
                    if (key9.mActivated == true)
                    {
                        e.Handled = true;
                        key9.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D0:
                    if (key0.mActivated == true)
                    {
                        e.Handled = true;
                        key0.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.A:
                    if (keyA.mActivated == true)
                    {
                        e.Handled = true;
                        keyA.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.B:
                    if (keyB.mActivated == true)
                    {
                        e.Handled = true;
                        keyB.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.C:
                    if (keyC.mActivated == true)
                    {
                        e.Handled = true;
                        keyC.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.D:
                    if (keyD.mActivated == true)
                    {
                        e.Handled = true;
                        keyD.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.E:
                    if (keyE.mActivated == true)
                    {
                        e.Handled = true;
                        keyE.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.F:
                    if (keyF.mActivated == true)
                    {
                        e.Handled = true;
                        keyF.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.G:
                    if (keyG.mActivated == true)
                    {
                        e.Handled = true;
                        keyG.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.H:
                    if (keyH.mActivated == true)
                    {
                        e.Handled = true;
                        keyH.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.I:
                    if (keyI.mActivated == true)
                    {
                        e.Handled = true;
                        keyI.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.J:
                    if (keyJ.mActivated == true)
                    {
                        e.Handled = true;
                        keyJ.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.K:
                    if (keyK.mActivated == true)
                    {
                        e.Handled = true;
                        keyK.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.L:
                    if (keyL.mActivated == true)
                    {
                        e.Handled = true;
                        keyL.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.M:
                    if (keyM.mActivated == true)
                    {
                        e.Handled = true;
                        keyM.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.N:
                    if (keyN.mActivated == true)
                    {
                        e.Handled = true;
                        keyN.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.O:
                    if (keyO.mActivated == true)
                    {
                        e.Handled = true;
                        keyO.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.P:
                    if (keyP.mActivated == true)
                    {
                        e.Handled = true;
                        keyP.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.Q:
                    if (keyQ.mActivated == true)
                    {
                        e.Handled = true;
                        keyQ.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.R:
                    if (keyR.mActivated == true)
                    {
                        e.Handled = true;
                        keyR.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.S:
                    if (keyS.mActivated == true)
                    {
                        e.Handled = true;
                        keyS.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.T:
                    if (keyT.mActivated == true)
                    {
                        e.Handled = true;
                        keyT.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.U:
                    if (keyU.mActivated == true)
                    {
                        e.Handled = true;
                        keyU.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.V:
                    if (keyV.mActivated == true)
                    {
                        e.Handled = true;
                        keyV.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.W:
                    if (keyW.mActivated == true)
                    {
                        e.Handled = true;
                        keyW.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.X:
                    if (keyX.mActivated == true)
                    {
                        e.Handled = true;
                        keyX.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.Y:
                    if (keyY.mActivated == true)
                    {
                        e.Handled = true;
                        keyY.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
                case Keys.Z:
                    if (keyZ.mActivated == true)
                    {
                        e.Handled = true;
                        keyZ.activate(mainMouseSpeed, mainClickDistance, mainClickSpeed);
                    }
                    break;
            }
        }

        private void updateYellowKey(mousekey newKey)
        {
            //This checks to see if there is a current key in memory and executes if there is
            if (currentkey != null)
            {
                if (currentkey.mActivated == true)
                {
                    currentkey.setGreen();
                }
                else
                {
                    currentkey.setBlack();
                }

                if (currentkey.relative == true)
                {
                    radioButton1.Checked = true;
                }
                else if (currentkey.relative == false)
                {
                    radioButton2.Checked = true;
                }
            }
            
            currentkey = newKey;
            newKey.setYellow();
            updateState(currentkey);
            updateClick(currentkey);
            Console.WriteLine("Update yellow " + currentkey.mCurrentKeyLabel.Text);
        }

        private void updateState(mousekey currentKey)
        {
            if (currentKey.mActivated == true)
            {
                pictureBox37.Image = OnGreen;
                pictureBox38.Image = OffBlack;
            }
            else
            {
                pictureBox37.Image = OnBlack;
                pictureBox38.Image = OffGreen;
            }
        }

        private void updateClick(mousekey currentKey)
        {
            radioButton1.Visible = true;
            radioButton2.Visible = true;
            switch (currentkey.clickType)
            {
                case 1:
                    pictureBox39.Image = LeftGreen;
                    pictureBox40.Image = NoClickBlack;
                    pictureBox41.Image = RightBlack;
                    break;
                case 2:
                    pictureBox39.Image = LeftBlack;
                    pictureBox40.Image = NoClickBlack;
                    pictureBox41.Image = RightGreen;
                    break;
                default:
                    pictureBox39.Image = LeftBlack;
                    pictureBox40.Image = NoClickGreen;
                    pictureBox41.Image = RightBlack;
                    break;
            }
            switch (currentkey.relative)
            {       
                case true:
                    radioButton1.Checked = true;
                    break;
                default:
                    radioButton2.Checked = true;
                    break;
            }
        }

        private void deselectBoxes()
        {
            radioButton1.Visible = false;
            radioButton2.Visible = false;
            pictureBox37.Image = OnBlack;
            pictureBox38.Image = OffBlack;
            pictureBox39.Image = LeftBlack;
            pictureBox40.Image = NoClickBlack;
            pictureBox41.Image = RightBlack;
            numericUpDown1.Value = 0;
            numericUpDown2.Value = 0;

            if (numericUpDown1.Visible == true)
            {
                numericUpDown1.Visible = false;
                pictureBox43.Visible = false;
                currentkey.yDistance = (int)numericUpDown1.Value;
                label5.Text = numericUpDown1.Value.ToString() + " px";
                label5.Visible = true;
            }

            if (numericUpDown2.Visible == true)
            {
                numericUpDown2.Visible = false;
                pictureBox44.Visible = false;
                currentkey.xDistance = (int)numericUpDown2.Value;
                label6.Text = numericUpDown2.Value.ToString() + " px";
                label6.Visible = true;
            }
        }

        #region Virtual Keyboard Events
        private void pictureBox1_Click(object sender, EventArgs e)
        {
            if (key1.mSelected == true)
            {
                deselectBoxes();
            }
            if (key1.mSelected == false)
                updateYellowKey(key1);
            else if (key1.mActivated == true)
                key1.setGreen();
            else
                key1.setBlack();
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            if (key2.mSelected == true)
            {
                deselectBoxes();
            }
            if (key2.mSelected == false)
                updateYellowKey(key2);
            else if (key2.mActivated == true)
                key2.setGreen();
            else
                key2.setBlack();
        }

        private void pictureBox3_Click(object sender, EventArgs e)
        {
            if (key3.mSelected == true)
            {
                deselectBoxes();
            }
            if (key3.mSelected == false)
                updateYellowKey(key3);
            else if (key3.mActivated == true)
                key3.setGreen();
            else
                key3.setBlack();
        }

        private void pictureBox4_Click(object sender, EventArgs e)
        {
            if (key4.mSelected == true)
            {
                deselectBoxes();
            }
            if (key4.mSelected == false)
                updateYellowKey(key4);
            else if (key4.mActivated == true)
                key4.setGreen();
            else
                key4.setBlack();
        }

        private void pictureBox5_Click(object sender, EventArgs e)
        {
            if (key5.mSelected == true)
            {
                deselectBoxes();
            }
            if (key5.mSelected == false)
                updateYellowKey(key5);
            else if (key5.mActivated == true)
                key5.setGreen();
            else
                key5.setBlack();
        }

        private void pictureBox6_Click(object sender, EventArgs e)
        {
            if (key6.mSelected == true)
            {
                deselectBoxes();
            }
            if (key6.mSelected == false)
                updateYellowKey(key6);
            else if (key6.mActivated == true)
                key6.setGreen();
            else
                key6.setBlack();
        }

        private void pictureBox7_Click(object sender, EventArgs e)
        {
            if (key7.mSelected == true)
            {
                deselectBoxes();
            }
            if (key7.mSelected == false)
                updateYellowKey(key7);
            else if (key7.mActivated == true)
                key7.setGreen();
            else
                key7.setBlack();
        }

        private void pictureBox8_Click(object sender, EventArgs e)
        {
            if (key8.mSelected == true)
            {
                deselectBoxes();
            }
            if (key8.mSelected == false)
                updateYellowKey(key8);
            else if (key8.mActivated == true)
                key8.setGreen();
            else
                key8.setBlack();
        }

        private void pictureBox9_Click(object sender, EventArgs e)
        {
            if (key9.mSelected == true)
            {
                deselectBoxes();
            }
            if (key9.mSelected == false)
                updateYellowKey(key9);
            else if (key9.mActivated == true)
                key9.setGreen();
            else
                key9.setBlack();
        }

        private void pictureBox10_Click(object sender, EventArgs e)
        {
            if (key0.mSelected == true)
            {
                deselectBoxes();
            }
            if (key0.mSelected == false)
                updateYellowKey(key0);
            else if (key0.mActivated == true)
                key0.setGreen();
            else
                key0.setBlack();
        }

        private void pictureBox11_Click(object sender, EventArgs e)
        {
            if (keyQ.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyQ.mSelected == false)
                updateYellowKey(keyQ);
            else if (keyQ.mActivated == true)
                keyQ.setGreen();
            else
                keyQ.setBlack();
        }

        private void pictureBox12_Click(object sender, EventArgs e)
        {
            if (keyW.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyW.mSelected == false)
                updateYellowKey(keyW);
            else if (keyW.mActivated == true)
                keyW.setGreen();
            else
                keyW.setBlack();
        }

        private void pictureBox13_Click(object sender, EventArgs e)
        {
            if (keyE.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyE.mSelected == false)
                updateYellowKey(keyE);
            else if (keyE.mActivated == true)
                keyE.setGreen();
            else
                keyE.setBlack();
        }

        private void pictureBox14_Click(object sender, EventArgs e)
        {
            if (keyR.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyR.mSelected == false)
                updateYellowKey(keyR);
            else if (keyR.mActivated == true)
                keyR.setGreen();
            else
                keyR.setBlack();
        }

        private void pictureBox15_Click(object sender, EventArgs e)
        {
            if (keyT.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyT.mSelected == false)
                updateYellowKey(keyT);
            else if (keyT.mActivated == true)
                keyT.setGreen();
            else
                keyT.setBlack();
        }

        private void pictureBox16_Click(object sender, EventArgs e)
        {
            if (keyY.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyY.mSelected == false)
                updateYellowKey(keyY);
            else if (keyY.mActivated == true)
                keyY.setGreen();
            else
                keyY.setBlack();
        }

        private void pictureBox17_Click(object sender, EventArgs e)
        {
            if (keyU.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyU.mSelected == false)
                updateYellowKey(keyU);
            else if (keyU.mActivated == true)
                keyU.setGreen();
            else
                keyU.setBlack();
        }

        private void pictureBox18_Click(object sender, EventArgs e)
        {
            if (keyI.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyI.mSelected == false)
                updateYellowKey(keyI);
            else if (keyI.mActivated == true)
                keyI.setGreen();
            else
                keyI.setBlack();
        }

        private void pictureBox19_Click(object sender, EventArgs e)
        {
            if (keyO.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyO.mSelected == false)
                updateYellowKey(keyO);
            else if (keyO.mActivated == true)
                keyO.setGreen();
            else
                keyO.setBlack();
        }

        private void pictureBox20_Click(object sender, EventArgs e)
        {
            if (keyP.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyP.mSelected == false)
                updateYellowKey(keyP);
            else if (keyP.mActivated == true)
                keyP.setGreen();
            else
                keyP.setBlack();
        }

        private void pictureBox21_Click(object sender, EventArgs e)
        {
            if (keyA.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyA.mSelected == false)
                updateYellowKey(keyA);
            else if (keyA.mActivated == true)
                keyA.setGreen();
            else
                keyA.setBlack();
        }

        private void pictureBox22_Click(object sender, EventArgs e)
        {
            if (keyS.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyS.mSelected == false)
                updateYellowKey(keyS);
            else if (keyS.mActivated == true)
                keyS.setGreen();
            else
                keyS.setBlack();
        }

        private void pictureBox23_Click(object sender, EventArgs e)
        {
            if (keyD.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyD.mSelected == false)
                updateYellowKey(keyD);
            else if (keyD.mActivated == true)
                keyD.setGreen();
            else
                keyD.setBlack();
        }

        private void pictureBox24_Click(object sender, EventArgs e)
        {
            if (keyF.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyF.mSelected == false)
                updateYellowKey(keyF);
            else if (keyF.mActivated == true)
                keyF.setGreen();
            else
                keyF.setBlack();
        }

        private void pictureBox25_Click(object sender, EventArgs e)
        {
            if (keyG.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyG.mSelected == false)
                updateYellowKey(keyG);
            else if (keyG.mActivated == true)
                keyG.setGreen();
            else
                keyG.setBlack();
        }

        private void pictureBox26_Click(object sender, EventArgs e)
        {
            if (keyH.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyH.mSelected == false)
                updateYellowKey(keyH);
            else if (keyH.mActivated == true)
                keyH.setGreen();
            else
                keyH.setBlack();
        }

        private void pictureBox27_Click(object sender, EventArgs e)
        {
            if (keyJ.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyJ.mSelected == false)
                updateYellowKey(keyJ);
            else if (keyJ.mActivated == true)
                keyJ.setGreen();
            else
                keyJ.setBlack();
        }

        private void pictureBox28_Click(object sender, EventArgs e)
        {
            if (keyK.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyK.mSelected == false)
                updateYellowKey(keyK);
            else if (keyK.mActivated == true)
                keyK.setGreen();
            else
                keyK.setBlack();
        }

        private void pictureBox29_Click(object sender, EventArgs e)
        {
            if (keyL.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyL.mSelected == false)
                updateYellowKey(keyL);
            else if (keyL.mActivated == true)
                keyL.setGreen();
            else
                keyL.setBlack();
        }

        private void pictureBox30_Click(object sender, EventArgs e)
        {
            if (keyZ.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyZ.mSelected == false)
                updateYellowKey(keyZ);
            else if (keyZ.mActivated == true)
                keyZ.setGreen();
            else
                keyZ.setBlack();
        }

        private void pictureBox31_Click(object sender, EventArgs e)
        {
            if (keyX.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyX.mSelected == false)
                updateYellowKey(keyX);
            else if (keyX.mActivated == true)
                keyX.setGreen();
            else
                keyX.setBlack();
        }

        private void pictureBox32_Click(object sender, EventArgs e)
        {
            if (keyC.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyC.mSelected == false)
                updateYellowKey(keyC);
            else if (keyC.mActivated == true)
                keyC.setGreen();
            else
                keyC.setBlack();
        }

        private void pictureBox33_Click(object sender, EventArgs e)
        {
            if (keyV.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyV.mSelected == false)
                updateYellowKey(keyV);
            else if (keyV.mActivated == true)
                keyV.setGreen();
            else
                keyV.setBlack();
        }

        private void pictureBox34_Click(object sender, EventArgs e)
        {
            if (keyB.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyB.mSelected == false)
                updateYellowKey(keyB);
            else if (keyB.mActivated == true)
                keyB.setGreen();
            else
                keyB.setBlack();
        }

        private void pictureBox35_Click(object sender, EventArgs e)
        {
            if (keyN.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyN.mSelected == false)
                updateYellowKey(keyN);
            else if (keyN.mActivated == true)
                keyN.setGreen();
            else
                keyN.setBlack();
        }

        private void pictureBox36_Click(object sender, EventArgs e)
        {
            if (keyM.mSelected == true)
            {
                deselectBoxes();
            }
            if (keyM.mSelected == false)
                updateYellowKey(keyM);
            else if (keyM.mActivated == true)
                keyM.setGreen();
            else
                keyM.setBlack();
        }
        #endregion

        private void label2_Click(object sender, EventArgs e)
        {

        }

        #region Control Panel
        //Key On
        private void pictureBox37_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                currentkey.mActivated = true;
                pictureBox37.Image = OnGreen;
                pictureBox38.Image = OffBlack;
            }
            else
            {
                MessageBox.Show("You must have a key selected to use that!");
            }
        }

        //Key Off
        private void pictureBox38_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                currentkey.mActivated = false;
                pictureBox37.Image = OnBlack;
                pictureBox38.Image = OffGreen;
            }
            else
            {
                MessageBox.Show("You must have a key selected to use that!");
            }
        }

        //No Click
        private void pictureBox40_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                currentkey.clickType = 0;
                pictureBox39.Image = LeftBlack;
                pictureBox40.Image = NoClickGreen;
                pictureBox41.Image = RightBlack;
            }
            else
            {
                MessageBox.Show("You must have a key selected to use that!");
            }
        }

        //Left Click
        private void pictureBox39_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                currentkey.clickType = 1;
                pictureBox39.Image = LeftGreen;
                pictureBox40.Image = NoClickBlack;
                pictureBox41.Image = RightBlack;
            }
            else
            {
                MessageBox.Show("You must have a key selected to use that!");
            }
        }

        //Right Click
        private void pictureBox41_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                currentkey.clickType = 2;
                pictureBox39.Image = LeftBlack;
                pictureBox40.Image = NoClickBlack;
                pictureBox41.Image = RightGreen;
            }
            else
            {
                MessageBox.Show("You must have a key selected to use that!");
            }
        }
        //Activates Vertical Settings
        private void label5_Click(object sender, EventArgs e)
        {
            label5.Visible = false;
            numericUpDown1.Visible = true;
            numericUpDown1.Value = currentkey.yDistance;
            pictureBox43.Visible = true;
            pictureBox55.Visible = true;
        }
        //Saves Vertical Settings
        private void pictureBox43_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                numericUpDown1.Visible = false;
                pictureBox43.Visible = false;
                pictureBox55.Visible = false;
                if (currentkey != null)
                {
                    currentkey.yDistance = (int)numericUpDown1.Value;
                }
                label5.Text = numericUpDown1.Value.ToString() + " px";
                label5.Visible = true;
            }
        }
        //Cancels Vertical Settings
        private void pictureBox55_Click(object sender, EventArgs e)
        {
            label5.Visible = true;
            numericUpDown1.Visible = false;
            pictureBox55.Visible = false;
            pictureBox43.Visible = false;
        }

        //Activates Horizontal Settings
        private void label6_Click(object sender, EventArgs e)
        {
            label6.Visible = false;
            numericUpDown2.Visible = true;
            numericUpDown2.Value = currentkey.xDistance;
            pictureBox44.Visible = true;
            pictureBox56.Visible = true;
        }
        //Saves Horizontal Settings
        private void pictureBox44_Click(object sender, EventArgs e)
        {
            if (currentkey != null && (currentkey.mPictureCurrent.Image == currentkey.mPictureYellow))
            {
                numericUpDown2.Visible = false;
                pictureBox44.Visible = false;
                pictureBox56.Visible = false;
                if (currentkey != null)
                {
                    currentkey.xDistance = (int)numericUpDown2.Value;
                }
                label6.Text = numericUpDown2.Value.ToString() + " px";
                label6.Visible = true;
            }
        }


        private void pictureBox56_Click(object sender, EventArgs e)
        {
            label6.Visible = true;
            numericUpDown2.Visible = false;
            pictureBox56.Visible = false;
            pictureBox44.Visible = false;
        }


        #endregion

        private void linkLabel1_LinkClicked_1(object sender, LinkLabelLinkClickedEventArgs e)
        {
            ProcessStartInfo sInfo = new ProcessStartInfo("http://apps.facebook.com/turbokeys-points");
            Process.Start(sInfo);
        }

        #region Menu Area
        //Pause Button
        private void pictureBox48_Click(object sender, EventArgs e)
        {
            HookManager.KeyDown -= new KeyEventHandler(HookManager_KeyDown);
            pictureBox49.Visible = true;
            pictureBox48.Visible = false;
            this.Icon = pauseIcon;
            this.Text = "Turbo-Keys are Paused";
        }

        //Play Button
        private void pictureBox49_Click(object sender, EventArgs e)
        {
            HookManager.KeyDown += new KeyEventHandler(HookManager_KeyDown);
            pictureBox49.Visible = false;
            pictureBox48.Visible = true;
            this.Icon = mainIcon;
            this.Text = "Turbo-Keys";
        }

        //Save Button
        private void pictureBox46_Click(object sender, EventArgs e)
        {
            HookManager.KeyDown -= new KeyEventHandler(HookManager_KeyDown);
            SaveFileDialog saveFiles = new SaveFileDialog();
            saveFiles.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\Turbo-Keys\";
            saveFiles.DefaultExt = "ini";
            saveFiles.Filter = "Turbo-Keys Settings Files (*.INI)|*.ini";
            saveFiles.FilterIndex = 1;
            saveFiles.AddExtension = true;
            if (saveFiles.ShowDialog() == DialogResult.OK)
            {
                //This creates the blank .ini file so the parser doesn't choke
                StreamWriter write = new StreamWriter(saveFiles.FileName);
                write.Write("");
                write.Flush();
                write.Dispose();

                IniParser parser = new IniParser(saveFiles.FileName);
                foreach (KeyValuePair<mousekey, string> mousekey in keyList)
                {

                    StringBuilder clickname = new StringBuilder();
                    StringBuilder xname = new StringBuilder();
                    StringBuilder yname = new StringBuilder();

                    clickname.Append("left");
                    clickname.Append(mousekey.Key.mKey);

                    xname.Append("xmove");
                    xname.Append(mousekey.Key.mKey);

                    yname.Append("ymove");
                    yname.Append(mousekey.Key.mKey);

                    string keyString = mousekey.Key.mKey.ToString();
                    string xNameString = xname.ToString();
                    string yNameString = yname.ToString();
                    string clickString = clickname.ToString();
                    string relativeString = "relative";

                    parser.AddSetting(mousekey.Key.mKey, clickString, mousekey.Key.clickType.ToString());
                    parser.AddSetting(mousekey.Key.mKey, xNameString, mousekey.Key.xDistance.ToString());
                    parser.AddSetting(mousekey.Key.mKey, yNameString, mousekey.Key.yDistance.ToString());
                    parser.AddSetting(mousekey.Key.mKey, relativeString, mousekey.Key.relative.ToString());

                }
                parser.SaveSettings();
                MessageBox.Show("Settings Saved!");
            }
            else
            {
                MessageBox.Show("You did not save your settings.");
            }
            saveFiles.Dispose();
            saveFiles = null;
            HookManager.KeyDown += new KeyEventHandler(HookManager_KeyDown);
            
        }

        //Load Button
        private void pictureBox45_Click(object sender, EventArgs e)
        {
            OpenFileDialog loadFiles = new OpenFileDialog();
            loadFiles.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\Turbo-Keys\";
            loadFiles.DefaultExt = "ini";
            loadFiles.Filter = "Turbo-Keys Settings Files (*.INI)|*.ini";
            loadFiles.FilterIndex = 1;
            loadFiles.FileName = "";

            if (loadFiles.ShowDialog() == DialogResult.OK)
            {
                StringBuilder filenamebuilder = new StringBuilder();

                IniParser parser;

                if (loadFiles.FileName.Contains("ini"))
                {
                    parser = new IniParser(loadFiles.FileName);
                }
                else
                {
                    filenamebuilder.Append(loadFiles.FileName);
                    filenamebuilder.Append(".ini");
                    parser = new IniParser(filenamebuilder.ToString());
                }

                foreach (KeyValuePair<mousekey, string> mousekey in keyList)
                {
                    //Builds the strings from the .ini files based off the current mousekey
                    StringBuilder clickname = new StringBuilder();
                    StringBuilder xname = new StringBuilder();
                    StringBuilder yname = new StringBuilder();

                    clickname.Append("left");
                    clickname.Append(mousekey.Key.mKey);

                    xname.Append("xmove");
                    xname.Append(mousekey.Key.mKey);

                    yname.Append("ymove");
                    yname.Append(mousekey.Key.mKey);

                    string keyString = mousekey.Key.mKey.ToString();
                    string xNameString = xname.ToString();
                    string yNameString = yname.ToString();
                    string clickString = clickname.ToString();

                    string xValue = parser.GetSetting(keyString, xNameString);
                    string yValue = parser.GetSetting(keyString, yNameString);
                    string clickValue = parser.GetSetting(keyString, clickString);
                    string relativeValue = parser.GetSetting(keyString, "relative");

                    //If the string is not null, but 0 length then the convert function will crash

                    if (clickValue != null && clickValue.Length >= 1)
                        mousekey.Key.clickType = Convert.ToInt32(clickValue);
                    if (yValue != null && yValue.Length >= 1)
                        mousekey.Key.yDistance = Convert.ToInt32(yValue);
                    if (xValue != null && xValue.Length >= 1)
                        mousekey.Key.xDistance = Convert.ToInt32(xValue);
                    if (relativeValue != null && relativeValue.Length >= 1)
                        mousekey.Key.relative = Convert.ToBoolean(relativeValue);
                    if (relativeValue == null)
                        mousekey.Key.relative = true;
                    mousekey.Key.setBlack();
                    currentkey.setBlack();
                    radioButton1.Visible = false;
                    radioButton2.Visible = false;

                }

                MessageBox.Show(" Settings Loaded! \n\n Remember you need to turn each \n Turbo-Key on before use.");
            }
            else
            {
                MessageBox.Show("You did not load any settings");
            }
            loadFiles.Dispose();
            loadFiles = null;
        }

        #endregion

        private void pictureBox52_Click(object sender, EventArgs e)
        {
            clickSwitch = 0;
            HookManager.MouseUp += new MouseEventHandler(HookManager_MouseClick);
            this.WindowState = FormWindowState.Minimized;
        }

        void HookManager_MouseClick(object sender, MouseEventArgs e)
        {
            if (currentkey != null && label7.Text.Length > 0)
            {
                switch (clickSwitch)
                {
                    case 0:
                        mouseXstart = e.X;
                        mouseYstart = e.Y;
                        clickSwitch = 1;
                        break;
                    case 1:
                        HookManager.MouseUp -= new MouseEventHandler(HookManager_MouseClick);
                        mouseXend = e.X;
                        mouseYend = e.Y;

                        mouseXsend = mouseXend - mouseXstart;
                        mouseYsend = mouseYend - mouseYstart;

                        currentkey.xDistance = (int)mouseXsend;
                        currentkey.yDistance = (int)mouseYsend;

                        label6.Text = mouseXsend.ToString() + " px";
                        label5.Text = mouseYsend.ToString() + " px";
                        clickSwitch = 2;

                        radioButton1.Checked = true;
                        radioButton2.Checked = false;
                        currentkey.relative = true;
                        this.WindowState = FormWindowState.Normal;
                        break;
                    case 4:
                        break;

                }
            }
            else
            {
                HookManager.MouseUp -= new MouseEventHandler(HookManager_MouseClick);
                this.WindowState = FormWindowState.Normal;
            }
        }

        //Sets absolute coordinates
        private void pictureBox53_Click(object sender, EventArgs e)
        {
            HookManager.MouseUp += new MouseEventHandler(HookManager_MouseUp);
            
            this.WindowState = FormWindowState.Minimized;
        }

        void HookManager_MouseUp(object sender, MouseEventArgs e)
        {
            
            HookManager.MouseUp -= new MouseEventHandler(HookManager_MouseUp);

            currentkey.xDistance = Cursor.Position.X;
            currentkey.yDistance = Cursor.Position.Y;
            currentkey.relative = false;
            radioButton1.Checked = false;
            radioButton2.Checked = true;

            label6.Text = Cursor.Position.X.ToString() + " px";
            label5.Text = Cursor.Position.Y.ToString() + " px";
            
            this.WindowState = FormWindowState.Normal;
            
        }

       
        //Reset button
        private void pictureBox47_Click(object sender, EventArgs e)
        {
            DialogResult result = MessageBox.Show("Are you sure you're sure you want to reset?", "Turbo-Keys Reset", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (result == DialogResult.Yes)
            {
                radioButton1.Visible = false;
                radioButton2.Visible = false;
                deselectBoxes();
                currentkey.setBlack();
                foreach (KeyValuePair<mousekey, string> mousekey in keyList)
                {
                    mousekey.Key.clickType = 0;
                    mousekey.Key.mActivated = false;
                    mousekey.Key.xDistance = 0;
                    mousekey.Key.yDistance = 0;
                    mousekey.Key.setBlack();
                }    
            }
        }

        private void label2_Click_1(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked == true)
            {
                currentkey.relative = true;
            }
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton2.Checked == true)
            {
                currentkey.relative = false;
            }
        }

        private void pictureBox54_Click(object sender, EventArgs e)
        {
            settingsForm.mouseSpeed = mainMouseSpeed;
            settingsForm.clickDistance = mainClickDistance;
            settingsForm.clickSpeed = mainClickSpeed;
            settingsForm.FormClosed += new FormClosedEventHandler(settingsForm_FormClosed);
            settingsForm.ShowDialog();
        }

        void settingsForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            mainMouseSpeed = settingsForm.mouseSpeed;
            mainClickDistance = settingsForm.clickDistance;
            mainClickSpeed = settingsForm.clickSpeed;
            settingsForm.FormClosed -= new FormClosedEventHandler(settingsForm_FormClosed);
        }

        private void pictureBox57_Click(object sender, EventArgs e)
        {
            if (advanced) //Warning, this has to be backwards
            {
                advanced = false;
                pictureBox47.Show();
                pictureBox52.Show();
                pictureBox53.Show();
                textBox1.Hide();
                pictureBox58.Hide();
                pictureBox57.Image = Advanced;
            }
            else
            {
                advanced = true;
                pictureBox47.Hide();
                pictureBox52.Hide();
                pictureBox53.Hide();
                textBox1.Show();
                pictureBox58.Show();
                pictureBox57.Image = AdvancedBlue;
            }
        }
    }
}
