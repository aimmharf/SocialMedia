from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



    
class User(AbstractUser):

    times_loggin_in = models.IntegerField(default=0, null=True)
    profile_image = models.ImageField(upload_to='images/', null=True)
    bio = models.TextField(max_length=10000000000, null=True, default=None)


    def __str__(self):
        return f'ID: {self.id}, Username: {self.username}, Email: {self.email}, First Name: {self.first_name}, Last Name: {self.last_name}'



    def serialize(self):
        return {
            "user": self.username,
            "id": self.id,
            "first_name": self.first_name,
            "last_name":self.last_name
        }
    

class Posts(models.Model):
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)
    date = models.DateTimeField()
    post = models.TextField(null=False)
    liked_users = models.ManyToManyField(User, related_name='UserLiked', null=True,  default=None)
    user = models.ForeignKey(User, related_name='userPost', on_delete=models.CASCADE, null=True)
   

    
    def __str__(self):
        return f'ID: {self.id}, From: {self.username}, Post: {self.post}, Likes: {len(self.liked_users.all())} '

    

class Follow(models.Model):
    userf = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True)
    user = models.ForeignKey(User, related_name='userfollow', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.userf} is following {self.user}"


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Userlike')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='postLike')
    def __str__(self):
        return f'{self.id}: {self.user} Liked {self.post.post}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userComment', null=True)
    comment = models.CharField(default=None, null=True, max_length=20000)
    post = models.ForeignKey(Posts, related_name='postComment', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Commented: '{self.comment}', Post: {self.post.post} "
    
    def serailize(self):
        return {
            "user": self.user.username,
            "comment": self.comment,
            "post": self.post.post
        }




   





