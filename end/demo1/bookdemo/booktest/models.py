from django.db import models


# Create your models here.

# 每一张表就是一个模型类

class Book(models.Model):
    """
    book继承了Model类 应为Model类拥有操作数据库的功能
    """
    title = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    pub_date = models.DateField(default="1983-06-01")

    def __str__(self):
        return self.title


class Hero(models.Model):
    """
    hero继承了model 也可以操作数据库
    """
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='male')
    content = models.CharField(max_length=100)
    # book 是一对多的外键 on_delete代表删除主表数据时如何做
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="heros")

    def __str__(self):
        return self.name


class UserManager(models.Manager):
    """
    自定义模型管理类  该模型不再具有objects对象
    """

    def deleteByTelrPhone(self, tele):
        # django默认的objects 是Manager类型  *.objects.get()
        user = self.get(telephone=tele)
        user.delete()

    def createUser(self, tele):
        # self.model 可以获取模型类
        user = self.model()
        user.telephone = tele
        user.save()


class User(models.Model):
    telephone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    # 自定义过管理字段之后不在有objects  自定义了一个新的objects
    objects = UserManager()

    def __str__(self):
        return self.telephone

    class Meta:
        # 表明
        db_table = "用户类"
        ordering = ["-telephone"]
        # admin页面进入模型类显示名字
        verbose_name = "用户模型类a"
        # admin页面在应用下方显示的模型名
        verbose_name_plural = "用户模型类s"


class Account(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    regist_date = models.DateField(auto_now_add=True, verbose_name="注册日期")
    # concact = models.OneToOneField('Concact',on_delete=models.CASCADE)


class Concact(models.Model):
    telephone = models.CharField(max_length=11, verbose_name="手机号")
    email = models.EmailField(default="1542819432@qq.com")
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="con")


class Article(models.Model):
    title = models.CharField(max_length=20, verbose_name="标题")
    sumary = models.TextField(verbose_name="正文")


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="标签名")
    articles = models.ManyToManyField(Article,related_name="tags")


# 一对多   一方Book  实例b  多方Hero  实例h    关系字段定义在多方
# 一找多    b.hero_set.all()    如果定义过related_name='heros' 则使用  b.heros.all()
# 多找一   h.book

# 一对一   一方Account  实例a   一方Concact 实例c   关系字段定义在任意一方
# a 找 c  a.concact
# c 找 a  c.account

# 多对多  多方Article  实例a    多方Tag 实例t   关系字段可以定义在任意一方
# 添加关系   t.articles.add(a)    移除关系  t.articles.remove(a)
# a 找 所有的 t   a.tag_set.all()   如果定义过related_name='tags' 则使用 a.tags.all()
# t 找 所有的 a   t.articles.all()