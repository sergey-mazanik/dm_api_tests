from hamcrest import (
    assert_that as hamcrest_assert, has_property, all_of, any_of, has_properties, equal_to, greater_than, has_length,
    not_none, none, is_,
    close_to, less_than_or_equal_to, greater_than_or_equal_to,
)

from assertpy import assert_that, soft_assertions


class GetV1Account:

    @classmethod
    def check_response_by_hamcrest(cls, response):
        hamcrest_assert(
            response, all_of(
                has_property('resource', has_property('login', has_length(greater_than(5)))),
                has_property('resource', has_property('roles', not_none())),
                has_property('resource', has_property('roles', is_(list))),
                has_property('resource', has_property('medium_picture_url', none())),
                has_property(
                    'resource',
                    has_property(
                        'settings', has_property(
                            'paging', has_properties(
                                {
                                    "posts_per_page": greater_than_or_equal_to(10),
                                    "comments_per_page": all_of(greater_than(9), is_(int), not_none()),
                                    "topics_per_page": any_of(equal_to(10), not_none()),
                                    "messages_per_page": equal_to(10) and close_to(10, 1),
                                    "entities_per_page": less_than_or_equal_to(10)
                                }
                            )
                        )
                    )
                ),
            )
        )

    @classmethod
    def check_response_by_assertpy(cls, response):
        with soft_assertions():
            assert_that(response.resource.login).starts_with('smazanik')
            assert_that(response.resource.info).is_instance_of(str)
            assert_that(response.resource.info).is_empty()
