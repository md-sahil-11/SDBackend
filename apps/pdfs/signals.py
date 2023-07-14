from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.pdfs.models import Pdf, PdfMember
from shared.choices import NotifyActionType
from shared.notify import notify
 
 
@receiver(post_save, sender=Pdf)
def create_pdf_member(sender, instance, created, **kwargs):
    if created:
        PdfMember.objects.get_or_create(
            pdf=instance,
            user=instance.created_by,
            is_creator=True
        )


@receiver(post_save, sender=PdfMember)
def notify_invitee(sender, instance, created, **kwargs):
    if created:
        if not instance.user.is_guest:
            notify(user=instance.user, subject="You have been invited", mail_template=NotifyActionType.INVITE.value)