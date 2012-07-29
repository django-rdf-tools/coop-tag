from django.conf import settings
from django.db.models.loading import get_model

# define the minimal weight of a tag in the tagcloud
TAGCLOUD_MIN = getattr(settings, 'TAGCLOUD_MIN', 1.0)

# define the maximum weight of a tag in the tagcloud
TAGCLOUD_MAX = getattr(settings, 'TAGCLOUD_MAX', 6.0)

# default models for tags and tagged items (override this in your settings)

TAGGED_ITEM_MODEL_NAME = getattr(settings, 'TAGGED_ITEM_MODEL', ('coop_tag', 'TaggedItem'))
TAGGED_ITEM_MODEL = get_model(*TAGGED_ITEM_MODEL_NAME)


TAG_MODEL_NAME = getattr(settings, 'TAG_MODEL', ('coop_tag', 'Tag'))
TAG_MODEL = get_model(*TAG_MODEL_NAME)



MAX_SUGGESTIONS = getattr(settings, 'TAGGER_MAX_SUGGESTIONS', 20)

TAGGER_CSS_FILENAME = getattr(settings, 'TAGGER_CSS_FILENAME', 'autoSuggest.css')

TAGGER_STATIC_URL = getattr(settings, 'TAGGER_STATIC_URL', '%sjquery-autosuggest' % settings.STATIC_URL)
