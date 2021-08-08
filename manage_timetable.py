#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  manage_timetable.py
#  
#  Copyright 2017 zerrouki <zerrouki@majd4>
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

if __name__ == "__main__":
    import sys
    sys.path.append('../support')
    sys.path.append('../')

import re
import string
import datetime
import getopt
import os
import xml.dom.minidom as minidom
import timetable.tm as tm


scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
def usage():
# "Display usage options"
    print("(C) CopyLeft 2012, %s"%AuthorName)
    print("Usage: %s -f filename [OPTIONS]" % scriptname)
    print(u"       %s 'السلام عليكم' [OPTIONS]\n" % scriptname);
#"Display usage options"
    print("\t[-f | --file= filename]input file to %s"%scriptname)
    print("\t[-h | --help]     outputs this usage message")
    print("\t[-v | --version]  program version")
    print("\t[-l | --limit]    treat only a limited number of line")
    print("\t[-t | --stat]     enable statistics display")
    print("\r\nThis program is licensed under the GPL License\n")

def grabargs():
#  "Grab command-line arguments"
    fname = ''
    options={
    'limit':False,
}
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVtlv:f:l:",
                               ["help", "version","stat", "limit=", "file="],)
    except getopt.GetoptError:
        usage()
        sys.exit(0)
    for o, val in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-V", "--version"):
            print(scriptversion)
            sys.exit(0)
        if o in ("-t", "--stat"):
            options['stat'] = True;
        if o in ("-l", "--limit"):
            try: options['limit'] = int(val);
            except: options['limit']=0;

        if o in ("-f", "--file"):
            fname = val
    utfargs=[]
    for a in args:
        # ~ utfargs.append( a.decode('utf8'));
        utfargs.append( a);
    text= u' '.join(utfargs);

    #if text: print text.encode('utf8');
    return (fname, options)
                
def main():
    
    filename, options = grabargs()
    
    try:
        xmldoc = minidom.parse(filename)
    except:
        print( "Can't Open the file", filename)
        sys.exit()
    # test add course
    given_group_name = "1MI 01"
    table_course ={}
    table_course['id'] = "100"
    table_course['name'] = "Physiologie"
    table_course['short_name'] = "Physiologie"
    table_course['course_type'] = "TD"
    table_course['num_of_lessons_per_week'] = "1"
    table_course['num_of_enrolled_students'] = "35"
    table_course['group_name'] = ""
    table_course['teacher_id'] = "12"
    table_course['extid'] = ""
    table_course['allowed_classrooms'] = ""
    # test add course 
    parser = tm.html_displayer(filename)
    xmldoc = parser.add_course(table_course, given_group_name)
    # test add courses

    commands = ["freerooms", "charge", "groups"]
    result = ""
    for cmd  in commands:
        result += "\n"+ parser.action(cmd)
    # ~ print(parser.display_html())
    # ~ result = parser.action(cmd, True)    
    print(result)


if __name__ == '__main__':
    main()

