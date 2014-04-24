using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace TurboKeys
{
    public partial class Settings : Form
    {
        public int mouseSpeed { get; set; }
        public int clickDistance { get; set; }
        public int clickSpeed { get; set; }

        public Settings()
        {
            InitializeComponent();
        }

        private void Settings_Load(object sender, EventArgs e)
        {
            trackBar1.Value = mouseSpeed;
            trackBar2.Value = clickDistance;
            trackBar3.Value = clickSpeed;
            label7.Text = mouseSpeed.ToString();
            label8.Text = clickDistance.ToString();
            label9.Text = clickSpeed.ToString();
            pictureBox3.Cursor = Cursors.Hand;
            pictureBox4.Cursor = Cursors.Hand;
        }

        //Cursor Speed
        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            label7.Text = trackBar1.Value.ToString();
        }

        //Click Distance
        private void trackBar2_Scroll(object sender, EventArgs e)
        {
            label8.Text = trackBar2.Value.ToString();
        }

        //Click Speed
        private void trackBar3_Scroll(object sender, EventArgs e)
        {
            label9.Text = trackBar3.Value.ToString();
        }


        //Randomize
        private void pictureBox3_Click(object sender, EventArgs e)
        {
            Random rand = new Random();
            trackBar1.Value = rand.Next(1, trackBar1.Maximum);
            trackBar2.Value = rand.Next(1, trackBar2.Maximum);
            trackBar3.Value = rand.Next(1, trackBar3.Maximum);
            label7.Text = trackBar1.Value.ToString();
            label8.Text = trackBar2.Value.ToString();
            label9.Text = trackBar3.Value.ToString();
        }
        //Save
        private void pictureBox4_Click(object sender, EventArgs e)
        {
            this.mouseSpeed = trackBar1.Value;
            this.clickDistance = trackBar2.Value;
            this.clickSpeed = trackBar3.Value;
            this.Close();
        }

        private void label12_Click(object sender, EventArgs e)
        {

        }

        private void trackBar3_Scroll_1(object sender, EventArgs e)
        {

        }


    }
}
