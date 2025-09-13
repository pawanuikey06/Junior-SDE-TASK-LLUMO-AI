from fastapi import APIRouter, HTTPException,Query
from models import UpdateEmployee
from models import CreateEmployee
from database import employee_collection

router = APIRouter()


# --- create Employee ---
@router.post("/employees")
async def create_employee(employee: CreateEmployee):
    # Checking for employee_id  if that is already exists
    existing = await employee_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    # Inserting new employee
    result = await employee_collection.insert_one(employee.dict())
    return {"inserted_id": str(result.inserted_id)}

# --- Get Employee ---
@router.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    # finding emp by id
    employee = await employee_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Converting ObjectId to string for JSON response
    employee["_id"] = str(employee["_id"])
    return employee



# --- Update Employee ---
@router.put("/employees/{employee_id}")
async def update_employee(employee_id: str, employee: UpdateEmployee):
    existing = await employee_collection.find_one({"employee_id": employee_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = {k: v for k, v in employee.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    await employee_collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )

    updated_employee = await employee_collection.find_one({"employee_id": employee_id})
    updated_employee["_id"] = str(updated_employee["_id"])
    return updated_employee

# --- Delete Employee ---
@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    # Check if employee exists
    existing = await employee_collection.find_one({"employee_id": employee_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Delete the employee
    result = await employee_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 1:
        return {"message": f"Employee {employee_id} deleted successfully."}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete employee")



@router.get("/employees")
async def list_employees(department: str = Query(None)):
    query = {"department": department} if department else {}
    cursor = employee_collection.find(query).sort("joining_date", -1)
    employees = []
    async for emp in cursor:
        emp["_id"] = str(emp["_id"])
        employees.append(emp)
    return employees