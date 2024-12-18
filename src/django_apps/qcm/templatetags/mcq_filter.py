import markdown
from django import template
from django.utils.safestring import mark_safe
from qa.mcq_db.models import AbstractReference

register = template.Library()


@register.filter
def markdown_to_html(markdown_text):
    """
    Convert Markdown text to HTML with support for extended syntax,
    and mark the result as safe to prevent escaping.
    """
    if markdown_text is None:
        return ""

    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.footnotes'
    ]

    # Use markdown to convert text to HTML
    html = markdown.markdown(markdown_text, extensions=extensions)

    # Mark the resulting HTML as safe
    return mark_safe(html)

@register.filter
def ref_to_html(reference: AbstractReference):
    html = reference.to_html()
    return mark_safe(html)