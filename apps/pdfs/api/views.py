from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from apps.pdfs.models import Comment, CommentLike, CommentReply, Pdf, PdfMember
from apps.pdfs.api.serializers import CommentReplySerializer, CommentSerializer, PdfMemberSerializer, PdfSerializer, CommentDetailSerializer
from apps.users.api.serializers import UserSerializer
from apps.users.models import User
from apps.users.services import add_token_to_user_serializer_selector, create_guest_user


class PdfViewSet(viewsets.ModelViewSet):
    serializer_class = PdfSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        pdf_ids = self.request.user.pdfs.all().values_list("pdf_id", flat=True)
        queryset = Pdf.objects.filter(id__in=pdf_ids)
        return queryset

    @action(
        detail=True,
        methods=["GET"],
        url_path="pdf-view"
    )
    def pdf_view(self, request, *args, **kwargs):
        pdf = self.get_object()
        try:
            return FileResponse(open(pdf.file.path, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()

    @action(
        detail=True,
        methods=["GET"],
    )
    def members(self, request, *args, **kwargs):
        pdf = self.get_object()
        member_ids = pdf.members.all().values_list("user_id", flat=True)
        users = User.objects.filter(id__in=member_ids)

        return Response(UserSerializer(users, many=True).data)
    
    @action(
        detail=True,
        methods=["GET"],
        serializer_class=CommentDetailSerializer
    )
    def comments(self, request, *args, **kwargs):
        pdf = self.get_object()
        comments = pdf.comments.all()
        data = self.serializer_class(comments, many=True).data

        return Response(data)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
        url_path="d/(?P<sharable_code>\w+)"
    )
    def access_pdf_using_link(self, request, *args, **kwargs):
        sharable_code = self.kwargs.get("sharable_code")
        pdf = get_object_or_404(Pdf, sharable_code=sharable_code)
        user = request.user
        if not user.is_authenticated:
            user = create_guest_user()
        PdfMember.objects.get_or_create(user=user, pdf=pdf)
            
        serializer = UserSerializer(user)
        data = serializer.data
        data = add_token_to_user_serializer_selector(data, user)
        return Response(data, status=status.HTTP_200_OK)

    
class PdfMemberViewSet(viewsets.ModelViewSet):
    queryset = PdfMember.objects.all()
    serializer_class = PdfMemberSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,]
    http_method_names = ["get", "post", "put", "delete"]

    def update(self, request, pk=None):
        instance = get_object_or_404(
            self.get_queryset().filter(user=request.user), pk=pk
        )
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.user:
            return Response({"detail": "Not Authorised."}, status=403)
        comment.delete()

        return Response({"success": True})

    @action(
        detail=True, methods=["PUT"], permission_classes=(permissions.IsAuthenticated,)
    )
    def like(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        if id is not None:
            CommentLike.objects.get_or_create(text_id=id, user=request.user)
        return Response({"success": True})

    @action(
        detail=True, methods=["PUT"], permission_classes=(permissions.IsAuthenticated,)
    )
    def unlike(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        if id is not None:
            if CommentLike.objects.filter(text_id=id, user=request.user).exists():
                CommentLike.objects.filter(text_id=id, user=request.user).delete()
        return Response({"success": True})


    @action(
        detail=True, methods=["GET"], permission_classes=(permissions.IsAuthenticated,)
    )
    def replies(self, request, *args, **kwargs):
        comment = self.get_object()
        replies = comment.replies.all()
        serializer = CommentReplySerializer(
            replies, many=True, context={"request": request}
        )
        return Response({"count": replies.count(), "results": serializer.data})


class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = [permissions.IsAuthenticated,]
    http_method_names = ["get", "post", "put", "delete"]

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(item, context={"request": request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(
            self.get_queryset().filter(user=request.user), pk=pk
        )
        serializer = self.serializer_class(
            instance, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user:
            return Response({"detail": "Not Authorised."}, status=403)
        instance.delete()
        return Response({"success": True})
    
    @action(
        detail=True, methods=["PUT"], permission_classes=(permissions.IsAuthenticated,)
    )
    def like(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        if id is not None:
            CommentLike.objects.get_or_create(text_id=id, user=request.user)
        return Response({"success": True})

    @action(
        detail=True, methods=["PUT"], permission_classes=(permissions.IsAuthenticated,)
    )
    def unlike(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        if id is not None:
            if CommentLike.objects.filter(text_id=id, user=request.user).exists():
                CommentLike.objects.filter(text_id=id, user=request.user).delete()
        return Response({"success": True})