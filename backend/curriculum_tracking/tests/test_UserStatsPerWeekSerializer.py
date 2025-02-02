from core.tests.factories import UserFactory
from curriculum_tracking.serializers import UserStatsPerWeekSerializer
from django.test import TestCase
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
)
from . import factories
from social_auth.tests.factories import SocialProfileFactory
from datetime import timedelta
from git_real.tests import factories as git_real_factories

from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
)
from curriculum_tracking.tests.factories import (
    ContentItemFactory,
    AgileCardFactory,
    RecruitProjectReviewFactory,
    TopicReviewFactory
)
from django.utils import timezone
from git_real.tests.factories import PullRequestReviewFactory


class TestingForTheStatsAPI(TestCase):
    def setUp(self):
        self.card_1 = AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
        )

        self.project_1 = self.card_1.recruit_project
        self.user = self.card_1.assignees.first()
        self.project_1.start_time = timezone.now() - timedelta(days=5)
        self.project_1.save()
        self.stats_serializer = UserStatsPerWeekSerializer()

        # Will use this repo card, PR, today, yesterday, two_days_before_yesterday and two_weeks_ago later on
        # in test 'test_pr_reviews_card_in_different_column_due_to_review_status'.
        self.today = timezone.now()
        self.yesterday = self.today - timezone.timedelta(days=1)
        self.two_days_before_yesterday = self.today - timezone.timedelta(days=3)
        self.two_weeks_ago = self.today - timezone.timedelta(days=14)

        self.repo_card_one = factories.AgileCardFactory(status=AgileCard.IN_PROGRESS)
        self.repo_card_one.recruit_project.repository = (
            git_real_factories.RepositoryFactory()
        )
        self.repo_card_one.save()

        self.pull_request = git_real_factories.PullRequestFactory(
            repository=self.repo_card_one.recruit_project.repository,
            updated_at=self.today,
        )
        self.pull_request.save()

    def test_one_card_in_progress_before_any_reviews(self):

        # One card, no reviews just yet, function 'get_cards_in_progress_column_as_assignee' should return one card
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.project_1.content_item, self.card_1.content_item)
        self.assertEqual(
            AgileCard.derive_status_from_project(self.project_1), AgileCard.IN_PROGRESS
        )
        self.assertEqual(self.stats_serializer.get_cards_in_progress_column_as_assignee(user=self.user), 1)

    def test_one_card_in_review_feedback_column(self):

        # Request for a review to happen on project_1, card_1
        request_review_time = self.project_1.start_time + timedelta(1)
        time_one = self.project_1.start_time - timedelta(days=6)
        self.project_1.request_review(force_timestamp=request_review_time)
        review_1 = RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT, recruit_project=self.project_1, timestamp=time_one
        )
        review_1.timestamp = time_one
        review_1.save()

        # review_1 had a status of NYC, so we should have at least one card in the 'REVIEW FEEDBACK' column
        self.assertEqual(self.stats_serializer.get_cards_in_review_feedback_column_as_assignee(user=self.user), 1)

    def test_no_card_in_completed_column_after_untrusted_competent_review(self):
        time_two = self.project_1.start_time + timedelta(days=4)
        review_2 = RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.project_1,
        )
        review_2.timestamp = time_two
        review_2.save()

        # review_2 had a status of COMPETENT, the reviewer is not trusted and therefore we should have zero cards in
        # the completed column
        self.assertEqual(self.stats_serializer.get_cards_in_complete_column_as_assignee(user=self.user), 0)

    def test_one_card_started_in_the_past_seven_days(self):
        self.assertEqual(self.stats_serializer.get_cards_started_last_7_days_as_assignee(user=self.user), 1)

    def test_no_cards_completed_in_past_seven_days(self):

        self.assertEqual(self.stats_serializer.get_cards_completed_last_7_days_as_assignee(user=self.user), 0)

    def test_one_card_in_complete_column(self):

        content_item_2 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )
        card_2 = AgileCardFactory(
            content_item=content_item_2,
            status=AgileCard.COMPLETE,
        )
        assigned_person = SocialProfileFactory().user
        card_2.assignees.set([assigned_person])

        # We should have at least one card in the completed column and since it went there within the last seven days
        # the function 'get_cards_completed_last_7_days_as_assignee' should also return at least one card
        self.assertEqual(self.stats_serializer.get_cards_in_complete_column_as_assignee(user=assigned_person), 1)
        self.assertEqual(self.stats_serializer.get_cards_completed_last_7_days_as_assignee(user=assigned_person), 1)

    def test_cards_in_the_review_column_waiting_for_a_review(self):

        # Two cards in the IN_REVIEW column
        content_item_3 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )

        card_3 = AgileCardFactory(
            content_item=content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        card_4 = AgileCardFactory(
            content_item=content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        assigned_person = SocialProfileFactory().user
        card_3.assignees.set([assigned_person])
        card_4.assignees.set([assigned_person])

        # We should get two cards in the review column waiting for a review
        self.assertEqual(self.stats_serializer.get_cards_in_review_column_as_assignee(user=assigned_person), 2)

    def test_pr_reviews_done_within_the_last_seven_days(self):

        # Now creating reviews on the PR
        yesterday_pr_review = PullRequestReviewFactory(
            pull_request=self.pull_request,
            submitted_at=self.yesterday,
            user=self.repo_card_one.assignees.first(),
        )

        two_days_ago_pr_review = PullRequestReviewFactory(
            pull_request=self.pull_request,
            submitted_at=self.two_days_before_yesterday,
            user=self.repo_card_one.assignees.first(),
        )

        two_weeks_ago_pr_review = PullRequestReviewFactory(
            pull_request=self.pull_request,
            submitted_at=self.two_weeks_ago,
            user=self.repo_card_one.assignees.first(),
        )

        # Three PR reviews were done but only two of them were done in the last seven days so we should get a value
        # of 2
        self.assertEqual(self.stats_serializer.get_pr_reviews_done_last_7_days(self.repo_card_one.assignees.first()), 2)

    def test_get_tilde_cards_reviewed_in_last_7_days(self):
        user = UserFactory()

        # no reviews done yet
        count = self.stats_serializer.get_tilde_cards_reviewed_in_last_7_days(user)
        self.assertEqual(count, 0)

        # add a review, but it's too old to count

        review1 = RecruitProjectReviewFactory(
            timestamp=self.two_weeks_ago, reviewer_user=user
        )
        review1.timestamp = self.two_weeks_ago
        review1.save()
        AgileCardFactory(recruit_project=review1.recruit_project)

        count = self.stats_serializer.get_tilde_cards_reviewed_in_last_7_days(user)
        self.assertEqual(count, 0)

        # add a review within the right timeframe

        review2 = RecruitProjectReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review2.timestamp = self.yesterday
        review2.save()
        AgileCardFactory(recruit_project=review2.recruit_project)
        # assert review.reviewer_user == user

        count = self.stats_serializer.get_tilde_cards_reviewed_in_last_7_days(user)
        self.assertEqual(count, 1)

        # add another review on the same card, so now the number of cards reviewed is still 1
        review3 = RecruitProjectReviewFactory(
            timestamp=self.yesterday,
            reviewer_user=user,
            recruit_project=review2.recruit_project,
        )
        review3.timestamp = self.yesterday
        review3.save()
        # AgileCardFactory(recruit_project=review3.recruit_project)

        count = self.stats_serializer.get_tilde_cards_reviewed_in_last_7_days(user)
        self.assertEqual(count, 1)

        # add another review, now the number of cards reviewed is 2

        review4 = RecruitProjectReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review4.timestamp = self.yesterday
        review4.save()
        AgileCardFactory(recruit_project=review4.recruit_project)

        count = self.stats_serializer.get_tilde_cards_reviewed_in_last_7_days(user)
        self.assertEqual(count, 2)

    def test_no_tilde_reviews_done_in_last_7_days(self):
        user = UserFactory()

        # add a review, but it's too old to count
        review = RecruitProjectReviewFactory(
            timestamp=self.two_weeks_ago, reviewer_user=user
        )
        review.timestamp = self.two_weeks_ago
        review.save()
        AgileCardFactory(recruit_project=review.recruit_project)
        count = self.stats_serializer.get_tilde_reviews_done_last_7_days(user)
        self.assertEqual(count, 0)

    def test_multiple_tilde_reviews_done_in_last_7_days(self):
        user = UserFactory()

        # add a review within the right timeframe
        review1 = RecruitProjectReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review1.timestamp = self.yesterday
        review1.save()
        AgileCardFactory(recruit_project=review1.recruit_project)

        # add another review, now the number of cards reviewed is 2
        review2 = RecruitProjectReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review2.timestamp = self.yesterday
        review2.save()
        AgileCardFactory(recruit_project=review2.recruit_project)

        # add a topic review, now the number of cards reviewed is 3
        review3 = TopicReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review3.timestamp = self.yesterday
        review3.save()
        AgileCardFactory(topic_progress=review3.topic_progress)
        count = self.stats_serializer.get_tilde_reviews_done_last_7_days(user)
        self.assertEqual(count, 3)

    def test_no_tilde_reviews_done(self):
        user = UserFactory()

        # no reviews done yet
        count = self.stats_serializer.get_total_tilde_reviews_done(user)
        self.assertEqual(count, 0)

    def test_multiple_tilde_reviews_done(self):
        user = UserFactory()

        # add a review
        review1 = RecruitProjectReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review1.timestamp = self.yesterday
        review1.save()
        AgileCardFactory(recruit_project=review1.recruit_project)

        # add really old review
        review2 = RecruitProjectReviewFactory(
            timestamp=self.two_weeks_ago, reviewer_user=user
        )
        review2.timestamp = self.two_weeks_ago
        review2.save()
        AgileCardFactory(recruit_project=review2.recruit_project)

        # add a topic review, now we should have 3 reviews
        review3 = TopicReviewFactory(
            timestamp=self.yesterday, reviewer_user=user
        )
        review3.timestamp = self.yesterday
        review3.save()
        AgileCardFactory(topic_progress=review3.topic_progress)
        count = self.stats_serializer.get_total_tilde_reviews_done(user)
        self.assertEqual(count, 3)
