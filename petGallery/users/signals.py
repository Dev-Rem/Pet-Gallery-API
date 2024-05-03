from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from posts.models import SavePost


@receiver(post_save, sender=CustomUser)
def create_save_post_obj_after_user_registered(sender, instance, created, **kwargs):
    if created:
        SavePost.objects.create(user=instance)
        print("New instance of MyModel created:", instance)
