from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils.timezone import now
from django_mysql.models import ListTextField
from django.db.models import IntegerField, EmailField, JSONField
# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_status = models.IntegerField(help_text="1. approved, 2. Pending, 3. Unapproved", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name = "Companie"   

class StoryDeletion(models.Manager):
    def get_queryset(self, *args, **kwargs):
        pass
        # return super.get_queryset(*args, **kwargs).filter(story_uploaded_time)   

class Story(models.Model):
    story_name = models.CharField(max_length=200)
    upload_user = models.CharField(max_length=200)
    story_uploaded_time = models.DateTimeField()
    sub_category_status = models.IntegerField(help_text="1. approved, 2. Pending, 3. Unapproved", null=True, blank=True )
    class Meta:
        verbose_name = 'Storie'

USER_ROLE_CHOICES = ((1,"CEO"), (2,"employee"), (3,None))

class User(AbstractUser):
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, default=None)
    user_role = models.IntegerField(choices=USER_ROLE_CHOICES, default=3)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="user_company")
    role = models.IntegerField(help_text="1.admin, 2.normal_user", null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField()
    description = models.TextField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Cart1(models.Model):
    user_ordered_items = models.JSONField(default=dict)   
    quantity = models.IntegerField(default=None, null=True, blank=True)

class Role(models.Model):    
    role_name = models.CharField(max_length=100)

# class Permisssion(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     add_product_permission = models.BooleanField(default=False)
#     edit_product_permission = models.BooleanField(default=False)
#     mark_product_obselete_permission = models.BooleanField(default=False)
#     change_company_info_permission = models.BooleanField(default=False)
#     view_order_status_permission = models.BooleanField(default=False)
#     buy_products_permission = models.BooleanField(default=False)
#     write_reviews_permission = models.BooleanField(default=False)
#     change_shipping_address = models.BooleanField(default=False)

class Permission(models.Model):
    permission_name = models.CharField(max_length=100)

class RoleAndPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    # permission = models.ForeignKey(Permission, on_delete=models.CASCADE)    
    # permission_given = models.BooleanField(default=False) 
    permissions_given = ListTextField(
        base_field = IntegerField(),
        default = None,
        null = True,
        blank = True,
        size=None,
    )

class SendMail(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    email =  ListTextField(
        base_field = EmailField(),
        default = None,
        null = True,
        blank = True,
        size=None,
    )

class RoleAndPermissionjson(models.Model):
    rolesandpermissions = models.JSONField(default=dict)    

class CartJson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    user_cart = models.JSONField(default=dict)

class DescriptionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)    

class ParentModel(models.Model):
    parent_name = models.CharField(max_length=255)

class ChildrenModel(models.Model):
    child_name = models.CharField(max_length=255)
    child_parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE, related_name="children")