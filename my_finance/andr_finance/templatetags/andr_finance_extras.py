from django import template

register = template.Library()


@register.inclusion_tag('andr_finance/modal_dialog_select_icon.html')
def modal_dialog_select_icon(images, images_path, icon_file=''):
    return {'images': images, 'images_path': images_path, 'icon_file': icon_file}


@register.inclusion_tag('andr_finance/tr_transaction.html')
def tr_transaction(transaction, group_object_id=None):
    return {'transaction': transaction, 'group_object_id': group_object_id}
