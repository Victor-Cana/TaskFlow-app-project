# TaskFlow - Project Management Database Application

## Team: Schema Squad

- **Dan Beecher** - beecher.d@northeastern.edu
- **Daniel Chang** - chang.dani@northeastern.edu
- **Fahd Khan** - khan.fah@northeastern.edu
- **Sidd Ramesh** - ramesh.si@northeastern.edu
- **Victor Canavan** - canavan.v@northeastern.edu

---

## Project Description

TaskFlow is a data-driven task and project management application that helps users organize projects, track productivity, and manage team collaboration. The system tracks tasks, resources, work sessions, and generates reports to provide insights into project progress and team performance.

---

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Clone the Repository
```bash
git clone https://github.com/Victor-Cana/TaskFlow-app-project.git
cd TaskFlow-app-project
```

### 2. Create Environment File

Create a `.env` file in the project root directory with the following content:
```env
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_DATABASE=ProjectDB
MYSQL_USER=taskflow_user
MYSQL_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key_here
```

> **Important:** Replace the placeholder values with your own secure passwords.

### 3. Start the Application
```bash
docker compose up -d
```

This command will:
- Start the MySQL database container
- Initialize the database with the schema from SQL files
- Start the API service container
- Execute all initialization scripts

### 4. Verify Services

Check that all containers are running:
```bash
docker compose ps
```

All services should show status as "Up" or "running".

---

## Accessing the Application

- **API:** http://localhost:8000
- **Database:** localhost:3306 (use credentials from `.env` file)

---

## Stopping the Application
```bash
# Stop all containers
docker compose down

# Stop and remove volumes (reset database)
docker compose down -v
```

---

## Troubleshooting

**Containers fail to start:**
- Verify your `.env` file exists and contains all required variables
- Check that ports 3306 and 8000 are not already in use

**Database connection errors:**
- Ensure password values match in your `.env` file
- Check container logs: `docker compose logs db`

**API errors:**
- Check API logs: `docker compose logs api`

---

## Database Schema

The database includes the following main tables:

- **Users** - User accounts and management hierarchy
- **Projects** - Project information and ownership
- **Resources** - Project files and materials
- **WorkSessions** - Time tracking
- **Reports** - Generated project reports
- **Messages** - Internal communications
- **AssignedTo** - Project assignments
- **HaveAccessTo** - Resource permissions

---

## Course Information

**Course:** CS 3200 - Database Design  
**Semester:** Fall 2025  
**Institution:** Northeastern University

## Demo Video
[Watch the demo video here](https://drive.google.com/file/d/1fV8YYGPvLyWOZHUy9eM1d8NxyVymNr0C/view?usp=sharing)
