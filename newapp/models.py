from userapp.models import Profile

from django.db import models
import uuid

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner_project', null=True, blank=True)
    tag = models.ManyToManyField("Tag", blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to="mypics/", 
                                    default="/mypics/default.jpg")
    demo_link = models.URLField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)
        
    def __str__(self):
        return self.title

    def get_reviews(self):
        reviews = self.review_project.all(
        ).values_list('owner__id', flat=True)
        return reviews
    
    def get_tag(self):
        return self.tag.all()

    @property
    def featuredImageUrl(self):
        try:
            img = self.featured_image.url
        except:
            img = ''
        return img

    @property
    def getVote(self):
        reviews = self.review_project.all()
        upvotes = reviews.filter(value="UP").count()
        totalvotes = reviews.count()

        ratio = (upvotes/totalvotes) * 100
        
        self.vote_total = totalvotes
        self.vote_ratio = ratio
        print(ratio)
        print(self.vote_ratio)
        
        self.save()

class Review(models.Model):

    VOTE = (
        ("UP", "up"),
        ("DOWN", "down")
    )
    # owner
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, 
                            unique=True, editable=False)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, 
                                    related_name="review_project")
    body = models.TextField(blank=True, null=False)
    value = models.CharField(max_length=5, choices=VOTE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('owner','project'))
        
    def __str__(self):
        return self.value

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, 
        unique=True, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
