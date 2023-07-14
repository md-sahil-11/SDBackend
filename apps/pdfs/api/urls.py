from rest_framework.routers import DefaultRouter

from . import views

app_name = "pdf-management"

router = DefaultRouter(trailing_slash=False)

router.register("pdfs", views.PdfViewSet, basename="pdfs")
router.register("pdf-members", views.PdfMemberViewSet, basename="pdf-members")
router.register("comments", views.CommentViewSet, basename="comments")
router.register("replies", views.CommentReplyViewSet, basename="replies")

urlpatterns = router.urls
