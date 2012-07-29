django-taggit
=============

``django-taggit`` a simpler approach to tagging with Django.  Add ``"taggit"`` to your
``INSTALLED_APPS`` then just add a TaggableManager to your model and go::

    from django.db import models

    from taggit.managers import TaggableManager

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()


Then you can use the API like so::

    >>> apple = Food.objects.create(name="apple")
    >>> apple.tags.add("red", "green", "delicious")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: green>, <Tag: delicious>]
    >>> apple.tags.remove("green")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: delicious>]
    >>> Food.objects.filter(tags__name__in=["red"])
    [<Food: apple>, <Food: cherry>]

Tags will show up for you automatically in forms and the admin.




============
Instructions
============

This is a reusable django app which adds some templatetags to django-taggit_.
This particular fork uses another version of django-templatetag-sugar_, by Jonas Geiregat, because only his version allows to give multiples arguments to a templatetag.
For example, here we are using the 'count' argument to limit the number of tags in the queryset.

Installation
============

Just install ``django-taggit-templatetags`` via ``pip``::

    $ pip install django-taggit-templatetags

After installing and configuring django-taggit_, just add ``taggit_templatetags`` to your ``INSTALLED_APPS`` in your ``settings.py``::

    INSTALLED_APPS = (
    ...
    'taggit_templatetags',
    ...
    )

Usage
=====

Now there are some templatetags enabled, at the moment only to create lists of tags and tag-clouds.

In your templates, you need to load ``taggit_extras``::

    ...
    {% load taggit_extras %}
    ...

--------
Taglists
--------

After loading ``taggit_extras`` you can create a list of tags for the whole project (in the sense of djangoproject), for an app (in the sense of djangoapp), for a model-class (to get a list for an instance of a model, just use its tag-field).

For the tags of a project, just do::

    {% get_taglist asvar tags %}

To limit the number of tags::

    {% get_taglist asvar tags count 25 %}

For the tags of an app, just do::

    {% get_taglist asvar tags for 'yourapp' %}

For the tags of a model, just do::

    {% get_taglist asvar tags for 'yourapp.yourmodel' %}

You can also customize the name of the tags manager in your model (the default is *tags*)::

    {% get_taglist asvar tags for 'yourapp.yourmodel:yourtags' %}

No matter what you do, you have a list of tags in the ``tags`` template variable. You can now iterate over it::

    <ul>
    {% for tag in tags %}
    <li>{{tag}} ({{tag.num_times}})</li>
    {% endfor %}
    <ul>

As you can see, each tag has an attribute ``num_times`` which declares how many times it was used. The list of tags is sorted descending by ``num_times``.

Inclusion-Tag
-------------

For convenience, there's an inclusion-tag. It's used analogue. For example, for a taglist of a model, just do::

    {% include_taglist 'yourapp.yourmodel' %}

---------
Tagclouds
---------

A very popular way to navigate through tags is a tagcloud_.  This app provides some tags for that::

    {% get_tagcloud as tags %}

or::

    {% get_tagcloud as tags for 'yourapp' %}

or::

    {% get_tagcloud as tags for 'yourapp.yourmodel' %}

respectivly. The resulting list of tags is ordered by their ``name`` attribute. Besides the ``num_items`` attribute, there's a ``weight`` attribute. Its maximum and minimum may be specified as the settings_ section reads.

Inclusion-Tag
-------------

Even for the tagcloud there's an inclusion-tag. For example, for a tagcloud of a model, just do::

{% include_tagcloud 'yourapp.yourmodel' %}

.. _settings:

Settings
========

There are a few settings to be set:

TAGGIT_TAGCLOUD_MIN (default: 1.0)
    This specifies the minimum of the weight attribute of a tagcloud's tags.

TAGGIT_TAGCLOUD_MAX (default: 6.0)
    This specifies the maximum of the weight attribute of a tagcloud's tags.

If you want to use the weight as font-sizes, just do as follows::

    <font size={{tag.weight|floatformat:0}}>{{tag}}</font>

So the weights are converted to integer values.

Thanks
======

Thanks to the python- and django-community, in particular to `Alex Gaynor`_, the inventor of django-taggit_ and a wonderful guy to argue with. Thanks to `Mathijs de Bruin`_ as well for his helpful pull requests.

.. _django-templatetag-sugar : https://github.com/jonasgeiregat/django-templatetag-sugar
.. _django-taggit: http://pypi.python.org/pypi/django-taggit
.. _tagcloud: http://www.wikipedia.org/wiki/Tagcloud
.. _Alex Gaynor: http://alexgaynor.net/
.. _Mathijs de Bruin: http://github.com/dokterbob






*** Credits ***
    This project is directly based on those projects:
    * Alex Gaynor
        * https://github.com/alex/django-taggit
    * Ludwik Trammer:
        * http://code.google.com/p/django-tagging-autocomplete/
    * Jeremy Epstein:
        * https://github.com/Jaza/django-taggit-autocomplete
    * Flavio Curella:
        * https://github.com/fcurella/django-taggit-autocomplete
    * Drew Wilson:
        * http://code.drewwilson.com/entry/autosuggest-jquery-plugin

*** Installation ***
   * Add "taggit_autosuggest" to your INSTALLED_APPS in your project settings
   * Run "python manage.py collectstatic" in your django site dir.
   * Add the following line to your project's urls.py file:
         (r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),


*** Settings ***
    TAGGIT_AUTOSUGGEST_STATIC_BASE_URL:
        Instead of collecting and serving the static files directly, you can
        also set this variable to your static base URL somewhere else.
    TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS (Defaults to 20):
        The amount of suggestions is limited, you can raise or lower the limit
        of default 20 using this setting.
    TAGGIT_AUTOSUGGEST_CSS_FILENAME (Defaults to 'autoSuggest.css'):
        Set the CSS file which best fits your site elements.
        The CSS file have to be in 'jquery-autosuggest/css/'.
    TAGGIT_AUTOSUGGEST_MODEL (Defaults to tuple('taggit','Tag'))
        The Tag model used, if you happen to use Taggit custom tagging.

*** Usage ***
To enable autosuggesting Tags, just let the tagged model use TaggableManager:
    from django.db import models
    from taggit_autosuggest.managers import TaggableManager


    class SomeModel(models.Model):

        tags = TaggableManager()
w






coop-tag
===============================================
Add-on for `django-coop <http://github.com/quinode/django-coop>`_ for managing tags with `django-taggit <http://github.com/quinode/django-taggit>`_, aligned with the `CommonTag RDF vocabulary <http://commontag.org>`_ specification.

Installation requires several custom modules::
hg+https://bitbucket.org/quinode/django-taggit-autosuggest#egg=taggit_autosuggest::
git+git://github.com/jonasgeiregat/django-templatetag-sugar.git#egg=templatetag_sugar::
git+https://github.com/quinode/django-taggit-templatetags#egg=taggit_templatetags::



License
=======
django-coop uses the same license as Django (BSD).
django-coop development is currently funded by `CREDIS <http://credis.org/>`_, FSE (European Social Fund) and `Conseil Régional Auvergne <http://www.auvergne.fr/>`_.
