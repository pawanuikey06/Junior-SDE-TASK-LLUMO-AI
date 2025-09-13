from pydantic import BaseModel ,Field
from typing import List ,Optional
from datetime import date


class EmployeeBase(BaseModel):
    name: str
    department:str
    salary:int
    joining_date:date
    skills:List[str]


class CreateEmployee(EmployeeBase):
    employee_id: str = Field(...)


class UpdateEmployee(BaseModel):
    name: Optional[str]
    department: Optional[str]
    salary: Optional[int]
    joining_date: Optional[date]
    skills: Optional[List[str]]
