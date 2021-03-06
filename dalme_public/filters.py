import calendar
import itertools

from django.db.models import OuterRef, Q, Subquery

import django_filters

from dalme_app.models import Attribute, Source, LocaleReference
from dalme_public import forms
from dalme_public.models import (
    Collection,
    Corpus,
    Essay,
    FeaturedInventory,
    FeaturedObject,
)


BOOLEAN_CHOICES = [('true', 'Yes'), ('false', 'No')]


def _map_source_types():
    # We have to filter over 'value_STR' rather than, say, 'pk' because of the
    # sideways denormalization scheme: there is no unique, one-to-one mapping
    # between Attributes with the same 'value_STR'. Compare:
    #
    #     attrs = Attribute.objects.filter(
    #         attribute_type__short_name='record_type'
    #     )
    #     set([x.value_STR for x in attrs])
    #     set([(x.pk, x.value_STR) for x in attrs])
    #
    # So, let's eliminate the duplicates and index the choices first before
    # sorting them for the frontend widget, that way we can reaccess them by
    # index later to get the right names back when a request with a query comes
    # in. See the `filter_type` method below.

    return {
        str(idx): attr['value_STR']
        for idx, attr in enumerate(Attribute.objects.filter(
            attribute_type__short_name='record_type',
            object_id__in=Source.objects.filter(type=13, workflow__is_public=True).values('id')
        ).values('value_STR').distinct())
    }


def corpus_choices():
    return [
        (corpus.pk, corpus.title)
        for corpus in Corpus.objects.all().order_by('title')
    ]


def collection_choices():
    return [
        (collection.pk, collection.title)
        for collection in Collection.objects.all().order_by('title')
    ]


def source_type_choices():
    type_map = _map_source_types()
    return sorted(list(type_map.items()), key=lambda choice: choice[1])


def locale_choices():
    locales = [int(i) for i in Attribute.objects.filter(
        attribute_type=36,
        sources__type=13,
        sources__workflow__is_public=True
    ).values_list(
        'value_JSON__id',
        flat=True
    ).distinct()]

    return [
        (i.id, i.name)
        for i in LocaleReference.objects.filter(id__in=locales)
        .order_by('name')
    ]


class SourceOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('name', 'Name'),
            ('-name', 'Name (descending)'),
            ('source_type', 'Type'),
            ('-source_type', 'Type (descending)'),
            ('date', 'Date'),
            ('-date', 'Date (descending)'),
        ]

    @staticmethod
    def get_value(field, value):
        if not value:
            return False
        return next((v for v in value if v and v.endswith(field)), False)

    @staticmethod
    def annotate_dates(qs):
        dates = Attribute.objects.filter(
            Q(sources=OuterRef('pk'), attribute_type__short_name='date')
            | Q(sources=OuterRef('pk'), attribute_type__short_name='start_date')
        )
        qs = qs.annotate(source_date=Subquery(dates.values('value_DATE_y')[:1]))
        return qs.distinct()

    @staticmethod
    def annotate_source_type(qs):
        record_types = Attribute.objects.filter(
            sources=OuterRef('pk'),
            attribute_type__short_name='record_type'
        )
        return qs.annotate(
            source_type=Subquery(record_types.values('value_STR')[:1])
        ).distinct()

    def filter(self, qs, value):
        qs = super().filter(qs, value=list())
        # For now any duplicates that remain here after filtering are
        # eliminated on the endpoint itself before going down the wire.
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#distinct
        date = self.get_value('date', value)
        if date:
            self.parent.annotated = True
            qs = self.annotate_dates(qs)

        source_type = self.get_value('source_type', value)
        if source_type:
            self.parent.annotated = True
            qs = self.annotate_source_type(qs)

        name = self.get_value('name', value)
        if name:
            qs = qs.order_by(name)

        return qs


class SourceFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.annotated = False
        super().__init__(*args, **kwargs)
        for definition in self.filters.values():
            definition.field.label_suffix = ''

    name = django_filters.CharFilter(
        label='Name',
        lookup_expr='icontains'
    )
    source_type = django_filters.MultipleChoiceFilter(
        label='Type',
        choices=source_type_choices,
        method='filter_type'
    )
    date_range = django_filters.DateFromToRangeFilter(
        label='Date Range',
        method='filter_date_range'
    )
    corpus = django_filters.ChoiceFilter(
        label='Corpus',
        choices=corpus_choices,
        method='filter_corpus'
    )
    collection = django_filters.ChoiceFilter(
        label='Collection',
        choices=collection_choices,
        method='filter_collection'
    )
    has_image = django_filters.ChoiceFilter(
        label='Has Image',
        method='filter_image',
        choices=BOOLEAN_CHOICES
    )
    has_transcription = django_filters.ChoiceFilter(
        label='Has Transcription',
        method='filter_transcription',
        choices=BOOLEAN_CHOICES
    )
    locale = django_filters.ChoiceFilter(
        label='Locale',
        choices=locale_choices,
        method='filter_locale'
    )

    order_by = SourceOrderingFilter()

    class Meta:
        model = Source
        form = forms.SourceFilterForm
        fields = [
            'name',
            'source_type',
            'date_range',
            'corpus',
            'collection',
            'has_transcription',
            'has_image',
            'locale',
            'order_by',
        ]

    def filter_type(self, queryset, name, value):
        # Now we can re-use the type map when a request comes in for filtering.
        type_map = _map_source_types()
        source_types = []
        for idx in value:
            try:
                source_types.append(type_map[idx])
            except KeyError:
                continue
        return queryset.filter(**{'attributes__value_STR__in': source_types})

    def filter_date_range(self, queryset, name, value):
        queryset = queryset.filter(
            attributes__attribute_type__id__in=[19, 26]
        ).distinct()

        after, before = value
        if after:
            queryset = queryset.filter(attributes__value_DATE_y__gte=after)
        if before:
            queryset = queryset.filter(attributes__value_DATE_y__lte=before)

        return queryset

    def filter_corpus(self, queryset, name, value):
        try:
            corpus = Corpus.objects.get(pk=value)
        except Corpus.DoesNotExist:
            return queryset.none()
        return queryset.filter(
            sets__set_id__in=[
                collection.specific.source_set.pk
                for collection in corpus.collections.all()
            ]
        )

    def filter_collection(self, queryset, name, value):
        try:
            collection = Collection.objects.get(pk=value)
        except Collection.DoesNotExist:
            return queryset.none()
        return queryset.filter(sets__set_id=collection.source_set.pk)

    def filter_image(self, queryset, name, value):
        value = True if value == 'true' else False
        return queryset.exclude(source_pages__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):
        value = True if value == 'true' else False
        return queryset.exclude(source_pages__transcription__isnull=value)

    def filter_locale(self, queryset, name, value):
        return queryset.filter(attributes__attribute_type=36, attributes__value_JSON__id=str(value))


class FeaturedFilter(django_filters.FilterSet):
    @property
    def qs(self):
        qs = super().qs

        kind = self.data.get('kind')
        if kind:
            model = {
                'essay': Essay,
                'inventory': FeaturedInventory,
                'object': FeaturedObject,
            }.get(kind)
            if model:
                qs = [page for page in qs if isinstance(page, model)]

        order = self.data.get('order_by', 'date')
        if order == 'date':
            grouped = []
            qs = reversed(sorted(qs, key=lambda obj: obj.go_live_at))
            by_year = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs, key=lambda obj: obj.go_live_at.year
                )
            ]
            for year, values in by_year:
                by_month = [
                    (key, list(values))
                    for key, values in itertools.groupby(
                        values, key=lambda obj: calendar.month_name[
                            obj.go_live_at.month
                        ]
                    )
                ]
                grouped.append((year, by_month))
        else:
            qs = sorted(qs, key=lambda obj: obj.owner.last_name)
            grouped = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs, key=lambda obj: f'{obj.author}'
                )
            ]

        return grouped
