from pydantic import BaseModel ,Field
from typing import List ,Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    name: str
    department:str
    salary:int
    joining_date:datetime
    skills:List[str]


class CreateEmployee(EmployeeBase):
    employee_id: str = Field(...)


class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[int] = None
    skills: Optional[List[str]] = None

