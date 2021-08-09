#/usr/bin/sh
# Build OpenCTT2 html: Latex tools

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
publish:
	git push origin master 

run:
	python3 timetable_webviewer.py
gui:
	python3 timetablegui.py 
exe:
	pyinstaller timetable_webviewer.spec
