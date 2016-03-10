from django.shortcuts import render, get_object_or_404
from .models import Post
#分頁模組：
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
##########class-based views############
from django.views.generic import ListView
class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'blog/post/list.html'
#######寄發email#########
from .forms import EmailPostForm
from django.core.mail import send_mail #email模組
def post_share(request, post_id):
  # Retrieve post by id
  post = get_object_or_404(Post, id=post_id, status='published')
  sent=False
  if request.method == 'POST':
    # Form was submitted
    form = EmailPostForm(request.POST)
    if form.is_valid():#確認form內容正確，form.errors錯誤訊息
      # Form fields passed validation
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
      message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
      send_mail(subject, message, 'hiapymail@gmail.com', [cd['to']])
      sent = True
      # ... send email
  else:
    form = EmailPostForm() #GET請求顯示空白form
  return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
#############################
def post_list(request):
  #posts = Post.published.all()
  #######分頁功能#######
  object_list = Post.published.all()
  paginator = Paginator(object_list, 3) # 3 posts in each page
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer deliver the first page
    posts = paginator.page(1)
  except EmptyPage:
    # If page is out of range deliver last page of results
    posts = paginator.page(paginator.num_pages)
  ######################
  return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post, 
                           slug=post,
                           status='published',
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
  return render(request, 'blog/post/detail.html', {'post': post})