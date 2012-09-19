from django.conf import settings
from django.utils.importlib import import_module

# define the minimal weight of a tag in the tagcloud
TAGGER_CLOUD_MIN = getattr(settings, 'TAGGER_CLOUD_MIN', 1.0)

# define the maximum weight of a tag in the tagcloud
TAGGER_CLOUD_MAX = getattr(settings, 'TAGGER_CLOUD_MAX', 6.0)

# default ForeignKey for TaggedItem : must be defined in YOUR settings if you have a custom Tag model
TAGGER_FKEY_NAME = getattr(settings, 'TAGGER_FKEY_NAME', 'coop_tag.Tag')

TAGGER_MAX_SUGGESTIONS = getattr(settings, 'TAGGER_MAX_SUGGESTIONS', 20)

TAGGER_CSS_FILENAME = getattr(settings, 'TAGGER_CSS_FILENAME', 'coop_tag.css')
# You can create your own css file using as a start the original autoSuggest.css in static/tagger/css/

TAGGER_STATIC_URL = getattr(settings, 'TAGGER_STATIC_URL', '%stagger' % settings.STATIC_URL)


def get_class(model):
    model_name = model.upper()
    if model_name in ('TAG', 'TAGGEDITEM'):
        try:
        #if hasattr(get_class, '_cache_class'):
            dict_cache = getattr(get_class, '_cache_class')
            return dict_cache[model_name]
        except:
            model_class = None

            try:
                full_class_name = getattr(settings, 'TAGGER_%s_MODEL' % model_name)
                module_name, class_name = full_class_name.rsplit('.', 1)
                module = import_module(module_name)
                model_class = getattr(module, class_name)

            except AttributeError:
                # Defaults models are hard-coded here :
                if model_name == 'TAG' and not hasattr(settings, 'TAGGER_TAG_MODEL'):
                    from coop_tag.models import Tag
                    model_class = Tag
                elif model_name == 'TAGGEDITEM' and not hasattr(settings, 'TAGGER_TAGGEDITEM_MODEL'):
                    from coop_tag.models import TaggedItem
                    model_class = TaggedItem

            if not model_class:
                raise Exception('No %s class configured' % model)

            try:
                dict_cache = getattr(get_class, '_cache_class')
                dict_cache[model_name] = model_class
            except:
                setattr(get_class, '_cache_class', {model_name: model_class})

            return model_class
    else:
        raise ValueError("Only Tag or TaggedItem models can be queried through this method")

