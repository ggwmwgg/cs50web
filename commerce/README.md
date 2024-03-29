## Commerce (from CS50W course | Updated)

### Description
An eBay-like e-commerce auction site where users are able to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

#### Technologies used:
- *Python*
- *Django*
- *HTML5*
- *CSS3/Bootstrap5*
- *Docker*
- *Unit tests/Django tests*
- *PostgreSQL*

#### Configuring(PC):
- Install ```requirements.txt```.
- Run ```python manage.py makemigrations``` to make migrations for the commerce app.
- Connect to your own PostgreSQL database in ```settings.py``` (by default it set to be working with docker).
- Apply migrations to db ```python manage.py migrate```
- Create a superuser using ```python manage.py createsuperuser``` to visit ```/admin``` page in future 
- Run ```python manage.py runserver 8080``` in ```/``` directory.
- Visit ```http://127.0.0.1:8000/```.

#### Docker (NEW):
- Install docker and docker-compose.
- Change database, user, password to your own in ```db.env``` and ```docker-compose.yml``` files.
- Build containers using ```docker-compose build```.
- Run containers using ```docker-compose up```, you can add ```-d``` flag to run in background.
- When containers are running, commands for tests and migrations are already applied (```entry.sh```).
- To enter bash use ```docker exec -it <container_name> bash```.
- To enter db container use ```docker exec -it db psql -U <db_user>```.
- To enter django console use ```docker exec -it commerce python manage.py shell```.
- Stop containers using ```docker-compose down```.

#### Tests (NEW):
- ```ModelsIndexTestCase``` created:
  - To test models (```User```, ```Category```, ```Listing```, ```Bid```, ```Comment```, ```Watchlist```).
  - To test ```index``` view.
- ```AuthTestCase``` created:
  - To test ```login_view```, ```logout_view``` and ```register``` views.
- ```ListingCategoriesTestCase``` created:
  - To test ```create```, ```listing```, ```categories``` and ```category``` views.
- ```ListingActionsTestCase``` created:
  - To test ```close```, ```add_comment```, ```watchlist```, and ```add_bid``` views.

#### Implementations:
- Models:
	- Application includes 5 models in addition to the User model: 
		- Category
		- Listing
		- Bid
		- Comment
		- Watchlist

- Create listing:
	- Users are able to visit a page to create a new listing, specify a title for the listing, a text-based description, and what the starting bid should be. 
	- Users will also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

- Active Listings Page:
	- The default route of application will let users view all of the currently active auction listings. 
	- For each active listing, this page will display the title, description, current price, and photo (if one exists for the listing).

- Listing Page:
	- Clicking on a listing will take users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing.
	- If the user is signed in, the user is able to add the item to their “Watchlist.” If the item is already on the watchlist, the user is able to remove it.
	- If the user is signed in, the user is able to bid on the item. The bid should be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user will be presented with an error.
	- If the user is signed in and is the one who created the listing, the user will have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
	- If a user is signed in on a closed listing page, and the user has won that auction, the page will say so.
	- Users who are signed in are able to add comments to the listing page. The listing page will display all comments that have been made on the listing.

- Watchlist:
	- Users who are signed in are able to visit a Watchlist page, which will display all of the listings that a user has added to their watchlist. Clicking on any of those listings will take the user to that listing’s page.

- Categories:
	- Users are be able to visit a page that displays a list of all listing categories. Clicking on the name of any category will take the user to a page that displays all of the active listings in that category.

- Django Admin Interface:
	- Via the Django admin interface, a site administrator (creation in Usage) is able to view, add, edit, and delete any listings, comments, and bids made on the site.

- New:
  	- Standard database replaced with PostgreSQL.
    - Docker and docker-compose added.
    - ```entry.sh``` added for migrations and tests.
    - ```db.env``` added for database configuration.
    - ```docker-compose.yml``` added for docker configuration.
    - ```Dockerfile``` added for docker configuration.
    - ```tests.py``` added and run automatically after migrations.

#### Contributing
Pull requests are welcome. For major changes please open an issue first.