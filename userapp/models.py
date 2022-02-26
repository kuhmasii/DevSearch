from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

class Profile(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                            unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profilepics/', blank=True, null=True,
        default="mypics/default.jpg")
    social_github = models.URLField(blank=True, null=True)
    social_twitter= models.URLField(blank=True, null=True)
    social_linkedin = models.URLField(blank=True, null=True)
    social_youtube = models.URLField(blank=True, null=True)
    social_website = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)
    
    
    def __str__(self):
        return self.user.username

    def get_skills(self):
        return self.profile_skills.all()
    
    def get_skill(self, skill_ids):
        return self.profile_skills.get(id=skill_ids)
    
    def get_projects(self):
        return self.owner_project.all()

    def get_project(self, detail_id):
        return self.owner_project.get(id=detail_id)
    
    @property
    def profileURL(self):
        try:
            img = self.profile_pic.url
        except:
            img = ''
        return img
    
class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                        primary_key=True, editable=False)
    profile = models.ForeignKey(Profile,
     on_delete=models.CASCADE, related_name="profile_skills")
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)    

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name