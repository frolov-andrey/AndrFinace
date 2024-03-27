from django import template


register = template.Library()


# @register.simple_tag
# def get_menu():
#     return menu


@register.inclusion_tag('andr_finance/modal_dialog_select_icon.html')
def modal_dialog_select_icon(cat_selected=0):
    return {'cat_selected': cat_selected}


# @register.inclusion_tag('women/list_tags.html')
# def show_all_tags():
#     tags = TagPost.objects.annotate(total_tags=Count('tags')).filter(total_tags__gt=0)
#     return {'tags': tags}
