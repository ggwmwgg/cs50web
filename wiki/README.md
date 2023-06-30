## Wiki (from CS50W course | Updated)

### Description
A website where users are able to create (using markdown), view and search for entries 

#### Technologies used:
- *Python*
- *Django*
- *HTML*
- *CSS/Bootstrap5*
- *Docker*
- *Unit tests/Django tests*
- *PostgreSQL*
- *Markdown*

#### Configuring:
- Install ```requirements.txt```.
- Run ```python manage.py runserver 8080``` in ```/``` directory.
- Visit ```http://127.0.0.1:8000/```.

#### Docker (NEW):
- Install docker and docker-compose.
- Change database, user, password to your own in ```db.env``` and ```docker-compose.yml``` files.
- Build containers using ```docker-compose build```.
- Run containers using ```docker-compose up```, you can add ```-d``` flag to run in background.
- When containers are running, commands for tests and migrations are already applied (```entry.sh```).
- To enter bash use ```docker exec -it <container_name> bash```.
- To enter django console use ```docker exec -it wiki python manage.py shell```.
- Stop containers using ```docker-compose down```.

#### Tests (NEW):
- Tests were created to test ```util.py``` functions (```save_entry```, ```get_entry```, ```list_entries```).
- To test ```models.py``` (```Entry```).
- To test ```views.py``` (```index```, ```entry```, ```search```, ```add```, ```random```, ```edit```, ```save```).
- To test ```NewPageForm```.
- Tests can be run using ```python manage.py test```, by default, in docker tests are run after migrations.

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
	- Clicking ```Random Page``` in the sidebar will take user to a random encyclopedia entry.

- Markdown to HTML Conversion:
	- On each entry’s page, any Markdown content in the entry file will be converted to HTML before being displayed to the user. I have used ```python-markdown2``` package and custom django filter to perform this conversion.

- Updated(from initial version):
	- Created ```Entry``` model to store entries in database and added a migration file.
	- ```util.py``` changed to work with ```PostgreSQL``` instead of filesystem.
    - ```settings.py``` db changed to work with ```PostgreSQL```.
    - Now default entries are added automatically if ```list_entries()``` is empty.
    - Docker and docker-compose added.
    - ```entry.sh``` added.
    - ```docker-compose.yml``` added for docker configuration.
    - ```Dockerfile``` added for docker configuration.
    - ```tests.py``` added and run automatically after migrations.

#### Contributing
Pull requests are welcome. For major changes please open an issue first.