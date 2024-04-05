from django import template

register = template.Library()


@register.inclusion_tag('andr_finance/modal_dialog_select_icon.html')
def modal_dialog_select_icon(images, images_path, icon_file=''):
    return {'images': images, 'images_path': images_path, 'icon_file': icon_file}


@register.inclusion_tag('andr_finance/tr_transaction.html')
def tr_transaction(transaction, balances, group_object_id=None, icon_default=''):
    return {'transaction': transaction, 'balance': balances[transaction.id], 'group_object_id': group_object_id, 'icon_default': icon_default}


@register.inclusion_tag('andr_finance/tr_account_balance.html')
def tr_account_balance(account, balances):
    return {'balance': balances[account.id]}

