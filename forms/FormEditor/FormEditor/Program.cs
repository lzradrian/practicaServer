using System;
using System.Collections.Generic;

namespace FormEditor
{
    class Program
    {
        static void Main(string[] args)
        {
            String inputPdf = args[0];
            String inputTxt = args[1];
            String outputPdf = args[2];
            FormEditorService.FillOutPDF(inputPdf,
                                         outputPdf,
                                         ReadPDFFieldsFromFile(inputTxt));
        }

        static Dictionary<string, string> ReadPDFFieldsFromFile(string filepath)
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
                //Console.WriteLine("da");
                //Console.WriteLine(splitLine[0] + " " + splitLine[1]);
                fields[splitLine[0]] = String.Join(' ', GetSubarray(splitLine, 1, splitLine.Length - 1));
            }
            return fields;
        }

        static Dictionary<string, Tuple<int, int, int, string>> ReadExcelFieldsFromFile(string filepath)
        {
            Dictionary<string, Tuple<int, int, int, string>> fields = new Dictionary<string, Tuple<int, int, int, string>>();
            string[] lines = System.IO.File.ReadAllLines(filepath);
            foreach (var line in lines)
            {
                string[] splitLine = line.Split(' ');
                string value = String.Join(' ', GetSubarray(splitLine, 4, splitLine.Length - 4));
                fields[splitLine[1]] = new Tuple<int, int, int, string>(Int32.Parse(splitLine[0]), Int32.Parse(splitLine[2]), Int32.Parse(splitLine[3]), value);
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
