from django.db import models


class ProfileQuerySet(models.QuerySet):
    def get_users_follows(self, user):
        return self.filter(followed_by__user__username=user)

    def get_users_following_me(self, user):
        return self.filter(follows__user__username=user)

    def is_following(self, toggle_user, user):
        following_list = self.filter(followed_by__user__username=user)
        if following_list.filter(user__username=toggle_user).exists():
            return True
        else:
            return False


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def get_users_follows(self, user):
        return self.get_queryset().get_users_follows(user)

    def get_users_following_me(self, user):
        return self.get_queryset().get_users_following_me(user)

    def is_following(self, toggle_user, user):
        return self.get_queryset().is_following(toggle_user, user)
