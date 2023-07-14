from django.apps import AppConfig


class PdfsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pdfs'

    def ready(self) -> None:
        import apps.pdfs.signals
        return super().ready()
