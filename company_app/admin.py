from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_name",)

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields':('email', 'password')})
fields[1] = ('Personal Info', {'fields':('first_name', 'last_name', 'full_name')})
UserAdmin.fieldsets = tuple(fields)
class UserAdmin(UserAdmin):
    fieldsets = (*UserAdmin.fieldsets,('Additional Fields',{'fields':('company','user_role', 'role')}))
    add_fieldsets = ((None, {'classes':('wide',), 'fields':('email', 'company','password1','password2')}),)
    list_display = ('email','selected_company','user_role', 'role')
    def selected_company(self, obj):
        try:
            return obj.company.company_name
        except:
            return None
    ordering = ('email',)            

class StoryAdmin(admin.ModelAdmin):
    list_display = ('story_name', 'upload_user')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'stock')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name')
    def product_name(self, obj):
        try:
            return obj.product.product_name
        except:
            return None
        
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_name',)

class RoleAndPermissionAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'permissions_given')
    def role_name(self, obj):
        try:
            return obj.role.role_name
        except:
            return None
        
class CartJsonAdmin(admin.ModelAdmin):
    list_display = ('user',)        

admin.site.register(DescriptionModel)        
admin.site.register(SendMail)
admin.site.register(Company, CompanyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RoleAndPermission, RoleAndPermissionAdmin)
admin.site.register(Cart1)
admin.site.register(RoleAndPermissionjson)
admin.site.register(CartJson, CartJsonAdmin)
admin.site.register(ParentModel)
admin.site.register(ChildrenModel)