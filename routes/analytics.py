from fastapi import APIRouter, HTTPException, Query
from database import employee_collection

router = APIRouter()

# --- AVG Salary Department wise ---
@router.get("/avg-salary")
async def average_salary_by_department():
    """
    Calculate average salary grouped by department.
    Always returns a list, even if some departments have no employees.
    """
    try:
        salary_pipeline = [
            {
                "$group": {
                    "_id": "$department",
                    "avg_salary": {"$avg": "$salary"},
                    "count": {"$sum": 1},
                }
            }
        ]

        salary_results = await employee_collection.aggregate(salary_pipeline).to_list(length=None)

        formatted_results = [
            {
                "department": doc["_id"] if doc["_id"] else "Unassigned",
                "avg_salary": round(doc["avg_salary"], 2) if doc.get("avg_salary") else 0,
                "employee_count": doc["count"],
            }
            for doc in salary_results
        ]

        return {
            "count": len(formatted_results),
            "departments": formatted_results
            
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating average salary: {str(e)}")


# --- Search Employees by Skill ---
@router.get("/search")
async def search_employees_by_skill(skill: str = Query(..., description="Skill to search for")):
    """
    Search employees by skill (case-insensitive, partial match)
    Example: /analytics/search?skill=AI
    """
    if not skill.strip():
        raise HTTPException(status_code=400, detail="Skill cannot be empty")

    query = {"skills": {"$elemMatch": {"$regex": skill, "$options": "i"}}}
    cursor = employee_collection.find(query)
    results = await cursor.to_list(length=None)

    if not results:
        raise HTTPException(status_code=404, detail=f"No employees found with skill '{skill}'")

    # Converting ObjectId to string
    for emp in results:
        emp["_id"] = str(emp["_id"])

    return {
        "count": len(results),
        "employees": results
    }

