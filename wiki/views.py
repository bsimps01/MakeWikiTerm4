from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from wiki.forms import PageForm
from wiki.models import Page
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })

class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        form = PageForm(instance = page)
        return render(request, 'page.html', {
          'page': page, 'form': form
        })

    def post(self, request, slug):

        page = self.get_queryset().get(slug__iexact=slug)
        form = PageForm(request.POST)
        page.title = request.POST['title']
        page.content = request.POST['content']
        page.save()
        context = {
          'page': page,
          'form': form,
        }
        return HttpResponseRedirect(reverse('wiki-details-page', args=[page.slug]))

class PageCreateView(CreateView):

    model = Page
    fields = ['title', 'content', 'author']
    template_name = 'create.html'

    