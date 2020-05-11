from django import template

from dalme_public.models import (
    FeaturedObject, FeaturedInventory, Features, Flat, Home
)


register = template.Library()


@register.simple_tag
def get_nav():
    home = Home.objects.first()
    return [
        page.specific for page in
        (home, *home.get_children().filter(show_in_menus=True))
    ]


@register.simple_tag(takes_context=True)
def get_breadcrumbs_nav(context):
    page = context['page']
    ancestors = [
        {
            'title': ancestor.specific.title_switch,
            'url': ancestor.specific.url,
            'active': False
        }
        for ancestor in page.get_ancestors()[1:]
    ]
    current = {'title': page.title_switch, 'url': page.url, 'active': True}
    breadcrumbs = [*ancestors, current]

    # We have to do some contortions here to make sure the RoutablePage
    # endpoints maintain the illusion of being actual Page objects.
    inventories = context.get('inventories')
    inventory = context.get('inventory')
    if inventories or inventory:
        collection = page.get_parent()
        breadcrumbs[-1].update({'active': False})
        breadcrumbs = [
            *breadcrumbs,
            {
                'title': 'Inventories',
                'url': f'{page.url}inventories/?collection={collection.pk}&set={page.pk}',
                'active': True if inventories else False,
            },
        ]

    if inventory:
        title = context['data']['short_name']
        url = page.url + f'inventories/{context["data"]["id"]}/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': title, 'url': url, 'active': True},
        ]

    return breadcrumbs


@register.simple_tag
def get_about_nav():
    return Flat.objects.all()


@register.simple_tag
def get_features_nav():
    features = Features.objects.first()
    return features.get_children() if features else []


@register.simple_tag
def get_object_nav():
    return reversed(FeaturedObject.objects.all().order_by(
        '-first_published_at'
    )[:3])


@register.simple_tag
def get_inventory_nav():
    return reversed(FeaturedInventory.objects.all().order_by(
        '-first_published_at'
    )[:3])


@register.simple_tag
def get_header_image_styles(header_image):
    colour = 'rgba(59, 103, 130, 0.6)'
    gradient = f'linear-gradient({colour}, {colour})'
    background = f'{gradient}, url({header_image.url})'
    return f'background: {background}; background-size: cover;'


@register.simple_tag(takes_context=True)
def get_source_details(context):
    page = context['page']
    source = page.source
    return None if not source else {
        'name': source.name,
    }
