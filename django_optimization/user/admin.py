from django.contrib import admin

from user.models import User, Profile

from django.utils.html import format_html


class ProfileAdmin(admin.ModelAdmin):
    ordering = ["-id"]  # id 필드를 역순으로 정렬
    list_display = [
        "nick_name",
        "image_tag",
        "profile_desc",
    ]

    def image_tag(self, obj: Profile):
        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
                obj.profile_img
            )
        )


admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
