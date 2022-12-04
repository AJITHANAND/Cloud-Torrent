from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='user_image', default='user.png')


class torrent(models.Model):
    name = models.CharField(max_length=1000)
    size = models.IntegerField()
    downloads = models.IntegerField(default=0)
    hash = models.CharField(max_length=40)
    progress = models.FloatField(default=0)
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class Gdrive(models.Model):
    name = models.CharField(max_length=1000)
    size = models.IntegerField()
    gid = models.TextField()
    dirid = models.TextField()
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    torrentid = models.ForeignKey(torrent, on_delete=models.CASCADE)
    hash = models.CharField(max_length=40)
