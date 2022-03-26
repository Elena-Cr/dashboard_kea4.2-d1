"""jan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from web import views as wviews
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Loading plotly Dash apps script




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', wviews.home, name="home"),
    path('required/', wviews.required, name="required"),
    # path('', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
    # re_path('^dash_plot$', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
	# path('^django_plotly_dash/', include('django_plotly_dash.urls')),
	# re_path('', TemplateView.as_view(template_name='home_dash.html'), name='home'),
    # re_path('^django_plotly_dash/', include('django_plotly_dash.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
