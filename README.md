# TakeNotes
#### Video Demo:  <[Click Here](https://youtu.be/4VTulaA2yck)>
#### Description:

My final project, **TakeNotes**, is a web-based note-taking application developed using Python's Flask framework, alongside JavaScript, SQLite 3, HTML, and CSS for front-end interactivity and design.

This project brings together everything I’ve learned in CS50, showing how I can now create a working web application that combines back-end and front-end development.

I chose to make an app using Python’s Flask framework as I wanted to further develop what I learned from week 9 of the course and the “Finance” problem set. Also, I wanted to dive a bit deeper into Bootstrap and learn Bootstrap Studio, which I used to make some parts of the static HTML pages look more aesthetically pleasing.

**TakeNotes** lets users easily organize their tasks and reminders by creating notes that include a date as well as some more useful functionalities like:
-	Changing the background color of each note, which helps in sorting and categorizing them.
-	Reordering notes by dragging and dropping them
-	Editing the content and the date of the note
-	Deleting notes when they’re no longer needed

Now I’ll go over each of the files I wrote for my project, talk about some more features and explain my thought process behind my decisions.

As any other web application, my project allows users to sign up, log in and log out, so let’s begin with these 3 features.

#### The Log In page("index.html")

The Log In page is the landing page of my app.
For its style I used mainly Bootstrap Studio as well as some inline style tags.
The basics of the page are login in with an email and password as well as an option to sign up in case the user does not have an account.

The HTML contains a core feature that I wanted to work with which are modals. I have used them as a way to check for errors and to improve the user’s experience:

-	If the user tries to click the log out nav bar button before logging in, a modal will pop up that says, “You need to be signed in to log out!”
-	On the other hand, if the user clicks the log in nav bar button when they are already logged in, a modal will pop up saying “You are already logged in!”
-	Modals that are built into the HTML “required” attribute will also show in case the user does not input their email or password correctly.

Additionally, I have included flashed messaging using Bootstrap alerts, Jinja2 and Python, these messages are triggered by:

-	Missing email and/or password fields, triggers the flashed message (email and/or password cannot be empty!”)
-	If the email and/or password are not in the database (Invalid email and/or password)

Once “Log In” is clicked session["user_id"]  is set to user_db[0]["id"] and the user is logged in.

#### The Sign-Up page("login.html")

The sign-up page is very similar to the log in page in styling, with the main difference being an extra input field to check for password confirmation.
It has the same modal features as the login page except for the “You are already logged in!” pop-up.
It also includes flashed messaging, in these cases:

-	The email, password and confirmation are left empty, prompts (Email/Password/Confirmation cannot be empty!)
-	The password and confirmation don’t match (Passwords do not match!)
-	Email is already registered (This email is already registered!)
-	The user is successfully registered (Registration successful! You can now log in.), redirects to the login page

Before a password is added to the SQLite 3 database it is passed in to the generate_password_hash function which hashes the password for better security.

#### The Index page("index.html")

The index (or notes) page includes the main aspect of the project which is taking notes.
Once the user has logged in, they are redirected to this page and greeted with an alert that displays “Logged In!”

The user can than go on to add a note, along with a date, by inputting the information and clicking “Add note”, this will add what was inputted to the container below, which previously had the placeholder text “no notes yet”.
The text and date will be stored in the SQL database and will stay there even if the user log’s out.
Along with the added note and date, multiple buttons will be displayed:
-	Edit: Will trigger JavaScript to display a hidden form (edit_note route in Python), text area and date input where the information previously stored can be changed.
-	Save/Cancel (Only after “Edit” is clicked): stores the edited content in the database, replacing the old note or exits out of the hidden form.
-	Update Color/Select Color: After choosing a color (white, pink, green, purple) from the select dropdown, the update color button will submit the form. The background color of the note will be changed and overwritten in the database.
-	Delete: Triggers the delete_note route in Python which removes the note and all its content, including date and color from the database.

These also include flashed messages:
-	“Note updates successfully!”
-	“Note color updated!”
-	“Note deleted”

#### Sortable Notes

Another trait that I wanted to add to my page was sortable notes, which I achieved by using the “Sortable” JavaScript library, which enables a group of DOM elements to be sortable.
This allows for easily re-ordering notes using drag-and-drop.

#### Log Out

Once “Log Out” is clicked a modal will display a message “Are you sure you want to log out?” along with the buttons “Log Out” and “Cancel”, which will effectively log out the user, clearing the session or cancel the operation.

#### Project.db
The tables I've used for the database of my project are as follows:

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT
NOT NULL, hash TEXT NOT NULL);

CREATE UNIQUE INDEX username ON users(email);

CREATE TABLE notes (

id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
user_id INTEGER NOT NULL,
notes TEXT NOT NULL, date TEXT, color TEXT,
FOREIGN KEY (user_id) REFERENCES users(id)
);

#### App.py and helpers.py

App.py contains all of the routes for my application which are:

- /signup: handles creating user's account
- /login: logs user in
- /(index): handles all of the note functionalities
- /logout: logs user out
- /delete_note: handles deleting notes
- /edit_note: handles editing notes

Helpers.py contains all of the helper functions for app.py:

- apology: which is not implemented in the page but was used to help me create my application's routes (this function was re-used from the "Finance" problem set)

- login_required: requires users to log in (also re-used from the "Finance" problem set)

#### Static folder

Contains all of the static files for the application including:

- bootstrap: "bootstrap.min.css", "bootstrap.min.js" (both from Bootstrap Studio)
- js: "scripts.js" (Main JavaScript file)

#### Conclusion

Overall, I am happy with the result of my project, with everything I have learned during the CS50x course, and I look forward to applying these skills and learning more about programming.

This was CS50!
