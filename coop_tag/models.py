# -*- coding:utf-8 -*-

from django.db import models, IntegrityError, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
#from mptt.models import MPTTModel, TreeForeignKey
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from coop_tag.settings import get_class, TAGGER_FKEY_NAME
from django.conf import settings
from django.db import router
import re


try:
    from south.modelsinspector import add_ignored_fields
    add_ignored_fields(["^coop_tag\.managers"])
except ImportError:
    pass  # without south this can fail silently


class TagBase(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)
    # parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    # class MPTTMeta:
    #     order_insertion_by = ['name']

    class Meta:
        abstract = True
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        # ordering = ['tree_id', 'lft']  # for FeinCMS TreeEditor

    def save(self, *args, **kwargs):
        if (not self.pk and not self.slug) or not self.slug:
            self.slug = self.uslugify(self.name)
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self)
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            trans_kwargs = {"using": using}
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
                    self.slug = self.uslugify(self.name, i)
        else:
            super(TagBase, self).save(*args, **kwargs)

    def uslugify(self, tag_name, i=None):
        #import pdb; pdb.set_trace()
        tag_name = unicode(re.sub('[^\w\s-]', '', tag_name).strip().lower())
        slug = mark_safe(re.sub('[-\s]+', '-', tag_name))
        if i is not None:
            slug += "_%d" % i
        return slug

    def tagged_items(self, selection=None):
        """
        Returns a dict of objects tagged with this tag, keys of the dict are model names.
        The 'selection' parameter can be used to pass a restrictive list of models names as strings.
        """
        from coop_tag.settings import get_class
        TaggedItem = get_class('taggeditem')
        items = {}
        for item in TaggedItem.objects.filter(tag=self):
            cls = item.content_object._meta.verbose_name_plural
            if not selection or cls in selection:
                if not cls in items:
                    items[cls] = []
                items[cls].append(item)
        return items


if not hasattr(settings, 'TAGGER_TAG_MODEL'):
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


class TaggedItemBase(ItemBase):
    tag = models.ForeignKey(TAGGER_FKEY_NAME, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True
        verbose_name = _("tagged item")
        verbose_name_plural = _("tagged items")

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
    object_id = models.IntegerField(verbose_name=_('Object id'), db_index=True)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content type'),
        related_name="%(app_label)s_%(class)s_taggeditem_items"
    )
    content_object = GenericForeignKey('content_type', 'object_id')


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
        # import pdb
        # pdb.set_trace()
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk

        return cls.tag_model().objects.filter(**kwargs).distinct()


if not hasattr(settings, 'TAGGER_TAGGEDITEM_MODEL'):
    class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
        pass
        #tag = models.ForeignKey(TAGGER_FKEY_NAME, related_name="%(app_label)s_%(class)s_items")

