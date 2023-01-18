## Mail (from CS50W course)

### Description
Website with front-end for an email client that makes API calls to send and receive emails.

#### Technologies used:
- *Python*
- *Django*
- *Javascript*
- *HTML*
- *CSS*

#### Configuring:
- Install ```requirements.txt```.
- Run ```python manage.py makemigrations``` to make migrations for the commerce app.
- Apply migrations to db ```python manage.py migrate```
- Run ```python manage.py runserver 8080``` in ```/``` directory.
- Visit ```http://127.0.0.1:8000/```.


#### Implementations:
	- Send mail:
		- When a user submits the email composition form, JavaScript code added to actually send the email.
		- Made via ```POST``` request to ```/emails```, passing in values for ```recipients```, ```subject```, and ```body```.
		- Once the email has been sent, the user’s sent mailbox is loaded.
		
	- Mailbox:
		- When a user visits their Inbox, Sent mailbox, or Archive, the appropriate mailbox loaded.
		- Made via ```GET``` request to ```/emails/<mailbox>``` to request the emails for a particular mailbox.
		- When a mailbox is visited, the application will first query the API for the latest emails in that mailbox.
		- When a mailbox is visited, the name of the mailbox will appear at the top of the page.
		- Each email will then be rendered in its own box (as a ```<div>``` with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.
		- If the email is unread, it will appear with a white background. If the email has been read, it will appear with a gray background.
		
	- View Mail:
		- When a user clicks on an email, the user will be taken to a view where they see the content of that email.
		- Made via ```GET``` request to ```/emails/<email_id>``` to request the email.
		- Application will show the email’s sender, recipients, subject, timestamp, and body.
		- Additional ```div``` to ```inbox.html``` added(in addition to ```emails-view``` and ```compose-view```) for displaying the email.
		- Once the email has been clicked on, it will be marked as read (via ```PUT```).
		
	- Archive and Unarchive:
		- Allows users to archive and unarchive emails that they have received.
		- When viewing an Inbox email, the user will be presented with a button that lets them archive the email. When viewing an Archive email, the user will be presented with a button that lets them unarchive the email. This requirement does not apply to emails in the Sent mailbox.
		- Made via ```PUT``` request to ```/emails/<email_id>``` to mark an email as archived or unarchived.
		- Once an email has been archived or unarchived, the user’s inbox reloading.
		
	- Reply:
		- Allows users to reply to an email.
		- When viewing an email, the user will be presented with a “Reply” button that lets them reply to the email.
		- When the user clicks the “Reply” button, they will be taken to the email composition form.
		- The composition form is pre-filled with the recipient field set to whoever sent the original email.
		- The subject line is pre-filled. If the original email had a subject line of ```foo```, the new subject line will be ```Re: foo```. (If the subject line already begins with ```Re:``` , it won't be added again.)
		- The body of the email is pre-filled with a line like ```"On Jan 1 2020, 12:00 AM foo@example.com wrote:"``` followed by the original text of the email.
	
#### Contributing
Pull requests are welcome. For major changes please open an issue first to discuss what you would like to change.