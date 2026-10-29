from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Expense
from datetime import date


class HomePageTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/home.html')


    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}"
        )

    
    def test_user_cannot_edit_another_users_expense(self):
        user1 = User.objects.create_user(
            username='user1',
            password='TestPass123!'
        )
        user2 = User.objects.create_user(
            username='user2',
            password='TestPass123!'
        )

        category = Category.objects.create(name='Test Food')

        expense = Expense.objects.create(
            user=user1,
            amount='150.00',
            category=category,
            date=date(2026, 10, 1),
            description='Lunch',
            payment_method='UPI'
        )

        self.client.login(
            username='user2',
            password='TestPass123!'
        )

        response = self.client.get(
            reverse('edit_expense', args=[expense.id])
        )

        self.assertEqual(response.status_code, 404)

