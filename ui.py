import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("👩‍💻 Employee Management UI")

# --- Sidebar navigation ---
menu = ["Add Employee", "Search Employee", "Update Employee", "List Employees", "Delete Employee",
        "Employees by Department", "Average Salary by Department","Search Employees by Skill"]
choice = st.sidebar.selectbox("Select Action", menu)

# --- Add Employee Page ---
if choice == "Add Employee":
    st.header("Add Employee")
    employee_id = st.text_input("Employee ID")
    name = st.text_input("Name")
    department = st.text_input("Department")
    salary = st.number_input("Salary", min_value=0)
    joining_date = st.date_input("Joining Date")
    skills = st.text_area("Skills (comma-separated)")

    if st.button("Add Employee"):
        payload = {
            "employee_id": employee_id,
            "name": name,
            "department": department,
            "salary": int(salary),
            "joining_date": str(joining_date),
            "skills": [s.strip() for s in skills.split(",") if s.strip()]
        }

        res = requests.post(f"{API_URL}/employees", json=payload)
        if res.status_code == 200:
            st.success("✅ Employee added successfully!")
        else:
            try:
                error_detail = res.json().get("detail")
            except Exception:
                error_detail = res.text
            st.error(f"❌ Error: {error_detail}")

# --- Search Employee Page ---
elif choice == "Search Employee":
    st.header("Search Employee by ID")
    search_id = st.text_input("Enter Employee ID to search")
    if st.button("Search Employee"):
        if search_id:
            res = requests.get(f"{API_URL}/employees/{search_id}")
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.error("❌ Employee not found")

# --- Update Employee Page ---
elif choice == "Update Employee":
    st.header("Update Employee")
    update_id = st.text_input("Employee ID to Update")
    update_name = st.text_input("New Name (leave blank if no change)")
    update_department = st.text_input("New Department (leave blank if no change)")
    update_salary = st.number_input("New Salary (leave 0 if no change)", min_value=0, value=0)
    update_skills = st.text_area("New Skills (comma-separated, leave blank if no change)")

    if st.button("Update Employee"):
        if update_id:
            payload = {}
            if update_name.strip():
                payload["name"] = update_name
            if update_department.strip():
                payload["department"] = update_department
            if update_salary > 0:
                payload["salary"] = update_salary
            if update_skills.strip():
                payload["skills"] = [s.strip() for s in update_skills.split(",") if s.strip()]

            if not payload:
                st.warning("⚠️ Please provide at least one field to update.")
            else:
                res = requests.put(f"{API_URL}/employees/{update_id}", json=payload)
                if res.status_code == 200:
                    st.success("✅ Employee updated successfully!")
                    st.json(res.json())
                else:
                    try:
                        error_detail = res.json().get("detail", res.text)
                    except Exception:
                        error_detail = res.text
                    st.error(f"❌ Error: {error_detail}")

# --- List Employees Page ---
elif choice == "List Employees":
    st.header("All Employees")
    department_filter = st.text_input("Filter by Department (optional)")
    res = requests.get(f"{API_URL}/employees?department={department_filter}")  
    if res.status_code == 200:
        employees = res.json()
        if employees:
            st.table(employees)
        else:
            st.warning("No employees found.")
    else:
        st.error("Failed to fetch employees.")

# --- Delete Employee Page ---
elif choice == "Delete Employee":
    st.header("Delete Employee")
    delete_id = st.text_input("Employee ID to Delete")
    if st.button("Delete Employee"):
        if delete_id.strip():
            res = requests.delete(f"{API_URL}/employees/{delete_id}")
            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error(f"❌ Error: {res.text}")


# --- Employees by Department Page ---
elif choice == "Employees by Department":
    st.header("Employees by Department")
    dept_filter = st.text_input("Enter Department to Filter")
    if st.button("Show Employees"):
        res = requests.get(f"{API_URL}/employees?department={dept_filter}")
        if res.status_code == 200:
            employees = res.json()
            if employees:
                st.table(employees)
            else:
                st.warning("No employees found in this department.")
        else:
            st.error("Failed to fetch employees.")

# --- Average Salary by Department Page ---
elif choice == "Average Salary by Department":
    st.header("Average Salary by Departments")
    if st.button("Show Average Salary"):
        res = requests.get(f"{API_URL}/employees/avg-salary")
        if res.status_code == 200:
            avg_salaries = res.json()
            st.table(avg_salaries)
        else:
            st.error("Failed to fetch average salary.")

# --- Search Employees by Skill Page ---
elif choice == "Search Employees by Skill":
    st.header("Search Employees by Skill")
    skill_input = st.text_input("Enter skill to search")
    if st.button("Search"):
        if skill_input.strip():
            res = requests.get(f"{API_URL}/employees/search?skill={skill_input}")
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list) and data:
                    st.table(data)
                else:
                    st.warning(data.get("message", "No results"))
            else:
                st.error("Failed to search employees.")
