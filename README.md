# Task Management and Report Submission System

This is a **Task Management and Report Submission Web Application** consisting of three user roles: **User**, **Admin**, and **SuperAdmin**.  

---

## SuperAdmin Credentials (for demonstration)
* **Username:** farhanatask  
* **Password:** novitask123  

---

## Features & Functionality

### 1. User
* Can view tasks assigned to them.
* Can see who assigned the task (Admin or SuperAdmin).
* Can view:
  * Task title
  * Description
  * Due date
  * Completion date
  * Status (Pending / Completed)
* Can submit task completion reports with:
  * Worked hours
  * Report description
* Can see pending and completed tasks clearly.
* Can view reports submitted for tasks.

### 2. Admin
* Can assign tasks to users.
* Can view all tasks assigned by them.
* Can monitor task status and reports of users.
* Can edit, reassign, or manage tasks under their supervision.

### 3. SuperAdmin
* Has ultimate control over the system.
* Can assign Admin roles to users.
* Can view all registered users.
* Can delete any user account.
* Can view all tasks in the system and see:
  * Which Admin assigned each task
  * Task status (Pending / Completed)
  * Completion reports and worked hours
* Can view all completed and pending reports.
* Can access system-wide analytics and insights.

---
* REST API Endpoints

* Authentication
    * JWT Authentication is used for secure access.
    * Users can login with username and password.
    * Successful login returns a JWT token for subsequent API requests.

* Task APIs (User-Specific)
    * GET /api/tasks/
        * Fetch all tasks assigned to the logged-in user.
    * PUT /api/tasks/{id}/
        * Update a task’s status.
        * When marking as Completed, must include:
            * Completion Report (text)
            * Worked Hours (number)
    * GET /api/tasks/{id}/report/
        * View Completion Report and Worked Hours.
        * Accessible only for Completed tasks.
        * Admins & SuperAdmins can access all reports.

* Example JSON payload for completing a task:
    {
        "status": "completed",
        "completion_report": "Fixed bugs, updated documentation.",
        "worked_hours": 4
    }

* Roles & Permissions
    * SuperAdmin
        * View/manage all users and admins.
        * Assign tasks to users.
        * View all task reports.
    * Admin
        * Assign tasks to their users.
        * View/manage tasks and reports within their team.
    * User
        * View assigned tasks.
        * Update task status.
        * Submit completion report and worked hours.

* Notes
    * Only logged-in users can access their respective API endpoints.
    * Admins and SuperAdmins can view all reports; users can only see their own.
    * The system uses SQLite database.

## Additional Features
* Profile section on every page:
  * Profile image
  * Social media links (GitHub, LinkedIn)
  * Email and username
* Dashboard statistics for tasks, pending and completed reports.


---


  ```bash
  python manage.py runserver
