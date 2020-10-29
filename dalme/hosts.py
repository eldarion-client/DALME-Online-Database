from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'public', 'dalme_public.urls', name='public'),
                         host(r'db', 'dalme_app.urls', name='db'),
                         host(r'data', 'dalme_api.urls', name='data'),
                         )
