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
    desc = models.TextField(blank=True)
    tagline = models.CharField(max_length=500,blank=True)
    end_date = models.DateField('Published until', blank=True,null=True)
    website = models.URLField(blank=True)
    zine_pic = models.URLField(blank=True)
    locale = models.CharField(max_length=500,blank=True)

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

    def __str__(self):
        if self.tagline != '':
            return (self.title + ': ' + self.tagline)
        else:
            return self.title

class Issue(models.Model):
    #required
    zine = models.ForeignKey(Zine,on_delete=models.CASCADE)
    pub_date = models.DateField()
    #optional
    title = models.CharField(max_length=500,blank=True)
    desc = models.TextField(blank=True)
    guest_authors = models.ManyToManyField(User,blank=True)
    number = models.IntegerField(default=1)
    cover = models.URLField(blank=True)

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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_joined = models.DateField()
    hideIdentity = models.BooleanField('Hide Identity',default=False)

    def authorLink(self):
        if self.hideIdentity:
            return 'Anonymous'
        else:
            return '<a href="'+reverse('user', args=(self.user.id,))+'">'+self.user.__str__()+'</a>'

    def zineLink(self):
        return self.zine.link()

    def link(self):
        return (self.zineLink()+' by '+self.authorLink())

    def __str__(self):
        string = self.zine.title + ' by '
        if self.hideIdentity:
            string += 'Anonymous'
        else:
            string += self.user.__str__()
        return string