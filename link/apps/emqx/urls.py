from django.urls import path

from emqx.views.acl import check_alc
from emqx.views.auth import check_auth
from emqx.views.hooks import hooks

urlpatterns = [
    path("emqx/acl/", check_alc, name="emqx_acl"),
    path("emqx/auth/", check_auth, name="check_auth"),
    path("emqx/hooks/", hooks, name="hooks"),
]
