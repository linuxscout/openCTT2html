import webview
import sys
import time
sys.path.append('../')
import timetable.tm as tm
class mywebviewer:
    def __init__(self,):
        pass
        self.filename = None
        # parser 
        self.parser = tm.html_displayer()
    def load_css(self, window, ):
        filepath = "./timetable/css/style.css"
        try:
            cssfile = open(filepath)
        except:
            print("Can't open CSS file", filepath)
            sys.exit()

        csstring = cssfile.read()
        # ~ print("CSS:", csstring)
        window.load_css(csstring)
    def open_file_dialog(self, window):
        
        time.sleep(3)
        file_types = ('TimeTable (*.oct)', 'All files (*.*)')

        filenames = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        print(filenames[0])
        self.filename = filenames[0]
        self.parser = tm.html_displayer(self.filename)
        window.load_url("resources/html/main.html")
        # ~ window.toggle_fullscreen()
        # ~ result = self.update("default")

        # ~ window.load_html(result)
        # ~ self.load_css(window)        
    
    def update(self, command):
        result = "Nothing"
        if command == "default":
            command = "timetables_groups"
        # ~ if command == "freerooms":
            # ~ room_type = self.rooms_opt.get()
            # ~ if room_type and room_type!="all":
                # ~ command +="_"+room_type
            # ~ result = self.parser.action(command)          
        # ~ elif command == "teachers":
            # ~ command = "availableteachers"
            # ~ teacher_type = self.teacher_opt.get()
            # ~ if teacher_type and teacher_type!="all":
                # ~ command +="_"+teacher_type
            # ~ result = self.parser.action(command)          
        # ~ elif command == "timetables":
            # ~ slot_type = self.tm_opt.get()
            # ~ if slot_type and slot_type!="all":
                # ~ command +="_"+slot_type
            result = self.parser.action(command)          
        if command == "affectation":
            result = self.parser.action(command)          
        elif command == "charges":
            result = self.parser.action(command)          
        elif command in self.parser.commands:
            result = self.parser.action(command) 
        else: # reset
            donothing()
            result = "Nothing to do with %s"%command
        return result

if __name__ == '__main__':
    viewer = mywebviewer()
    window = webview.create_window('Open file dialog', 'https://pywebview.flowrl.com/hello')
    webview.start(viewer.open_file_dialog, window)
    # ~ webview.start(viewer.load_css, window)

