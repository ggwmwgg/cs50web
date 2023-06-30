import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Email


# Create your tests here.
class ModelsIndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", email='user1@mail.com', password="password")
        self.user2 = User.objects.create_user(username="user2", email='user2@mail.com', password="password")
        self.user3 = User.objects.create_user(username="user3", email='user3@mail.com', password="password")
        self.email1 = Email.objects.create(
                    user=self.user1,
                    sender=self.user1,
                    subject='Test subject',
                    body='Test email1 body',
                    read=False,
                    archived=False
        )
        self.email1.recipients.add(self.user2)
        self.email2 = Email.objects.create(
                    user=self.user1,
                    sender=self.user1,
                    subject='Test subject',
                    body='Test email2 body',
                    read=False,
                    archived=False
        )
        self.email2.recipients.add(self.user2)
        self.email2.recipients.add(self.user3)
        self.email3 = Email.objects.create(
                    user=self.user1,
                    sender=self.user1,
                    subject='Test subject',
                    body='Test email3 body',
                    read=False,
                    archived=False
        )
        self.email3.recipients.add(self.user3)

    def test_user(self):
        # Test User model
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user2.username, 'user2')

    def test_email(self):
        # Test Email model
        self.assertEqual(self.email1.user, self.user1)
        self.assertEqual(self.email2.sender, self.user1)
        self.assertEqual(self.email3.recipients.all()[0], self.user3)
        self.assertEqual(self.email1.subject, 'Test subject')

    def test_index_not_logged_in(self):
        # Test index view unauthorized
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_index_logged_in(self):
        # Test index view authorized
        self.client.force_login(self.user1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mail/inbox.html')

    def test_compose_not_logged_in(self):
        # Test compose view unauthorized
        response = self.client.get(reverse('compose'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, "/accounts/login/?next=/emails")

    def test_compose_logged_in_get(self):
        # Test compose view with GET request
        self.client.force_login(self.user1)
        response = self.client.get(reverse('compose'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "POST request required."})

    def test_compose_logged_in_post_no_recipients(self):
        # Test compose view with POST request and no recipients
        self.client.force_login(self.user1)
        data = {
            "recipients": "",
            "subject": "Test subject",
            "body": "Test body"
        }
        response = self.client.post(reverse('compose'), data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "At least one recipient required."})

    def test_compose_logged_in_post_invalid_email(self):
        # Test compose view with POST request and invalid email
        self.client.force_login(self.user1)
        data = {
            "recipients": "invalid_email@mail.com",
            "subject": "Test subject",
            "body": "Test body"
        }
        response = self.client.post(reverse('compose'), data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "User with email invalid_email@mail.com does not exist."})

    def test_compose_logged_in_post(self):
        # Test compose view with POST request
        self.client.force_login(self.user1)
        data = {
            "recipients": f'{self.user2.email} , {self.user3.email}',
            "subject": "Test subject",
            "body": "Test body for test"
        }
        response = self.client.post(reverse('compose'), data, content_type="application/json")
        last_email = Email.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, {"message": "Email sent successfully."})
        self.assertEqual(last_email.sender, self.user1)
        self.assertEqual(last_email.recipients.all()[0], self.user2)
        self.assertEqual(last_email.recipients.all()[1], self.user3)
        self.assertEqual(last_email.body, "Test body for test")

    def test_mailbox_not_logged_in(self):
        # Test mailbox view unauthorized
        response = self.client.get(reverse('mailbox', args=['inbox']))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, "/accounts/login/?next=/emails/inbox")

    def test_mailbox_logged_in_invalid(self):
        # Test mailbox view with invalid mailbox
        self.client.force_login(self.user1)
        response = self.client.get(reverse('mailbox', args=['invalid']))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid mailbox."})

    def test_mailbox_logged_in(self):
        # Test mailbox view with valid mailbox
        self.client.force_login(self.user1)
        response = self.client.get(reverse('mailbox', args=['inbox']))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('mailbox', args=['sent']))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 3)
        self.assertEqual(response_data[0]['sender'], self.user1.email)

    def test_email_not_logged_in(self):
        # Test email view unauthorized
        response = self.client.get(reverse('email', args=[self.email1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, f"/accounts/login/?next=/emails/{self.email1.id}")

    def test_email_logged_invalid(self):
        # Test email view with invalid email id
        self.client.force_login(self.user1)
        response = self.client.get(reverse('email', args=[100]))
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {"error": "Email not found."})

    def test_email_logged_post(self):
        # Test email view with POST request
        self.client.force_login(self.user1)
        response = self.client.post(reverse('email', args=[self.email1.id]))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "GET or PUT request required."})

    def test_email_logged_get(self):
        # Test email view with GET request
        self.client.force_login(self.user1)
        response = self.client.get(reverse('email', args=[self.email1.id]))
        self.assertEqual(response.status_code, 200)
        data = {
            "id": self.email1.id,
            "sender": self.user1.email,
            "recipients": [self.user2.email],
            "subject": self.email1.subject,
            "body": self.email1.body,
            "timestamp": self.email1.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": False,
            "archived": False
        }
        self.assertJSONEqual(response.content, data)

    def test_email_logged_put_read(self):
        # Test email view with PUT request read
        self.client.force_login(self.user1)
        data = {
            "read": True
        }
        response = self.client.put(reverse('email', args=[self.email1.id]), data, content_type="application/json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Email.objects.get(id=self.email1.id).read, True)

    def test_email_logged_put_archived(self):
        # Test email view with PUT request archived
        self.client.force_login(self.user1)
        data = {
            "archived": True
        }
        response = self.client.put(reverse('email', args=[self.email1.id]), data, content_type="application/json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Email.objects.get(id=self.email1.id).archived, True)
        # Test email view with PUT request unarchived
        data = {
            "archived": False
        }
        response = self.client.put(reverse('email', args=[self.email1.id]), data, content_type="application/json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Email.objects.get(id=self.email1.id).archived, False)


class AuthViewsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', email='test@example.com', password='password')

    def test_login_view_get(self):
        # Test login view with GET request
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mail/login.html')

    def test_login_view_post_invalid(self):
        # Test login view with POST request invalid
        data = {
            "email": "invalid",
            "password": "invalid"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email and/or password.")
        self.assertTemplateUsed(response, 'mail/login.html')

    def test_login_view_post_valid(self):
        # Test login view with POST request valid
        data = {
            "email": self.user.username,
            'password': 'password'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_logout_view(self):
        # Test logout view
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        redirected_response = self.client.get(response.url)
        self.assertURLEqual(redirected_response.url, reverse('login'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_register_view_get(self):
        # Test register view with GET request
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mail/register.html')

    def test_register_invalid_confirmation(self):
        # Test register view with POST request invalid confirmation
        data = {
            "email": "user@example.com",
            "password": "password",
            "confirmation": "invalid"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")

    def test_register_invalid_email(self):
        # Test register view with POST request invalid email
        data = {
            "email": self.user.username,
            "password": "password",
            "confirmation": "password"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email address already taken.")

    def test_register_valid(self):
        # Test register view with POST request valid
        data = {
            'email': 'unique@mail.com',
            'password': 'password',
            'confirmation': 'password'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


