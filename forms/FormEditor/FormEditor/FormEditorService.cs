using iText.Forms;
using iText.Kernel.Pdf;
using OfficeOpenXml;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace FormEditor
{
    class FormEditorService
    {
        public static void FillOutPDF(string inputFile, string outputFile, Dictionary<String, String> inputFields)
        {
            PdfReader reader = new PdfReader(inputFile);
            PdfWriter writer = new PdfWriter(outputFile);
            PdfDocument pdfDoc = new PdfDocument(reader, writer);
            var form = PdfAcroForm.GetAcroForm(pdfDoc, true);
            var fields = form.GetFormFields();
            foreach(var field in fields)
            {
                //Console.WriteLine(field.Key);
            }
            foreach(var keyValuePair in inputFields)
            {
                fields[keyValuePair.Key].SetValue(keyValuePair.Value);
            }
            form.FlattenFields();
            pdfDoc.Close();
        }

        public static void FillOutExcel(string inputFile, Dictionary<String, Tuple<int, int, int, String>> inputFields)
        {
            FileInfo fileInfo = new FileInfo(inputFile);
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
            ExcelPackage package = new ExcelPackage(fileInfo);
            ExcelWorksheet worksheet = package.Workbook.Worksheets.FirstOrDefault();

            foreach(var KeyValuePair in inputFields)
            {
                int type = KeyValuePair.Value.Item1;
                int row = KeyValuePair.Value.Item2;
                int column = KeyValuePair.Value.Item3;
                string value = KeyValuePair.Value.Item4;
                switch(type)
                {
                    case 1:
                    {
                        worksheet.Cells[row, column].Value = value;
                        break;
                    }
                    case 2:
                    {
                        if(value != "-")
                        {
                            worksheet.Cells[row, column].Value = value;
                        }
                        break;
                    }
                    case 3:
                    {
                        worksheet.Cells[row, column].Value = "x";
                        break;
                    }
                    default:
                    {
                        throw new InvalidOperationException("");
                    }
                }
            }

            package.Save();
        }
    }
}
