How to Open the Project
To run the simple-data-management application, follow these steps: <br />

1. Open Command Line Interface: <br />
Open your terminal or command prompt.

2. Navigate to the Project Directory: <br />
Use the cd command to navigate to the simple-data-management directory.<br />
For example:
cd path/to/your/project/simple-data-management

3. Navigate to the Flask App Directory: <br />
Once inside the simple-data-management directory, navigate to the flask_app directory: <br />
cd flask_app

4. Run the Application: <br />
Execute the following command to start the Flask application:<br />
python app.py

6. Access the Application:<br />
Ctrl + left click to open the local hosted link from the command prompt to access the application via web.

What the Simple Data Management app Does:<br />
This application is a basic data management system designed to store, organize, and retrieve data. It provides a user-friendly interface for managing records related to individuals. 

The main features of the application include:

Viewing Records: Users can view a list of all stored records through the records.html.<br />
Adding Records: Users can add new records by providing details to the form in create.html using required valid inputs for first name, last name, and date of birth.<br />
Updating Records: Users can update existing records with new information through pressing the update icon opening up a modal on any records' card.<br />
Deleting Records: Users can delete records using the trash bin icon on any records' card.<br />
<br />
The application is built using the Flask web framework and uses a CSV file (people.csv) to store data.
