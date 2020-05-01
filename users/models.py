from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # Folder profile_pics terbikin sendiri oleh django, untuk lokasi simpannya.
    # tapi kita uda ubah di settings.py, jadinya ntar dia simpan nama(sesuai kita bikin) dulu baru profile_pics

    def __str__(self): # Cara dia menampilkan, gk pake juga bisa tapi kurang yg kita inginkan
        return f'{self.user.username} Profile '

    def save(self, *args, **kwargs):  # ini bagian buat resize pictures
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)