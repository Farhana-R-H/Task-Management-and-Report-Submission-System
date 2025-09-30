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

## Additional Features
* Profile section on every page:
  * Profile image
  * Social media links (GitHub, LinkedIn)
  * Email and username
* Dashboard statistics for tasks, pending and completed reports.


---


  ```bash
  python manage.py runserver
