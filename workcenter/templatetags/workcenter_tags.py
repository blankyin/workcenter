__author__ = 'yinchangjiang.ht'

from django import template
# from workcenter.models import Menu
import workcenter.settings as settings

register = template.Library()


@register.filter(name="key")
def key(model_dict, key_name):
    try:
        value = model_dict[key_name]
    except:
        value = settings.TEMPLATE_STRING_IF_INVALID
    return value


# @register.tag(name="nav_menu")
# def do_nav_menu(parser, token):
#     effective_menus = Menu.objects.filter(status="1").order_by("sort")
#     return NavMenuNode(effective_menus)
#
#
# class NavMenuNode(template.Node):
#     def __init__(self, effective_menus):
#         self.effective_menus = effective_menus
#
#     def render(self, context):
#         context["nav_menu"] = self.effective_menus
#         return ''

