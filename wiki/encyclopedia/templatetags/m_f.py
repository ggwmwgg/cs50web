# Markdown to HTML custom django filter
from django import template
import markdown2

register = template.Library()

@register.filter
def md_to_html(text):
    return markdown2.markdown(text)