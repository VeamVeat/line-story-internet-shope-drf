from django.contrib import admin
from django.urls import path
from django.utils.safestring import mark_safe

from products.models import File
from users.forms import ProfileAdminForm
from users.models import User, Profile
from users.views import BlockedUserView


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'is_active', 'is_staff')
    list_display_links = ('email',)
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    # readonly_fields = ('is_blocked',)

    change_form_template = 'admin/users/custom_change_form.html'

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if extra_context is None:
            user = User.objects.get(pk=object_id)
            extra_context = {'user_id': object_id,
                             'user_image_url': user.profile.image.image.url}

        return super(UserAdmin, self).change_view(request,
                                                  object_id=object_id,
                                                  form_url=form_url,
                                                  extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<user_id>',
                 self.admin_site.admin_view(BlockedUserView.as_view()),
                 name='blocked_user'),
        ]
        return my_urls + urls


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'age', 'phone', 'image', 'region', 'balance_user')
    readonly_fields = ('balance_user', 'file_image', 'age')
    form = ProfileAdminForm

    fieldsets = (
        (None, {
            'fields': ('user', 'age', 'phone', 'region', 'balance_user', 'picture', 'file_image'),
        }),
    )

    @staticmethod
    def file_image(obj):
        file_width = 100
        file_height = 100

        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.image.url,
            width=file_width,
            height=file_height,
        )
        )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['picture'] and request.user.is_superuser:
            file = form.cleaned_data['picture']
            profile_image = File.objects.get(id=obj.image.id)
            profile_image.image = file
            profile_image.save()
        return super(ProfileAdmin, self).save_model(request, obj, form, change)
