from django import template


register = template.Library()


@register.inclusion_tag('andr_finance/modal_dialog_select_icon.html')
def modal_dialog_select_icon(images, images_path, icon_file=''):
    return {'images': images, 'images_path': images_path, 'icon_file': icon_file}

