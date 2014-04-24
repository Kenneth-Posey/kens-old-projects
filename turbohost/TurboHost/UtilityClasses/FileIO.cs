using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using TurboHost.UtilityClasses;
using System.IO;

namespace TurboHost
{
    class FileIO
    {
        public string FolderPath { get; set; }

        public FileIO()
        {
            FolderPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + @"\TurboHost-Screenshots\";
            CheckScreenshotDirectory();
            CheckSettingsFile();
        }

        private void CheckSettingsFile()
        {
            bool tFileExists = File.Exists(GetSettingsFilePath());
            if (!tFileExists)
            {
                FileStream tNewFile = File.Create(GetSettingsFilePath());
                tNewFile.Close();
            }
        }

        public string GetSettingsFilePath()
        {
            string tFileName = "TurboHostSettings.ini";
            tFileName = FolderPath + tFileName;
            return tFileName;
        }

        private void CheckScreenshotDirectory()
        {
            bool tDirectoryExists = Directory.Exists(FolderPath);
            if (!tDirectoryExists)
                Directory.CreateDirectory(FolderPath);
        }
    }
}
