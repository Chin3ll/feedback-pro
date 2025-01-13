from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sorting_feedback.urls')),  # Include app's URLs
    path('', include('accounts.urls')),
]
