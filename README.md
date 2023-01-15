# Portfolio

Digital Portfolio Using Flask

Viewers can signup and give ratings or comments about the Projects

# How to run this project: 

1. Open VSCode or any other code editor. And Install Packages mentioned in app.py and other files.
2. Open the app.py file and edit the SQLALCHEMY_DATABASE_URI field and add your mysql database password by replacing the "addyourpasswordhere" keywords
3. Open create_db.py and update your password there as well
4. Firstly excute the create_db.py script by running the following command: "py create_db.py"
5. Now you have to connect  the created database with your code so execute the following commands in your terminal:
	i. python
	ii. from app import app, db
	iii. app.app_context().push()
	iv. db.create_all()
	v. exit()
6. These commands will create a table called "users" in the mysql database
7. now execute the following command in the terminal: "py app.py"
