from django import template
from django.urls import reverse
from django.urls import resolve
from django.utils import translation

register = template.Library()


class TranslatedURL(template.Node):

    def __init__(self, language):
        self.language = language

    def render(self, context):
        view = resolve(context['request'].path)
        request_language = translation.get_language()
        translation.activate(self.language)
        url = reverse(f"{view.namespace}:{view.url_name}",
                       args=view.args, kwargs=view.kwargs)
        translation.activate(request_language)
        return url


@register.tag(name='translate_url')
def do_translate_url(_, token):
    language = token.split_contents()[1]
    return TranslatedURL(language)
