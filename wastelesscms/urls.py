from coderedcms import admin_urls as crx_admin_urls
# from coderedcms import search_urls as crx_search_urls  # Comment out
from coderedcms import urls as crx_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from wagtail.documents import urls as wagtaildocs_urls
from website import views as website_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    path("docs/", include(wagtaildocs_urls)),
    
    # Replace default search with AI search
    path("search/", website_views.ai_powered_search, name='crx_search'),  # Use crx_search name
    
    path("", include(crx_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
