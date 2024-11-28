# TasksFastAPI

A task management API built using **FastAPI** with features such as user authentication, CRUD operations for posts, and role-based access control. This project serves as a practical demonstration of FastAPI capabilities, including JWT authentication, database interactions, and creating a RESTful API.

## Features

- **User Authentication**: JWT authentication with login and signup functionality.
- **CRUD Operations for Posts**: Create, read, update, and delete posts.
- **Role-based Authorization**: Different access levels for different user roles (e.g., admin vs. regular user).
- **Post Ownership**: Users can only update or delete their own posts.
- **SQLAlchemy ORM**: Utilizes SQLAlchemy for ORM-based database interactions.
  
## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **JWT (JSON Web Tokens)**: For secure user authentication and authorization.
- **Uvicorn**: A lightning-fast ASGI server for running FastAPI applications.
- **Alembic**

## Getting Started

### Prerequisites

- Python 3.6+
- Pip (Python's package installer)

### Installation

Clone the repository:

```bash
git clone https://github.com/DanielKhan1403/tasksFastApi.git
cd tasksFastApi
