django-setstatus
=============

A time limited status that can be applied to any model.

e.g. apply status "promoted" to object FeaturedObject for 1 week.

Installation
------------

1. pip install -e git://github.com/jtrain/django-setstatus.git#egg=django-setstatus
2. add ``'setstatus'`` to your ``INSTALLED_APPS`` in your ``settings.py``
3. sync your database::
  
  python manage.py syncdb
4. if you use South you may migrate from a previous version.::
  
  python manage.py migrate setstatus

5. you may set some status choices in your ``settings.py`` file on the variable ``SETSTATUS_CHOICES``::

  SETSTATUS_CHOICES = (
	(0, "Eggs"),
        (1, "Fish"),
        (2, "Milk"),
  )

Usage
-----

Add SetStatusAdminInline to the inlines of models that you would like to 
set status for::

  class MyObject(model.Admin):
    inlines = (SetStatusAdminInline,)
	
That is it, the rest will take place in the admin interface as you give MyObject
a status of (0, "Eggs") for a period of 1 week, or longer it should be so lucky.


