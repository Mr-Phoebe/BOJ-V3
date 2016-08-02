#!/usr/bin/env python
# -*- coding: utf-8 -*-
from User.models import *
from Course.models import *

univ = University.addUniversity('test')
rootuser = User.addUser('root', '123456', univ, 'university')
univ.admin = rootuser
univ.save()

sch = School.addSchool('XINTONG', 'SICE', univ)
xintongrootuser = User.addUser('xtroot', '123456', univ, 'school')
sch.admin = xintongrootuser
sch.save()

grp1 = Group.addGroup('09211301', sch)
grp2 = Group.addGroup('09211302', sch)
gu1 = User.addUser('grot1', '123456', univ, 'group')
gu2 = User.addUser('grot2', '123456', univ, 'group')
gu3 = User.addUser('grot3', '123456', univ, 'group')

u1 = User.addUser('user1', '123456', univ)
u2 = User.addUser('user2', '123456', univ)
u3 = User.addUser('user3', '123456', univ)
grp1.addMember(u1)
grp1.addMember(u2)
grp2.addMember(u2)
grp2.addMember(u3)

pcadmin = User.addUser('pcadmin', '123456', univ, 'course')
shana = User.addUser('shana', '123456', univ, 'courseclass')

coursepc = Course.addCourse(sch, None, '1100010', 'Chinese English')

cc_id = CourseClass.addCourseClass(coursepc, shana, '1', 2013)
cc = CourseClass.getById( cc_id)
cc.addGroup(grp1)
cc.addGroup(grp2)

teacher = User.addUser('teacher', '123456', univ, 'course')
yoko = User.addUser('yoko', '123456', univ, 'courseclass')
coursepc = Course.addCourse(sch, teacher, '1100019', 'Chinese English')
cc = CourseClass.addCourseClass(coursepc, yoko, '2009211101', 2013)
