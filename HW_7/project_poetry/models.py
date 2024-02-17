from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    subjects = relationship("Subject", back_populates="teacher")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now())
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="grades")
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="grades")
