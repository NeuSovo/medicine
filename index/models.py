from django.db import models
from simditor.fields import RichTextField

# Create your models here.


class LunBo(models.Model):

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"
        ordering = ['-id']

    def __str__(self):
        return self.title or 'null'
    
    title = models.CharField(verbose_name='标题', max_length=50, null=True, blank=True)
    img = models.ImageField(verbose_name='图片', default='img/demo.jpg', upload_to="img")
    vurl = models.URLField(verbose_name='视频地址', null=True, blank=True)


class Index(models.Model):
    class Meta:
        verbose_name = "首页"
        verbose_name_plural = "首页"
        ordering = ['-id']

    title = models.CharField(verbose_name='标题', max_length=50)
    img = models.ImageField(verbose_name='图片', default='img/demo.jpg', upload_to='img')
    summary = RichTextField(verbose_name='简介', null=True, blank=True)

