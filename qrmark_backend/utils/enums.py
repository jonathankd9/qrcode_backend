from enum import Enum

class Gender(Enum):
    MALE = 'MALE'
    FEMALE  = 'FEMALE'
    MR = 'MR'
    MRS = 'MRS'

class Level(Enum):
    L100 = '100'
    L200 = '200'
    L300 = '300'
    L400 = '400'
    L500 = '500'
    L600 = '600'
    
class Semester(Enum):
    SEMESTER_1 = 'SEMESTER_1'
    SEMESTER_2 = 'SEMESTER_2'