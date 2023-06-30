import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Category, Listing, Bid, Comment, Watchlist


# Create your tests here.
class ModelsIndexTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", email="user1@email.com", password="password")
        self.user2 = User.objects.create_user(username="user2", email="user2@email.com", password="password")
        self.user3 = User.objects.create_user(username="user3", email="user3@email.com", password="password")
        self.category1 = Category.objects.create(name="category1")
        self.category2 = Category.objects.create(name="category2")
        self.listing1 = Listing.objects.create(title="listing1 by user1", description="description1", starting_bid=1.00, category=self.category1, user=self.user1, is_active=True)
        self.listing2 = Listing.objects.create(title="listing2 by user1", description="description2", starting_bid=2.00, category=self.category2, user=self.user1, is_active=True)
        self.bid1 = Bid.objects.create(bid=1.50, user=self.user2, listing=self.listing1)
        self.bid2 = Bid.objects.create(bid=2.50, user=self.user3, listing=self.listing1)
        self.comment1 = Comment.objects.create(comment="comment1", user=self.user2, listing=self.listing2)
        self.comment2 = Comment.objects.create(comment="comment2", user=self.user3, listing=self.listing2)
        self.watchlist1 = Watchlist.objects.create(user=self.user1)
        self.watchlist1.listing.add(self.listing1)
        self.watchlist1.listing.add(self.listing2)

    def test_user(self):
        # Test User model
        self.assertEqual(self.user1.username, "user1")
        self.assertEqual(self.user2.email, "user2@email.com")

    def test_category(self):
        # Test Category model
        self.assertEqual(self.category1.name, "category1")
        self.assertEqual(self.category2.name, "category2")

    def test_listing(self):
        # Test Listing model
        self.assertEqual(self.listing1.title, "listing1 by user1")
        self.assertEqual(self.listing2.description, "description2")
        self.assertEqual(Listing.objects.all().count(), 2)

    def test_bid(self):
        # Test Bid model
        self.assertEqual(self.bid1.bid, 1.50)
        self.assertEqual(self.bid2.user, self.user3)
        self.assertEqual(Bid.objects.all().count(), 2)

    def test_comment(self):
        # Test Comment model
        comments_count_listing1 = Comment.objects.filter(listing=self.listing1).count()
        comments_count_listing2 = Comment.objects.filter(listing=self.listing2).count()
        self.assertEqual(self.comment1.comment, "comment1")
        self.assertEqual(self.comment2.user, self.user3)
        self.assertEqual(Comment.objects.all().count(), 2)
        self.assertEqual(comments_count_listing1, 0)
        self.assertEqual(comments_count_listing2, 2)

    def test_watchlist(self):
        # Test Watchlist model
        self.assertEqual(self.watchlist1.user, self.user1)
        self.assertEqual(self.watchlist1.listing.all().count(), 2)
        self.assertEqual(Watchlist.objects.all().count(), 1)

    def test_index(self):
        # Test index view
        response = self.client.get(reverse("index"))
        #print(response.context["listings"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["listings"]), 2)
        self.assertIsNone(response.context["alert_type"])
    def test_index_alert(self):
        # Test index view with alert
        response = self.client.get(reverse("index"), {"alert_message": "alert_message", "alert_type": "alert-success"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["alert_message"], "alert_message")
        self.assertEqual(response.context["alert_type"], "alert-success")


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", email="user1@email.com", password="password")
        self.user2 = User.objects.create_user(username="user2", email="user2@email.com", password="password")
        self.user3 = User.objects.create_user(username="user3", email="user3@email.com", password="password")

    def test_login_view_get_method(self):
        # Test login view
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/login.html")

    def test_login_view_post_method(self):
        # Test login view
        data = {
            "username": "user1",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('index') + '?alert_message=Logged+in+successfully%21&alert_type=alert-success',
            fetch_redirect_response=False
        )

    def test_login_view_invalid_post_method(self):
        # Test login view with invalid credentials
        data = {
            "username": self.user1.username,
            "password": "password1"
        }
        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/login.html")
        self.assertContains(response, "Invalid username and/or password.")

    def test_logout_view(self):
        # Test logout view
        self.client.force_login(self.user1)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('index') + '?alert_message=Logged+out+successfully%21&alert_type=alert-dark',
            fetch_redirect_response=False
        )

    def test_register_view_get_method(self):
        # Test register view
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/register.html")

    def test_register_view_post_method(self):
        # Test register view
        data = {
            "username": "user4",
            "email": "user4@email.com",
            "password": "password",
            "confirmation": "password"
        }
        response = self.client.post(reverse("register"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('index') + '?alert_message=Registered%20successfully!&alert_type=alert-success',
            fetch_redirect_response=False
        )

    def test_register_view_post_method_invalid_pw(self):
        # Test register view with invalid password confirmation
        data = {
            "username": "user4",
            "email": "user4@email.com",
            "password": "password",
            "confirmation": "password1"
        }
        response = self.client.post(reverse("register"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/register.html")
        self.assertContains(response, "Passwords must match.")

    def test_register_view_post_method_taken_username(self):
        # Test register view with taken username
        data = {
            "username": self.user1.username,
            "email": "user4@email.com",
            "password": "password",
            "confirmation": "password"
        }
        response = self.client.post(reverse("register"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/register.html")
        self.assertContains(response, "Username already taken.")
        # print("Username already taken.")


class ListingCategoriesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", email="user1@mail.com", password="password")
        self.user2 = User.objects.create_user(username="user2", email="user2@mail.com", password="password")
        self.user3 = User.objects.create_user(username="user3", email="user3@mail.com", password="password")

        self.category1 = Category.objects.create(name="category1")
        self.category2 = Category.objects.create(name="category2")
        self.category3 = Category.objects.create(name="category3")

        self.listing1 = Listing.objects.create(
            title="listing1",
            description="description1",
            starting_bid=1,
            category=self.category1,
            user=self.user1
        )
        self.listing2 = Listing.objects.create(
            title="listing2",
            description="description2",
            starting_bid=2,
            category=self.category1,
            user=self.user2
        )

    def test_create_view_get_method(self):
        # Test create view
        self.client.force_login(self.user1)
        response = self.client.get(reverse("create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/create.html")

    def test_create_view_post_method(self):
        # Test create view
        data = {
            'title': 'listing3',
            'description': 'description3',
            'starting_bid': '1.00',
            'image_url': 'listing3.jpg',
            'category': self.category1.id

        }
        self.client.force_login(self.user1)
        response = self.client.post(reverse("create"), data=data)
        self.assertEqual(response.status_code, 302)
        last_listing = Listing.objects.last()
        self.assertRedirects(
            response,
            reverse("listing", args=(last_listing.id,)) + "?alert_message=Listing+created+successfully%21&alert_type=alert-success",
            fetch_redirect_response=False
        )

    def test_listing_view_invalid(self):
        # Test listing view with invalid listing id
        last_listing = Listing.objects.last()
        last_listing = last_listing.id + 1
        response = self.client.get(reverse("listing", args=(last_listing,)))
        self.assertRedirects(
            response,
            reverse("index") + "?alert_message=Listing%20not%20found.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_listing_view(self):
        # Test listing view
        response = self.client.get(reverse("listing", args=(self.listing1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/listing.html")
        self.assertContains(response, self.listing1.title)
        self.assertContains(response, self.listing1.description)
        self.assertContains(response, self.listing1.starting_bid)
        self.assertContains(response, self.listing1.category.name)
        self.assertContains(response, self.listing1.user.username)

    def test_categories(self):
        # Test categories view
        response = self.client.get(reverse("categories"))
        categories_count = Category.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/categories.html")
        self.assertContains(response, self.category1.name)
        self.assertContains(response, self.category2.name)
        self.assertContains(response, self.category3.name)
        self.assertEqual(categories_count, 3)

    def test_category(self):
        # Test category view
        response = self.client.get(reverse("category", args=(self.category1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auctions/category.html")
        self.assertEqual(response.context['category'].name, self.category1.name)
        self.assertEqual(len(response.context['listings']), 2)

    def test_category_invalid(self):
        # Test category view with invalid category id
        last_category = Category.objects.last()
        last_category = last_category.id + 1
        response = self.client.get(reverse("category", args=(last_category,)))
        self.assertRedirects(
            response,
            reverse("index") + "?alert_message=Category%20not%20found.&alert_type=alert-danger",
            fetch_redirect_response=False
        )


class ListingActionsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", email="user1@mail.com", password="password")
        self.user2 = User.objects.create_user(username="user2", email="user2@mail.com", password="password")
        self.category1 = Category.objects.create(name="category_1")
        self.category2 = Category.objects.create(name="category_2")
        self.category3 = Category.objects.create(name="category_3")

        self.listing1 = Listing.objects.create(
            title="listing_1",
            description="description_1",
            starting_bid=1.5,
            # current_bid=1.5,
            category=self.category1,
            user=self.user1
        )
        self.listing2 = Listing.objects.create(
            title="listing_2",
            description="description_2",
            starting_bid=2.05,
            # current_bid=2.05,
            category=self.category1,
            user=self.user2
        )
        watchlist_user1 = Watchlist(user=self.user1)
        watchlist_user1.save()
        watchlist_user1.listing.add(self.listing1)

    def test_close_invalid(self):
        # Test close view invalid listing id
        self.client.force_login(self.user1)
        last_listing = Listing.objects.last()
        last_listing = last_listing.id + 1
        response = self.client.get(reverse("close", args=(last_listing,)))
        self.assertRedirects(
            response,
            reverse("index") + "?alert_message=Listing%20not%20found.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_close_get(self):
        # Test close view get method
        self.client.force_login(self.user1)
        response = self.client.get(reverse("close", args=(self.listing1.id,)))
        self.assertRedirects(response, reverse("index"))

    def test_close_listing_invalid(self):
        # Test close view post method with not owner user
        self.client.force_login(self.user2)
        listing_test = Listing.objects.create(
            title="listing_test",
            description="description_test",
            starting_bid=2.05,
            category=self.category1,
            user=self.user1
        )
        response = self.client.post(reverse("close", args=(listing_test.id,)))
        self.assertRedirects(
            response,
            reverse("listing", args=(listing_test.id,)) + "?alert_message=You%20are%20not%20the%20owner%20of%20this%20listing.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_close_invalid_listing(self):
        # Test close view post method with invalid listing id
        self.client.force_login(self.user1)
        last_listing = Listing.objects.last()
        last_listing = last_listing.id + 1
        response = self.client.post(reverse("close", args=(last_listing,)))
        self.assertRedirects(
            response,
            reverse("index") + "?alert_message=Listing%20not%20found.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_close_listing(self):
        # Test close view post method
        self.client.force_login(self.user1)
        listing_test = Listing.objects.create(
            title="listing_test",
            description="description_test",
            starting_bid=2.05,
            category=self.category1,
            user=self.user1
        )
        response = self.client.post(reverse("close", args=(listing_test.id,)))
        self.assertRedirects(
            response,
            reverse("listing", args=(listing_test.id,)) + "?alert_message=Listing%20closed%20successfully!&alert_type=alert-dark",
            fetch_redirect_response=False
        )

    def test_add_comment_invalid_listing(self):
        # Test add comment view with invalid listing id
        self.client.force_login(self.user1)
        last_listing = Listing.objects.last()
        last_listing = last_listing.id + 1
        response = self.client.post(reverse("add_comment", args=(last_listing,)))
        self.assertRedirects(
            response,
            reverse("index") + "?alert_message=Listing%20not%20found.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_add_comment_get(self):
        # Test close view get method
        self.client.force_login(self.user2)
        response = self.client.get(reverse("add_comment", args=(self.listing1.id,)))
        self.assertRedirects(response, reverse("index"))

    def test_add_comment_post(self):
        # Test add comment view post method
        self.client.force_login(self.user1)
        data = {
            "comment": "comment_test"
        }
        response = self.client.post(reverse("add_comment", args=(self.listing1.id,)), data=data)
        self.assertRedirects(
            response,
            reverse("listing", args=(self.listing1.id,)) + "?alert_message=Comment%20added%20successfully!&alert_type=alert-success",
            fetch_redirect_response=False
        )

    def test_watchlist_get(self):
        # Test watchlist view get method
        self.client.force_login(self.user1)
        response = self.client.get(reverse("watchlist"))
        self.assertFalse(response.context['empty'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['listings']), 1)

    def test_watchlist_get_empty(self):
        # Test watchlist view get method with empty watchlist
        self.client.force_login(self.user2)
        response = self.client.get(reverse("watchlist"))
        self.assertTrue(response.context['empty'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['listings']), 0)

    def test_watchlist_post_invalid_listing(self):
        # Test watchlist view post method with invalid listing id
        self.client.force_login(self.user1)
        last_listing = Listing.objects.last()
        last_listing = last_listing.id + 1
        data = {
            "listing_id": last_listing,
            "action": "a"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("index") + "?alert_message=Listing%20not%20found.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_watchlist_already_added(self):
        # Test watchlist view post method with already added listing
        self.client.force_login(self.user1)
        data = {
            "listing_id": self.listing1.id,
            "action": "a"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("listing", args=(self.listing1.id,)) + "?alert_message=Listing%20already%20in%20watchlist.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_watchlist_add(self):
        # Test watchlist view post method with add action
        self.client.force_login(self.user2)
        data = {
            "listing_id": self.listing1.id,
            "action": "a"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("listing", args=(self.listing1.id,)) + "?alert_message=Listing%20added%20to%20watchlist%20successfully!&alert_type=alert-success",
            fetch_redirect_response=False
        )

    def test_watchlist_remove_invalid_listing(self):
        # Test watchlist view post method with listing that is not in watchlist
        self.client.force_login(self.user1)
        data = {
            "listing_id": self.listing2.id,
            "action": "r"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("listing", args=(self.listing2.id,)) + "?alert_message=Listing%20not%20found%20in%20watchlist.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_watchlist_remove(self):
        # Test watchlist view post method with remove action
        self.client.force_login(self.user1)
        data = {
            "listing_id": self.listing1.id,
            "action": "r"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("listing", args=(self.listing1.id,)) + "?alert_message=Listing%20removed%20from%20watchlist%20successfully!&alert_type=alert-dark",
            fetch_redirect_response=False
        )

    def test_watchlist_remove_r_invalid_listing(self):
        # Test watchlist view post method with listing that is not in watchlist
        self.client.force_login(self.user1)
        data = {
            "listing_id": self.listing2.id,
            "action": "remove"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("watchlist") + "?alert_message=Listing%20not%20found%20in%20watchlist.&alert_type=alert-danger",
            fetch_redirect_response=False
        )

    def test_watchlist_remove_r(self):
        # Test watchlist view post method with remove action
        self.client.force_login(self.user1)
        data = {
            "listing_id": self.listing1.id,
            "action": "remove"
        }
        response = self.client.post(reverse("watchlist"), data=data)
        self.assertRedirects(
            response,
            reverse("watchlist") + "?alert_message=Listing%20removed%20from%20watchlist%20successfully!&alert_type=alert-dark",
            fetch_redirect_response=False
        )

    def test_add_bid_get(self):
        # Test add bid view get method
        self.client.force_login(self.user1)
        response = self.client.get(reverse("add_bid", args=(self.listing1.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("listing", args=(self.listing1.id,)))

    def test_add_bid_post(self):
        # Test add bid view post method
        self.client.force_login(self.user1)
        response = self.client.post(reverse("add_bid", args=(self.listing1.id,)), data={"bid": 5.0})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("listing", args=(self.listing1.id,)) + "?alert_message=Bid%20added%20successfully!&alert_type=alert-success",
            fetch_redirect_response=False
        )


