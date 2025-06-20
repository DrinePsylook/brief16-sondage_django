from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def card(title="", content="", **kwargs):
    """
    Composant carte réutilisable
    """
    card_classes = "bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 dark:bg-gray-800"
    
    card_html = f'''
    <div class="{card_classes}">
        {f'<div class="p-6 border-b border-gray-200 dark:border-gray-700"><h3 class="text-xl font-semibold text-gray-900 dark:text-white">{title}</h3></div>' if title else ''}
        <div class="p-6">{content}</div>
    </div>
    '''
    
    return mark_safe(card_html)