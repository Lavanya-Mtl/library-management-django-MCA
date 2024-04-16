from django.urls import path

from .views import *
app_name='members'
urlpatterns = [
    path("", members_home,name='index'),
    path("add",add_member,name="add_member"),
    path('edit/<int:id>',edit_member,name='edit_member'),
    path('delete/<int:id>',delete_member,name='delete_member'),
    path('view/<int:id>',view_member,name='view_member'),
    path('payfine/<int:id>',pay_fine,name="pay_fine"),
    path('addpenalty/<int:id>',add_penalty,name="add_penalty"),
    path('membertobook/<int:id>',membertobook,name="member_to_book"),
]
