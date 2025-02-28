from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from .views.masafa import *
router.register(r'dispatch', DispatchViewSet)
router.register(r'crossborder', CrossborderViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'item', ItemViewSet)
router.register(r'paymentdetails', PaymentdetailsViewSet)
router.register(r'service', ServiceViewSet)
router.register(r'item_group', ItemGroupViewSet)
router.register(r'vehicle', VehicleViewSet)
router.register(r'discount', DiscountViewSet)
router.register(r'supplier', SupplierViewSet)
router.register(r'employee', EmployeeViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'driver', DriverViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
