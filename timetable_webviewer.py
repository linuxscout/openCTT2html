#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  jsapi.py
#  
#  Copyright 2021 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import threading
import time
import sys
import random
import webview
import web.webviewer as webviewer
from web.jsapi import Api


if __name__ == '__main__':

    filename = "resources/html/main.html"
    viewer = webviewer.mywebviewer()    
    # welcome window
    welcomefilename = "resources/html/welcome.html"

    # ~ window_welcome = webview.create_window('Welcome', welcomefilename)
    # ~ webview.start(viewer.destroy, window_welcome)
    # ~ time.sleep(3)

    # main window
    api = Api(viewer)
    window = webview.create_window('Open file dialog', welcomefilename, js_api=api, )
    webview.start(api.viewer.open_file_dialog, window, debug=True)        
    # ~ window = webview.create_window('API example', html=htmlcontent, js_api=api)
    # ~ window = webview.create_window('API example', filename, js_api=api)
    # ~ webview.start()

