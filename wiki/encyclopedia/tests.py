from django.test import TestCase, Client, RequestFactory
from .models import Entry
from .util import list_entries, save_entry, get_entry
from django.urls import reverse
from .views import NewPageForm


class WikiTestCase(TestCase):
    # Setting up the test database
    def setUp(self):
        # Create default entries
        self.client = Client()
        self.factory = RequestFactory()
        Entry.objects.create(title="CSS", title_lower="css", content="# CSS")  # Post 1
        Entry.objects.create(title="Django", title_lower="django", content="# Django")  # Post 2
        Entry.objects.create(title="Flask", title_lower="flask", content="# Flask")  # Post 3
        Entry.objects.create(title="Git", title_lower="git", content="# Git")  # Post 4
        Entry.objects.create(title="HTML", title_lower="html", content="# HTML")  # Post 5
        Entry.objects.create(title="Java", title_lower="java", content="# Java")  # Post 6

    # Testing the functions in util.py (list_entries(), save_entry(), get_entry())
    def test_list_entries(self):
        # Test list_entries() function
        self.assertEqual(list_entries(), ["CSS", "Django", "Flask", "Git", "HTML", "Java"])
        self.assertEqual(Entry.objects.count(), 6)

    def test_save_entry(self):
        # Test save_entry() function
        save_entry("Python", "# Python")
        self.assertEqual(Entry.objects.count(), 7)

    def test_get_entry(self):
        # Test get_entry() function
        self.assertEqual(get_entry("CSS"), "# CSS")

    def test_wrong_get_entry(self):
        # Test get_entry() function with wrong entry
        self.assertEqual(get_entry("C"), None)

    def test_list_entries_again(self):
        # Test list_entries() function after adding Python entry
        Entry.objects.create(title="Python", content="# Python")  # Post 7
        self.assertEqual(list_entries(), ["CSS", "Django", "Flask", "Git", "HTML", "Java", "Python"])
        self.assertEqual(Entry.objects.count(), 7)

    # Testing the views
    def test_index(self):
        # Test index view
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["entries"], ["CSS", "Django", "Flask", "Git", "HTML", "Java"])

    def test_entry(self):
        # Test entry view
        response = self.client.get("/wiki/CSS")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title"], "CSS")
        self.assertEqual(response.context["content"], "# CSS")
        self.assertTemplateUsed(response, "encyclopedia/entry.html")

    def test_wrong_entry(self):
        # Test entry view with wrong entry
        response = self.client.get("/wiki/C")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title"], "C")
        self.assertTemplateUsed(response, "encyclopedia/404.html")

    def test_search(self):
        # Test search view
        response = self.client.get("/search?q=CSS")
        self.assertRedirects(response, "/search/?q=CSS", status_code=301, target_status_code=302)

    def test_wrong_but_exist_search(self):
        # Test search view with wrong entry but which exist
        response = self.client.get("/search?q=CS")
        self.assertEqual(response.status_code, 301)

    def test_wrong_search(self):
        # Test search view with wrong entry
        response = self.client.get("/search?q=Kek")
        self.assertEqual(response.status_code, 301)

    def test_add(self):
        # Test add view
        response = self.client.get("/add")
        self.assertEqual(response.status_code, 301)

    def test_add_valid_form(self):
        # Create a valid form data dictionary
        response = self.client.post(reverse('add'), {'title': 'Test Title', 'content': 'Test Content'})
        self.assertRedirects(response, reverse('entry', args=('Test Title',)))

    def test_add_existing_title(self):
        # Create an entry with the same title to simulate an existing title error
        Entry.objects.create(title='Test Title', title_lower="test title", content='Existing Content')
        response = self.client.post(reverse('add'), {'title': 'Test Title', 'content': 'Test Content'})
        self.assertTemplateUsed(response, 'encyclopedia/add.html')
        self.assertTrue(response.context['error'])

    def test_add_invalid_form(self):
        # Create an invalid form data dictionary with missing fields
        response = self.client.post(reverse('add'), {})
        self.assertTemplateUsed(response, 'encyclopedia/add.html')
        self.assertIsInstance(response.context['form'], NewPageForm)

    def test_random(self):
        # Test random view
        response = self.client.get("/random")
        self.assertEqual(response.status_code, 301)

    def test_edit(self):
        # Test edit view get method
        response = self.client.get('/edit/Git')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/edit.html')

    def test_edit_valid_form(self):
        # Test edit view post method with valid form
        response = self.client.post("/edit/Git", {"title": "Git", "content": "Test Content"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('save'))

    def test_edit_invalid_form(self):
        # Test edit view post method with invalid form
        response = self.client.post("/edit/", {"title": "", "content": ""})
        self.assertEqual(response.status_code, 404)

    def test_save(self):
        # Test save view post method with valid form
        response = self.client.post('/save/', {'title': 'Git', 'content': 'Test Content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('entry', args=('Git',)))

    def test_save_invalid_form(self):
        # Test save view post method with invalid form
        response = self.client.post("/save/", {"title": "None", "content": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/edit.html')
