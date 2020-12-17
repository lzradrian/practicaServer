using iText.Forms;
using iText.Kernel.Pdf;
using System;
using System.Collections.Generic;
using System.Text;

namespace FormEditor
{
    class FormEditorService
    {
        public static void FillOutForm(string inputFile, string outputFile, Dictionary<String, String> inputFields)
        {
            PdfReader reader = new PdfReader(inputFile);
            PdfWriter writer = new PdfWriter(outputFile);
            PdfDocument pdfDoc = new PdfDocument(reader, writer);
            var form = PdfAcroForm.GetAcroForm(pdfDoc, true);
            var fields = form.GetFormFields();
            /*foreach(var pair in fields)
            {
                Console.WriteLine(pair.Key);
            }*/
            foreach(var keyValuePair in inputFields)
            {
                fields[keyValuePair.Key].SetValue(keyValuePair.Value);
            }
            form.FlattenFields();
            pdfDoc.Close();
        }
    }
}
