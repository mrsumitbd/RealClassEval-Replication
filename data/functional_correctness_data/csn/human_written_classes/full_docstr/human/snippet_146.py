from django.conf import settings
import re
from django.utils.text import slugify

class MenuItem:
    """
    MenuItem represents an item in a menu, possibly one that has a sub-menu (children).
    """

    def __init__(self, title, url, children=[], weight=1, check=None, visible=True, slug=None, exact_url=False, **kwargs):
        """
        MenuItem constructor

        title       either a string or a callable to be used for the title
        url         the url of the item
        children    an array of MenuItems that are sub menus to this item
                    this can also be a callable that generates an array
        weight      used to sort adjacent MenuItems
        check       a callable to determine if this item is visible
        slug        used to generate id's in the HTML, auto generated from
                    the title if left as None
        exact_url   normally we check if the url matches the request prefix
                    this requires an exact match if set

        All other keyword arguments passed into the MenuItem constructor are
        assigned to the MenuItem object as attributes so that they may be used
        in your templates. This allows you to attach arbitrary data and use it
        in which ever way suits your menus the best.
        """
        self.url = url
        self.title = title
        self.visible = visible
        self.children = children
        self.weight = weight
        self.check_func = check
        self.slug = slug
        self.exact_url = exact_url
        self.selected = False
        self.parent = None
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def check(self, request):
        """
        Evaluate if we should be visible for this request
        """
        if callable(self.check_func):
            self.visible = self.check_func(request)

    def process(self, request):
        """
        process determines if this item should be visible, if its selected, etc...
        """
        self.check(request)
        if not self.visible:
            return
        if callable(self.url):
            self.url = self.url(request)
        if callable(self.title):
            self.title = self.title(request)
        if self.slug is None:
            self.slug = slugify(self.title)
        if callable(self.children):
            children = list(self.children(request))
        else:
            children = list(self.children)
        for child in children:
            child.parent = self
            child.process(request)
        self.children = [child for child in children if child.visible]
        self.children.sort(key=lambda child: child.weight)
        hide_empty = getattr(settings, 'MENU_HIDE_EMPTY', False)
        if hide_empty and len(self.children) == 0:
            self.visible = False
            return
        curitem = None
        for item in self.children:
            item.selected = False
            if item.match_url(request):
                if curitem is None or len(curitem.url) < len(item.url):
                    curitem = item
        if curitem is not None:
            curitem.selected = True

    def match_url(self, request):
        """
        match url determines if this is selected
        """
        matched = False
        if self.exact_url:
            if re.match(f'{self.url}$', request.path):
                matched = True
        elif re.match('%s' % self.url, request.path):
            matched = True
        return matched