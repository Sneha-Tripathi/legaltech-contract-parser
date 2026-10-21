from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("features/", views.features_view, name="features"),

    path("faq/", views.faq_view, name="faq"),

    path("upload/", views.upload_contract, name="upload"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("contracts/", views.contracts_list, name="contracts_list"),

    path(
        "result/<int:contract_id>/",
        views.result_view,
        name="result",
    ),

    path(
        "download/<int:contract_id>/",
        views.download_report,
        name="download_report",
    ),

    path(
        "delete/<int:contract_id>/",
        views.delete_contract,
        name="delete_contract",
    ),

    # ---- New Routes ----

    path(
        "risk-explorer/",
        views.risk_explorer,
        name="risk_explorer",
    ),

    path(
        "clause-explorer/",
        views.clause_explorer,
        name="clause_explorer",
    ),

    # ---- Settings & Profile ----

    path(
        "settings/",
        views.settings_view,
        name="settings",
    ),

    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),
]