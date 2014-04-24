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
    public partial class TextReplacements : Form
    {
        public string tTextboxContents { get; set; }
        public bool tUpdateText { get; set; }
        public TextReplacements()
        {
            InitializeComponent();
        }

        private void TextReplacements_Load(object sender, EventArgs e)
        {
            textBox1.Text = tTextboxContents;
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            tTextboxContents = textBox1.Text;
            tUpdateText = true;
            this.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            tUpdateText = false;
            this.Close();
        }
    }
}
