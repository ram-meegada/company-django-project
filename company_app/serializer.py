from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    company_unpck = serializers.SerializerMethodField()
    user_role_unpck = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','email','company','company_unpck','user_role','user_role_unpck']
    def get_company_unpck(self, obj):
        try:
            return obj.company.company_name
        except:
            return None
    def get_user_role_unpck(self, obj):
        try:
            return obj.get_user_role_display()
        except:
            return None
        


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','company_name']

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_name', 'product_price']
    def get_product_name(self, obj):
        try:
            return obj.product.product_name
        except:
            return None
    def get_product_price(self, obj):
        try:
            return obj.product.price
        except:
            return None
        
# class PermissionSerializer(serializers.ModelSerializer):
#     add_product_permission = serializers.BooleanField()
#     edit_product_permission = serializers.BooleanField()
#     mark_product_obselete_permission = serializers.BooleanField()
#     change_company_info_permission = serializers.BooleanField()
#     view_order_status_permission = serializers.BooleanField()
#     buy_products_permission = serializers.BooleanField()
#     write_reviews_permission = serializers.BooleanField()
#     change_shipping_address = serializers.BooleanField()
#     name_of_role = serializers.SerializerMethodField()
#     class Meta:
#         model = Permission
#         fields = ['id', 'role', 'name_of_role', 'add_product_permission', 'edit_product_permission', 'mark_product_obselete_permission',
#                   'change_company_info_permission', 'view_order_status_permission', 'buy_products_permission',
#                   'write_reviews_permission', 'change_shipping_address']
#     def get_name_of_role(self, obj):
#         try:
#             return obj.role.role_name
#         except:
#             return None

class PermissionSerializer(serializers.ModelSerializer):
    permissions_given = serializers.ListField(child=serializers.IntegerField(min_value=None, max_value=None))
    # permission_given = serializers.BooleanField()
    class Meta:
        model = RoleAndPermission
        fields = ['id', 'role', 'permissions_given']

class SendMailSerializer(serializers.ModelSerializer):
    email = serializers.ListField(child=serializers.EmailField())
    class Meta:
        model = SendMail
        fields = ['id', 'subject', 'content', 'email']

# class AllRolePermissionSerializer(serializers.ModelSerializer):
#     role_name = serializers.SerializerMethodField()
#     class Meta:
#         model = RoleAndPermission
#         fields = ['id', 'role', 'role_name']
#     def get_role_name(self, obj):
#         try:
#             return obj.role.role_name
#         except:
#             return None

class JsonRolePermSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAndPermissionjson
        fields = ['id', 'rolesandpermissions']

class AddProductToJsonCartSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    user_cart_details = serializers.SerializerMethodField()
    class Meta:
        model = CartJson
        fields = ['id', 'user', 'full_name','user_cart_details']
    def get_full_name(self, obj):
        try:
            return obj.user.full_name
        except:
            return None
    def get_user_cart_details(self, obj):
        temp = obj.user_cart
        ans = {}
        num = 1
        for i in temp:
            ans[f"product{num}"] = Product.objects.get(id=int(i)).product_name
            ans[f"quantity of product{num}"] = temp[i]
            ans[f"price of the product{num}"] = Product.objects.get(id=int(i)).price
            num += 1
        return ans    
    
class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionModel
        fields = ['id', 'user', 'description']

class AllUserSerializer(serializers.ModelSerializer):
    # descriptions = DescriptionSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildrenModel
        fields = ['id', 'child_name', 'child_parent']               

class ParentSerializer(serializers.ModelSerializer):
    children = ChildrenSerializer(many=True)
    class Meta:
        model = ParentModel
        fields = ['id', 'parent_name', 'children', 'children']