from django.db import models

from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    hit = models.IntegerField(default=0)
    reg_date = models.DateTimeField(auto_now=True)
    group_no = models.CharField(max_length=20, default=0)
    order_no = models.CharField(max_length=20, default=1)
    depth = models.CharField(max_length=20, default=0)
    img_ori_name = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return f'Board({self.title}, {self.contents}, {self.hit}, {self.reg_date}, {self.order_no}, {self.depth}, {self.img_ori_name}, {self.img_url}, {self.user})'
