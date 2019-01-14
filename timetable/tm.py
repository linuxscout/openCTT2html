#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testdom2.py
#  
#  

import xml.dom.minidom as minidom
import sys
import copy
import os.path

TERMS= {
"1":"08:00 - 09:30",
"2":"09:30 - 11:00",
"3":"11:00 - 12:30",
"4":"12:30 - 13:00",
"5":"13:00 - 14:30",
"6":"14:30 - 16:00",
}
DAYS= {
"1":"Samedi",
"2":"Dimanche",
"3":"Lundi",
"4":"Mardi",
"5":"Mercredi",
"6":"Jeudi",
}
TIMETABLE_TEMPLATE={
        # line terms, col: days
        #TERM N°1
        "1":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "2":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "3":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "4":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "5":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "6":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,
        } 
TIMETABLE_TEMPLATE_FORBIDDEN={
        # line terms, col: days
        #TERM N°1
        "1":{"1":{"course_type":"unvailable"}, "2":{"course_type":"unvailable"}, "3":{"course_type":"unvailable"}, "4":{"course_type":"unvailable"},"5":{"course_type":"unvailable"}, "6":{"course_type":"unvailable"}, }   ,  
        "2":{"1":{"course_type":"unvailable"}, "2":{"course_type":"unvailable"}, "3":{"course_type":"unvailable"}, "4":{"course_type":"unvailable"},"5":{"course_type":"unvailable"}, "6":{"course_type":"unvailable"}, }   ,   
        "3":{"1":{"course_type":"unvailable"}, "2":{"course_type":"unvailable"}, "3":{"course_type":"unvailable"}, "4":{"course_type":"unvailable"},"5":{"course_type":"unvailable"}, "6":{"course_type":"unvailable"}, }   ,  
        "4":{"1":{"course_type":"unvailable"}, "2":{"course_type":"unvailable"}, "3":{"course_type":"unvailable"}, "4":{"course_type":"unvailable"},"5":{"course_type":"unvailable"}, "6":{"course_type":"unvailable"}, }   ,  
        "5":{"1":{"course_type":"unvailable"}, "2":{"course_type":"unvailable"}, "3":{"course_type":"unvailable"}, "4":{"course_type":"unvailable"},"5":{"course_type":"unvailable"}, "6":{"course_type":"unvailable"}, }   ,   
        "6":{"1":{"course_type":"unvailable"}, "2":{"course_type":"unvailable"}, "3":{"course_type":"unvailable"}, "4":{"course_type":"unvailable"},"5":{"course_type":"unvailable"}, "6":{"course_type":"unvailable"}, }   ,
        }          
FREETIMETABLE_TEMPLATE ={       # line terms, col: days
        #TERM N°1
        "1":{"1":[], "2":[], "3":[], "4":[],"5":[], "6":[], }   ,  
        "2":{"1":[], "2":[], "3":[], "4":[],"5":[], "6":[], }   ,   
        "3":{"1":[], "2":[], "3":[], "4":[],"5":[], "6":[], }   ,  
        "4":{"1":[], "2":[], "3":[], "4":[],"5":[], "6":[], }   ,  
        "5":{"1":[], "2":[], "3":[], "4":[],"5":[], "6":[], }   ,   
        "6":{"1":[], "2":[], "3":[], "4":[],"5":[], "6":[], }   ,
        } 
class openclassModel:
    def __init__(self, filename = None):
        """ load the file if defined,
        else, we can load the  file with other method
        """

        self.xmldoc = None
        selfteachers    = None
        self.courses    = None
        self.groups    = None
        self.classrooms  = None       
        self.courses_assignation = []
        if filename:
            self.load(filename)
        else:
            pass
    
    def load(self, filename):
        """ load the xml file """
        try:
            xmldoc = minidom.parse(filename)
        except:
            print "Can't Open the file", DATA_FILE
            sys.exit()
        self.xmldoc = xmldoc
        selfteachers    = self.read_teachers()
        self.courses, self.groups    = self.read_courses()
        self.classrooms  = self.read_classrooms()
        self.courses_assignation = self.calcul_courses_assignation()
        self.read_slots()
           
            
    def read_courses(self):
        #get courses
        """
          <course id="152">
          <name>Physique 1</name>
          <short_name>Physique 1-G11</short_name>
          <course_type>TD</course_type>
          <num_of_lessons_per_week>1</num_of_lessons_per_week>
          <num_of_enrolled_students>25</num_of_enrolled_students>
          <group_name>
          </group_name>
          <teacher_id>62</teacher_id>
          <extid>
          </extid>
          <allowed_classrooms>
          <classroom_id>4</classroom_id>
          </allowed_classrooms>
        """
        xmldoc = self.xmldoc
        edu_programs = xmldoc.getElementsByTagName('edu_program')
        courses_table ={}
        groups_table = {}
        for edu_program in   edu_programs:
              
            group_name = edu_program.getElementsByTagName('name')[0].firstChild.data
            groups_table[group_name]= {"courses":[],
                "timetable":copy.deepcopy(TIMETABLE_TEMPLATE)
            }
            courses = edu_program.getElementsByTagName('course')
            # display personne by personne
            for course in courses:
                #~ print "course n°", course.getAttribute('id') 
                #~ print "Name", course.getElementsByTagName('name')[0].firstChild.data
                #~ print "course_type", course.getElementsByTagName('course_type')[0].firstChild.data
                #~ print "num_of_lessons_per_week", course.getElementsByTagName('num_of_lessons_per_week')[0].firstChild.data
                #~ print "teacher_id", course.getElementsByTagName('teacher_id')[0].firstChild.data 
                #~ # get number of courses to hold together
                #~ print "together_courses_nb", course.getElementsByTagName('course_id').length

                courses_table[course.getAttribute('id')] = {
                "name": course.getElementsByTagName('name')[0].firstChild.data,
                "course_type": course.getElementsByTagName('course_type')[0].firstChild.data,
                "short_name": course.getElementsByTagName('short_name')[0].firstChild.data,
                "num_of_lessons_per_week": course.getElementsByTagName('num_of_lessons_per_week')[0].firstChild.data,
                "teacher_id": course.getElementsByTagName('teacher_id')[0].firstChild.data,
                "together_courses_nb": course.getElementsByTagName('course_id').length,
                "group_name": group_name,
                "timetable":copy.deepcopy(TIMETABLE_TEMPLATE)

                
                }
                groups_table[group_name]["courses"].append(course.getAttribute('id'))

        self.courses = courses_table
        self.groups =groups_table
        return courses_table, groups_table

    def read_classrooms(self):
        """
        <classroom id="1">
          <name>Amphi 5</name>
          <extid>
          </extid>
          <capacity>1000</capacity>
          <spec_slots type="unallowed">
            <spec_slot>
              <day_index>1</day_index>
              <term_index>4</term_index>
            </spec_slot>
            <spec_slot>
              <day_index>2</day_index>
              <term_index>4</term_index>
            </spec_slot>
        """
        xmldoc = self.xmldoc
        #get classrooms
        classrooms = xmldoc.getElementsByTagName('classroom')
        #~ print classrooms
        classrooms_table ={}
        # display personne by personne
        for classroom  in classrooms:
            cid = classroom.getAttribute('id')
            cname = classroom.getElementsByTagName('name')[0].firstChild.data
            classrooms_table[cid]= {'name':cname,
                "timetable":copy.deepcopy(TIMETABLE_TEMPLATE)
            }
            # add type to classes
            if "tp" in cname.lower():
                classrooms_table[cid]['type'] = "tp"
            elif "amphi" in cname.lower():
                classrooms_table[cid]['type'] = "amphi"
            else:
                classrooms_table[cid]['type'] = "salle"
            #un allowed slot
            spec_type= classroom.getElementsByTagName('spec_slots')[0].getAttribute("type")
            if spec_type.lower() == "allowed":
                classrooms_table[cid]["timetable"] = copy.deepcopy(TIMETABLE_TEMPLATE_FORBIDDEN)
            slots = classroom.getElementsByTagName('spec_slot')
            for slot in slots:
                term_index = slot.getElementsByTagName('term_index')[0].firstChild.data
                day_index = slot.getElementsByTagName('day_index')[0].firstChild.data
                if spec_type.lower() == "unallowed":             
                    classrooms_table[cid]["timetable"][term_index][day_index] = {"course_type":"unvailable"}
                else:
                    classrooms_table[cid]["timetable"][term_index][day_index] = {}

         
        self.classrooms =  classrooms_table
        return self.classrooms
    
    def read_teachers(self):
        xmldoc = self.xmldoc
        #get teachers
        teachers = xmldoc.getElementsByTagName('teacher')
        #~ print teachers
        teachers_table ={}
        # display personne by personne
        for teacher  in teachers:
            teachers_table[teacher.getAttribute('id')]= {'name':teacher.getElementsByTagName('name')[0].firstChild.data,
                 "last_name": teacher.getElementsByTagName('last_name')[0].firstChild.data,
                 "title": teacher.getElementsByTagName('title')[0].firstChild.data,
                 "edu_rank": teacher.getElementsByTagName('edu_rank')[0].firstChild.data,
                 "extid": teacher.getElementsByTagName('extid')[0].firstChild.data,
                 "TD":0, "COURS":0, "TP":0,
                "timetable":copy.deepcopy(TIMETABLE_TEMPLATE) 

             }       
        self.teachers = teachers_table
        return self.teachers
    def read_slots(self):
        """
        <lesson_in_tt>
            <course_id>384</course_id>
            <day_index>4</day_index>
            <term_index>2</term_index>
            <classroom_id>6</classroom_id>
        </lesson_in_tt>
        """
        xmldoc = self.xmldoc 
        courses = self.courses
        teachers = self.teachers
        classrooms = self.classrooms
        groups = self.groups
        #get slots
        slots = xmldoc.getElementsByTagName('lesson_in_tt')
        #~ print slots
        slots_table ={"teachers":{},
        "groups":{},
        "classrooms":{},
        }
        # get element
        for slot in slots:
            course_id = slot.getElementsByTagName('course_id')[0].firstChild.data
            teacher_id = courses.get(course_id,{}).get("teacher_id","0")
            teacher_name = teachers.get(teacher_id,{}).get("name","")[0] +". " +teachers.get(teacher_id,{}).get("last_name","")
            course_type = courses.get(course_id,{}).get("course_type","0")
            course_name = courses.get(course_id,{}).get("name","0")
            short_name = courses.get(course_id,{}).get("short_name","0")
            group_name = courses.get(course_id,{}).get("group_name","0")
            day_index = slot.getElementsByTagName('day_index')[0].firstChild.data
            term_index = slot.getElementsByTagName('term_index')[0].firstChild.data
            classroom_id = slot.getElementsByTagName('classroom_id')[0].firstChild.data
            classroom_name = classrooms.get(classroom_id,{}).get("name","")
            aslot = {"course_id": course_id,
                 "day_index": day_index ,
                 "term_index":term_index,
                 "classroom_id": classroom_id,
                 "classroom_name": classroom_name,
                 "teacher_id":teacher_id,
                 "teacher_name":teacher_name,
                 "group_name":group_name,
                 "course_name":course_name,
                 "course_type":course_type,
                 "short_name":short_name,
             } 
            teachers[teacher_id]['timetable'][term_index][day_index] = aslot
            classrooms[classroom_id]['timetable'][term_index][day_index] = aslot
            groups[group_name]['timetable'][term_index][day_index] = aslot
            courses[course_id]['timetable'][term_index][day_index] = aslot
        self.teachers= teachers
        self.classrooms = classrooms 
        self.groups =groups
        self.courses =courses
        return True
    
    def calcul_courses_assignation(self,  teacher_dept = False):
        courses = self.courses
        teachers = self.teachers
        self.courses_assignation = []
        header = """Courses Assignation -22"""

        for key, course in courses.iteritems():
            # get teacher info
            #~ if not teacher_dept or teachers[course['teacher_id']]['extid'] == teacher_dept:
            tech = teachers[course['teacher_id']]['name'] + " " + teachers[course['teacher_id']]['last_name']
            item = {"teacher": tech,
             "group_name": course['group_name'], 
             "course_type":course['course_type'], 
             "course_name":course['name'],
             "extid":teachers[course['teacher_id']]['extid'],
            }
            self.courses_assignation.append(item)
        return self.courses_assignation
        
    def calcul_charge_teachers(self,):
        """ Calculate the teacher charge """
        courses = self.courses
        teachers = self.teachers
        for key, course in courses.iteritems():
            #~ course = courses[key]
            # get teacher info
            tid = course['teacher_id']
            tech = teachers[tid]['name']
            try:
                nb_lessons = int(course['num_of_lessons_per_week'])
            except:
                nb_lessons  = 1
            if course['course_type'].upper() == "TP":
                teachers[tid]['TP'] += nb_lessons
            if course['course_type'].upper() == "TD":
                teachers[tid]['TD'] += nb_lessons
            if course['course_type'].upper() == "COURS":
                if course["together_courses_nb"]:   
                    # if the course is hold together with other courses the number of lessones will be divided on number of together courses to ajust count
                    teachers[tid]['COURS'] += float(nb_lessons) / (course["together_courses_nb"]+1)
                else:
                    teachers[tid]['COURS'] += nb_lessons
        for tid in teachers:

            teachers[tid]['seance'] = teachers[tid]['COURS'] + teachers[tid]['TD'] + teachers[tid]['TP']
            if teachers[tid]['edu_rank'].lower().startswith("vac"):
                teachers[tid]['charge'] = teachers[tid]['seance'] *1.5
                teachers[tid]['vacation'] = teachers[tid]['charge'] 
            else: # permannant
                teachers[tid]['charge'] =teachers[tid]['COURS'] * 2.25 + teachers[tid]['TD']*1.5 + teachers[tid]['TP'] *1.125
                teachers[tid]['vacation'] = teachers[tid]['charge'] - 9 
        self.teachers = teachers
        return teachers

    def display_courses_teachers(self,  teacher_dept = False):
        header = """Courses Assignation -22"""
        table =[]
        for assign in self.courses_assignation:
            # get teacher info
            if not teacher_dept or assign['extid'] == teacher_dept:
                item = assign.values()
                table.append(item)
        
        return self.display_table(header, table)


        

    def add_course(self, table_course,  given_group_name):
        """
        Add courses to a group
        """
        """
          <course id="152">
          <name>Physique 1</name>
          <short_name>Physique 1-G11</short_name>
          <course_type>TD</course_type>
          <num_of_lessons_per_week>1</num_of_lessons_per_week>
          <num_of_enrolled_students>25</num_of_enrolled_students>
          <group_name>
          </group_name>
          <teacher_id>62</teacher_id>
          <extid>
          </extid>
          <allowed_classrooms>
          <classroom_id>4</classroom_id>
          </allowed_classrooms>
        """
        xmldoc = self.xmldoc
        edu_programs = xmldoc.getElementsByTagName('edu_program')
        courses_table ={}
        groups_table = {}
        for edu_program in edu_programs:
              
            group_name = edu_program.getElementsByTagName('name')[0].firstChild.data
            if group_name == given_group_name:
                courses = edu_program.getElementsByTagName('courses')[0]
                # add a course 
                course = xmldoc.createElement("course")
                course.setAttribute('id',table_course['id'])
                
                for key in table_course:
                    if key != "id":
                        element = xmldoc.createElement(key)
                        text = xmldoc.createTextNode(table_course[key])
                        element.appendChild(text)
                        course.appendChild(element)
                
                courses.appendChild(course)
        xmldoc = self.xmldoc
        return xmldoc   

#~ class displayer(openclassModel):
    #~ def __init__(self,):
        #~ super(openclassModel).__init__()
    
    def display_charge_teachers(self, teacher_dept=False):
        """ display charge by teacher"""
        teachers = self.teachers
        text_permannant = self.display_header(">TEACHERS' Charge",2)
        text_permannant += "\n"+u"\t".join(['Nom',u'séance','Charge', 'Vacation','COURS','TD', "TP"])
        

        for tid in teachers:
            if not teacher_dept or teachers[tid]['extid'] == teacher_dept:
                text_permannant +="\n" + u"\t".join([teachers[tid]['name'], 
                teachers[tid]['edu_rank'],
                teachers[tid]['last_name'],
                str(teachers[tid]['seance']),
                str(teachers[tid]['charge']),
                str(teachers[tid]['vacation']),
                str(teachers[tid]['COURS']), 
                str(teachers[tid]['TD']),
                unicode(teachers[tid]['TP']),
                ])
        return text_permannant
        


      
    def display_slot_by_group(self, ):
        """
        display slots by groups
        """
        groups = self.groups
        text = ""
        for group_name in sorted(groups):
            text += self.display_header("%s"%group_name,2)
            time_table = groups[group_name]['timetable']
            text += self.display_timetable(time_table,"teacher_name", "classroom_name")
        return text;
            
    def display_slot_by_teacher(self,):
        """
        display slots by teacher
        """
        teachers = self.teachers

        text = """"""
        for tid in teachers:
            if teachers[tid]['charge'] > 0:
                text += self.display_header("%s. %s %s (%s)"%(teachers[tid]["title"], teachers[tid]["name"],
                 teachers[tid]["last_name"], teachers[tid]["edu_rank"]), 2)
                # display charge
                text+= self.display_charge(teachers[tid])
                time_table = teachers[tid]['timetable']

                text += self.display_timetable(time_table,"group_name", "classroom_name")
        return text;    
    

    
    def display_availaible_teachers(self,  detailled=False, teacher_type=False, course_type=False, teacher_dept=False):
        """
        display available teachers
        """
        teachers = self.teachers
        present_time_table = copy.deepcopy(FREETIMETABLE_TEMPLATE)
        text = self.display_header("Available TEACHERS",2)
        if teacher_type:
            teacher_type = teacher_type.upper()
            text+= self.display_header("Type: %s"%teacher_type, 1)
        if detailled :
            text+= self.display_header("Detailled",2)
        else:
            text+= self.display_header("Summury", 2)        
        if course_type: 
            course_type = course_type.upper()
            text+= self.display_header("Course type: %s"%course_type)



        for tid in teachers:
            if not teacher_type or teachers[tid]["edu_rank"].upper() ==  teacher_type:
                if not teacher_dept or teachers[tid]["extid"] ==  teacher_dept:
                    time_table = teachers[tid]["timetable"]
                    for term in ("1","2","3","4","5","6"):
                        for day in ("1","2","3","4","5","6"):
                            aslot = time_table[term][day]
                            if aslot:
                                if not course_type or  aslot['course_type'].upper() == course_type:
                                    if detailled:
                                        teacher_name = u" ".join([aslot['teacher_name'], 
                                            aslot['course_name'],
                                            aslot['course_type'],
                                            aslot['group_name'],
                                            aslot['classroom_name'],
                                             ] )
                                    else:
                                        teacher_name = aslot['teacher_name']
                                    present_time_table[term][day].append(teacher_name)
        text += self.display_freetimetable(present_time_table)       
        return text;

      
    def display_slot_by_classroom(self, occupation=False):
        """
        display slots by classroom
        """

        classrooms = self.classrooms
        text = ""
        for tid in classrooms:
            text += self.display_header(classrooms[tid]["name"], 2)
            time_table = classrooms[tid]["timetable"]
            text += self.display_timetable(time_table,"group_name", "teacher_name", occupation)       
        return text;
        
    def display_free_classroom(self, class_type = "", occupation=False):
        """
        display free classroom
        """
        classrooms = self.classrooms    
        freetime_table = copy.deepcopy(FREETIMETABLE_TEMPLATE)
        text = self.display_header("FREE CLASSROOMS %s"%class_type,2)
        #~ if class_type:
            #~ classrooms = [classrooms[c]  for c in classrooms if class_type in classrooms[c]["name"].lower()]
        for tid in classrooms:
            if not class_type  or class_type.lower()  ==  classrooms[tid]["type"].lower():
                time_table = classrooms[tid]["timetable"]
                for term in ("1","2","3","4","5","6"):
                    for day in ("1","2","3","4","5","6"):
                        if not time_table[term][day]:
                            freetime_table[term][day].append(classrooms[tid]["name"])
                        elif occupation: # display occupation of rooms to allow changement
                            freetime_table[term][day].append(classrooms[tid]["name"] + " [X]")
        text += self.display_freetimetable(freetime_table)       
        return text; 
    def display_freetimetable(self, time_table):
        pass
    def display_charge(self, time_table):
        pass
    def display_header(self, header_level = 1):
        pass
    def display_table(self, header, table):
        pass
    def display_timetable(self, time_table, field1, field2, occupation=False):
        pass
    
class html_displayer(openclassModel):
    def __init__(self, filename = None ):
        openclassModel.__init__(self, filename)
    def display_timetable(self, time_table, field1, field2, occupation=False):
        """
        display a time table
        fields to display
        """
        text = ""
        text+= """\n<table border='1' class="timetable">"""
        text+= "\n<thead>"
        text+= "<th class='term'>Horaire</th>"
        for d in("1","2","3","4","5","6"):
            text+= "<th class='day'>%s</th>"%DAYS[d]
        text+= "</thead>"

        for term in ("1","2","3","4","5","6"):
            text += "\n<tr><td>%s</td>"%TERMS[term]
            for day in ("1","2","3","4","5","6"):
                if time_table[term][day]:
                    if occupation:
                        text += """<td class='occuped'>MI</td>"""
                    else:
                        text += """<td class='%s'> 
                        <span class='course' alt='%s'>%s - %s</span>/
                        <span class='%s'>%s </span>@
                        <span class='%s'>%s </span>
                        </td>"""%(time_table[term][day].get("course_type",""),
                                time_table[term][day].get("course_name",""),                
                                time_table[term][day].get("short_name",""),                
                                time_table[term][day].get("course_type",""),                
                        field1, time_table[term][day].get(field1,""),
                        field2, time_table[term][day].get(field2,""),
                        )
                else:
                    text += """<td/>""" 
            text += "</tr>"
        text += "\n</table>"
        return text;          
        
    def display_freetimetable(self, time_table):
        """
        display a time table
        fields to display
        """
        text = ""
        text+= "\n<table border='1' class='timetable'>"
        text+= "\n<thead>"
        text+= "<th>Horaire</th>"
        for d in("1","2","3","4","5","6"):
            text+= "<th>%s</th>"%DAYS[d]
        text+= "</thead>"

        for term in ("1","2","3","4","5","6"):
            text += "\n<tr><td>%s</td>"%TERMS[term]
            for day in ("1","2","3","4","5","6"):
                text += """<td class='freerooms'><ul>"""
                for fr  in sorted(time_table[term][day]):
                    text += "<li>%s</li>"%fr 
                text += """</ul></td>"""
            text += "</tr>"
        text += "\n</table>"
        return text;

                
    def display_charge(self, teacher):
        text= u"""\n<table border='1'>
<tr>
<th>Charge</th> 
<th>Vacation</th>
<th>Cours</th>
<th>TD</th>
<th>TP</th>
<th>Séances</th>
</tr>
<tr>
<th>%.3f</th> 
<th>%.3f</th>
<th>%.0f</th>
<th>%d</th>
<th>%d</th>
<th>%.0f</th>
</tr>
</table>
<hr/>"""%(teacher["charge"],
            teacher["vacation"],
            teacher["COURS"],
            teacher["TD"],
            teacher["TP"],
            teacher["seance"],        
            )      
        return text

    def display_header(self, header, level = 1):
        if level == 1:
            tag = "h1"
        elif level == 2:
            tag = "h2"
        else:
            tag = "h3"
        return "\n<header><%s>%s</%s></header>"%(tag, header, tag)

    def display_table(self, header, table):
        """
        """
        #~ thead = table[0]
        html = """<h2> %s </h2>"""%header
        html += """<table border='1' class='timetable'>"""
        for item in table:
            html += u"<tr><td>" + u"</td><td>".join(item) + "</td></tr>"
        html += "</table>"
        
        return html
    def display_charge_teachers_html(self, teacher_dept=False):
        """ display charge by teacher"""
        text = u"""\n"\n<h2>TEACHERS' Charge</h2>"
        <table border='1'>
        <thead>
        <th>Type</th> 
        <th>Nom</th> 
        <th>Charge</th> 
        <th>Vacation</th>
        <th>Cours</th>
        <th>TD</th>
        <th>TP</th>
        <th>Séances</th>
        </thead>"""
        for tid in self.teachers:
            if not teacher_dept or self.teachers[tid]['extid'] == teacher_dept:

                text += u"""
                <tr>
                <td>%s</td> 
                <td>%s</td>        
                <td>%.3f</td> 
                <td>%.3f</td>
                <td>%.0f</td>
                <td>%d</td>
                <td>%d</td>
                <td>%.0f</td>
                </tr>
                """%(
                self.teachers[tid]["edu_rank"],
                self.teachers[tid]["name"] +" " + self.teachers[tid]["last_name"] ,
                self.teachers[tid]["charge"],
                self.teachers[tid]["vacation"],
                self.teachers[tid]["COURS"],
                self.teachers[tid]["TD"],
                self.teachers[tid]["TP"],
                self.teachers[tid]["seance"],        
                )
        text += u"""\n</table>"""
        return text            

    def display_html(self, stylefile = ""):
        """
        """
        #~ teachers    = read_teachers(xmldoc)
        #~ courses     = read_courses(xmldoc)
        #~ courses, groups    = read_courses(xmldoc)
        #~ classrooms  = read_classrooms(xmldoc)
        #~ teachers, classrooms, groups, courses  = read_slots(xmldoc,  courses, teachers, classrooms, groups)
        teachers = self.calcul_charge_teachers()
        if stylefile:
            stylefile_path = os.path.join(os.path.dirname(__file__), stylefile)
        else:
            stylefile_path = os.path.join(os.path.dirname(__file__), "css/style.css")
        try:
            stylesheetfile = open(stylefile_path, "r")
        except:
            print("can't open style sheet %s"%stylefile_path)
            stylesheetfile = False
        
        if stylesheetfile:
            stylesheet = stylesheetfile.read()
        else:
            stylesheet = ""
            
        
        html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<!--<link rel="stylesheet" href="style.css">-->
<title>Emploi de Temps</title>
<style  type='text/css'>
%s
</style>
</head>
<body>
"""%stylesheet
        
        print html.encode('utf8')

        print "<h1><a name='sommaire'>Sommaire</a> </h2>"
        print "<ul>"
        print "<li><a href='#%s'>%s</a></li>"%("groups", "Par groupe")
        print "<li><a href='#%s'>%s</a></li>"%("teachers", "Par Enseignant")
        print "<li><a href='#%s'>%s</a></li>"%("classrooms", "Salles")
        print "<li><a href='#%s'>%s</a></li>"%("freerooms", "Salles Libres")
        print "<li><a href='#%s'>%s</a></li>"%("availableteachers", "Enseignants Disponibles")
        print "<li><a href='#%s'>%s</a></li>"%("charges", "Charges")
        print "<li><a href='#%s'>%s</a></li>"%("affectation", "Affectation")
        print "</ul>"
        print "<br/><a name='groups'>Groups</a>"
        html = self.display_slot_by_group()
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"
        
        
        print "<br/><a name='teachers'></a>"
        html = self.display_slot_by_teacher()
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"
        
        print "<br/><a name='classrooms'></a>"
        #~ html = display_slot_by_classroom(classrooms, occupation=True)
        html = self.display_slot_by_classroom()
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"
        
        print "<br/><a name='freerooms'></a>"
        html = self.display_free_classroom()
        print html.encode('utf8')
        print "<br/><a name='freerooms'></a>"
        html = self.display_free_classroom("tp")
        print html.encode('utf8')
        print "<br/><a name='freerooms'></a>"
        html = self.display_free_classroom("salle")
        print "<br/><a name='freerooms'></a>"
        html = self.display_free_classroom("salle",occupation = True)
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"    
        
        #~ html = self.display_global_courses()
        #~ print html.encode('utf8')
        
            
        print "<br/><a name='availableteachers'></a>"
        html = self.display_availaible_teachers(teacher_dept="info")
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"    
        
        html = self.display_availaible_teachers(teacher_type ="vac",teacher_dept="info")
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"    
        
        html = self.display_availaible_teachers(detailled =True,teacher_dept="info")
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"    
        
        html = self.display_availaible_teachers(teacher_dept="info", course_type ="TP", detailled =True)
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"    
        
        html = self.display_availaible_teachers(teacher_dept="info", course_type ="COURS", detailled =True)
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"   
        
        print "<br/><a name='charges'></a>" 
        html = self.display_charge_teachers_html( teacher_dept ="info")
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"    

        #~ html = display_charge_teachers (teachers, teacher_dept ="info")
        #~ print html.encode('utf8')
        #~ print "<br/><a href='#sommaire'>TOP</a>"    
        
        print "<br/><a name='affectation'></a>" 
        html = self.display_courses_teachers ( teacher_dept ="info")
        print html.encode('utf8')
        print "<br/><a href='#sommaire'>TOP</a>"

        print "</body></html>"
        
      
def main():
    DATA_FILE = "../data/tm18.oct"
    try:
        # o
        xmldoc = minidom.parse(DATA_FILE)
    except:
        print "Can't Open the file", DATA_FILE
        sys.exit()
    parser = html_displayer(DATA_FILE)
    parser.display_html ()

if __name__ == '__main__':
    main()

