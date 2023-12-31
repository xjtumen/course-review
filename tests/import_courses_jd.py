#!/usr/bin/env python3
import sys
import uuid

from pymongo import MongoClient

sys.path.append('..')  # fix import directory

from app import app, db
from app.models import *
from datetime import datetime
import pickle

import dataclasses

import dataclasses
import pickle
from pathlib import Path
import pandas as pd

client = MongoClient('127.0.0.1', 27017, connectTimeoutMS=3000)
# mongoclient = client['courses']
# colall = mongoclient['all']  # offical+review

mongoclient = client['test']
colall = mongoclient['all_courses']  # offical+review


dept_str_to_num = {
"人文社会科学学院": 1,
"公共政策与管理学院": 2,
"化学工程与技术学院": 3,
"化学学院": 4,
"实践教学中心/工程坊": 5,
"法学院": 6,
"材料科学与工程学院": 7,
"电子与信息学部": 8,
"军事教研室": 9,
"生命科学与技术学院": 10,
"机械工程学院": 11,
"外国语学院": 12,
"前沿科学技术研究院": 13,
"体育中心": 14,
"管理学院": 15,
"学生就业创业指导服务中心": 16,
"经济与金融学院": 17,
"学工部/学生处/武装部": 18,
"航天航空学院": 19,
"物理学院": 20,
"人居环境与建筑工程学院": 21,
"电气工程学院": 22,
"金禾经济研究中心": 23,
"马克思主义学院": 24,
"数学与统计学院": 25,
"医学部": 26,
"能源与动力工程学院": 27,
"新闻与新媒体学院": 28,
"教务处": 29,
"团委": 30,
"西浦交流学院": 31,
"西安交通大学米兰理工联合设计与创新学院": 32,
"中国西部高等教育评估中心": 33,
"人工智能学院": 34,
"钱学森学院/钱学森书院": 35,
"国际教育学院": 36,
}




@dataclasses.dataclass
class JDCourse:
  name: str
  id: str
  semester: str
  recommendation: str
  reviews: list
  optional_course_is_core: bool
  highest: float
  average: float
  lowest: float
  df_course: pd.DataFrame
  class_headcount: int


# jd = pickle.load(open('/tmp/courses.pickle', 'rb'))


depts_code_map = dict()
classes_map = dict()
majors_map = dict()
titles_map = dict()
teachers_id_map = dict()
teachers_name_map = dict()
# We should load all existing courses, because SQLAlchemy does not support .merge on non-primary-key,
# and we want to preserve course ID (primary key) for each (cno, term) pair.
course_classes_map = dict()
course_terms_map = dict()
courses_map = dict()


def load_courses(insert=True):
  for name, i in dept_str_to_num.items():
    dept = Dept()
    dept.code = i
    dept.name = name

    db.session.add(dept)
  db.session.commit()

  all_teachers = dict()
  for doc in colall.find():
    if doc['开课单位'] in ["法学院",
                           "实践教学中心/工程坊",
                           "学生就业创业指导服务中心",
                           "教务处",
                           "学工部/学生处/武装部",
                           "团委",
                           "国际教育学院",
                           "中国西部高等教育评估中心",
                           "西安交通大学米兰理工联合设计与创新学院",
                           "西浦交流学院",
                           "钱学森学院/钱学森书院"]:
      continue
    for teacher in doc['teachers']:
      assert isinstance(teacher, str)
      if teacher not in all_teachers:
        t = Teacher()
        t.name = teacher
        t.dept_id = dept_str_to_num[doc['开课单位']]
        db.session.add(t)
        all_teachers[teacher] = t
  for doc in colall.find():
    for teacher in doc['teachers']:
      if teacher not in all_teachers:
        t = Teacher()
        t.name = teacher
        t.dept_id = dept_str_to_num[doc['开课单位']]
        db.session.add(t)
        all_teachers[teacher] = t
  db.session.commit()

  existing_depts = Dept.query.all()
  for dept in existing_depts:
    depts_code_map[dept.code] = dept
  print('%d existing departments loaded' % len(depts_code_map))

  existing_teachers = Teacher.query.all()
  print('%d existing teachers loaded' % len(existing_teachers))

  existing_courses = Course.query.all()
  print('%d existing courses loaded' % len(existing_courses))

  existing_course_classes = CourseClass.query.all()
  print('%d existing course classes loaded' % len(existing_course_classes))

  existing_course_terms = CourseTerm.query.all()
  print('%d existing course terms loaded' % len(existing_course_terms))

  new_teacher_count = 0
  new_course_count = 0
  new_term_count = 0
  new_class_count = 0
  new_dept_count = 0

  int_allow_empty = lambda string: int(string) if string.strip() else 0
  course_kcbh = {}
  print('Data loaded with %d courses' % colall.count_documents({}))

  user = User.query.filter_by(username='initbot1').first()
  if user is None:
    user = User(username='initbot', email='initbot@xjtumen.nonexists', password=str(uuid.uuid4().hex))
    user.xjtumen_username = 'course_init_bot'

    user.role = 'Bot'
    user.save()
    user.confirm()

  for doc in colall.find():
    # print(doc)

    course = Course()
    course.name = doc['课程名']

    course.dept_id = dept_str_to_num[doc['开课单位']]

    if doc.get('备注') is not None:
      if doc.get('other_fields') is None or len(doc['other_fields']) == 0:
        doc['other_fields'] = doc.get('备注')
      else:
        doc['other_fields'] = doc.get('备注') + '\n' + doc['other_fields']
    if doc.get('选课要求') is not None:
      if doc.get('other_fields') is None or len(doc['other_fields']) == 0:
        doc['other_fields'] = doc.get('选课要求') + '\n' + doc['other_fields']
      else:
        doc['other_fields'] = doc.get('选课要求')
    course.introduction = doc['other_fields']
    db.session.add(course)
    this_course_teachers = set()
    course.teachers = [all_teachers[t] for t in set(doc['teachers'])]
    # print(set(doc['teachers']))
    db.session.commit()

    course_rate = CourseRate()
    course_rate.course = course
    db.session.add(course_rate)

    sem_cls_list = doc.get('semester_class_list')
    if sem_cls_list is None:
      continue

    if len(sem_cls_list) == 1 and sem_cls_list[0]['semester'] == '20771':
      course_term = CourseTerm()
      db.session.add(course_term)
      course_term.course = course
      course_term.term = '20772'
      course_term.courseries = doc['课程号']
      if (got:=doc.get('选课班级')) is not None:
        course_term.teaching_classes = got
      course_term.code = doc['课程号']

    for sem_cls in sem_cls_list:
      course_term = CourseTerm()
      if sem_cls == 'semester':
        exit(9)
      db.session.add(course_term)
      course_term.course_type = doc['类型']

      if  sem_cls.get('highest') is not None:
        course_term.grade_highest = sem_cls['highest']
        course_term.grade_lowest = sem_cls['lowest']
        course_term.grade_average = sem_cls['average']

      course_term.course = course
      if (got := doc.get('现在模块')) is not None:
        course_term.join_type = got
      if doc.get('学时') is not None:
        course_term.hours = doc['学时']
      if doc.get('学分') is not None:
        course_term.credit = doc['学分']

      if len(sem_cls['semester']) != 5:
        print(sem_cls)
        print(course)
        exit(10)
      course_term.term = sem_cls['semester']
      if sem_cls.get('grade_range_student_count_list') is not None:
        course_term.has_grade_graph = True
        course_term.grade_u60 = sem_cls['grade_range_student_count_list'][0]
        course_term.grade_61_70 = sem_cls['grade_range_student_count_list'][1]
        course_term.grade_71_80 = sem_cls['grade_range_student_count_list'][2]
        course_term.grade_81_90 = sem_cls['grade_range_student_count_list'][3]
        course_term.grade_91_100 = sem_cls['grade_range_student_count_list'][4]
      else:
        course_term.has_grade_graph = False
      course_term.courseries = doc['课程号']
      course_term.code = doc['课程号']
      # course_term.class_numbers = '2'

      course_class = CourseClass()
      # update course class info
      course_class.course = course

      if len(sem_cls['semester']) != 5:
        print(sem_cls)
        print(course)
        exit(10)
      course_class.term = sem_cls['semester']

      # course_class.cno = '1'
      db.session.add(course_class)

      if doc.get('has_review_entry'): # None or False
        once = False
        for review_content in sem_cls['review_text_list']:
          review = Review()
          db.session.add(review)
          review.course = course

          if len(sem_cls['semester']) != 5:
            print(sem_cls)
            print(course)
            exit(10)

          review.term = sem_cls['semester']
          review.difficulty = 2
          review.homework = 2
          review.grading = 2
          review.gain = 2
          review.rate = 5
          review.author = user
          review.content = review_content
          if once:
            if (recomm := sem_cls.get('recommendation')) is not None:
              review.content = f'{recomm}\n{review.content}'
          review.update_time = datetime.utcnow()

          history = ReviewHistory()
          db.session.add(history)

          history.difficulty = review.difficulty
          history.homework = review.homework
          history.grading = review.grading
          history.gain = review.gain
          history.rate = review.rate
          history.content = review.content
          history.author_id = review.author_id
          history.course_id = review.course_id
          history.term = review.term
          history.publish_time = review.publish_time
          history.update_time = review.update_time
          history.is_anonymous = review.is_anonymous
          history.only_visible_to_student = review.only_visible_to_student
          history.is_hidden = review.is_hidden
          history.is_blocked = review.is_blocked

          history.review_id = review.id
          history.operation = 'create'
          history.operation_user_id = user.id

    db.session.commit()


with app.app_context():
  # we have merge now, do not drop existing data
  db.create_all()
  load_courses()
