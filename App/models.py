from django.db import models

# Create your models here.
from django.db.models import CASCADE

from App.views_constant import ORDER_STATUS_NOT_PAY


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=128)
    trackid = models.IntegerField(default=1)
    class Meta:
        abstract = True
'''
    比如第一个abstract=True这个东东，是为了继承，将该基类定义为抽象类，即不必生成数据库表单，只作为一个可以继承的基类，把一些子类必须的代码放在基类，避免重复代码也避免重复录入数据库。大概是这么个意思吧？

   再比如db_table='xxxx'这个东东更简单些，其实就是指定该类的数据库表单名字。当然如果不指定也没关系，Django会自动默认的按照一定规则生成数据模型对应的数据库表名。至于合不合你的意那就得看缘分了，所以自己指定往往比较好。

    又比如ordering=‘xxxxx’，是表示按照指定的字段进行数据库的排序。主要是为了好看好查找。你可以指定任意的表单名称或内容，数据库生成之后就会按照指定的列进行排序。还可以升序降序随机，唉反正挺复杂的。

'''



class MainWheel(Main):
    '''
    axf_wheel(img,name,trackid)
    '''

    class Meta:
        db_table = 'axf_wheel'

class MainNav(Main):
    class Meta:
        db_table = "axf_nav"

class MainMustBuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'

class MainShop(Main):
    class Meta:
        db_table = "axf_shop"

class MainShow(Main):
    categoryid = models.IntegerField(default=1)
    brandname = models.CharField(max_length=64)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField(default=1)
    productid1 = models.IntegerField(default=1)
    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField(default=1)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = "axf_mainshow"

class FoodType(models.Model):
    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_foodtype'

class Goods(models.Model):

    productid =models.IntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=1)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'

class AXFUser(models.Model):
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64)
    u_icon = models.ImageField(upload_to="icons/%Y/%m/%d/")
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_user'

class Cart(models.Model):
    c_user = models.ForeignKey(AXFUser, on_delete=models.CASCADE)
    c_goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'

class Order(models.Model):
    o_user = models.ForeignKey(AXFUser, on_delete=models.CASCADE)
    o_price = models.FloatField(default=0)
    o_time =models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=ORDER_STATUS_NOT_PAY)

    class Meta:
        db_table = 'axf_order'

class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    o_goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    o_goods_num=models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_ordergoods'
