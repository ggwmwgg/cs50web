## Twitter (from CS50W course | Updated)

### Description
A twitter like website with client-side web API and Django server where users are able to create posts, follow each other, comment, like/unlike and bookmark posts. 

#### Technologies used:
- *Python*
- *Django*
- *Javascript*
- *HTML*
- *CSS/Bootstrap5*
- *Docker*
- *Unit tests/Django tests*
- *PostgreSQL*

#### Configuring:
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
- To enter django console use ```docker exec -it twitter python manage.py shell```.
- Stop containers using ```docker-compose down```.

#### Tests (NEW):
- ```ModelsAuthTestCase``` created: 
  - To test models (```User```, ```Post```, ```Comment```) and relations between them.
  - To test ```index```, ```login_view```, ```logout_view```, ```register``` and ```index``` views. 
- ```CreatePostTestCase``` created:
  - To test ```create``` view.
- ```NotFoundTestCase``` created:
  - To test ```404``` page.
- ```PostsTestCase``` created:
  - To test ```posts_wo_pg```, ```posts_all```, ```posts``` and ```post``` views.
- ```ProfileUserTestCase``` created:
  - To test ```profile_own```, ```profile_wo_pg```, ```profile```, ```followers``` and ```users``` views.
  
#### Implementations:
- New Post:
    - Users who are signed in are able to write a new text-based post by filling in text into a ```text area``` and then clicking a button to submit the post.
- All Posts:
    - Each post includes the ```username``` of the poster, the post ```content``` itself, the ```date``` and ```time``` at which the post was made, and the number of ```likes``` and ```comments``` the post has.
- Profile Page:
    - Displaying the ```number``` of ```followers``` the user has, as well as the ```number``` of people that the user ```follows``` and number of posts.
    - Clicking on followers or following numbers will open a ```modal``` window which will show current followers/following users.
    - For any other user who is signed in, page also displays a ```Follow``` or ```Unfollow``` button that will let the current user toggle whether or not they are following this user’s posts. This only applies to any “other” user: a user cannot follow themselves.
- Following:
    - The ```Following``` link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
    - This page behaves just as the ```All Posts``` page does, just with a more limited set of posts.
- Pagination: 
    - On any page that displays a post, posts are displayed ```10 on a page``` (using django pagination, bootstrap 5 pagination and js)
    - If there are more than ten posts, a ```Next``` button will appear to take the user to the next page of posts (which are older than the current page of posts). If not on the first page, a ```Previous``` button will appear to take the user to the previous page of posts as well.
- Edit Post:
    - Users are able to click an ```Edit``` button or link on any of their own posts to edit that post.
    - The user should then able to ```Save``` the edited post. Using JavaScript, I've achieved this without requiring a reload of the entire page.
- “Like” and ```Unlike```/```Comment```/```Bookmark```:
    - Users are able to ```like```/```unlike```, ```comment``` and add to ```bookmarks``` any posts.
- Admin Panel:
    - Admin Panel view was also modified to make some fixes/corrections effectively.
- Updated(from initial version):
  	- Standard database (sqlite3) replaced with PostgreSQL.
    - Fixed migrations.
    - Docker and docker-compose added.
    - ```entry.sh``` added for migrations and tests.
    - ```db.env``` added for database configuration.
    - ```docker-compose.yml``` added for docker configuration.
    - ```Dockerfile``` added for docker configuration.
    - ```tests.py``` added and run automatically after migrations.

#### Contributing
Pull requests are welcome. For major changes please open an issue first.