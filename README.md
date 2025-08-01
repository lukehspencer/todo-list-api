# Todo List API
*Project completed: March 2025*

API in Python that implements user authentication and todo list management to help people stay organized with their tasks.

## Overview
Built a RESTFUL API using Flask that logs in a user and allows them access to their todo list. User and todo list information are stored in seperate databases created using flask_sqlalchemy. 

## Functionality
- User must create an accounts with a username and password to access their todo lists
- User can add an item with a title and description to their todo list
- User can get a specific item and/or all items in their todo list
- User can update the title and/or description of a specific item
- User can delete a specific item and/or all items in their todo list

## Files & Folders
- `main.py` - Implements RESTFUL API with CRUD operations
- `models.py` - Creates user and todo models for SQLAlchemy databases
- `test.py` - Test API functionality
- `instance/` - Stores databases

## Technologies Used
- Python
- Flask
- flask_restful
- flask_sqlalchemy
- flask_jwt_extended
- flask_bcrypt
- requests
