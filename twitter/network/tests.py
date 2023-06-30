import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Post, Comment


class ModelsAuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Creating users
        self.test_user = User.objects.create(username='user1', email='user1@mail.com', password='user1',
                                             name='user one', bio='user1 bio', url='image1.com/user1.jpg')
        self.test_user.save()
        User.objects.create(username='user2', email='user2@mail.com', password='user2',
                            name='user two', bio='user2 bio', url='image2.com/user2.jpg')

        User.objects.create(username='user3', email='user3@mail.com', password='user3',
                            name='user three', bio='user3 bio', url='image3.com/user3.jpg')
        User.objects.create(username='user4', email='user4@mail.com', password='user4',
                            name='user four', bio='user4 bio', url='image4.com/user4.jpg')
        User.objects.create(username='user5', email='user5@mail.com', password='user5',
                            name='user five', bio='user5 bio', url='image5.com/user5.jpg')
        # Creating posts
        self.post1 = Post.objects.create(user=User.objects.get(username='user1'),
                            body='post 1 liked by user2,3,4')
        self.post2 = Post.objects.create(user=User.objects.get(username='user2'),
                            body='post 2 commented by user 1 and 3')
        self.post3 = Post.objects.create(user=User.objects.get(username='user3'),
                            body='post 3 bookmarked by user 1 and 2')
        self.post4 = Post.objects.create(user=User.objects.get(username='user4'),
                            body='post 4 commented by user 3 and 5')
        self.post5 = Post.objects.create(user=User.objects.get(username='user5'),
                            body='post 5 commented by user 1 and liked by user 3')

    # Testing models
    def test_users_count(self):
        # Test users count
        self.assertEqual(User.objects.count(), 5)

    def test_posts_count(self):
        # Test posts count
        self.assertEqual(Post.objects.count(), 5)

    def test_likes_add_remove(self):
        # Test likes add
        post = self.post2
        post.likes.add(User.objects.get(username='user2'))
        post.likes.add(User.objects.get(username='user3'))
        post.likes.add(User.objects.get(username='user4'))
        self.assertEqual(post.likes.count(), 3)
        post.likes.remove(User.objects.get(username='user2'))
        self.assertEqual(post.likes.count(), 2)

    def test_comments_add_remove(self):
        # Test comments add
        post = self.post2
        comment = Comment.objects.create(body='comment 1 by user 1')
        comment.user.set([User.objects.get(username='user1')])
        post.comments.add(comment)
        comment2 = Comment.objects.create(body='comment 2 by user 3')
        comment2.user.set([User.objects.get(username='user3')])
        post.comments.add(comment2)
        self.assertEqual(post.comments.count(), 2)
        self.assertEqual(comment2.body, 'comment 2 by user 3')

    def test_bookmarks_add_remove(self):
        # Test bookmarks add
        post = self.post2
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        user1.saved_posts.add(post)
        user2.saved_posts.add(post)
        self.assertEqual(user1.saved_posts.count(), 1)
        self.assertEqual(user2.saved_posts.count(), 1)
        user1.saved_posts.remove(post)
        self.assertEqual(user1.saved_posts.count(), 0)

    def test_followers_add_remove(self):
        # Test followers add
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        user3 = User.objects.get(username='user3')
        user1.followers.add(user2)
        user1.followers.add(user3)
        user1.following.add(user2)
        user1.following.add(user3)
        self.assertEqual(user1.followers.count(), 2)
        user1.followers.remove(user2)
        user1.following.remove(user2)
        self.assertEqual(user1.followers.count(), 1)
        self.assertEqual(user1.following.count(), 1)

    # Testing views
    def test_index(self):
        # Test index page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_login_correct(self):
        # Test login with correct credentials
        User.objects.create_user(username='user10', password='user10')
        response = self.client.post('/login', json.dumps({
            'username': 'user10',
            'password': 'user10'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Login successful.')

    def test_login_incorrect(self):
        # Test login with incorrect credentials
        response = self.client.post('/login', json.dumps({
            'username': 'user1',
            'password': 'user2'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid username and/or password.')

    def test_login_get(self):
        # Test login get
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_logout(self):
        # Test logout
        self.client.login(username=self.test_user.username,
                          password=self.test_user.password)
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, '/accounts/login/?next=/logout')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_register_pw_errors(self):
        # Test registration with wrong password confirmation
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "username6",
            "email": "user6@email.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user7",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'passwords_mismatch')
        # Test registration with too short password
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "user6",
            "email": "user6@mail.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user",
            "confirmation": "user",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'password_length')
        # Test registration with too long password
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "user6",
            "email": "user6@mail.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "useruseruseruseruser",
            "confirmation": "useruseruseruseruser",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'password_length')

    def test_register_username_errors(self):
        # Test registration with username already taken
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "user1",
            "email": "user6@email.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user6",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'username_taken')
        # Test registration with too short username < 5
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "use",
            "email": "user6@email.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user6",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'username_length')
        # Test registration with too long username > 25
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "useruseruseruseruseruseruser",
            "email": "user6@email.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user6",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'username_length')

    def test_register_email_errors(self):
        # Test registration with email already taken
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "user6",
            "email": "user1@mail.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user6",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'email_taken')
        # Test registration with invalid email
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "user6",
            "email": "user1@mail",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user6",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'email_invalid')

    def test_register_success(self):
        # Test registration with valid credentials
        response = self.client.post('/register', json.dumps({
            "name": "user6",
            "username": "user6",
            "email": "user6@mail.com",
            "bio": "user6 bio",
            "url": "image6.com/user6.jpg",
            "password": "user6",
            "confirmation": "user6",
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Successfully registered.')


class CreatePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='username',
            password='password'
        )
        self.post = Post.objects.create(
            body='test body',
            user=self.user
        )

    # POST tests
    def test_create_post_with_empty_body(self):
        # Test create post with empty body
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('create'), {'text': ''})
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn('error', json_response)
        self.assertEqual(json_response['error'], 'Content is required.')

    def test_create_post_without_login(self):
        # Test create post without login
        response = self.client.post(reverse('create'), {'text': ''})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/post/create')

    def test_create_post_success(self):
        # Test create post with valid body
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('create'), {'text': 'This is a test post.'})
        self.assertEqual(response.status_code, 201)
        json_response = response.json()
        self.assertIn('message', json_response)
        self.assertEqual(json_response['message'], 'Post created successfully.')

    # PUT tests
    def test_update_post_without_login(self):
        # Test update post without login
        response = self.client.put(reverse('create'), {'text': ''})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/post/create')

    def test_update_post_not_owner(self):
        # Test post edition by a user that is not the owner
        fake_user = User.objects.create_user(
            username='fake_user',
            password='password'
        )
        self.client.force_login(fake_user)
        data = {
            "text": "Updated text",
            "id": self.post.id,
        }
        response = self.client.put(reverse('create'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        json_response = response.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "You are not the owner of this post.")

    def test_update_post_empty_body(self):
        # Test post edition with empty body
        self.client.force_login(self.user)

        data = {
            "text": "",
            "id": self.post.id,
        }
        response = self.client.put(reverse('create'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "Content is required.")

    def test_update_post_success(self):
        # Test post edition with a post that does not exist
        self.client.force_login(self.user)
        data = {
            "text": "Updated text",
            "id": self.post.id,
        }
        response = self.client.put(reverse('create'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        json_response = response.json()
        self.assertIn("message", json_response)
        self.assertEqual(json_response["message"], "Post updated successfully.")


class NotFoundViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_not_found(self):
        # Test not found view
        response = self.client.get(reverse('404'))
        self.assertEqual(response.status_code, 200)  # Assuming success status code is 200
        self.assertTemplateUsed(response, 'network/index.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], None)


class PostsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='username',
            password='password'
        )
        self.post = Post.objects.create(
            body='test body',
            user=self.user
        )
        self.user2 = User.objects.create_user(
            username='username2',
            password='password'
        )
        self.post2 = Post.objects.create(
            body='test body 2',
            user=self.user2
        )
        self.user3 = User.objects.create_user(
            username='username3',
            password='password'
        )
        self.post3 = Post.objects.create(
            body='test body 3',
            user=self.user3
        )
        self.post3_1 = Post.objects.create(
            body='test body 3_1',
            user=self.user3,
        )
        self.post3_2 = Post.objects.create(
            body='test body 3_2',
            user=self.user3,
        )
        # Follow first user by second user
        self.user2.followers.add(self.user)
        self.user.following.add(self.user2)

    def test_posts_wo_pg(self):
        # Test posts without pagination
        response = self.client.get(reverse('posts_wo_pg', args=['all']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts', args=['all', 1]))

    def test_posts_wo_pg_invalid(self):
        # Test posts without pagination with invalid type
        response = self.client.get(reverse('posts_wo_pg', args=['invalid']))
        self.assertRedirects(response, reverse('404') + '?error=This page doesn\'t exist')

    def test_posts_all(self):
        # Test posts without type
        response = self.client.get(reverse('posts_all'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('posts', args=['all', 1]))

    def test_posts_with_t_p(self):
        # Test posts with type and page
        response = self.client.get(reverse('posts', args=['all', 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_posts_with_invalid_t_p(self):
        # Test posts with invalid type
        response = self.client.get(reverse('posts', args=['invalid', 1]))
        self.assertRedirects(response, reverse('404') + "?error=This page doesn't exist")
        # Test posts with invalid page
        response = self.client.get(reverse('posts', args=['all', 10]))
        self.assertRedirects(response, reverse('404') + "?error=This page doesn't exist")

    def test_post_get_method(self):
        # Test post get method
        self.client.force_login(self.user)
        response = self.client.get(reverse('post'), data={'page': 1, 'type': 'all'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data['results'], list)
        self.assertGreater(len(response_data['results']), 0)
        self.assertEqual(response_data['results'][0]['user_id'], self.user3.id)

    def test_post_invalid_get_method(self):
        # Test post get method with invalid type
        self.client.force_login(self.user)
        response = self.client.get(reverse('post'), data={'page': 1, 'type': 'invalid'})
        self.assertRedirects(response, reverse('404') + "?error=Invalid request")

    def test_post_put_method_likes(self):
        # Test add like
        self.client.force_login(self.user)
        data = {
            "post_id": self.post.id,
            "method": "like",
            "action": "add",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        post_likes = Post.objects.get(id=self.post.id).likes.all()
        self.assertEqual(post_likes.count(), 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Post liked successfully.")
        # Test remove like
        data = {
            "post_id": self.post.id,
            "method": "like",
            "action": "remove",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        post_likes = Post.objects.get(id=self.post.id).likes.all()
        self.assertEqual(post_likes.count(), 0)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Post unliked successfully.")
        # Test invalid method
        data = {
            "post_id": self.post.id,
            "method": "like",
            "action": "invalid",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Invalid request.")

    def test_post_put_method_bookmark(self):
        # Test add bookmark
        self.client.force_login(self.user)
        data = {
            "post_id": self.post.id,
            "method": "bookmark",
            "action": "add",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Post bookmarked successfully.")
        self.assertEqual(self.user.saved_posts.count(), 1)
        # Test remove bookmark
        data = {
            "post_id": self.post.id,
            "method": "bookmark",
            "action": "remove",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Post unbookmarked successfully.")
        self.assertEqual(self.user.saved_posts.count(), 0)
        # Test invalid method
        data = {
            "post_id": self.post.id,
            "method": "bookmark",
            "action": "invalid",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('404') + "?error=Invalid request")

    def test_post_put_method_comments(self):
        # Test add comment
        self.client.force_login(self.user)
        data = {
            "post_id": self.post.id,
            "method": "comment",
            "text": "Test comment",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'Comment added successfully.')
        # Test empty comment
        data = {
            "post_id": self.post.id,
            "method": "comment",
            "text": "",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Content is required.")

    def test_post_put_method_unauthorized(self):
        # Test unauthorized user
        data = {
            "post_id": self.post.id,
            "method": "like",
            "action": "add",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Login required.")

    def test_post_put_method_invalid(self):
        # Test invalid method
        self.client.force_login(self.user)
        data = {
            "post_id": self.post.id,
            "method": "invalid",
            "action": "add",
        }
        response = self.client.put(reverse('post'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('404') + "?error=Invalid request")


class ProfileUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='password')
        self.user2 = User.objects.create_user(username='username2', password='password')
        self.post_user = Post.objects.create(user=self.user, body='Test post')

    def test_profile_own(self):
        # Test own profile
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile_own'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', args=[self.user.id, 1]))

    def test_profile_wo_pg(self):
        # Test profile without page number
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile_wo_pg', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', args=[self.user.id, 1]))

    def test_profile_wo_pg_invalid(self):
        # Test profile without page number with invalid user id
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile_wo_pg', args=['6']))
        self.assertRedirects(response, reverse('404') + '?error=User not found')

    def test_profile_wo_pg_wo_login(self):
        # Test profile without page number without login
        response = self.client.get(reverse('profile_wo_pg', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/profile/{self.user.id}')

    def test_profile(self):
        # Test profile
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile', args=[self.user.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_profile_invalid_user(self):
        # Test profile with invalid user id
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile', args=[99, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('404') + "?error=User not found")

    def test_profile_invalid_page(self):
        # Test profile with invalid page id
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile', args=[self.user.id, 99]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('404') + "?error=This page doesn't exist")

    def test_followers(self):
        # Test followers
        self.client.force_login(self.user)
        response = self.client.get(reverse('followers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')

    def test_followers_not_logged(self):
        # Test followers not logged in
        response = self.client.get(reverse('followers'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/followers')

    def test_user_not_logged(self):
        # Test user not logged in
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/user')

    def test_user_get_profile(self):
        # Test user get profile id 1
        self.user.following.add(self.user2)
        self.user2.followers.add(self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse('users'), data={'profile': self.user.id})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data['following'], list)
        self.assertEqual(response_data['id'], self.user.id)
        self.assertEqual(response_data['following'][0], self.user2.id)

    def test_user_get_followers(self):
        # Test user get own followers
        self.user.following.add(self.user2)
        self.user2.followers.add(self.user)
        self.client.force_login(self.user2)
        response = self.client.get(reverse('users'), data={'followers': self.user2.id})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['follow'][0]['id'], self.user.id)
        self.assertFalse(response_data['follow'][0]['is_followed'])

    def test_user_get_following(self):
        # Test user get own following list
        self.user.following.add(self.user2)
        self.user2.followers.add(self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse('users'), data={'following': self.user.id})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['follow'][0]['id'], self.user2.id)
        self.assertTrue(response_data['follow'][0]['is_followed'])

    def test_user_get_invalid_method(self):
        # Test user get invalid method
        self.client.force_login(self.user)
        response = self.client.get(reverse('users'), data={'invalid': self.user.id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('404') + "?error=Invalid request")

    def test_user_put_follow(self):
        # Test user put follow
        self.client.force_login(self.user2)
        data = {
            "method": "follow",
            "id": self.user.id,
        }
        response = self.client.put(reverse('users'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'User followed successfully.')

    def test_user_put_unfollow(self):
        # Test user put follow
        self.client.force_login(self.user)
        data = {
            "method": "unfollow",
            "id": self.user2.id,
        }
        response = self.client.put(reverse('users'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'User unfollowed successfully.')

    def test_user_put_invalid(self):
        # Test user put invalid method
        self.client.force_login(self.user)
        data = {
            "method": "invalid",
            "id": self.user2.id,
        }
        response = self.client.put(reverse('users'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('404') + "?error=Invalid request")
