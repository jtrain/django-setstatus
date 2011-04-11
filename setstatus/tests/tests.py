"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.client import Client

import django.template as template

from setstatus.tests.models import Factory
from setstatus.models import SetStatus

import datetime

class SetStatusBaseCase(TestCase):

    def setUp(self):
        self.client = Client()

def get_for_model(ContentType, model):
    return ContentType.objects.get(app_label=model._meta.app_label,
                                   model=model._meta.object_name.lower())


class FactoryModelBaseCase(SetStatusBaseCase):

    def setUp(self):
        super(FactoryModelBaseCase, self).setUp()
        self.factory = Factory.objects.create(name='BigFactory')
        self.co = get_for_model(ContentType, self.factory)

        # keep the tests current and not stale much.
        self.year = datetime.datetime.now().year

class ActiveAndInactiveStatus(FactoryModelBaseCase):
    """
    Base class that creates an active status of index "0".
              and creates an inactive status of index "1".

    """

    def setUp(self):
        super(ActiveAndInactiveStatus, self).setUp()

        # create next week starting date.
        next_week = datetime.datetime.now() + datetime.timedelta(days=7)

        s = SetStatus.objects.create(
                    status='1', start_at=next_week,
                    end_at=datetime.datetime(self.year, 12, 31),
                    content_type=self.co,
                    object_id=self.factory.id)

        s.save()

        self.inactive = s

        s = SetStatus.objects.create(
                    status='0', start_at=datetime.datetime.now(),
                    end_at=datetime.datetime(self.year, 12, 31),
                    content_type=self.co,
                    object_id=self.factory.id)

        s.save()

        self.active = s

class ActiveStatusTest(ActiveAndInactiveStatus):

    def test_status_active_returns_active(self):
        self.assertTrue(self.active.active())

    def test_status_not_active_start_at_next_week(self):
        self.assertFalse(self.inactive.active())

class HasStatusTemplateFilterTest(ActiveAndInactiveStatus):
    """
    Test the template filter that checks for status.

    """
    def _getfilter(self, filtername):
        return template.get_library('setstatus_tags').filters[filtername]

    def test_has_status_true_for_valid_status(self):
        has_status = self._getfilter('has_status')
        self.assertEqual(
                has_status(self.factory, u'LOW'),
                True)

    def test_has_status_false_for_invalid_status(self):
        has_status = self._getfilter('has_status')
        self.assertEqual(
                has_status(self.factory, u'MEDIUM'),
                False)


    def test_has_status_false_for_missing_status(self):
        has_status = self._getfilter('has_status')
        self.assertEqual(
                has_status(self.factory, u'HIGH'),
                False)

