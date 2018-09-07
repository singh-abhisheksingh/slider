import os
import win32com.client
import pythoncom

def Slide_Extractor():
	pythoncom.CoInitialize()
	slide_directory = os.listdir('./uploads')
	print (slide_directory)
	ppt_list = []
	for ppt in slide_directory:
		if ppt.endswith('.pptx') or ppt.endswith('.ppt'):
			ppt_list.append(ppt)
	print (ppt_list)

	Application = win32com.client.Dispatch("PowerPoint.Application")
	Application.Visible = True

	slide_count = 0
	old_count = 0

	for element in ppt_list:
		print(element, type(element))
		path = os.listdir('./uploads')
		print(path, type(path))
		if(element in path):
			print("Yes")
		print(str(path)+element)
		Presentation = Application.Presentations.Open('D:/slider/app/uploads/'+element)

		slide_count = slide_count + len(Presentation.Slides)
		print (slide_count)

		for c in range(old_count, slide_count):
			Presentation.Slides[c-old_count].Export(r'D:\slider\app\media\image{0}.jpg'.format(c), "JPG", 1366, 768)

		old_count = slide_count

	Application.Quit()

	return slide_count

def Content():
	
	IMAGE_LIST = []
	count = Slide_Extractor()
	for i in range(0,count):
		IMAGE_LIST.append("image{0}.jpg".format(i))

	print(IMAGE_LIST)

	return IMAGE_LIST


def Display():
	slide_directory = os.listdir('./uploads')
	print (slide_directory)
	ppt_list = []
	for ppt in slide_directory:
		if ppt.endswith('.pptx') or ppt.endswith('.ppt'):
			ppt_list.append(ppt)
	print (ppt_list)
	return ppt_list


def Delete(file_name):
	if(file_name[:3] == "yes"):
		file_name = file_name[4:]
		os.remove("./uploads/"+file_name)
		slide_directory = os.listdir('./uploads')
		print (slide_directory)
	else:
		print("You did not want to delete")