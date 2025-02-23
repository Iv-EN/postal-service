from django.urls import path

from .apps import MailingConfig
from .views import (HomeView, MailingCreateView, MailingDeleteView,
                    MailingDetailsView, MailingListView,
                    MailingRecipientCreateView, MailingRecipientDeleteView,
                    MailingRecipientListView, MailingRecipientUpdateView,
                    MailingUpdateView, MessageCreateView, MessageDeleteView,
                    MessageDetailsView, MessageListView, MessageUpdateView,
                    MailingRecipientDetailsView)

app_name = MailingConfig.name

urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "recipients/",
        MailingRecipientListView.as_view(),
        name="mailing_recipient_list"
    ),
    path(
        "recipients/create/",
        MailingRecipientCreateView.as_view(),
        name="mailing_recipient_create",
    ),
    path(
        "recipients/<int:pk>/",
        MailingRecipientDetailsView.as_view(),
        name="mailing_recipient_detail"
    ),
    path(
        "recipients/update/<int:pk>/",
        MailingRecipientUpdateView.as_view(),
        name="mailing_recipient_update",
    ),
    path(
        "recipients/delete/<int:pk>/",
        MailingRecipientDeleteView.as_view(),
        name="mailing_recipient_delete",
    ),
    path(
        "messages/",
         MessageListView.as_view(),
         name="message_list"
         ),
    path(
        "messages/<int:pk>/",
        MessageDetailsView.as_view(),
        name="message_detail"
        ),
    path("messages/create/",
         MessageCreateView.as_view(),
         name="message_create"
         ),
    path(
        "messages/update/<int:pk>/",
        MessageUpdateView.as_view(),
        name="message_update"
    ),
    path(
        "messages/delete/<int:pk>/",
        MessageDeleteView.as_view(),
        name="message_delete"
    ),
    path("mailings/",
         MailingListView.as_view(),
         name="mailing_list"
         ),
    path("mailings/create/",
         MailingCreateView.as_view(),
         name="mailing_create"
         ),
    path(
        "mailings/update/<int:pk>/",
        MailingUpdateView.as_view(),
        name="mailing_update"
    ),
    path(
        "mailings/delete/<int:pk>/",
        MailingDeleteView.as_view(),
        name="mailing_delete"
    ),
path(
        "mailings/<int:pk>/",
        MailingDetailsView.as_view(),
        name="mailing_detail"
    ),
]
