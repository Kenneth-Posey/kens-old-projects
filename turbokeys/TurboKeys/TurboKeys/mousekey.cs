using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Resources;
using System.Reflection;
using MouseKeyboardLibrary;
using System.Threading;
using Gma.UserActivityMonitor;

namespace TurboKeys
{
    public class mousekey
    {

        public PictureBox mPictureCurrent { get; set; }
        public Image mPictureBlack { get; set; }
        public Image mPictureGreen { get; set; }
        public Image mPictureYellow { get; set; }
        public bool mSelected { get; set; }
        public bool mActivated { get; set; }
        public int xDistance { get; set; }
        public int yDistance { get; set; }
        public int clickType { get; set; }
        public Label mCurrentKeyLabel { get; set; }
        public Label mXMovement { get; set; }
        public Label mYMovement { get; set; }
        public string mKey { get; set; }
        public bool relative { get; set; }
        public int clickSpeed { get; set; }    

        public void setGreen()
        {
            mPictureCurrent.Image = mPictureGreen;
            mSelected = false;
            mActivated = true;
            mCurrentKeyLabel.Text = "";
            mXMovement.Text = "";
            mYMovement.Text = "";
            Console.WriteLine("Set Green " + mCurrentKeyLabel.Text);
        }

        public void setBlack()
        {
            mPictureCurrent.Image = mPictureBlack;
            mSelected = false;
            mActivated = false;
            mCurrentKeyLabel.Text = "";
            mXMovement.Text = "";
            mYMovement.Text = "";
            Console.WriteLine("Set Black " + mCurrentKeyLabel.Text);
        }

        public void setYellow()
        {
            mPictureCurrent.Image = mPictureYellow;
            mSelected = true;
            mCurrentKeyLabel.Text = mKey;
            mXMovement.Text = xDistance.ToString() + " px";
            mYMovement.Text = yDistance.ToString() + " px";
            Console.WriteLine("Set Yellow " + mCurrentKeyLabel.Text);

        }


        public void activate(int speed, int distance, int pClickSpeed)
        {
            int xFinish;
            int yFinish;
            clickSpeed = pClickSpeed;

            if (mActivated == true)
            {
                Random sleeprand = new Random(); 
                switch (clickType)
                {
                    case 1:
                        if (relative == true)
                        {
                            xFinish = Cursor.Position.X + xDistance;
                            yFinish = Cursor.Position.Y + yDistance;

                            move(Cursor.Position.X, Cursor.Position.Y, xFinish, yFinish, speed);
                            leftClick(distance);
                        }
                        else
                        {
                            xFinish = xDistance;
                            yFinish = yDistance;

                            move(Cursor.Position.X, Cursor.Position.Y, xFinish, yFinish, speed);
                            leftClick(distance);
                        }
                        break;
                    case 2:
                        if (relative == true)
                        {
                            xFinish = Cursor.Position.X + xDistance;
                            yFinish = Cursor.Position.Y + yDistance;

                            move(Cursor.Position.X, Cursor.Position.Y, xFinish, yFinish, speed); 
                            rightClick(distance);
                        }
                        else
                        {
                            xFinish = xDistance;
                            yFinish = yDistance;

                            move(Cursor.Position.X, Cursor.Position.Y, xFinish, yFinish, speed);
                            rightClick(distance);
                        }
                        break;
                    default:
                        if (relative == true)
                        {
                            xFinish = Cursor.Position.X + xDistance;
                            yFinish = Cursor.Position.Y + yDistance;

                            move(Cursor.Position.X, Cursor.Position.Y, xFinish, yFinish, speed);
                            mouseAdjust(distance);
                        }
                        else
                        {
                            xFinish = xDistance;
                            yFinish = yDistance;

                            move(Cursor.Position.X, Cursor.Position.Y, xFinish, yFinish, speed);
                            mouseAdjust(distance);
                        }
                        break;
                }
            }
        }

        private void move(double xStart, double yStart, double xFinish, double yFinish, double speed)
        {
            Point point = new Point();
            List<Point> points = new List<Point>();
            Random ampRand = new Random();

            //double distance = Math.Sqrt(Math.Pow((xFinish - xStart), 2) + Math.Pow((yFinish - yStart), 2));
            //double chunk = distance / speed;
            double differenceX = (xFinish - xStart);
            double differenceY = (yFinish - yStart);
            Console.WriteLine("Speed: " + speed);
            if (Math.Abs(differenceX) < speed && 
                Math.Abs(differenceY) < speed && 
                Math.Abs(differenceX) <= Math.Abs(differenceY))
                speed = Math.Abs(differenceY);
            if (Math.Abs(differenceY) < speed && 
                Math.Abs(differenceX) < speed && 
                Math.Abs(differenceY) <= Math.Abs(differenceX))
                speed = Math.Abs(differenceX);
            Console.WriteLine("New Speed: " + speed);

            double chunkX = differenceX / speed;
            double chunkY = differenceY / speed;
            double i = 0;
            Random time = new Random();
            if (speed > 0)
            {
                while (i <= speed) //(Cursor.Position.X <= xFinish && Cursor.Position.Y <= yFinish)
                {
                    point.X = (int)(xStart + chunkX * i);
                    point.Y = (int)(yStart + chunkY * i);
                    points.Add(point);

                    i++;
                }

                foreach (Point p in points)
                {
                    MouseSimulator.X = p.X;
                    MouseSimulator.Y = p.Y;
                    double sleeptime = time.NextDouble();
                    Thread.Sleep((int) (sleeptime * speed / 10) + 1);
                }
            }
            else
            {
                MouseSimulator.X = (int) xFinish;
                MouseSimulator.Y = (int) yFinish;
            }
        }

        private void leftClick(int distance)
        {
            Random rand = new Random();

            if (clickSpeed == null)
                clickSpeed = rand.Next(1, 20);

            int posX = rand.Next((-1 * distance), distance);
            int posY = rand.Next((-1 * distance), distance);
            int sleeptime = clickSpeed;

            MouseSimulator.X = Cursor.Position.X + posX;
            MouseSimulator.Y = Cursor.Position.Y + posY;
            Console.WriteLine("posX = " + posX + " posY = " + posY);
            MouseSimulator.MouseDown(MouseButtons.Left);
            Thread.Sleep(sleeptime);
            MouseSimulator.MouseUp(MouseButtons.Left);
        }

        private void rightClick(int distance)
        {
            Random rand = new Random();

            if (clickSpeed == null)
                clickSpeed = rand.Next(1, 20);

            int posX = rand.Next((-1 * distance), distance);
            int posY = rand.Next((-1 * distance), distance);
            int sleeptime = clickSpeed;

            MouseSimulator.X = Cursor.Position.X + posX;
            MouseSimulator.Y = Cursor.Position.Y + posY;
            Console.WriteLine("posX = " + posX + " posY = " + posY);
            MouseSimulator.MouseDown(MouseButtons.Right);
            Thread.Sleep(sleeptime);
            MouseSimulator.MouseUp(MouseButtons.Right);
        }

        private void mouseAdjust(int distance)
        {
            Random rand = new Random();

            int posX = rand.Next((-1 * distance), distance);
            int posY = rand.Next((-1 * distance), distance);

            MouseSimulator.X = Cursor.Position.X + posX;
            MouseSimulator.Y = Cursor.Position.Y + posY;
            Console.WriteLine("posX = " + posX + " posY = " + posY);
        }
    }
}
