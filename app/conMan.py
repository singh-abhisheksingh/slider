import os, ghostscript, sys, locale, glob
from PyPDF2 import PdfFileMerger

def Slide_Extractor():

	files = glob.glob('./media/*')
	print ("REMOVING FILES: ", files)
	for f in files:
		os.remove(f)

	slide_directory = os.listdir('./uploads')
	ppt_list = []
	for ppt in slide_directory:
		if ppt.endswith('.pptx') or ppt.endswith('.ppt'):
			ppt_list.append(ppt)
	print (ppt_list)

	directory = os.getcwd()
	directory = directory + '/uploads'
	os.chdir(directory)

	for element in ppt_list:
		command = os.popen('unoconv -f pdf ' + element)
		command.close()

	merger = PdfFileMerger()

	pdf_directory = os.listdir()
	pdf_list = []
	for pdf in pdf_directory:
		if pdf.endswith('.pdf'):
			pdf_list.append(pdf)
			merger.append(pdf)
	print (pdf_list)

	directory = directory + '/../media'
	os.chdir(directory)
	print (os.getcwd())

	merger.write("combine.pdf")

	args = ["gs", "-q", "-o", "image%d.png", "-sDEVICE=pngalpha", "combine.pdf"]
	encoding = locale.getpreferredencoding()

	args = [a.encode(encoding) for a in args]
	ghostscript.Ghostscript(*args)

	image_directory = os.listdir()
	image_list = []
	for image in image_directory:
		if image.endswith('.png'):
			image_list.append(image)
	print (image_list)
	print (len(image_list))

	directory = directory + '/..'
	os.chdir(directory)
	print (os.getcwd())

	return (len(image_list))