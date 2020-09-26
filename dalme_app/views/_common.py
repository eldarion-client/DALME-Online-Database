from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from dalme_app.utils import DALMEMenus as dm


@method_decorator(login_required, name='dispatch')
class DALMEListView(TemplateView):
    template_name = 'dalme_app/list-views.html'
    page_title = None
    dt_config = None
    breadcrumb = []
    helpers = None
    includes = None
    editor = 'true'
    form_template = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = self.get_config()
        breadcrumb = config['breadcrumb']
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        context['page_title'] = config['page_title']
        context['page_chain'] = get_page_chain(breadcrumb, context['page_title'])
        context['config'] = config['dt_config']
        context['helpers'] = config['helpers']
        context['includes'] = config['includes']
        context['form_template'] = config['form_template']
        context['editor'] = config['editor']
        return context

    def get_config(self, *args, **kwargs):
        return {
            'page_title': self.page_title,
            'dt_config': self.dt_config,
            'breadcrumb': self.breadcrumb,
            'helpers': self.helpers,
            'includes': self.includes,
            'form_template': self.form_template,
            'editor': self.editor
            }


def get_page_chain(breadcrumb, current=None):
    i_count = len(breadcrumb)
    title = ''
    if current and current != breadcrumb[i_count-1][0]:
        if len(current) > 55:
            current = current[:55] + ' <i class="fa fa-plus-circle fa-fw" data-toggle="tooltip" data-placement="bottom" title="{}"></i> '.format(current)
        for i in breadcrumb:
            if i[1] != '':
                title += '<a href="{}" class="title_link">{}</a>'.format(i[1], i[0])
            else:
                title += i[0]
            title += ' <i class="fa fa-caret-right fa-fw"></i> '
        title += '<span class="title_current">{}</span>'.format(current)
    else:
        c = 0
        while c <= i_count - 1:
            if c == i_count - 1:
                title += '<span class="title_current">{}</span>'.format(breadcrumb[c][0])
            else:
                title += breadcrumb[c][0] + ' <i class="fa fa-caret-right fa-fw"></i> '
            c = c + 1
    return title