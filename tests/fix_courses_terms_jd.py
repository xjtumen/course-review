#!/usr/bin/env python3
import sys

sys.path.append('..')  # fix import directory

from app import app, db
from app.models import Course, Review
from app.models import *

# require an app context to work
ctx = app.test_request_context()
ctx.push()


existing_course_terms = CourseTerm.query.all()

existing_course_classes = CourseClass.query.all()

courses = Course.query.all()
for i, course in enumerate(courses):
  # if course.name == '思考，快与慢':
  #   tmp = course
  # if i == 300:
  #   tmp2 = course
  # print()
  # continue

  if course.latest_term is None:
    course_term = CourseTerm()
    db.session.add(course_term)
    course_term.course = course
    course_term.term = '20221'

    course_term2 = CourseTerm()
    db.session.add(course_term2)
    course_term2.course = course
    course_term2.term = '20222'

    # course_class = CourseClass()
    # course_class.term = '20231'
    # course_class.course = course
    #
    # course_class2 = CourseClass()
    # db.session.add(course_class2)
    # course_class2.term = '20232'
    # course_class2.course = course
    #
    # db.session.add(course_class)
    # db.session.add(course_class2)

    print(course.name)

db.session.commit()
