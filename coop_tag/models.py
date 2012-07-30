# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
#from django_extensions.db import fields as exfields
#from positions.fields import PositionField

import re
import django
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import IntegrityError, transaction
from django.conf import settings
import coop_tag

# from autosuggest :

try:
    from south.modelsinspector import add_ignored_fields
    add_ignored_fields(["^coop_tag\.managers"])
except ImportError:
    pass  # without south this can fail silently


def unicode_slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return mark_safe(re.sub('[-\s]+', '-', value))


# rather add an MPTT tree

# class BaseTagCategory(models.Model):
#     label = models.CharField(_(u'label'), max_length=100)
#     #uri = models.CharField(_(u'tag URI'), blank=True, max_length=250, editable=False)
#     slug = exfields.AutoSlugField(populate_from='label', blank=True)
#     position = PositionField()

#     def __unicode__(self):
#         return self.label

#     class Meta:
#         verbose_name = _(u'tag category')
#         verbose_name_plural = _(u'tag categories')
#         ordering = ['position']
#         abstract = True


class TagBase(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            if django.VERSION >= (1, 2):
                from django.db import router
                using = kwargs.get("using") or router.db_for_write(
                    type(self), instance=self)
                # Make sure we write to the same db for all attempted writes,
                # with a multi-master setup, theoretically we could try to
                # write and rollback on different DBs
                kwargs["using"] = using
                trans_kwargs = {"using": using}
            else:
                trans_kwargs = {}
            i = 0
            while True:
                i += 1
                try:
                    sid = transaction.savepoint(**trans_kwargs)
                    res = super(TagBase, self).save(*args, **kwargs)
                    transaction.savepoint_commit(sid, **trans_kwargs)
                    return res
                except IntegrityError:
                    transaction.savepoint_rollback(sid, **trans_kwargs)
                    self.slug = self.slugify(self.name, i)
        else:
            return super(TagBase, self).save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = unicode_slugify(tag)  # YES, we allow accents in slugs ! i18n powa !!!
        if i is not None:
            slug += "_%d" % i
        return slug


if not hasattr(settings, 'TAG_MODEL'):
    # No alternative tag model has been defined, we create one from the abstract
    class Tag(TagBase):
        pass


class ItemBase(models.Model):
    def __unicode__(self):
        return ugettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag
        }

    class Meta:
        abstract = True

    @classmethod
    def tag_model(cls):
        return cls._meta.get_field_by_name("tag")[0].rel.to

    @classmethod
    def tag_relname(cls):
        return cls._meta.get_field_by_name('tag')[0].rel.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'content_object': instance
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        return {
            "content_object__in": instances,
        }


# only now we can import this
from coop_tag.settings import TAG_MODEL


class TaggedItemBase(ItemBase):
    tag = models.ForeignKey(TAG_MODEL, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return cls.tag_model().objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()


class GenericTaggedItemBase(ItemBase):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content type'),
        related_name="%(app_label)s_%(class)s_tagged_items"
    )
    content_object = GenericForeignKey()

    class Meta:
        abstract = True

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'object_id': instance.pk,
            'content_type': ContentType.objects.get_for_model(instance)
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        # TODO: instances[0], can we assume there are instances.
        return {
            "object_id__in": [instance.pk for instance in instances],
            "content_type": ContentType.objects.get_for_model(instances[0]),
        }

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        return cls.tag_model().objects.filter(**kwargs).distinct()


if not hasattr(settings, 'TAGGED_ITEM_MODEL'):
    class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
        pass
    setattr(coop_tag.settings, 'TAGGED_ITEM_MODEL', TaggedItem)


