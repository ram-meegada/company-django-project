from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from django.http import Http404
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from .helpers import *
from company_project import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.permissions import AllowAny
import ast

class UserRegistration(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        email = request.data.get('email')
        company = request.data.get('company')
        password = make_password(request.data.get('password'))
        try:
            usr = User.objects.get(email=email)
            return Response({"message":"email already existed"})
        except:
            checking = email[email.index("@")+1:email.index(".")]
            com_name = Company.objects.filter(company_name = checking)
            users_com = User.objects.filter(company_id=company)
            if checking != Company.objects.filter(id = company).first().company_name:
                return Response({"message":"Mail doesn't belongs to your selected company"})
            if com_name:
                if not users_com:
                    crt = User.objects.create(email=email, company_id=company, user_role=1, password=password)
                    items = User.objects.filter(email=crt.email)
                    serializer = self.serializer_class(items[0])
                    return Response({"data":serializer.data},status=status.HTTP_200_OK)
                elif users_com:
                    crt = User.objects.create(email=email, company_id=company, user_role=2, password=password)
                    items = User.objects.filter(email=crt.email)
                    
                    serializer = self.serializer_class(items[0])
                    return Response({"data":serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"message":"There is no such company existed"})

class DisplayAllCompanies(APIView):
    serializer_class = CompanySerializer
    def get(self, request):
        all_companies = Company.objects.all()
        serializer = self.serializer_class(all_companies, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class AddProductToCartView(APIView):
    def post(self, request):
        user = request.data.get("user")
        product = request.data.get("product")
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response({"data": serialized_data}, status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)     
    
class GetAllProductsInCartOfUserView(APIView):
    def get(self, request, id):
        all_products = Cart.objects.filter(user_id = id)
        serializer = CartSerializer(all_products, many=True)
        serialized_data = serializer.data
        return Response({"data": serialized_data, "code":status.HTTP_200_OK})

class UserCartCheckoutView(APIView):
    def get(self, request, id):
        all_products = Cart.objects.filter(user_id = id)
        serializer = CartSerializer(all_products, many=True)
        serialized_data = serializer.data
        price_details = self.display_price_details(all_products)
        return Response({"Price_details":price_details ,"code":status.HTTP_200_OK})
    def display_price_details(self, x):
        lst = []
        total = 0
        for i in x:
            lst.append((i.product.product_name, i.product.price))
            total += i.product.price
        lst.append(("Total", total))
        return lst

class UserPlaceOrderView(APIView):
    def delete(self, request, id):
        all_products = Cart.objects.filter(user_id = id).delete()
        return Response({"data":None, "code":status.HTTP_204_NO_CONTENT})

class UserAddProductToCart1ViewNew(APIView):
    def post(self, request):
        user = request.data["user"],
        product =  request.data.get("product")
        items = Cart1.objects.all()
        if not items:
            crt = Cart1.objects.create(user_ordered_items={user[0]:[product]})
        elif items and str(user[0]) not in items[0].user_ordered_items:
            items[0].user_ordered_items[str(user[0])] = [product]    
            items[0].save()
        elif items and str(user[0]) in items[0].user_ordered_items:
            items[0].user_ordered_items[str(user[0])].append(product)
            items[0].save()
        return Response({"data": None, "code":status.HTTP_201_CREATED})
    
class NewGetAllProductsInCartOfUserView(APIView):
    def get(self, request, id):
        items = Cart1.objects.all()
        user = User.objects.get(id=id).email
        data = [('user_mail', user)]
        for i in items[0].user_ordered_items[str(id)]:
            x = Product.objects.get(id=i)
            data.append({"product_name": x.product_name, "product_price": x.price})
        return Response(data, status=status.HTTP_200_OK)    
    
class UserCart1CheckOut(APIView):
    def get(self, request, id):
        items = Cart1.objects.all()[0].user_ordered_items[str(id)]
        price_details = self.show_price_details(items)
        return Response({"price_details":price_details, "code":status.HTTP_200_OK})
    def show_price_details(self, items):
        lst = []
        total = 0
        for i in items:
            temp = Product.objects.get(id=i)
            lst.append((temp.product_name, temp.price))
            total += temp.price
        lst.append(("Total", total))
        return lst

class NewUserPlaceOrderView(APIView):
    def delete(self, request, id):
        item = Cart1.objects.all()[0]
        del item.user_ordered_items[str(id)]
        item.save()
        return Response({"data":None, "code":status.HTTP_204_NO_CONTENT})

# class RoleAndPermissionView(APIView):
#     def post(self, request):
#         role = request.data.get('role')
#         add_product_permission = request.data.get('role_name')
#         edit_product_permission = request.data.get('edit_product_permission')
#         mark_product_obselete_permission = request.data.get('mark_product_obselete_permission')
#         change_company_info_permission = request.data.get('change_company_info_permission')
#         view_order_status_permission = request.data.get('view_order_status_permission')
#         buy_products_permission = request.data.get('buy_products_permission')
#         write_reviews_permission = request.data.get('write_reviews_permission')
#         change_shipping_address = request.data.get('change_shipping_address')
#         serializer = PermissionSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             serialized_data = serializer.data
#             return Response({"data": serialized_data, "code": status.HTTP_201_CREATED})
#         return Response({"message": serializer.errors, "code": status.HTTP_400_BAD_REQUEST})
    
# class GetAllRolesAndPermissions(APIView):
#     def get(self, request):
#         rolespermissions = Permission.objects.all()
#         serializer = PermissionSerializer(rolespermissions, many=True)
#         serialized_data = serializer.data
#         return Response({"data": serialized_data, "code":status.HTTP_200_OK})

class RoleAndPermissionView(APIView):
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response({"data":serialized_data, "code":status.HTTP_201_CREATED})
        return Response({"message":serializer.errors, "code":status.HTTP_400_BAD_REQUEST})
    
class GetAllRolesAndPermissions(APIView):
    def get(self, request):
        items = RoleAndPermission.objects.all()
        all_roles_permissions = self.display_roles_permissions(items)
        return Response({"data":all_roles_permissions, "code":status.HTTP_200_OK})
    def display_roles_permissions(self, items):
        all_roles_permissions = {}
        for i in items:
            lst = []
            for j in i.permissions_given:
                lst.append(Permission.objects.get(id=j).permission_name)
            all_roles_permissions[Role.objects.get(id=i.role_id).role_name] = lst
        return all_roles_permissions
    
class SendMail(APIView):
    def post(self, request):
        subject = request.data.get("subject")
        content = request.data.get("content")
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            self.mail(serialized_data)
            return Response({"data":serialized_data, "code":status.HTTP_201_CREATED})
        return Response({"message":serializer.errors, "code":status.HTTP_400_BAD_REQUEST})
    def mail(self, serialized_data):
        email = "stefenwarner13@gmail.com"
        context = {"subject":serialized_data["subject"],"content":serialized_data["content"]}
        body_msg = render_to_string ('email/contentmail.html', context)
        msg = EmailMultiAlternatives ("Checking purpose", body_msg, settings.DEFAULT_FROM_EMAIL, serialized_data["email"])
        msg.content_subtype = "html"
        msg.send()

class OwnerAddRolesPermJson(APIView):
    def post(self, request):
        items = RoleAndPermissionjson.objects.all().first()
        if items == None:
            serializer = JsonRolePermSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response({"data": serialized_data, "code":status.HTTP_201_CREATED})
            return Response({"message": serializer.errors, "code":status.HTTP_400_BAD_REQUEST})
        else:
            serializer = JsonRolePermSerializer(items, data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response({"data": serialized_data, "code":status.HTTP_201_CREATED})
            return Response({"message": serializer.errors, "code":status.HTTP_400_BAD_REQUEST})

class GetAllJsonRolesAndPermission(APIView):
    def get(self, request):
        items = RoleAndPermissionjson.objects.all().first()
        roles_permissions = self.get_all_rol_perm(items)
        return Response({"given permissions":roles_permissions, "code":status.HTTP_200_OK})
    def get_all_rol_perm(self,items):
        all_roles_permissions = {}
        for i in items.rolesandpermissions:
            permissions = []
            for j in items.rolesandpermissions[i]:
                permissions.append(Permission.objects.get(id=j).permission_name)
            all_roles_permissions[Role.objects.get(id=int(i)).role_name] = permissions 
        return all_roles_permissions          

# class AddProductToJsonCart(APIView):
#     def post(self, request):
#         user = request.data.get("user")
#         product = request.data.get("product")
#         quantity = request.data.get("quantity")
#         orders = CartJson.objects.all().first()
#         x = ast.literal_eval(orders.user_cart)
#         if orders == None:
#             user_orders, productandquantity = {}, {}
#             productandquantity[product] = quantity
#             user_orders[user] = productandquantity
#             crt = CartJson.objects.create(user_id=user,user_cart = user_orders)
#             return Response({"data":"done", "code":status.HTTP_201_CREATED})
#         elif orders is not None and x.get(user) is not None:
#             x[user][product] = quantity
#             orders.user_cart = x
#             orders.save()
#             return Response({"data":"done", "code":status.HTTP_201_CREATED})
#         elif orders is not None and x.get(user) is None:
#             x[user] = {}
#             x[user][product] = quantity
#             orders.user_cart = x
#             orders.save()
#             return Response({"data":"done", "code":status.HTTP_201_CREATED})
#         return Response({"code":status.HTTP_400_BAD_REQUEST})

class AddProductToJsonCart(APIView):
    def post(self, request):
        user = request.data["user"]
        product =  request.data.get("product")
        quantity = request.data.get("quantity")
        prd = Product.objects.get(id=product)
        x = prd.stock
        if x-quantity < 0:
            return Response({"message":f"There are only {prd.stock} left in stock"})
        prd.stock = x-quantity
        prd.save()
        try:
            item = CartJson.objects.get(user_id=user)
            if str(product) in item.user_cart:
                item.user_cart[str(product)] += quantity
            else:        
                item.user_cart[str(product)] = quantity
            item.save()
            return Response({"message":"done", "code":status.HTTP_200_OK}) 
        except:
            crt = CartJson.objects.create(user_id=user, user_cart={product:quantity})
            return Response({"message":"done", "code":status.HTTP_201_CREATED})

class GetAllProductsInJsonCart(APIView):
    def get(self, request, id):
        items = CartJson.objects.get(user_id=id)
        serializer = AddProductToJsonCartSerializer(items)
        serialized_data = serializer.data
        return Response({"data":serialized_data, "code":status.HTTP_200_OK})    
    
class UserCartCheckoutView(APIView):
    def get(self, request, id):
        item = CartJson.objects.get(user_id=id)
        price_details = self.display_price_details(item)
        return Response({"Your Order": price_details[0], "Price Details":price_details[1], "Total":price_details[2], "code":status.HTTP_200_OK})
    def display_price_details(self,item):
        lst = []
        lst1 = []
        total = 0
        num = 1
        for i in item.user_cart:
            x = Product.objects.get(id = int(i))
            lst.append({"product":x.product_name, "quantity":item.user_cart[i], "total price":item.user_cart[i]*x.price}) 
            lst1.append({f"Booking Amount Product{num}":item.user_cart[i]*x.price})
            num += 1
            total += item.user_cart[i]*x.price
        return (lst, lst1, total)

class UserJsonPlaceOrderView(APIView):
    def delete(self, request, id):
        item = CartJson.objects.get(user_id=id)
        item.delete()
        return Response({"data":None, "code":status.HTTP_204_NO_CONTENT})
    
class GetAllDescriptionsView(APIView):
    def get(self, request):
        desc = DescriptionModel.objects.all()
        serializer = DescriptionSerializer(desc, many=True)
        serialized_data = serializer.data
        return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"All Records"})    
    
class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data['email']
        password= request.data['password']
        try:
            user= User.objects.get(email=email)
            chk_pwd = check_password(password, user.password)
            if chk_pwd:
                token = RefreshToken.for_user(user)
                data = {"user":user.full_name,"access_token":str(token.access_token),"refresh_token":str(token)}
                return Response({"data":data})
            else:
                data = {"user":user.full_name,'message':"wrong password"}
                return Response(data)
        except:
            data = {"user":"no user found"}
            return Response(data)

class GetAllUsersView(APIView):
    def get(self, request):
        print(request.user, "===============================")
        try:
            user = User.objects.get(email=request.user)
            if user.role == 1:
                users = User.objects.all()
                serializer = AllUserSerializer(users, many=True)
                serialized_data = serializer.data
                return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"All records"})    
            else:
                return Response({"data":None, "code":status.HTTP_403_FORBIDDEN, "message":"You don't have permission to access this api"})
        except:
            return Response({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"user details not found"})
     
class GetAllParentsView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        all_parents = ParentModel.objects.all()
        serializer = ParentSerializer(all_parents, many=True)
        serialized_data = serializer.data
        return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"All Parent details successfully fetched"})
    
class GetAllChildrenView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        all_parents = ChildrenModel.objects.all()
        serializer = ChildrenSerializer(all_parents, many=True)
        serialized_data = serializer.data
        return Response({"data":serialized_data, "code":status.HTTP_200_OK, "message":"All Children details successfully fetched"})