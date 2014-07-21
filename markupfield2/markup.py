from django.utils.html import escape, urlize, linebreaks

DEFAULT_MARKUP_TYPES = {
    #format: type, renderer (needs to be a function).

    "html": lambda content: content,
    "plain": lambda content: urlize(linebreaks(escape(content))),
}

def get_renderer(type):
    return markup_types()[type]

def markup_types():
    return DEFAULT_MARKUP_TYPES