from django import template

from quiz_info.models import Carousel, RoundMenu

register = template.Library()


@register.inclusion_tag("quiz_info/tags/carousel.html")
def show_top_carousel_memu():
    files = Carousel.objects.all()
    return {"files": files}


@register.inclusion_tag("quiz_info/tags/round_menu.html")
def show_round_menu():
    files = RoundMenu.objects.all()
    return {"files": files}
