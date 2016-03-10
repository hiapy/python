from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse #透過名稱建立URL
#自訂資料庫管理物件
class PublishedManager(models.Manager):
  def get_queryset(self):
    return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )
  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique_for_date='publish') #用在文章的url，根據日期唯一性
  author = models.ForeignKey(User, related_name='blog_posts') #資料一對多，從User來
  body = models.TextField() #文章內容
  publish = models.DateTimeField(default=timezone.now) #發布時間
  created = models.DateTimeField(auto_now_add=True) 
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') #使用choices限制選項
  
  #################
  objects = models.Manager() # The default manager.
  published = PublishedManager() # Our custom manager.
  #################

  def get_absolute_url(self):
    return reverse('blog:post_detail', args=[
                      self.publish.year,
                      self.publish.strftime('%m'), #用strftime()來讓個位數前面補0變成兩位數
                      self.publish.strftime('%d'),
                      self.slug
                    ]
                  )
     
  class Meta: #依發佈日期排序，負號表示descending
    ordering = ('-publish',)
  
  def __str__(self):
    return self.title
class Comment(models.Model):
  post = models.ForeignKey(Post, related_name='comments')
  name = models.CharField(max_length=80)
  email = models.EmailField()
  body = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)
  
  class Meta:
    ordering = ('created',)
    
  def __str__(self):
    return 'Comment by {} on {}'.format(self.name, self.post)
