from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from .views import (AppViewSet, BulkDeleteAPIView,  ReminderViewSet,
                    ChangeLogViewSet, CreateAppAPIView, CreateDocumentAPIView,
                    CreateModuleAPIView, DataImportAPIView, DocumentViewSet,
                    GroupViewSet, LoginView, LogoutView, MigrateAPIView,
                    ModuleViewSet, OTPActivationView, PermissionViewSet,
                    ProfileView, ResendOTPView, SendEmailView, SendSmsView,
                    UserGetViewSet, UserGroupPermissions, UserIPAddressViewSet,
                    UserViewSet, RoleViewSet, BranchViewSet, PrintFormatViewSet, CreatePrintFormatAPIView,
                    AddItemToCrossborderAPIView,
                    AddItemToDispatchAPIView,
                    TransitCrossborderAPIView,
                    ItemDispatchAPIView,
                    TrackItemsView,
                    CreateInvoiceView,
                    DetailedReportView
                    )

router = DefaultRouter()
router.register(r"app", AppViewSet)
router.register(r"module", ModuleViewSet) 
router.register(r"document", DocumentViewSet)
router.register(r"print_format", PrintFormatViewSet)
router.register(r"print_formats", PrintFormatViewSet)
router.register(r"apps", AppViewSet)
router.register(r"modules", ModuleViewSet) 
router.register(r"documents", DocumentViewSet)
router.register(r"changelogs", ChangeLogViewSet)
router.register(r"users", UserViewSet)
router.register(r"core/user", UserViewSet)
router.register(r'core/reminder', ReminderViewSet) 
router.register(r'core/role_type', RoleViewSet) 
router.register(r'core/branch', BranchViewSet) 
router.register(r'core/rolegroup', GroupViewSet)
router.register(r'core/group', GroupViewSet)
router.register(r'core/permission', PermissionViewSet)
router.register(r'user-ip-addresses', UserIPAddressViewSet, basename='user-ip-addresses')



static_urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    path("", include(router.urls)),
    path("newmodule/", CreateModuleAPIView.as_view(), name="create-module"),
    path("newapp/", CreateAppAPIView.as_view(), name="create-app"),
    path("newdoc/", CreateDocumentAPIView.as_view(), name="create-document"),
    path("newprintformat/", CreatePrintFormatAPIView.as_view(), name="create-print-format"),
    path("migrate/", MigrateAPIView.as_view(), name="migrate"),
    path("login/", LoginView.as_view(), name="login"),
    path("getuser/", UserGetViewSet.as_view(), name="getuser"),
    path("otp/activate/", OTPActivationView.as_view(), name="otp_activate"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend_otp"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("roles/", UserGroupPermissions.as_view(), name="roles"),
    path("sendsms/", SendSmsView.as_view(), name="sms"),
    path("dataimport/", DataImportAPIView.as_view(), name="dataimport"),
    path("bulkdelete/", BulkDeleteAPIView.as_view(), name="bulkdelete"),
    path("sendemail/", SendEmailView.as_view(), name="email"),
    path("admin/", admin.site.urls),
    
    path("track/", TrackItemsView.as_view(), name="track"),
    path("", include(static_urlpatterns)),
    path(
        "crossborder/add-item/",
        AddItemToCrossborderAPIView.as_view(),
        name="add-item-to-crossborder",
    ),
    path(
        "crossborder/update-status/",
        TransitCrossborderAPIView.as_view(),
        name="crossborder/update-status",
    ),
    path(
        "dispatch/add-item/",
        AddItemToDispatchAPIView.as_view(),
        name="add-item-to-dispatch",
    ),
    path(
        "item/dispatch/",
        ItemDispatchAPIView.as_view(),
        name="item/dispatch/",
    ),
    path(
        "createinvoice/",
        CreateInvoiceView.as_view(),
        name="createinvoice",
    ),
     path('reports/detailed/', DetailedReportView.as_view(), name='detailed-report'),
 ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [    path('masafa/', include('masafa_app.urls')),]


