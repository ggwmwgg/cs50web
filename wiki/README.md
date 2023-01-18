## Wiki (from CS50W course)

### Description
A website where users are able to create (using markdown), view and search for entries 

#### Technologies used:
- *Python*
- *Django*
- *HTML*
- *CSS*

#### Configuring:
- Install ```requirements.txt```.
- Run ```python manage.py runserver 8080``` in ```/``` directory.
- Visit ```http://127.0.0.1:8000/```.


#### Implementations:
- Entry Page:
	- Visiting ```/wiki/TITLE```, where ```TITLE``` is the title of an encyclopedia entry, render a page that displays the contents of that encyclopedia entry.
	- The view get the content of the encyclopedia entry by calling the appropriate ```util``` function.
	- If an entry is requested that does not exist, the user be presented with an error page indicating that their requested page was not found.
	- If the entry does exist, the user be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.

- Index Page:
	- Updated ```index.html``` such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.

- Search:
	- User is able to type a query into the search box in the sidebar to search for an encyclopedia entry.
	- If the query matches the name of an encyclopedia entry, the user will be redirected to that entry’s page.
	- If the query does not match the name of an encyclopedia entry, the user will instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ```ytho```, then ```Python``` will appear in the search results.
	- Clicking on any of the entry names on the search results page will take the user to that entry’s page.

- New Page:
	- Clicking “Create New Page” in the sidebar will take the user to a page where they can create a new encyclopedia entry.
	- Users are able to enter a title for the page and, in a ```textarea```, able to enter the Markdown content for the page.
	- Users are able to click a button to save their new page.
	- When the page is saved, if an encyclopedia entry already exists with the provided title, the user will be presented with an error message.
	- Otherwise, the encyclopedia entry will be saved to disk, and the user will be taken to the new entry’s page.

- Edit Page: 
	- On each entry page, the user is able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a ```textarea```.
	- The ```textarea``` is pre-populated with the existing Markdown content of the page. (i.e., the existing content will be the initial value of the textarea).
	- The user is able to click a button to save the changes made to the entry.
	- Once the entry is saved, the user will be redirected back to that entry’s page.

- Random Page:
	- Clicking “Random Page” in the sidebar will take user to a random encyclopedia entry.

- Markdown to HTML Conversion:
	- On each entry’s page, any Markdown content in the entry file will be converted to HTML before being displayed to the user. I have used ```python-markdown2``` package and custom django filter to perform this conversion.

#### Contributing
Pull requests are welcome. For major changes please open an issue first to discuss what you would like to change.