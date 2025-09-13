# Employee Management API

This project is a FastAPI-based backend application that demonstrates CRUD operations with MongoDB using Motor (an async driver).

## Features

- Add new employees
- Get list of employees
- Get employee by ID
- Update employee details
- List Employee by Department
- Delete employee
- Search employees by skill
- Calculate average salary by department

## Tech Stack

- **FastAPI** - Web framework
- **MongoDB** - NoSQL database
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Project Structure



## Setup Instructions

### 1. Clone the repository



### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=employee_db
COLLECTION_NAME=employees
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

### 6. API Documentation

After running, visit:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### Employees

- **Add Employee**
  - `POST /employees/`
  - Request body:
    ```json
    {
      "name": "John Doe",
      "department": "AI",
      "salary": 50000,
      "joining_date": "2025-09-13",
      "skills": ["Python", "ML"],
      "employee_id": "E101"
    }
    ```

- **Get All Employees**
  - `GET /employees/`

- **Get Employee by ID**
  - `GET /employees/{employee_id}`

- **Update Employee**
  - `PUT /employees/{employee_id}`

- **Delete Employee**
  - `DELETE /employees/{employee_id}`

- **Search Employees by Skill**
  - `GET /employees/search?skill=Python`

- **Average Salary by Department**
  - `GET /employees/average-salary?department=AI`

## Example Requests

### Add Employee

```bash
curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Alice",
        "department": "AI",
        "salary": 70000,
        "joining_date": "2025-09-13",
        "skills": ["FastAPI", "Python"],
        "employee_id": "E102"
      }'
```

### Search by Skill

```bash
curl "http://127.0.0.1:8000/employees/search?skill=Python"
```

### Average Salary

```bash
curl "http://127.0.0.1:8000/employees/average-salary?department=AI"
```
