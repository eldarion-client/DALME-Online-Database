from calendar import month_name

from django import template
from django.db.models.functions import Coalesce
from elasticsearch_dsl.utils import AttrDict

from dalme_public.serializers import PublicSourceSerializer
from dalme_public.models import (
    Collections,
    Essay,
    ExploreMapText,
    FeaturedObject,
    FeaturedInventory,
    Features,
    Footer,
    Home,
    SearchHelpBlock
)

from datetime import date

register = template.Library()


@register.inclusion_tag(
    'dalme_public/includes/_footer.html', takes_context=True
)
def footer(context):
    return {
        'footer': Footer.objects.first(),
        'year': context['year'],
        'project': context['project'],
    }


@register.filter
def classname(obj):
    return obj.specific.__class__.__name__


@register.simple_tag
def get_nav():
    home = Home.objects.first()
    return [
        page.specific for page in
        (home, *home.get_children().live().filter(show_in_menus=True))
    ]


@register.simple_tag(takes_context=True)
def nav_active(context, tab):
    page = context['page'].specific
    tab = tab.specific
    if page == tab:
        return True
    if not isinstance(tab, Home):
        if page in [desc.specific for desc in tab.get_descendants()]:
            return True
    return False


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
    records = context.get('records')
    record = context.get('record')
    search = context.get('search')
    explore = context.get('explore')

    if records or record:
        collection = context['request'].GET.get('collection', False)
        breadcrumbs[-1].update({'active': False})
        breadcrumbs = [
            *breadcrumbs,
            {
                'title': 'Records',
                'url': f'{page.url}records/?collection={page.id}',  # noqa
                'active': True if records else False,
            },
        ]

    if record:
        title = context['data']['short_name']
        url = page.url + f'records/{context["data"]["id"]}/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': title, 'url': url, 'active': True},
        ]

    if search:
        breadcrumbs[-1].update({'active': False})
        url = f'{page.url}/search/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': 'Search', 'url': url, 'active': True},
        ]

    if explore:
        breadcrumbs[-1].update({'active': False})
        url = f'{page.url}/explore/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': 'Explore', 'url': url, 'active': True},
        ]

    return breadcrumbs


@register.simple_tag(takes_context=True)
def get_flat_nav(context):
    page = context['page']
    if not page.show_in_menus:
        return [p.specific for p in page.get_parent().get_siblings().live().filter(show_in_menus=True)]
    else:
        return [p.specific for p in page.get_siblings().live().filter(show_in_menus=True)]


@register.simple_tag
def get_object_nav():
    return FeaturedObject.objects.live().specific().annotate(
        published=Coalesce('go_live_at', 'first_published_at')
    ).order_by('published')[:3]


@register.simple_tag
def get_inventory_nav():
    return FeaturedInventory.objects.live().specific().annotate(
        published=Coalesce('go_live_at', 'first_published_at')
    ).order_by('published')[:3]


@register.simple_tag(takes_context=True)
def get_header_image_styles(context, header_image):
    gradients = {
        'DALME': '125deg, rgba(6, 78, 140, 0.5) 0%, rgba(17, 74, 40, 0.5) 100%',  # noqa
        'project': '125deg, rgba(83, 134, 160, 0.7) 0%, rgba(58, 74, 60, 0.9) 100%',  # noqa
        'features': '125deg, rgba(99, 98, 58, 0.7) 0%, rgba(80, 41, 43, 0.9) 100%',  # noqa
        'collections': '125deg, rgba(95, 81, 111, 0.7) 0%, rgba(23, 62, 101, 0.9) 100%',  # noqa
        'about': '125deg, rgba(155, 149, 76, 0.7) 0%, rgba(63, 73, 54, 0.9) 100%',  # noqa
        'generic': '59deg, #11587c 54.62%, #1b1b1b',
    }
    page = context['page']
    value = False
    count = 0

    while not value and count < 4:
        value = gradients.get(page.slug, False)
        page = page.get_parent()

    if not value:
        value = gradients['generic']

    gradient = f'linear-gradient({value})'
    background_image = f'background-image: {gradient}, url({header_image.url})'
    return f'{background_image}; background-size: cover; width: 100%;'


@register.simple_tag(takes_context=True)
def get_source_details(context):
    page = context['page']
    source = page.source
    source_set = page.source_set

    if source:
        data = PublicSourceSerializer(source).data
        name = data['name']
        short_name = data['short_name']
        date = data.get('date')
        city = data.get('city')

    url = None
    if source and source_set:
        stem = 'public/DALME/collections'
        collection = source_set.public_collections.first()
        url = f'/{stem}/{collection.slug}/records/{source.pk}'

    return {
        'source': source,
        'source_set': source_set,
        'name': name,
        'short_name': short_name,
        'date': date,
        'city': city,
        'url': url,
        'collections': Collections.objects.first(),
    }


@register.simple_tag(takes_context=True)
def get_features_filter_q(context, key, value):
    params = f'?{key}={value}' if value != 'all' else ''
    for param_key, param_value in context['request'].GET.items():
        if param_key != key:
            if not params:
                params += f'?{param_key}={param_value}'
            else:
                params += f'&{param_key}={param_value}'
    return params


@register.simple_tag()
def get_features_url():
    return Features.objects.first().url


@register.simple_tag()
def get_features_nav_q(key):
    return {
        'essays': '?kind=essay',
        'inventories': '?kind=inventory',
        'objects': '?kind=object',
    }[key]


@register.simple_tag()
def get_recent_objects():
    objs = FeaturedObject.objects.live().specific().order_by('go_live_at')[:3]
    return [
        {'url': obj.url, 'month': month_name[obj.go_live_at.month]}
        for obj in objs
    ]


@register.simple_tag()
def get_recent_inventories():
    objs = FeaturedInventory.objects.live().specific().order_by('go_live_at')[:3]
    return [
        {'url': obj.url, 'month': month_name[obj.go_live_at.month]}
        for obj in objs
    ]


@register.simple_tag()
def get_recent_essays():
    objs = Essay.objects.live().specific().order_by('go_live_at')[:3]
    return [
        {'url': obj.url, 'month': month_name[obj.go_live_at.month]}
        for obj in objs
    ]


@register.simple_tag()
def collection_date_range(collection):
    years = sorted(collection.source_set.get_public_time_coverage().keys())
    try:
        return f'{years[0]} - {years[-1]}' if len(years) > 1 else f'{years[0]}+'
    except IndexError:
        return 'Unknown'


@register.simple_tag()
def get_snippet(obj, width):
    return obj.snippet(width)


@register.simple_tag(takes_context=True)
def get_citation(context):
    accessed = date.today()
    page = context['page']
    page_class = page.get_verbose_name()
    citation = {
        'editor': [
            {'family': 'Smail', 'given': 'Daniel Lord'},
            {'family': 'Pizzorno', 'given': 'Gabriel H.'},
            {'family': 'Morreale', 'given': 'Laura'}
        ],
        "accessed": {"date-parts": [[accessed.year, accessed.month, accessed.day]]},
    }

    if page_class == 'Collections':
        citation.update({
            'type': 'book',
            'title': 'The Documentary Archaeology of Late Medieval Europe',
            'URL': "https://dalme.org",
            'issued': {'date-parts': [[accessed.year]]}
        })
    else:
        citation.update({
            'type': 'chapter',
            'container-title': 'The Documentary Archaeology of Late Medieval Europe',
            'title': page.title,
            'URL': page.get_full_url(context['request'])
        })
        if page_class == 'Flat':
            citation['issued'] = {'date-parts': [[accessed.year]]}
        elif page_class == 'Collection':
            citation['author'] = [{'literal': page.source_set.owner.profile.full_name}]
            citation['issued'] = {'date-parts': [[accessed.year]]}
        else:
            author = page.alternate_author if page.alternate_author is not None else page.author
            citation['author'] = [{'literal': author}]
            citation['issued'] = {'date-parts': [[
                    page.last_published_at.year,
                    page.last_published_at.month,
                    page.last_published_at.day
                ]]}

    return citation


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def dd_record_name(name, part=''):
    try:
        name_string = name.split('(')
        if part == 'loc':

            try:
                return name_string[1][:-1]

            except IndexError:
                return 'Archival location not available'

        return name_string[0]

    except AttributeError:
        return name


@register.simple_tag
def search_help():
    return SearchHelpBlock.objects.first()


@register.simple_tag
def explore_map_text():
    return ExploreMapText.objects.first()


@register.filter
def to_dict(target):
    if type(target) is AttrDict:
        return target.to_dict()
    if type(target) is list and type(target[0]) is tuple:
        return {i[0]: i[1] for i in target}


@register.simple_tag
def dict_key_lookup(_dict, key):
    return _dict.get(key, '')


@register.filter
def in_list(value, list_string):
    _list = []
    conversions = {
        'none': None,
        'blank': '',
        'empty': ' '
    }

    for item in list_string.split(','):
        if item in conversions:
            _list.append(conversions[item])
        else:
            _list.append(item)

    return value in _list


@register.filter
def get_highlights(meta, context):
    highlights = []
    if 'highlight' in meta:
        fields = list(meta.highlight.to_dict().keys())
        for field in fields:
            for fragment in meta.highlight[field]:
                try:
                    highlights.append({'field': context[field]['label'], 'fragment': fragment})

                except KeyError:
                    field_tokens = field.split('.')
                    field_tokens.pop(-1)
                    highlights.append({'field': context['.'.join(field_tokens)]['label'], 'fragment': fragment})

    if 'inner_hits' in meta:
        docs = list(meta.inner_hits.to_dict().keys())
        for doc in docs:
            for hit in meta.inner_hits[doc].hits:
                if hit.meta:
                    try:
                        fields = hit.meta.highlight.to_dict().keys()
                        for field in fields:
                            for fragment in hit.meta.highlight[field]:
                                highlights.append({'field': f'Folio {hit.folio}', 'fragment': fragment, 'link': hit.folio})

                    except AttributeError:
                        pass

    return highlights
