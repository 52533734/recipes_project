from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Wishlist

class RecipeAppTests(TestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='user1234')

        # Create ingredients and recipes from dataset (subset)
        self.ing1 = Ingredient.objects.create(name='Broccoli')
        self.ing2 = Ingredient.objects.create(name='Tofu')
        self.ing3 = Ingredient.objects.create(name='Garlic')

        self.recipe1 = Recipe.objects.create(
            name='Broccoli and Tofu Stir Fry',
            description='Stir-fried broccoli and tofu with soy sauce and spices.',
            instructions='Step-1: Cube tofu and sauté until golden; Step-2: Add broccoli and garlic; Step-3: Stir-fry 5 min; Step-4: Add soy sauce; Step-5: Serve immediately.',
            cuisine='Chinese'
        )
        self.recipe1.ingredients.add(self.ing1, self.ing2, self.ing3)

        self.recipe2 = Recipe.objects.create(
            name='Quinoa and Roasted Beet Salad',
            description='Protein-rich salad with quinoa, roasted beets, and dressing.',
            instructions='Step-1: Roast beetroot; Step-2: Cook quinoa; Step-3: Mix quinoa, beetroot, and arugula; Step-4: Crumble feta on top; Step-5: Drizzle olive oil and lemon juice, serve.',
            cuisine='Mediterranean'
        )

        self.client = Client()

    # 1. Registration page loads
    def test_registration_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    # 2. User registration works
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        self.assertRedirects(response, reverse('recipe_list'))

    # 3. Login page loads
    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    # 4. User login works
    def test_user_login(self):
        login = self.client.login(username='testuser', password='user1234')
        self.assertTrue(login)

    # 5. Recipe list page shows recipes
    def test_recipe_list_display(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertContains(response, 'Broccoli and Tofu Stir Fry')
        self.assertContains(response, 'Quinoa and Roasted Beet Salad')

    # 6. Recipe detail page displays correct recipe
    def test_recipe_detail(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe1.id]))
        self.assertContains(response, 'Broccoli and Tofu Stir Fry')
        self.assertContains(response, 'Stir-fried broccoli and tofu with soy sauce and spices.')
        self.assertContains(response, 'Broccoli')
        self.assertContains(response, 'Tofu')

    # 7. Search by recipe name works
    def test_search_recipe_name(self):
        response = self.client.get(reverse('recipe_list') + '?q=Broccoli')
        self.assertContains(response, 'Broccoli and Tofu Stir Fry')
        self.assertNotContains(response, 'Quinoa and Roasted Beet Salad')

    # 8. Filter by cuisine works
    def test_filter_cuisine(self):
        response = self.client.get(reverse('recipe_list') + '?cuisine=Mediterranean')
        self.assertContains(response, 'Quinoa and Roasted Beet Salad')
        self.assertNotContains(response, 'Broccoli and Tofu Stir Fry')

    # 9. Wishlist add and display
    def test_add_to_wishlist(self):
        self.client.login(username='testuser', password='user1234')
        response = self.client.get(reverse('add_to_wishlist', args=[self.recipe1.id]))
        self.assertEqual(Wishlist.objects.filter(user=self.user, recipe=self.recipe1).count(), 1)
        response = self.client.get(reverse('wishlist'))
        self.assertContains(response, 'Broccoli and Tofu Stir Fry')

    # 10. Prevent duplicate wishlist entries
    def test_wishlist_no_duplicates(self):
        self.client.login(username='testuser', password='user1234')
        self.client.get(reverse('add_to_wishlist', args=[self.recipe1.id]))
        self.client.get(reverse('add_to_wishlist', args=[self.recipe1.id]))
        self.assertEqual(Wishlist.objects.filter(user=self.user, recipe=self.recipe1).count(), 1)

    # 11. Invalid registration (password mismatch)
    def test_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
        'username': 'user2',
        'email': 'user2@example.com',
        'password1': 'pass12345',
        'password2': 'pass54321'
        })
        self.assertContains(response, "didn’t match")
        self.assertEqual(User.objects.filter(username='user2').count(), 0)
    
    # 12. Search returns no results
    def test_search_no_results(self):
        response = self.client.get(reverse('recipe_list') + '?q=NonExistentRecipe')
        self.assertContains(response, "No recipes found")

    # 13. Access wishlist without login redirects to login page
    def test_wishlist_redirect_without_login(self):
        response = self.client.get(reverse('wishlist'))
        self.assertRedirects(response, f'/login/?next={reverse("wishlist")}')

    # 14. Access recipe detail with invalid ID returns 404
    def test_recipe_detail_invalid_id(self):
        response = self.client.get(reverse('recipe_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    # 15. Adding wishlist without login redirects to login
    def test_add_wishlist_redirect_without_login(self):
        response = self.client.get(reverse('add_to_wishlist', args=[self.recipe1.id]))
        self.assertRedirects(response, f'/login/?next={reverse("add_to_wishlist", args=[self.recipe1.id])}')
