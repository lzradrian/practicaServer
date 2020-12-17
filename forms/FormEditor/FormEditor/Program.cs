using System;
using System.Collections.Generic;

namespace FormEditor
{
    class Program
    {
        static void Main(string[] args)
        {
            FormEditorService.FillOutForm("../../../../../AcordPractica-Forms.pdf",
                                          "../../../../../AcordPractica-Forms-Filled.pdf",
                                          ReadFieldsFromFile("../../../../../mock_input.txt"));
        }

        static Dictionary<string, string> ReadFieldsFromFile(string filepath)
        {
            Dictionary<string, string> fields = new Dictionary<string, string>();
            string[] lines = System.IO.File.ReadAllLines(filepath);
            foreach(var line in lines)
            {
                string[] splitLine = line.Split(' ');
                if(splitLine.Length < 2)
                {
                    throw new ArgumentException("Field must contain at least a key and a value.");
                }
                fields[splitLine[0]] = String.Join(' ', GetSubarray(splitLine, 1, splitLine.Length - 1));
            }
            return fields;
        }

        static string[] GetSubarray(string[] array, int startIndex, int length)
        {
            string[] result = new string[length];
            Array.Copy(array, startIndex, result, 0, length);
            return result;

        }
    }
}
