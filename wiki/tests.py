from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page

class PageDetailViewTests(TestCase):

# Create your tests here.
    def test_detail_page(self):
        """ Tests the slug generated when saving a Page. """
        # Author is a required field in our model.
        # Create a user for this test and save it to the test database.
        user = User.objects.create()
        user.save()

        # Create and save a new page to the test database.
        page = Page(title="My Detail Test Page", content="details_test", author=user)
        page.save()

        # Make sure the slug that was generated in Page.save()
        # matches what we think it should be.
        slug = page.slug
        response = self.client.get(f'/{slug}/')

        self.assertEqual(response.status_code, 200)
        
        info = self.client.get('/')
        self.assertContains(info, 'makewiki', html=True)

    def test_edit_page(self):
        # Make some test data to be displayed on the page.
        user = User.objects.create()
        user.save()

        page = Page.objects.create(title="My Test Page", content="edit_test", author=user)
        page.save()
        # Issue a GET request to the MakeWiki homepage.
        # When we make a request, we get a response back.
        post_data = {'title': 'Test', 
        'content': 'Who dat?', 
        'author': user.id 
        }

        response = self.client.post('/form/', data = post_data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)

        # Check that the number of pages passed to the template
        # matches the number of pages we have in the database.
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

    def test_page_creation(self):
                user = User.objects.create()
        user.save()

        page = Page.objects.create(title="My Test Page", content="edit_test", author=user)
        page.save()

        post_data = {'title': 'Baseball', 
        'content': 'I love the game', 
        'author': user.id 
        }

        response = self.client.post('/form/', data = post_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(page_object.title, 'Baseball')