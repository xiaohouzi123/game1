from django.db import models

'''
    User
        \
         UserRoleRelation
        /
    Role
        \
         RolePermRelation
        /
    Permission
'''


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

    def roles(self):
        relations = UserRoleRelation.objects.filter(uid=self.id).only('role_id')
        role_id_list = [r.role_id for r in relations]
        return Role.objects.filter(id__in=role_id_list)

    def perms(self):
        role_relations = UserRoleRelation.objects.filter(uid=self.id).only('role_id')
        role_id_list = [r.role_id for r in role_relations]
        perm_relations = RolePermRelation.objects.filter(role_id__in=role_id_list).only('perm_id')
        perm_id_list = [r.perm_id for r in perm_relations]
        return Permission.objects.filter(id__in=perm_id_list)

    def add_role(self, role_name):
        role = Role.objects.get(name=role_name)
        UserRoleRelation.add_relation(self.id, role.id)

    def del_role(self, role_name):
        role = Role.objects.get(name=role_name)
        UserRoleRelation.del_relation(self.id, role.id)

    def has_perm(self, perm_name):
        '''检查是否具有某种权限'''
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False


class UserRoleRelation(models.Model):
    uid = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_relation(cls, uid, role_id):
        cls.objects.get_or_create(uid=uid, role_id=role_id)

    @classmethod
    def del_relation(cls, uid, role_id):
        cls.objects.filter(uid=uid, role_id=role_id).delete()


class Role(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def add_perm(self, perm_name):
        perm = Permission.objects.get(name=perm_name)
        RolePermRelation.add_relation(self.id, perm.id)

    def del_perm(self, perm_name):
        perm = Permission.objects.get(name=perm_name)
        RolePermRelation.del_relation(self.id, perm.id)

    def perms(self):
        relations = RolePermRelation.objects.filter(role_id=self.id).only('perm_id')
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)


class RolePermRelation(models.Model):
    '''
    角色与权限的关系

        角色      权限
        ================
        老板
                查看工资
                查看财务报表
                批假

        总监
                查看工资
                查看财务报表
                批作业
                批假

        财务
                查看工资
                发工资
                查看财务报表

        讲师
                批作业
                批假
    '''
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_relation(cls, role_id, perm_id):
        cls.objects.get_or_create(role_id=role_id, perm_id=perm_id)

    @classmethod
    def del_relation(cls, role_id, perm_id):
        cls.objects.filter(role_id=role_id, perm_id=perm_id).delete()


class Permission(models.Model):
    '''
    权限类型
        add_post       添加帖子
        del_post       删除帖子
        add_comment    发表评论
        del_comment    删除评论
        del_user       删除用户
    '''
    name = models.CharField(max_length=16, unique=True)
