from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("document.pdf", "rb"))

#splitting pdf into single pages:
#change range parameters if you want each PDFs to be exact n pages
# example: for i in range(1, inputpdf.numPages, 3)

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)
