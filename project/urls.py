from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("transactions/", include("apps.transactions.urls")),
    path("categories/", include("apps.categories.urls")),
    path("investments/", include("apps.investments.urls")),
    path("metas/", include("apps.goals.urls")),
    path("subscriptions/", include("apps.subscriptions.urls")),
    path('budget/', include('apps.budget.urls')),
]
