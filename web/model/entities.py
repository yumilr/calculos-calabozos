from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import connector
import datetime

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    username = Column(String(12))
    score = Column(Integer, Sequence('question_id_seq'), primary_key=True)

class Question(connector.Manager.Base):
    __tablename__ = 'questions'
    id = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    content = Column(String(500), default="")
    difficulty_id = Column(Integer, ForeignKey('difficulties.id'))
    answer_type_id = Column(Integer, ForeignKey('answer_types.id'))
    right_answer = Column(String(500))
    accept_error = Column(Boolean, default=True)
    margin_error = Column(Float, default=0)

class Difficulty(connector.Manager.Base):
    __tablename__ = 'difficulties'
    id = Column(Integer, Sequence('difficulty_id_seq'), primary_key=True)
    # guarda el ultimo id insertado anteriormente para sólo sumarle
    time = Column(Integer)
    difficulty = Column(String(20))

class AnswerType(connector.Manager.Base):
    __tablename__ = 'answer_types'
    id = Column(Integer, Sequence('answer_type_id_seq'), primary_key=True)
    answer_type = Column(String(20))

class WrongAnswer(connector.Manager.Base):
    __tablename__ = 'wrong_answers'
    id = Column(Integer, Sequence('wrong_answer_id_seq'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    content = Column(String(250))
