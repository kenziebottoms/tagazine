from django.db import models
from django.urls import reverse

class User(models.Model):
    #required
    username = models.CharField(max_length=200)
    member_since = models.DateField('Member since')
    #optional
    name = models.CharField(max_length=500,blank=True)
#    user_pic = models.ImageField(upload_to='user_pics',blank=True)

    def __str__(self):
        if self.name != '':
            return self.name
        else:
            return self.username

class Zine(models.Model):
    #required
    title = models.CharField(max_length=500)
    start_date = models.DateField('Published since')
    authors = models.ManyToManyField(User, through='Authorship')
    show_author = models.BooleanField(default=True)
    external = models.BooleanField(default=False)
    #optional
    tagline = models.CharField(max_length=500,blank=True)
    end_date = models.DateField('Published until', blank=True,null=True)
    website = models.URLField(blank=True)
#    zine_pic = models.ImageField(upload_to='zine_pics', blank=True)

    def __str__(self):
        if self.tagline != '':
            return (self.title + ': ' + self.tagline)
        else:
            return self.title

class Authorship(models.Model):
    zine = models.ForeignKey(Zine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField()
    hideIdentity = models.BooleanField('Hide Identity',default=False)

    def authorLink(self):
        if self.hideIdentity:
            return 'Anonymous'
        else:
            return '<a href="'+reverse('user', args=(self.user.id,))+'">'+self.user.__str__()+'</a>'

    def zineLink(self):
        return '<a href="'+reverse('zine',args=(self.zine.id,))+'">'+self.zine.title+'</a>'

    def link(self):
        return (self.zineLink()+' by '+self.authorLink())

    def __str__(self):
        string = self.zine.title + ' by '
        if self.hideIdentity:
            string += 'Anonymous'
        else:
            string += self.user.__str__()
        return string