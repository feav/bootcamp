from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy

import markdown
from bootcamp.multimedia.forms import MultimediaForm, CategorieMediaForm
from bootcamp.multimedia.models import Multimedia, MultimediaComment, CategorieMedia
from bootcamp.decorators import ajax_required

def _multimedias(request, multimedia):
    paginator = Paginator(multimedia, 10)
    page = request.GET.get('page')
    try:
        multimedias = paginator.page(page)
    except PageNotAnInteger:
        multimedias = paginator.page(1)

    except EmptyPage:
        multimedias = paginator.page(paginator.num_pages)
    popular_tags = CategorieMedia.objects.all()
    return render(request, "multimedia/multimedias.html", {
            'multimedias':multimedias,
            'popular_tags': popular_tags
        })
def _blocs(request, bloc):
    paginator = Paginator(multimedia, 10)
    page = request.GET.get('page')
    try:
        blocs = paginator.page(page)
    except PageNotAnInteger:
        blocs = paginator.page(1)

    except EmptyPage:
        blocs = paginator.page(paginator.num_pages)

    return render(request, "multimedia/blocs.html", {
            'blocs':blocs,
        })


class CreateMultimedia(LoginRequiredMixin, CreateView):
    """

    """
    template_name = 'multimedia/write.html'
    form_class = MultimediaForm
    success_url = reverse_lazy('multimedias')

    def form_valid(self, form):

        form.instance.create_user = self.request.user
        return super(CreateMultimedia, self).form_valid(form)

class EditMultimedia(LoginRequiredMixin, UpdateView):
    template_name = 'multimedia/edit.html'
    model = Multimedia
    form_class = MultimediaForm
    success_url = reverse_lazy('multimedias')

@login_required
def multimedias(request):
    all_multimedias = Multimedia.get_published()
    return _multimedias(request, all_multimedias)

@login_required
def multimedia(request, slug):
    multimedia = get_object_or_404(Multimedia, slug=slug, status=Multimedia.PUBLISHED)
    return render(request, 'multimedia/multimedia.html', {'multimedia': multimedia})


@login_required
def bloc_tag(request, bloc):
    multimedias = Multimedia.objects.filter(bloc__slug=bloc).filter(status='P')
    return _multimedias(request, multimedias)


@login_required
def drafts(request):
    drafts = Multimedia.objects.filter(create_user=request.user,
                                    status=Multimedia.DRAFT)
    return render(request, 'multimedia/drafts.html', {'drafts': drafts})

class EditBloc(LoginRequiredMixin, UpdateView):
    template_name = 'multimedia/editbloc.html'
    model = CategorieMedia
    form_class = CategorieMediaForm
    success_url = reverse_lazy('blocs')

@login_required
def blocs(request):
    all_blocs = CategorieMedia.objects.all()
    return _blocs(request, all_multimedias)

@login_required
def bloc(request, slug):
    bloc = get_object_or_404(CategorieMedia, slug=slug)
    return render(request, 'multimedia/bloc.html', {'bloc': bloc})
    

@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            multimedia_id = request.POST.get('multimedia')
            multimedia = Multimedia.objects.get(pk=article_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                multimedia_comment = MultimediaComment(user=request.user,
                                                 multimedia=multimedia,
                                                 comment=comment)
                multimedia_comment.save()
            html = ''
            for comment in multimedia.get_comments():
                html = '{0}{1}'.format(html, render_to_string(
                    'multimedia/partial_multimedia_comment.html',
                    {'comment': comment}))

            return HttpResponse(html)

        else:   # pragma: no cover
            return HttpResponseBadRequest()

    except Exception:   # pragma: no cover
        return HttpResponseBadRequest()

