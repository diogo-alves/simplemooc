from django.test import TestCase

from model_mommy import mommy

from simplemooc.courses.models import Course


class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = mommy.make(
            Course, name='Python na Web com Django', _quantity=5
        )
        self.courses_devs = mommy.make(
            Course, name='Python para Devs', _quantity=10
        )

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)
