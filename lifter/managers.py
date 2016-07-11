
class Manager(object):
    """Used to retrieve / order / filter preferences pretty much as django's ORM managers"""
    queryset_class = None
    parser_class = None

    def __init__(self, store, model, queryset_class=None, **kwargs):

        from . import query
        self.model = model
        self.store = store
        self.queryset_class = queryset_class or self.queryset_class or query.QuerySet
        self.parser = kwargs.pop('parser', None)

    def get_store(self):
        return self.store

    def get_queryset(self):
        return self.queryset_class(manager=self, model=self.model)

    def all(self):
        return self.get_queryset().all()

    def execute(self, query):
        query.hints['model'] = self.model
        query.hints['parser'] = self.parser
        
        try:
            handler = getattr(self.get_store(), 'handle_{0}'.format(query.action))
        except AttributeError:
            raise ValueError('Unsupported {0} action'.format(query.action))

        return handler(query)

    def __getattr__(self, attr):
        # Try to proxy on queryset if possible
        return getattr(self.get_queryset(), attr)
