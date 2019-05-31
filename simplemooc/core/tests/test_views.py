from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.home_url = "core:home"

    def test_home_status_code(self):
        response = self.client.get(reverse(self.home_url))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_home_templates_used(self):
        response = self.client.get(reverse(self.home_url))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')


class ContactViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.contact_url = "core:contact"

    def test_contact_status_code(self):
        response = self.client.get(reverse(self.contact_url))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_contact_templates_used(self):
        response = self.client.get(reverse(self.contact_url))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'contact.html')
