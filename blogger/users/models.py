from django.db import models
from django.contrib.auth.models import User
from .managers import ProfileManager
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        im = img.convert("RGB")

        if im.height > 300 or im.width > 300 :
            output_size = (300, 300)
            im.thumbnail(output_size)
            im.save(self.image.path)
