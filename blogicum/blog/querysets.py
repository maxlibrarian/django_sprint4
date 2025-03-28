from django.db.models import Count, QuerySet
from django.utils.timezone import now


class PostFilteredQuerySet(QuerySet):
    def published(self):
        return self.select_related(
            'category', 'author', 'location'
        ).filter(
            pub_date__lte=now(),
            category__is_published=True,
            is_published=True
        )

    def post_annotation(self):

        return self.select_related(
            'category', 'author', 'location'
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        )
