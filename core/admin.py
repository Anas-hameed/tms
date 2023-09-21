"""This module register model to admin page and add display, filtering customizations"""

from django.contrib import admin

from core.models import (
    User,
    UserProfile,
    TrainingPlan,
    Invite,
    Enrolment,
    Module,
    Task,
)


class UserProfileInline(admin.StackedInline):
    """Inline for user Profile to allow inline insertion"""

    model = UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User model custimzation on the admin page"""

    list_display = [
        'id',
        'username',
        'email',
        'is_superuser',
        'role',
    ]
    fields = [
        'username',
        'email',
        'password',
        'role',
    ]
    empty_value_display = 'unknown'
    list_filter = [
        ('is_active', admin.BooleanFieldListFilter),
        ('is_superuser', admin.BooleanFieldListFilter),
    ]
    inlines = [
        UserProfileInline,
    ]
    search_fields = [
        'email',
        'username',
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """This is custimzation display for the direction table"""

    list_display = [
        'gender',
        'bio',
        'profile_image',
        'user',
    ]


@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    """admin panel custimzation for the training plan"""

    list_display = [
        'id',
        'name',
        'description',
        'create_date',
        'duration',
        'creater',
    ]


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    """admin panel custimzation for the invite"""

    list_display = [
        'id',
        'email',
        'invite_date',
        'training_id',
        'inviter',
        'invitee',
    ]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """admin panel custimzation for the invite"""

    list_display = [
        'id',
        'name',
        'descrption',
        'attactment_link',
        'create_date',
        'training_plan',
    ]


admin.site.register(Enrolment)
admin.site.register(Task)
