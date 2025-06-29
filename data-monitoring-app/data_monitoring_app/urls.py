from django.contrib import admin
from django.urls import path
from .views.rule_views import rule_list, toggle_rule, add_rule, delete_rule, edit_rule
from .views.home_view import home
from .views.alert_views import alert_list, past_alerts, clear_alerts, clear_past_alerts
from .views.search_view import view_and_search_tables, view_table_data, search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('rules/', rule_list, name='rule_list'),
    path('rules/toggle/<str:rule_name>/', toggle_rule, name='toggle_rule'),
    path('rules/add/', add_rule, name='add_rule'),
    path('rules/delete/<str:rule_name>/', delete_rule, name='delete_rule'),
    path('alerts/', alert_list, name='alert_list'),
    path('alerts/past/', past_alerts, name='past_alerts'),
    path('search/', search_view, name='search'),
    path('tables/', view_and_search_tables, name='view_and_search_tables'),
    path('tables/<str:schema>/<str:table>/', view_table_data, name='view_table_data'),
    path('alerts/clear/', clear_alerts, name='clear_alerts'),
    path('alerts/past/clear/', clear_past_alerts, name='clear_past_alerts'),
    path('rules/edit/<str:rule_name>/', edit_rule, name='edit_rule'),
]