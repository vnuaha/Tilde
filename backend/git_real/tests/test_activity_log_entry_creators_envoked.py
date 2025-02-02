from django.test import TestCase
from rest_framework.test import APITestCase

from git_real.models import Repository
from .utils import get_body_and_headers
from git_real.permissions import IsWebhookSignatureOk
from django.urls import reverse
from git_real import views
import mock

# from git_real.models import PullRequest, PullRequestReview, Push
from .factories import RepositoryFactory, PullRequestReview
from social_auth.tests.factories import SocialProfileFactory
from activity_log.models import LogEntry
import git_real.activity_log_creators as creators


class log_pr_reviewed_Tests(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_adding_a_pr_review(self, has_permission):
        has_permission.return_value = True

        # self.assertEqual(PullRequest.objects.all().count(), 0)
        self.assertEqual(PullRequestReview.objects.all().count(), 0)

        body, headers = get_body_and_headers("pull_request_review_submitted")
        review_data = body["review"]
        social_profile = SocialProfileFactory(github_name=review_data["user"]["login"])

        url = reverse(views.github_webhook)

        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        # self.assertEqual(PullRequest.objects.all().count(), 1)
        self.assertEqual(PullRequestReview.objects.all().count(), 1)

        # pr = PullRequest.objects.first()
        pr_review = PullRequestReview.objects.first()

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, social_profile.user)
        self.assertEqual(entry.effected_user, repo.user)
        self.assertEqual(entry.object_1, pr_review)
        self.assertEqual(entry.object_2, repo)
        self.assertEqual(entry.event_type.name, creators.PR_REVIEWED)
