#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testdom2.py
#  
#  

DATA_FILE = 'tm18.oct'
import xml.dom.minidom as minidom
import sys
import copy

TERMS= {
"1":"08:00-09:30",
"2":"09:30-11:00",
"3":"11:00-12:30",
"4":"12:30-13:00",
"5":"13:00-14:30",
"6":"14:30-16:00",
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

def read_courses(xmldoc):
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
    edu_programs = xmldoc.getElementsByTagName('edu_program')
    courses_table ={}
    for edu_program in   edu_programs:  
        group_name = edu_program.getElementsByTagName('name')[0].firstChild.data
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
            "timetable":copy.copy(TIMETABLE_TEMPLATE)
            
            }
    return courses_table
def read_classrooms(xmldoc):
    #get classrooms
    classrooms = xmldoc.getElementsByTagName('classroom')
    #~ print classrooms
    classrooms_table ={}
    # display personne by personne
    for classroom  in classrooms:
        classrooms_table[classroom.getAttribute('id')]= {'name':classroom.getElementsByTagName('name')[0].firstChild.data,
                      "timetable":copy.copy(TIMETABLE_TEMPLATE)}       
    return classrooms_table
    
def read_teachers(xmldoc):
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
             "TD":0, "COURS":0, "TP":0,
             "timetable":copy.copy(TIMETABLE_TEMPLATE)
         }       
    return teachers_table
def read_slots(xmldoc, courses):
    """
    <lesson_in_tt>
        <course_id>384</course_id>
        <day_index>4</day_index>
        <term_index>2</term_index>
        <classroom_id>6</classroom_id>
    </lesson_in_tt>
    """
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
        course_type = courses.get(course_id,{}).get("course_type","0")
        course_name = courses.get(course_id,{}).get("name","0")
        short_name = courses.get(course_id,{}).get("short_name","0")
        group_name = courses.get(course_id,{}).get("group_name","0")
        day_index = slot.getElementsByTagName('day_index')[0].firstChild.data
        term_index = slot.getElementsByTagName('term_index')[0].firstChild.data
        classroom_id = slot.getElementsByTagName('classroom_id')[0].firstChild.data
        aslot = {"course_id": course_id,
             "day_index": day_index ,
             "term_index":term_index,
             "classroom_id": classroom_id,
             "teacher_id":teacher_id,
             "group_name":group_name,
             "course_name":course_name,
             "course_type":course_type,
             "short_name":short_name,
         } 
        if teacher_id not in slots_table["teachers"]:
            slots_table["teachers"][teacher_id] = [aslot,]
        else:
            slots_table["teachers"][teacher_id].append(aslot)
        if group_name not in slots_table["groups"]:
            slots_table["groups"][group_name]= [aslot, ]
        else:
            slots_table["groups"][group_name].append(aslot)
        if classroom_id not in slots_table["classrooms"]:
            slots_table["classrooms"][classroom_id]= [aslot,]
        else:
            slots_table["classrooms"][classroom_id].append(aslot)
    return slots_table
    
def display_courses_teachers(courses, teachers):
    for key, course in courses.iteritems():
        #~ course = courses[key]
        # get teacher info
        tech = teachers[course['teacher_id']]['name'] + " " + teachers[course['teacher_id']]['last_name']
        print (u"\t".join([ course['group_name'], tech, course['course_type'],course['name']  ])).encode("utf8")
        
def calcul_charge_teachers(courses, teachers):
    """ Calculate the teacher charge """
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
    return teachers
    
def display_charge_teachers(teachers):
    """ display charge by teacher"""
    text_permannant = ""
    for tid in teachers:
        text_permannant +="\n"+ u"%s\tNom : %s %s\tséance:%.2f\tCharge:%.2f\tVacation:%.2f\tCOURS:%d.0f\tTD:%d\tTP:%d"%(teachers[tid]['name'], 
        teachers[tid]['edu_rank'],
        teachers[tid]['last_name'],
        teachers[tid]['seance'],
        teachers[tid]['charge'],
        teachers[tid]['vacation'],
        teachers[tid]['COURS'], 
        teachers[tid]['TD'],
        teachers[tid]['TP'],
        )
    #~ print "*"*50
    #~ print text_permannant.encode('utf8')
    return text_permannant

    
def display_slot_by_group(slots, courses, teachers, classrooms):
    """
    display slots by groups
    """
    """
        aslot = {"course_id": course_id,
             "day_index": day_index ,
             "term_index":term_index,
             "classroom_id": classroom_id,
             "teacher_id":teacher_id,
             "group_name":group_name,
             "course_name":course_name,
             "course_type":course_type,
             "short_name":short_name,
         } 
    """

    text = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<link rel="stylesheet" href="style.css">
<title></title>
</head>"""
    for group_name in slots["groups"]:
        text += "\n<h2>%s</h2>"%group_name
        text+= "\n<table border='1'>"
        text+= "\n<tr>"
        text+= "<th>Horaire</th>"
        for d in("1","2","3","4","5","6"):
            text+= "<th>%s</th>"%DAYS[d]
        text+= "</tr>"
        time_table = {
        #TERM N°1
        "1":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "2":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "3":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "4":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "5":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "6":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,
        }   
        for slot in slots["groups"][group_name]:
            term_index = slot['term_index']
            day_index = slot['day_index']
            time_table[term_index][day_index] = {"course_name":slot["course_name"],
                "teacher": teachers[slot["teacher_id"]]["name"][0] +". "+ teachers[slot["teacher_id"]]["last_name"],
                "classroom": classrooms[slot["classroom_id"]]["name"],
                "group_name": slot["group_name"],                
                "course_type": slot["course_type"],                
                "short_name": slot["short_name"],                
                    }    
        for term in ("1","2","3","4","5","6"):
            text += "\n<tr><td>%s</td>"%TERMS[term]
            for day in ("1","2","3","4","5","6"):
                text += """<td class='%s'> 
                <span class='course' alt='%s'>%s - %s</span>
                <span class='teacher'>%s </span>
                <span class='classroom'>%s </span>
                </td>"""%(time_table[term][day].get("course_type",""),
                        time_table[term][day].get("course_name",""),                
                        time_table[term][day].get("short_name",""),                
                        time_table[term][day].get("course_type",""),                
                time_table[term][day].get("teacher",""),
                time_table[term][day].get("classroom",""),
                )
            text += "</tr>"
        text += "\t</table>"
    text += "\t</body></html>"
    return text;
            
def display_slot_by_teacher(slots, courses, teachers, classrooms):
    """
    display slots by teacher
    """
    """
        aslot = {"course_id": course_id,
             "day_index": day_index ,
             "term_index":term_index,
             "classroom_id": classroom_id,
             "teacher_id":teacher_id,
             "group_name":group_name,
             "course_name":course_name,
             "course_type":course_type,
             "short_name":short_name,
         } 
    """

    text = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<link rel="stylesheet" href="style.css">
<title></title>
</head>"""
    for tid in slots["teachers"]:
        text += "\n<h2>%s. %s %s (%s)</h2>"%(teachers[tid]["title"], teachers[tid]["name"],
         teachers[tid]["last_name"], teachers[tid]["edu_rank"])
        # display charge
        text+= u"""\n<table border='1'>
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
        </table>"""%(teachers[tid]["charge"],
        teachers[tid]["vacation"],
        teachers[tid]["COURS"],
        teachers[tid]["TD"],
        teachers[tid]["TP"],
        teachers[tid]["seance"],        
        )
        
        
        # display a time table
        text+= "\n<table border='1'>"
        text+= "\n<tr>"
        text+= "<th>Horaire</th>"
        for d in("1","2","3","4","5","6"):
            text+= "<th>%s</th>"%DAYS[d]
        text+= "</tr>"
        time_table = {
        #TERM N°1
        "1":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "2":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "3":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "4":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "5":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "6":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,
        }   
        for slot in slots["teachers"][tid]:
            term_index = slot['term_index']
            day_index = slot['day_index']
            time_table[term_index][day_index] = {"course_name":slot["course_name"],
                "teacher": teachers[slot["teacher_id"]]["name"][0] +". "+ teachers[slot["teacher_id"]]["last_name"],
                "group_name": slot["group_name"],
                "classroom": classrooms[slot["classroom_id"]]["name"],
                "course_type": slot["course_type"],                
                "short_name": slot["short_name"],                
                    }    
        for term in ("1","2","3","4","5","6"):
            text += "\n<tr><td>%s</td>"%TERMS[term]
            for day in ("1","2","3","4","5","6"):
                text += """<td class='%s'> 
                <span class='course' alt='%s'>%s - %s</span>
                <span class='group_name'>%s </span>
                <span class='classroom'>%s </span>
                </td>"""%(time_table[term][day].get("course_type",""),
                        time_table[term][day].get("course_name",""),                
                        time_table[term][day].get("short_name",""),                
                        time_table[term][day].get("course_type",""),                
                time_table[term][day].get("group_name",""),
                time_table[term][day].get("classroom",""),
                )
            text += "</tr>"
        text += "\t</table>"
    text += "\t</body></html>"
    return text;    
    
def display_slot_by_classroom(slots, courses, teachers, classrooms):
    """
    display slots by classroom
    """
    """
        aslot = {"course_id": course_id,
             "day_index": day_index ,
             "term_index":term_index,
             "classroom_id": classroom_id,
             "teacher_id":teacher_id,
             "group_name":group_name,
             "course_name":course_name,
             "course_type":course_type,
             "short_name":short_name,
         } 
    """

    text = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<link rel="stylesheet" href="style.css">
<title></title>
</head>"""
    for tid in slots["classrooms"]:
        text += "\n<h2>%s</h2>"%classrooms[tid]["name"]
       
        # display a time table
        text+= "\n<table border='1'>"
        text+= "\n<tr>"
        text+= "<th>Horaire</th>"
        for d in("1","2","3","4","5","6"):
            text+= "<th>%s</th>"%DAYS[d]
        text+= "</tr>"
        time_table = {
        #TERM N°1
        "1":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "2":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "3":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "4":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,  
        "5":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,   
        "6":{"1":{}, "2":{}, "3":{}, "4":{},"5":{}, "6":{}, }   ,
        }   
        for slot in slots["classrooms"][tid]:
            term_index = slot['term_index']
            day_index = slot['day_index']
            time_table[term_index][day_index] = {"course_name":slot["course_name"],
                "teacher": teachers[slot["teacher_id"]]["name"][0] +". "+ teachers[slot["teacher_id"]]["last_name"],
                "group_name": slot["group_name"],
                "classroom": classrooms[slot["classroom_id"]]["name"],
                "course_type": slot["course_type"],                
                "short_name": slot["short_name"],                
                    } 
        for term in ("1","2","3","4","5","6"):
            text += "\n<tr><td>%s</td>"%TERMS[term]
            for day in ("1","2","3","4","5","6"):
                text += """<td class='%s'> 
                <span class='course' alt='%s'>%s - %s</span>
                <span class='group_name'>%s </span>
                <span class='teacher'>%s </span>
                </td>"""%(time_table[term][day].get("course_type",""),
                        time_table[term][day].get("course_name",""),                
                        time_table[term][day].get("short_name",""),                
                        time_table[term][day].get("course_type",""),                
                        time_table[term][day].get("group_name",""),
                        time_table[term][day].get("teacher",""),                
                )
            text += "</tr>"
        text += "\t</table>"
    text += "\t</body></html>"
    return text;    
def main():
    try:
        # o
        xmldoc = minidom.parse(DATA_FILE)
    except:
        print "Can't Open the file", DATA_FILE
        sys.exit()
    #~ #treat_doc(xmldoc)
    #~ treat_doc(xmldoc)
    #~ display_tel_personne(xmldoc)
    teachers    = read_teachers(xmldoc)
    courses     = read_courses(xmldoc)
    classrooms  = read_classrooms(xmldoc)
    slots  = read_slots(xmldoc, courses)
    #~ print classrooms
    #~ print "*"*50
    #~ print slots
    #~ print "*"*50        
    #~ display_courses_teachers(courses, teachers)
    teachers = calcul_charge_teachers (courses, teachers)
    #~ display_charge_teachers (courses, teachers)
    html = display_slot_by_group(slots, courses, teachers, classrooms)
    print html.encode('utf8')
    html = display_slot_by_teacher(slots, courses, teachers, classrooms)
    print html.encode('utf8')
    html = display_slot_by_classroom(slots, courses, teachers, classrooms)
    print html.encode('utf8')



    return 0
if __name__ == '__main__':
    main()

