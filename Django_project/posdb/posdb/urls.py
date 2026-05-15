# posdb/urls.py (Update សម្រាប់ Bonus Challenge 6)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings # បន្ថែមថ្មី
from django.conf.urls.static import static # បន្ថែមថ្មី

urlpatterns = [
    path('',           RedirectView.as_view(url='/accounts/login/'), name='home'),
    path('admin/',     admin.site.urls),
    path('sales/',     include('sales.urls')),
    path('accounts/',  include('django.contrib.auth.urls')),
]

# បន្ថែមផ្នែកខាងក្រោមនេះ ដើម្បីឱ្យប្រព័ន្ធអាចបង្ហាញរូបភាពទំនិញបាន
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)