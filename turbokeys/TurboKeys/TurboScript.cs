using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace TurboKeys
{
    public class TurboScript
    {
        //Command Parser
        void Parser(string pScript)
        {
            string[] ScriptSplit = Regex.Split(pScript, "\r\n");
            List<string> ScriptList = ScriptSplit.ToList();


        }

        //Controller
        void Controller(string pCommandName, string[] pParameters)
        {
            switch (pCommandName.ToLowerInvariant())
            {
                case "move":
                    break;
                case "pause":
                    break;
                case "click":
                    break;
                case "loop":
                    break;
                case "imagesearch":
                    break;
                default:
                    break;
            }
        }

        //Move
        void Move(string[] pParameters) { }

        //Pause
        void Pause(string[] pParameters) { }

        //Click
        void Click(string[] pParameters) { }

        //Loop?
        void Loop(string[] pParameters) { }

        //Imagesearch 
        void Imagesearch(string[] pParameters) { }
    }
}
