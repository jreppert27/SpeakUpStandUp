Anonymous Question Platform
Introduction
The Anonymous Question Platform is a web-based application designed to facilitate anonymous question submissions from students and allow teachers to respond to those questions. Built using Python and Flask, this platform enables real-time interaction in an educational setting, enhancing classroom engagement and providing a safe space for students to ask questions anonymously.

Features
Anonymous Question Submission: Students can submit questions without revealing their identity.
Real-time Updates: Questions and teacher responses are displayed and updated every 5 seconds.
Teacher Response Interface: Teachers can view all submitted questions and provide responses through a dedicated interface.
Access Control: The teacher's page is accessible only from the teacher's computer based on IP address.
Delete All Questions: Teachers have the ability to delete all questions and responses with a single action.
Navigation Sidebar: A consistent sidebar allows easy navigation between pages.
Simple UI: Clean and user-friendly interface suitable for educational environments.
Installation and Setup
Prerequisites
Python 3.x: Make sure Python 3 is installed on your system.
pip: Python package installer should be available.
Flask: Install Flask using pip if not already installed.
Dependencies
Install the required Python packages:

bash
Copy code
pip install flask
Directory Structure
Ensure your project directory has the following structure:

arduino
Copy code
your_project/
├── app.py
├── questions.db
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── submit_question.html
│   ├── thank_you.html
│   ├── view_questions.html
│   ├── teacher.html
│   └── 403.html
└── static/
    └── styles.css
Setting Up the Application
Clone or Download the Repository:

Clone this repository or download the source code to your local machine.

Navigate to the Project Directory:

bash
Copy code
cd your_project
Initialize the Database:

The database will be initialized automatically when you run the application for the first time.

Running the Application
Start the Flask Application:

Run the following command in your terminal:

bash
Copy code
python app.py
You should see output similar to:

csharp
Copy code
Host IP address: 192.168.1.100
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
Access the Application:

Teacher's Computer:

Home Page: http://localhost:5000/
Teacher Page: http://localhost:5000/teacher
Students' Computers:

Home Page: http://192.168.1.100:5000/ (Replace with your actual IP address)
Usage Instructions
For the Teacher
Access the Teacher Page:

Navigate to http://localhost:5000/teacher on your computer.

Respond to Questions:

View submitted questions.
Enter responses in the provided text areas.
Click "Submit Response" to save your response.
Delete All Questions:

Click the "Delete All Questions" button.
Confirm the action when prompted.
All questions and responses will be deleted.
For Students
Submit a Question:

Navigate to http://<teacher's_IP_address>:5000/submit in your web browser.
Enter your question in the text area.
Click "Submit" to send your question anonymously.
View Questions and Responses:

Navigate to http://<teacher's_IP_address>:5000/questions.
View submitted questions and teacher responses.
The page refreshes automatically every 5 seconds.
Configuring for Network Access
Allow External Access
Modify the app.run() call in app.py to listen on all network interfaces:

python
Copy code
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
Find Your IP Address
On the teacher's computer, find the local IP address:

Windows:

bash
Copy code
ipconfig
macOS/Linux:

bash
Copy code
ifconfig
Note the IP address (e.g., 192.168.1.100).

Adjust Firewall Settings
Ensure that your firewall allows incoming connections on port 5000.

Windows Firewall:

Open "Windows Defender Firewall with Advanced Security".
Create a new inbound rule for port 5000.
macOS Firewall:

Go to "System Preferences" > "Security & Privacy" > "Firewall".
Add an exception for the application or allow incoming connections.
Linux (ufw):

bash
Copy code
sudo ufw allow 5000
Troubleshooting
OperationalError: no such column: response
If you encounter the following error:

makefile
Copy code
sqlite3.OperationalError: no such column: response
It means your database schema is outdated. To fix this:

Option 1: Alter the Existing Database (Recommended):

Use the SQLite command-line tool to add the missing column.

bash
Copy code
sqlite3 questions.db
In the SQLite prompt:

sql
Copy code
ALTER TABLE questions ADD COLUMN response TEXT;
.exit
Option 2: Delete and Recreate the Database:

If no important data is stored, delete questions.db and restart the app.

bash
Copy code
rm questions.db
python app.py
Students Cannot Access the Application
Ensure the Flask app is running and accessible.
Verify the correct IP address and port number.
Check firewall settings on both the teacher's and students' computers.
Confirm that both devices are on the same local network.
Security Considerations
Access Control:

The teacher's pages are restricted to the teacher's computer based on IP address.
Data Privacy:

No personal information is collected from students.
Network Security:

Ensure your local network is secure to prevent unauthorized access.
Application Structure
app.py
Contains the Flask application code, including route definitions and database interactions.

Templates
base.html: Base template with common layout and sidebar navigation.
home.html: Home page template.
submit_question.html: Template for the question submission page.
thank_you.html: Thank you page displayed after question submission.
view_questions.html: Template for displaying questions and responses to students.
teacher.html: Teacher's interface for viewing and responding to questions.
403.html: Custom 403 Forbidden error page.
Static Files
styles.css: Contains CSS styles for the application.
Future Enhancements
User Authentication: Implement password protection for the teacher's pages.
Input Validation: Enhance validation and sanitization of user input.
Database Migrations: Use tools like Alembic for database schema changes.
Responsive Design: Improve UI for better mobile device support.
License
This project is intended for educational purposes.

Acknowledgments
Flask: https://flask.palletsprojects.com/
SQLite: https://www.sqlite.org/index.html
Contact
For any questions or support, please contact the project maintainer.