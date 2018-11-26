from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

import markdown




@python_2_unicode_compatible
class CategorieMedia(models.Model):

	title = models.CharField(max_length=25)
	description = models.CharField(max_length=500)
	slug = AutoSlugField(populate_from='title')

	def __str__(self):
		return self.title

	
	def get_multimedias(self):
		return Multimedia.objects.filter(bloc=self)

class Multimedia(models.Model):
    """docstring for Multimedia"""

    DRAFT = 'D'
    PUBLISHED = 'P'
    FILE = 'F'
    VIDEO = 'V'
    AUDIO = 'A'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    CATEGORIES = (
    	(FILE, 'File'),
    	(VIDEO, 'Video'),
    	(AUDIO, 'Audio'),
    )
    multimedia_link = models.FileField(upload_to="media/")
    title = models.CharField(blank=False, max_length=500)
    slug = AutoSlugField(populate_from='title')
    categorie = models.CharField(max_length=1, choices=CATEGORIES, default=VIDEO)
    bloc =  models.ForeignKey(CategorieMedia)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = _("Multimedia")
        verbose_name_plural = _("Multimedias")
        ordering = ("title",)


    @staticmethod
    def get_published():
        videos = Multimedia.objects.filter(status=Multimedia.PUBLISHED)
        return videos

    @staticmethod
    def get_videos():
    	videos = Multimedia.objects.filter(categorie=Multimedia.VIDEO)
    	return videos

    @staticmethod
    def get_files():
    	files = Multimedia.objects.filter(categorie=Multimedia.FILE)
    	return files

    @staticmethod
    def get_audios():
    	audios = Multimedia.objects.filter(categorie=Multimedia.AUDIO)
    	return audios


    def get_comments(self):
        return MultimediaComment.objects.filter(multimedia=self)

    

@python_2_unicode_compatible
class MultimediaComment(models.Model):
    multimedia = models.ForeignKey(Multimedia)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _("Multimedia Comment")
        verbose_name_plural = _("Multimedia Comments")
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.multimedia.title)

    def get_comment_as_markdown(self):
        return markdown.markdown(self.comment, safe_mode='escape')
