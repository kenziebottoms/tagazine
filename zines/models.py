from django.db import models
from django.urls import reverse
from django.conf import settings
import os, re, datetime

# tag slugs
from django.utils.text import slugify

# integrating native User model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# thumbnails
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from mimetypes import MimeTypes
import urllib

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
        authorships = Authorship.objects.filter(user_profile=self.id)
        for authorship in authorships:
            if authorship.zine.published:
                return True
        return False
    def hasUnPublishedContent(self):
        authorships = Authorship.objects.filter(user_profile=self.id)
        for authorship in authorships:
            if authorship.zine.published == False:
                return True
            if authorship.zine.unPublishedContent():
                return True
        return False
    def __str__(self):
        if self.name != '':
            return self.name
        else:
            return self.user.username

    def create_thumb(self):
        if not self.pic:
            return

        mime = MimeTypes()
        url = urllib.pathname2url(self.pic.path)
        directory = "/".join(url.split('/')[:-2])
        mime_type = mime.guess_type(url)[0]

        thumb = Image.open(self.pic.path)
        TARGET_SIZE = [150, 150]
        width, height = thumb.size
        if width > height:
            THUMB_SIZE = [int(TARGET_SIZE[0]*width/float(height)), TARGET_SIZE[1]]
        else:
            THUMB_SIZE = [TARGET_SIZE[0],int(TARGET_SIZE[1]*height/float(width))]

        mid_x = THUMB_SIZE[0] / 2
        mid_y = THUMB_SIZE[1] / 2
        # shrinks it down to at most 150x150 but keeps aspect ratio
        thumb = thumb.resize(THUMB_SIZE,Image.ANTIALIAS)
        # crops it down to a square from that
        thumb = thumb.crop((mid_x-(TARGET_SIZE[0]/2),mid_y-(TARGET_SIZE[1]/2),mid_x+(TARGET_SIZE[0]/2),mid_y+(TARGET_SIZE[1]/2)))

        filename, ext = os.path.splitext(self.pic.name)
        filename = str(filename+"_150x150"+ext)

        temp_image = open(os.path.join(directory,filename), 'w')
        thumb.save(temp_image)

        thumb_data = open(os.path.join(directory, filename), 'r')
        thumb_file = File(thumb_data)

        self.thumb.save(filename, thumb_file)

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

class Zine(models.Model):
    #required
    title = models.CharField(max_length=500)
    start_date = models.DateField('Published since')
    authors = models.ManyToManyField(Profile, through='Authorship')
    show_author = models.BooleanField(default=True)
    external = models.BooleanField('Externally hosted',default=False)
    submissions_open = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    primary_language = models.CharField(max_length=300, default='English')
    #optional
    desc = models.TextField(blank=True)
    contact_email = models.CharField(max_length=200,blank=True)
    submission_email = models.CharField(max_length=200,blank=True)
    tagline = models.CharField(max_length=500,blank=True)
    end_date = models.DateField('Published until', blank=True,null=True)
    website = models.URLField(blank=True)
    cover = models.FileField(upload_to='covers')
    locale = models.CharField(max_length=500,blank=True)
    tags = models.ManyToManyField(Tag,blank=True)

    def issueCount(self):
        return Issue.objects.filter(zine=self.id).count()

    def link(self):
        return '<a href="'+reverse('zine',args=(self.id,))+'">'+self.title+'</a>'

    def authorsLink(self):
        authorships = Authorship.objects.filter(zine=self.id)
        if len(authorships) == 1:
            return authorships[0].authorLink()
        else:
            string = ''
            for authorship in authorships:
                string += authorship.authorLink()
                if authorship != authorships[len(authorships)-1]:
                    string += ', '
            return string

    def lastUpdated(self):
        issues = Issue.objects.filter(zine=self.id)
        if issues:
            return issues.latest('pub_date').pub_date
        else:
            return datetime.date(1900,1,1)

    def firstIssue(self):
        return Issue.objects.filter(zine=self.id).order_by('number').first()

    def unPublishedContent(self):
        return Issue.objects.filter(zine=self.id,published=False)

    def __str__(self):
        if self.tagline != '':
            return (self.title + ': ' + self.tagline)
        else:
            return self.title

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
    cover = models.FileField(upload_to='covers')

    def guestAuthorsLink(self):
        guest_authors = self.guest_authors.all()
        if len(guest_authors.all()) == 1:
            return guest_authors.all()[0].link()
        else:
            string = ''
            for author in guest_authors:
                string += author.link()
                if author != guest_authors[len(guest_authors)-1]:
                    string += ', '
            return string
    def displayTitle(self):
        if self.title == '':
            return self.zine.title+' #'+str(self.number)
    def titleLink(self):
        string = self.zine.link()+' &raquo '
        if self.title == '':
            string += '#'+str(self.number)
        else:
            string += self.title
        return string

    class Meta:
        order_with_respect_to = 'zine'
    def __str__(self):
        return self.displayTitle()

class Authorship(models.Model):
    zine = models.ForeignKey(Zine,on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_joined = models.DateField()
    hideIdentity = models.BooleanField('Hide Identity',default=False)

    def authorLink(self):
        if self.hideIdentity:
            return 'Anonymous'
        else:
            return self.user_profile.link()

    def zineLink(self):
        return self.zine.link()

    def link(self):
        return (self.zine.Link()+' by '+self.authorLink())

    def __str__(self):
        string = self.zine.title + ' by '
        if self.hideIdentity:
            string += 'Anonymous'
        else:
            string += self.user_profile.__str__()
        return string
    class Meta:
        auto_created = True

class Page(models.Model):
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    content = models.FileField(upload_to='issues')
    subtitles = models.TextField(blank=True)
    class Meta:
        order_with_respect_to = 'issue'
    def __str__(self):
        pages = map(int,Page.objects.filter(issue=self.issue).values_list('id',flat=True))
        pageNo = pages.index(self.id)+1
        return (self.issue.displayTitle() + '.' + str(pageNo))
