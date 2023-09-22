# Run and Install

### Steps to install and run the project.
#### [Step 1](#step-1-clone-the-repository): Clone the Repository
#### [Step 2](#step-2-check-the-directory): Check the Directory
#### [Step 3](#step-3-Create-and-activate-a-virtual-environment): Create and activate a virtual environment
#### [Step 4](#step-4-Create-a-.env-file): Create a `.env` file 
#### [Step 5](#step-5-install-the-required-modules): Install the Required Modules
#### [Step 5](#step-6-database-migrations): Database Migrations
#### [Step 6](#step-7-run-tests): Run Tests

## Step 1: Clone the repository
Clone the repository and using this command on terminal:
```commandline
git clone https://github.com/KunKid-cmd/ku-polls.git
```

## Step 2: Check the directory
To ensure that your are in the correct directory (ku-polls), run the following command:

Windows:
```commandline
cd
```

macOS / Linux:
```commandline
pwd
```

If you are not in the correct directory, navigate to the project directory before proceeding with the installation:
```commandline
cd ku-polls
```
## Step 3: Create and activate a virtual environment:

for Mac/Linux, use this command: 
```
python -m venv venv           # Create the virtual environment
. venv/bin/activate           # Start the virtual environment
```
   
for Windows, use this command:
```
python -m venv venv
. .\venv\Scripts\activate
```

## Step 4: Create a `.env` file :
   
for **Mac/Linux**, use this command:
   ```
   cp sample.env .env
   ```
    
for **Windows**, use this command:
   ```
   copy sample.env .env
   ```
Please fix this file before runserver.

## Step 5: Install the required modules

Installing the required `Python` modules by executing the following command:
```commandline
pip install -r requirements.txt
```

To verify that all modules are installed, run the following command:
```commandline
pip list
```

## Step 6: Database migrations

To create a new database, run the following command:
```commandline
python manage.py migrate
```
or
```commandline
python3 manage.py migrate
```

Load the initial data for the polls app, run the following command:

```commandline
python manage.py loaddata data/polls.json data/users.json
```
or
```commandline
python3 manage.py loaddata data/polls.json data/users.json
```

## Step 7: Run tests

To execute the test, run the following command:
```commandline
python manage.py test polls
```
or
```commandline
python3 manage.py test polls
```


