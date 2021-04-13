### Run the command as shown in the order inside the virtual environment of project
1. Install all the requirements
    ```python
    pip install -r requirements.txt
2. Make migrattions
    ```python
     python manage.py makemigrations
3. Migrate the migrations
    ```python
    python manage.py migrate
4. Run **group.py**
    ```python
    python group.py
5. Create **superuser** provide **groups.id: 1** (group id of admin)
    ```python
    python manage.py createsuperuser
6. Run server
    ```python
    python manage.py runserver

#### Four groups
1. Admin
2. Regional Manager
3. Worker
4. Customer

**Admin** group user can 
1. Login
2. Add a new user
3. List all users
4. View individual user
5. Delete users
6. Update all users


**Regional manager** group user can
1. Login
2. List all users
3. Add a new user (executors)
4. View and Update own detail
5. View and Update order detail


**Worker** group user can
1. Login
2. List all users
3. Add a new user (customers)
4. View and Update own detail
5. View and Update order detail


**Customer** group user can
1. Login
2. List all users
3. Add a new user (self)
4. View and Update own detail
5. View and Update order detail


Without login, no user can get access to the system.
