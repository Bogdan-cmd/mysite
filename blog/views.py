from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

#PT HOME PAGE
class PostListView(ListView):
    model = Post

    def get_queryset(self): #METODA CE IMI PERMITE SA AM ACCES LA COLECTIA MEA DIN BD
        #METODA VA RETURNA TOATE ACELE OBIECTE CARE CORESP. FILTRELOR MELE
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        #APELEAZA METODA Post
        #TOATE objects DE ACOLO
        #filter DE OBIECTE PRIN CONDITIILE DATE DE MINE
        # __lte -> less than or equal two <= timezone(now)
        #'-published_date' -> - ordoneaza descrescator


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    #NU VREAU PE NIMENI SA ACCESEZE SA ACCESEZ ACEST VIEW
    #AICI APARE MIXINS -> PT LOGIN
    login_url = '/login/' #CAND O PERSOANA E LOGATA, UNDE SA FIE REDIRECTIONATA
    redirect_field_name = 'blog/post_detail.html' #REDIRECTIONEAZA AICI

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html' #CHIAR E O VARIABILA BUILT-IN DJANGO
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
     model = Post
     #AICI MAI JOS PAGINA ASTEAPTA PANA CAND AM STERS CEVA PENTRU A RETURNA success_url
     success_url = reverse_lazy('post_list')

#POSTEZ POSTURI, DAR INAINTE CA ELE SA FIE POSTATE MERG IN SECTIUNEA DRAFTS
#VOI CREEA UN VIEW CE LISTEAZA TOATE DRAFTURILE NEPUBLICATE
#CLASA PENTRU DRAFTS
class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    login_url ='/login/'
    redirect_field_name = 'blog/post_list.html'

    #VREAU UN QuerySet CARE SA NU AIBA DATA PUBLICARII
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
        #CONDITIA ESTE __isnull=True

#######################################
## Functions that require a pk match - adica cele de la comments##
#######################################

#O FUNCTIE PT A PUBLICA LUCRURI
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

#O FUNCTIE PT PUBLICAREA COMMENTARIULUI IN SINE
@login_required #convenience decorator -> view-ul este valabil doar daca utilizatorul este logat
def add_comment_to_post(request,pk): #pk -> link the actual comment to the post
    #obiectul post ori luam obiectul post ori 404(nu il gasim)
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid(): #
            comment = form.save(commit=False)
            comment.post = post #post din modelul Comment sa-l fac egal cu post itself, ala de mai sus
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})


#PENTRU CA COMENTARIUL SA FIE APROBAT PE PAGINA
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve() #models.py sa ma uit
    return redirect('post_detail',pk=comment.post.pk)


#PENTRU STERGEREA UNUI COMMENT
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk #ce am facut la linia 97 aduc aici ca o noua variabila
    comment.delete() #salvez in post_pk comentariul inainte sa sterg
    return redirect('post_detail',pk=post_pk) #imi reamintesc aici de pk-ul sters
