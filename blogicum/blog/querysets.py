from django.db.models import Count, QuerySet
from django.utils.timezone import now


class PostFilteredQuerySet(QuerySet):
    def join_related(self):

        return self.select_related('category', 'author', 'location')

    def published(self):

        return self.join_related().filter(
            pub_date__lte=now(),
            category__is_published=True,
            is_published=True
        )

    def post_annotation(self):

        return self.join_related().order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        )
