import sys, os, PythonMagick, PyPDF2

class magazine(object):

    def getNumberOfPages(self, pdfPath):
        pdf_im = pyPdf.PdfFileReader(file(pdfPath, "rb"))
        return pdf_im.getNumPages()            

    def saveFrontCoverImage(self, pdfPath):
        if (os.path.isfile(pdfPath)):
            im = PythonMagick.Image()
            im.density('300')
            im.read(pdfPath + '[0]')
            im.write(pdfPath[:-3] + 'png')

magazine = magazine()
magazine.saveFrontCoverImage('test.pdf')

sys.exit(0)



print('Converting %d pages.' % npage)
for p in range(npage):
    im = PythonMagick.Image()
    im.density('300')
    im.read(pdf + '[' + str(p) +']')
    im.write('file_out-' + str(p)+ '.png')

sys.exit(0)

p = PythonMagick.Image()    
p.density('300')
#p.read(pdf)
#p.write('doc.jpg')
image = PythonMagick.Image(pdf)
image.write('doc.jpg')
image.transform('300x300')
image.write('doc_small.jpg')
