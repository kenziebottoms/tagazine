from django.db import models
from django.urls import reverse
from django.conf import settings
import os, re, datetime, json
from django.shortcuts import get_object_or_404

# tag slugs
from django.utils.text import slugify

# integrating native User model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# thumbnails
import image_processing

class Profile(models.Model):
    #required
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    member_since = models.DateField(auto_now_add=True)
    #optional
    name = models.CharField(max_length=500,blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    pic = models.ImageField(upload_to='users',blank=True)
    thumb = models.ImageField(upload_to='users',blank=True)
    location = models.CharField(max_length=500,blank=True)

    # info fns
    def link(self):
        return '<a href="'+reverse('profile', args=(self.id,))+'">'+self.__str__()+'</a>'    

    def hasPublishedContent(self):
        zines = Zine.objects.filter(authors=self.id,published=True)
        return (len(zines) > 0)

    def hasUnPublishedContent(self):
        private_zines = Zine.objects.filter(authors=self,published=False)
        private_issues = Issue.objects.filter(zine__authors=self,published=False)
        return (private_zines or private_issues)

    def __str__(self):
        if self.name != '':
            return self.name
        else:
            return self.user.username

    def create_thumb(self):
        if not self.pic:
            return
        image_processing.crop(self.pic, self.thumb, 150, 150)

@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Tag(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique=True,editable=False)
    #optional
    parent_tag = models.ForeignKey('self',blank=True,null=True)

    def genSlug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Tag.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.genSlug()
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, title):
        tag = cls(title=title)
        tag.save()
        return tag

class Zine(models.Model):
    #required
    title = models.CharField(max_length=500)
    start_date = models.DateField('Published since',default=datetime.datetime.now)
    authors = models.ManyToManyField(Profile)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='owner',null=True)
    show_author = models.BooleanField(default=True)
    external = models.BooleanField('Externally hosted',default=False)
    submissions_open = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    primary_language = models.CharField(max_length=300, default='English')
    slug = models.SlugField(unique=True,editable=False,blank=True)
    #optional
    desc = models.TextField(blank=True)
    contact_email = models.CharField(max_length=200,blank=True)
    submission_email = models.CharField(max_length=200,blank=True)
    tagline = models.CharField(max_length=500,blank=True)
    end_date = models.DateField('Published until', blank=True,null=True)
    website = models.URLField(blank=True)
    cover = models.ImageField(upload_to='covers')
    thumb = models.ImageField(upload_to='covers',blank=True)
    locale = models.CharField(max_length=500,blank=True)
    tags = models.ManyToManyField(Tag,blank=True)

    def issueCount(self):
        return Issue.objects.filter(zine=self.id).count()

    def link(self):
        return '<a href="'+reverse('zine',args=(self.id,))+'">'+self.title+'</a>'

    def authorsLink(self):
        return ', '.join(map(lambda a: a.link(), self.authors.all()))

    def lastUpdated(self):
        issues = Issue.objects.filter(zine=self.id)
        if issues:
            return issues.latest('pub_date').pub_date
        else:
            # TODO: wtf
            return datetime.date(1900,1,1)

    def firstIssue(self):
        return Issue.objects.filter(zine=self.id).order_by('number').first()

    def unPublishedContent(self):
        return Issue.objects.filter(zine=self.id,published=False)

    def genSlug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        existing = Zine.objects.filter(slug=unique_slug)
        while existing.exists() and existing[0].id != self.id:
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.genSlug()
        super(Zine, self).save(*args, **kwargs)

    def __str__(self):
        title = self.title
        if self.tagline:
            title += ': ' + self.tagline
        return title

class Issue(models.Model):
    #required
    zine = models.ForeignKey(Zine,on_delete=models.CASCADE)
    pub_date = models.DateField()
    published = models.BooleanField(default=False)
    #optional
    title = models.CharField(max_length=500,blank=True)
    desc = models.TextField(blank=True)
    guest_authors = models.ManyToManyField(Profile,blank=True)
    ext_guest_authors = models.TextField(blank=True)
    number = models.IntegerField(default=1)
    cover = models.ImageField(upload_to='issues',blank=True)
    thumb = models.ImageField(upload_to='issues',blank=True)

    # TODO: add external guest authors here
    def guestAuthorsLink(self):
        return ', '.join(map(lambda a: a.link(), self.guest_authors.all()))

    # 'Issue Title' or 'Zine Title #2'
    def displayTitle(self):
        return self.title or self.zine.title+' #'+str(self.number)

    def titleLink(self):
        string = self.zine.link()+' &raquo '
        addon = self.title or '#'+str(self.number)
        return string+addon

    class Meta:
        order_with_respect_to = 'zine'

    def create_thumb(self):
        if not self.cover:
            return
        image_processing.crop(self.cover, self.thumb, 400, 300)

    def __str__(self):
        return str(self.displayTitle())

class Page(models.Model):
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    content = models.ImageField(upload_to='issues')
    #optional
    thumb = models.ImageField(upload_to='issues',blank=True)
    subtitles = models.TextField(blank=True)

    class Meta:
        order_with_respect_to = 'issue'

    # TODO: there's a better way to do this
    def __str__(self):
        pages = map(int,Page.objects.filter(issue=self.issue).values_list('id',flat=True))
        pageNo = pages.index(self.id)+1
        return (self.issue.displayTitle() + '.' + str(pageNo))

def get_stats():
    stats = []
    stats.append(['Total zines', Zine.objects.count()])
    stats.append(['Total published zines', Zine.objects.filter(published=True).count()])
    stats.append(['Total issues', Issue.objects.count()])
    stats.append(['Total pages',  Page.objects.count()])
    stats.append(['Total users', User.objects.count()])
    return stats

def get_user_stats(user_id):
    stats = []
    user = get_object_or_404(User, pk=user_id)
    profile = user.profile
    stats.append([str(profile)+'\'s zines', Zine.objects.filter(authors=profile).count()])
    stats.append([str(profile)+'\'s published zines', Zine.objects.filter(published=True,authors=profile).count()])
    stats.append([str(profile)+'\'s issues', Issue.objects.filter(zine__authors=profile).count()])
    stats.append([str(profile)+'\'s pages',  Page.objects.filter(issue__zine__authors=profile).count()])
    return stats