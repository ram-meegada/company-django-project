from . import views
from django.urls import path
from .views import *
urlpatterns = [
    path('api/user-registration/', UserRegistration.as_view()),
    path('api/all-company/', DisplayAllCompanies.as_view()),
    path('product/add-cart/', AddProductToCartView.as_view()),
    path('user/products-in-cart/<int:id>/', GetAllProductsInCartOfUserView.as_view()),
    path('user/cart/checkout/<int:id>/', UserCartCheckoutView.as_view()),
    path('user/place-order/<int:id>/', UserPlaceOrderView.as_view()),
    path('productnew/add-cart/', UserAddProductToCart1ViewNew.as_view()),
    path('usernew/products-in-cart/<int:id>/', NewGetAllProductsInCartOfUserView.as_view()),
    path('user/cart1/checkout/<int:id>/', UserCart1CheckOut.as_view()),
    path('user/cart1/place-order/<int:id>/', NewUserPlaceOrderView.as_view()),
    path('owner/roleandpermission/', RoleAndPermissionView.as_view()),
    path('owner/allroleandpermission/', GetAllRolesAndPermissions.as_view()),
    path('sendmail/', SendMail.as_view()),
    path('owner/jsonrolesandpermission/', OwnerAddRolesPermJson.as_view()),
    path('owner/alljsonrolesandpermission/', GetAllJsonRolesAndPermission.as_view()),
    path('user/add-products-jsoncart/', AddProductToJsonCart.as_view()),
    path('user/all-products-jsoncart/<int:id>/', GetAllProductsInJsonCart.as_view()),
    path('user/jsoncartcheckout/<int:id>/', UserCartCheckoutView.as_view()),
    path('user/jsonplaceorder/<int:id>/', UserJsonPlaceOrderView.as_view()),
    path('alldescription/', GetAllDescriptionsView.as_view()),
    path('allusers/', GetAllUsersView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('all-parents/', GetAllParentsView.as_view()),
    path('all-children/', GetAllChildrenView.as_view()),

]