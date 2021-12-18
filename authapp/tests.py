from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command

from mainapp.models import ProductCategory, Product


class AuthUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.category = ProductCategory.objects.create(
            name='cat1'
        )
        for i in range(10):
            Product.objects.create(
                name=f'prod-{i}',
                category=self.category,
                short_desc='shortdesc',
                description='desc',
            )

        self.superuser = ShopUser.objects.create_superuser(
            username='django',
            password='geekbrains',
        )

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_anonymous)
        # self.assertEqual(response.context['title'], 'главная')
        # self.assertNotContains(response, 'Пользователь', status_code=200)
        # # self.assertNotIn('Пользователь', response.content.decode())

        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)

    def test_redirect(self):
        product = Product.objects.first()
        response = self.client.get(f'/basket/add/{product.pk}/')
        self.assertEqual(response.status_code, 302)
