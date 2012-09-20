coop-tag
========

An app for managing tags largely built on `django-taggit <http://github.com/quinode/django-taggit>`_
We integrated in this package two other add-ons for taggit :
- `django-taggit-autosuggest <https://bitbucket.org/quinode/django-taggit-autosuggest>`_
- `django-taggit-templatetags <https://github.com/quinode/django-taggit-templatetags>`_

So we have a nice styled autocomplete widget and some templatetags to use taggit.
Tag slugs are unicode-friendly. That means accented letters are valid URI characters (like they should be !)
So you can have differents slugs for differents tags.

Installation and dependencies::
    $ pip install git+git://github.com/quinode/django-templatetag-sugar.git
    $ pip install django-autoslug
    $ pip install unicode-slugify
    $ pip install coop_tag

Add `coop_tag` (with an underscore) to INSTALLED_APPS in your django project settings.
Run `python manage.py collectstatic` in your django project directory.
Add the following line a the bottom of your project's urls.py file::
        (r'^', include('coop_tag.urls')),


Usage
=====

To enable Tags, just let the tagged model use the TaggableManager::

    from django.db import models
    from coop_tag.managers import TaggableManager

    class SomeModel(models.Model):
        ...
        tags = TaggableManager(help_text="your optional help text", blank=True,)

If you want to leverage Generic Relations, you can use a `through` model::

    from coop_tag.managers import TaggableManager
    from coop_tag.models import TaggedItem

    class SomeModel(models.Model):
        tags = TaggableManager(through=TaggedItem, blank=True,)

The Tag model and the optional TaggedItem model are configurable, you can use your owns (see seetings above)

You can use the great taggit API like so::

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


Template tags
=============

Fork of `django-taggit-templatetags`, a reusable django app which adds some templatetags to django-taggit_.
This particular fork uses a fork of django-templatetag-sugar_, by Jonas Geiregat, only this version allows us to give multiples arguments to a templatetag.

Now there are some templatetags enabled, at the moment only to create lists of tags and tag-clouds.
In your templates, you need to load ``tagger_extras``::

    ...
    {% load tagger_extras %}
    ...

--------
Taglists
--------

After loading ``tagger_extras`` you can create a list of tags for the whole project (in the sense of djangoproject), for an app (in the sense of djangoapp), for a model-class (to get a list for an instance of a model, just use its tag-field).

For the tags of a project, just do::

    {% get_taglist asvar tags %}

To limit the number of tags::

    {% get_taglist asvar tags count 25 %}

For the tags of an app, just do::

    {% get_taglist asvar tags for_obj 'yourapp' %}

For the tags of a model, just do::

    {% get_taglist asvar tags for_obj 'yourapp.yourmodel' %}

You can also customize the name of the tags manager in your model (the default is *tags*)::

    {% get_taglist asvar tags for_obj 'yourapp.yourmodel:yourtags' %}

No matter what you do, you have a list of tags in the ``tags`` template variable. You can now iterate over it::

    <ul id="tags" class="indextags">
        {% get_taglist asvar all_tags for_obj target_app count 15 %}
        {% for tag in all_tags %}
        <li class="tag">
            <a href="{{ tag.get_absolute_url }}">{{tag}} ({{tag.num_times}})</a>
        </li>
        {% endfor %}
    </ul>

As you can see, each tag has an attribute ``num_times`` which declares how many times it was used. The list of tags is sorted descending by ``num_times``.


Inclusion-Tag
-------------

For convenience, there's an inclusion-tag. It's used analogue. For example, for a taglist of a model, just do::

    {% include_taglist 'yourapp.yourmodel' %}

Tagclouds
---------

A very popular way to navigate through tags is a tagcloud_.  This app provides some tags for that::

    {% get_tagcloud as tags %}

or::

    {% get_tagcloud as tags for 'yourapp' %}

or::

    {% get_tagcloud as tags for 'yourapp.yourmodel' %}

respectivly. The resulting list of tags is ordered by their ``name`` attribute. Besides the ``num_items`` attribute, there's a ``weight`` attribute. Its maximum and minimum may be specified as the settings_ section reads.

Inclusion-Tag in Tagcloud
-------------------------

Even for the tagcloud there's an inclusion-tag. For example, for a tagcloud of a model, just do::

{% include_tagcloud 'yourapp.yourmodel' %}

.. _settings:

Optional Settings
=================

TAGGER_TAG_MODEL (Defaults to 'coop_tag.models.Tag')
    The Tag model used, if you happen to use a custom model.
TAGGER_TAGGEDITEM_MODEL (Defaults to 'coop_tag.models.TaggedItem')
    The Taggeditem model used, if you happen to use a custom model.
TAGGER_FKEY_NAME (Defaults to 'coop_local.Tag')
    The linked model on the through model can also be customized (use only if you have the two settings above set)

TAGGER_STATIC_URL:
    Instead of collecting and serving the static files directly, you can also set this variable to your static base URL somewhere else.
TAGGER_CSS_FILENAME (Defaults to 'coop_tag.css'):
    Set the CSS file which best fits your site elements.
TAGGER_MAX_SUGGESTIONS (Defaults to 20):
    The amount of suggestions is limited, you can raise or lower the limit of default 20 using this setting
TAGGER_CLOUD_MIN (default: 1.0)
    This specifies the minimum of the weight attribute of a tagcloud's tags.
TAGGER_CLOUD_MAX (default: 6.0)
    This specifies the maximum of the weight attribute of a tagcloud's tags.

If you want to use the weight as font-sizes, just do as follows::

    <font size={{tag.weight|floatformat:0}}>{{tag}}</font>

So the weights are converted to integer values.


.. _django-templatetag-sugar : https://github.com/jonasgeiregat/django-templatetag-sugar
.. _django-taggit: http://pypi.python.org/pypi/django-taggit


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
    * Mathijs de Bruin:
        * http://github.com/dokterbob


License
=======
coop-tag uses the same license as Django (BSD).
coop-tag development is currently funded by `CREDIS <http://credis.org/>`_, FSE (European Social Fund) and `Conseil Regional Auvergne <http://www.auvergne.fr/>`_.
