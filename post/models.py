from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comments(self):
        return Comment.objects.filter(post_id=self.id).order_by('-created')

    def tags(self):
        relations = PostTagRelation.objects.filter(post_id=self.id).only('tag_id')
        tag_id_list = [r.tag_id for r in relations]
        return Tag.objects.filter(id__in=tag_id_list)

    def update_tags(self, tag_names):
        '''更新帖子与标签的关系'''
        tag_names = set(tag_names)
        Tag.ensure_tag_name(tag_names)  # 确保传入的 tag name 在 Tag 表中存在

        old_tags = self.tags()
        old_tag_names = set(t.name for t in old_tags)

        # 创建与新 Tags 的关系
        need_add_relation_tag_names = tag_names - old_tag_names
        PostTagRelation.add_post_tags(self.id, need_add_relation_tag_names)

        # 删除不存在的关系
        need_del_relation_tag_names = old_tag_names - tag_names
        PostTagRelation.del_post_tags(self.id, need_del_relation_tag_names)


class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def user(self):
        if not hasattr(self, '_user'):
            self._user = User.objects.get(id=self.uid)
        return self._user

    @property
    def post(self):
        if not hasattr(self, '_post'):
            self._post = Post.objects.get(id=self.post_id)
        return self._post


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=16)

    def posts(self):
        relations = PostTagRelation.objects.filter(tag_id=self.id).only('post_id')
        post_id_list = [r.post_id for r in relations]
        return Post.objects.filter(id__in=post_id_list)

    @classmethod
    def ensure_tag_name(cls, tag_names):
        '''确保 tag_names 存在，不存在的创建出来'''
        exist_tags = cls.objects.filter(name__in=tag_names)
        exist_tag_names = [t.name for t in exist_tags]
        need_create_names = [name for name in tag_names if name not in exist_tag_names]
        if need_create_names:
            need_create_tags = [cls(name=name) for name in need_create_names]
            cls.objects.bulk_create(need_create_tags)


class PostTagRelation(models.Model):
    '''
        文章              标签

        念奴娇.id         宋词.id
        念奴娇.id         古典.id
        念奴娇.id         文学.id
        巡山.id          西游记.id
        巡山.id          古典.id
        巡山.id          文学.id
        巡山.id          神话.id
    '''
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    @classmethod
    def add_relation(cls, post_id, tag_id):
        '''添加 post 与 tag 的关系'''
        cls.objects.create(post_id=post_id, tag_id=tag_id)

    @classmethod
    def del_relation(cls, post_id, tag_id):
        '''删除 post 与 tag 的关系'''
        cls.objects.get(post_id=post_id, tag_id=tag_id).delete()

    @classmethod
    def add_post_tags(cls, post_id, tag_names):
        '''批量添加 post 与 tag 的关系'''
        tags = Tag.objects.filter(name__in=tag_names).only('id')
        tag_id_list = [t.id for t in tags]
        need_create_relations = [cls(post_id=post_id, tag_id=tid) for tid in tag_id_list]
        cls.objects.bulk_create(need_create_relations)

    @classmethod
    def del_post_tags(cls, post_id, tag_names):
        '''批量删除 post 与 tag 的关系'''
        tags = Tag.objects.filter(name__in=tag_names).only('id')
        tag_id_list = [t.id for t in tags]
        cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()
