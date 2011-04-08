"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.client import Client

from setstatus.tests.models import Factory
from setstatus.models import SetStatus

import datetime

class SetStatusBaseCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
                            'gary', 'gary@example.com', 'gary')
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

class ActiveStatusTest(FactoryModelBaseCase):

    def test_status_active_returns_active(self):
        s = SetStatus.objects.create(
                    status='0', start_at=datetime.datetime(self.year, 1, 1),
                    end_at=datetime.datetime(self.year, 12, 31),
                    content_object=self.co,
                    modified_by=self.user)
        s.save()
        self.assertTrue(s.active())

    def test_status_not_active_start_at_next_week(self):

        # create next week starting date.
        next_week = datetime.datetime.now() + datetime.timedelta(days=7)

        s = SetStatus.objects.create(
                    status='0', start_at=next_week,
                    end_at=datetime.datetime(self.year, 12, 31),
                    content_object=self.co,
                    modified_by=self.user)
        s.save()
        self.assertFalse(s.active())

