from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男'),
        ('F', '女'),
        ('U', '保密'),
    )

    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    sex = models.CharField(max_length=8, choices=SEX)
    age = models.IntegerField()
    perm_id = models.IntegerField()

    @property
    def perm(self):
        if not hasattr(self, '_perm'):
            self._perm = Permission.objects.get(id=self.perm_id)
        return self._perm

    def has_perm(self, perm_name):
        '''检查是否具有某种权限'''
        need_perm = Permission.objects.get(name=perm_name)
        return self.perm.level >= need_perm.level


class Permission(models.Model):
    name = models.CharField(max_length=16)
    level = models.IntegerField()
