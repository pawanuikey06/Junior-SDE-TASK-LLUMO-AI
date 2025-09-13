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
async def search_employees_by_skill(skill: str = Query(None, description="Skill to search for (optional)")):
    """
    Return employees who have the given skill in their skills array.
    If no skill is provided, return all distinct skills available.
    Example: /employees/search?skill=Python
    """
    try:
        # If skill not provided → return all available skills
        if not skill:
            pipeline = [
                {"$unwind": "$skills"},
                {"$group": {"_id": "$skills"}},
                {"$sort": {"_id": 1}},
            ]
            all_skills = await employee_collection.aggregate(pipeline).to_list(length=None)
            available_skills = [s["_id"] for s in all_skills] if all_skills else []
            return {"available_skills": available_skills, "count": len(available_skills)}

        # Otherwise, search employees with that skill
        queries = [
            {"skills": {"$regex": f"^{skill}$", "$options": "i"}},   # exact case-insensitive
            {"skills": {"$regex": skill, "$options": "i"}},          # partial match
            {"skills": skill},                                       # exact match
            {"skills": {"$in": [skill, skill.lower(), skill.upper(), skill.title()]}},  # variations
        ]

        results = None
        successful_query = None

        for i, query in enumerate(queries):
            cursor = employee_collection.find(query)
            temp_results = await cursor.to_list(length=None)
            if temp_results:
                results = temp_results
                successful_query = i
                break

        if not results:
            return {
                "message": f"No employees found with skill '{skill}'",
                "hint": "Try without ?skill=... to see available skills",
            }

        # Format employees
        formatted_results = []
        for emp in results:
            emp["_id"] = str(emp["_id"])
            formatted_results.append(emp)

        return {
            "count": len(formatted_results),
            "employees": formatted_results,
            "query_used": f"Query {successful_query + 1}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching employees: {str(e)}")

