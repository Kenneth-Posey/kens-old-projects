using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace TurboHost
{
    public partial class NewBet : Form
    {
        public string tPlayerOne { get; set; }
        public string tPlayerTwo { get; set; }
        public string tBet { get; set; }

        public int tX { get; set; }
        public int tY { get; set; }

        public NewBet()
        {
            InitializeComponent();
        }

        private void NewBet_Load(object sender, EventArgs e)
        {
            if (tX == null || tX < 0)
            {
                tX = 0;
            }
            if (tY == null || tY < 0)
            {
                tY = 0;
            }
            this.Location = new Point(tX, tY);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (textBox1.Text != null && textBox1.Text.Trim().Length > 0) tPlayerOne = textBox1.Text.Trim().Replace(" ", "_");
            if (textBox2.Text != null && textBox2.Text.Trim().Length > 0) tPlayerTwo = textBox2.Text.Trim().Replace(" ", "_");
            if (textBox3.Text != null && textBox3.Text.Trim().Length > 0) tBet = textBox3.Text.Trim();
            tX = this.Location.X;
            tY = this.Location.Y;
            this.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Close();
        }

    }
}
