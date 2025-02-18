from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sorting_feedback.views import custom_404_view, custom_500_view

handler404 = 'sorting_feedback.views.custom_404_view'
handler500 = 'sorting_feedback.views.custom_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sorting_feedback.urls')),  # Include app's URLs
    path('', include('accounts.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 