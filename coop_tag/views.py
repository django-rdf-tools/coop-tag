# -*- coding:utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.shortcuts import render_to_response

from coop_tag.settings import get_class, TAGGER_MAX_SUGGESTIONS

Tag = get_class('tag')
TaggedItem = get_class('taggeditem')


def tagged_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    tag = get_object_or_404(Tag, slug=slug)
    qs = queryset.filter(pk__in=TaggedItem.objects.filter(
        tag=tag, content_type=ContentType.objects.get_for_model(queryset.model)
    ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["tag"] = tag
    return object_list(request, qs, **kwargs)

    # PB : n'est bon que si on passe le queryset d'un modèle spécifique


def tag_detail(request, slug):
    context = {}
    tag = Tag.objects.get(slug=slug)
    return render_to_response('tag/tag_detail.html', { 'tag': tag }, RequestContext(request))


from django.http import HttpResponse
from django.utils import simplejson as json


def list_tags(request):
    """
    Returns a list of JSON objects with a `name` and a `value` property that
    all start like your query string `q` (not case sensitive).
    """
    query = request.GET.get('q', '')
    limit = request.GET.get('limit', TAGGER_MAX_SUGGESTIONS)
    try:
        request.GET.get('limit', TAGGER_MAX_SUGGESTIONS)
        limit = min(int(limit), TAGGER_MAX_SUGGESTIONS)  # max or less
    except ValueError:
        limit = TAGGER_MAX_SUGGESTIONS

    tag_name_qs = Tag.objects.filter(name__istartswith=query).\
        values_list('name', flat=True)
    data = [{'name': n, 'value': n} for n in tag_name_qs[:limit]]

    return HttpResponse(json.dumps(data), mimetype='application/json')

