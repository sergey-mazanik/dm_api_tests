from assertpy import assert_that, soft_assertions


class DeleteV1AccountLogin:

    @classmethod
    def check_response_by_assertpy(cls, response):
        with soft_assertions():
            assert_that(response.status_code).is_equal_to(204)
            assert_that(response.request.headers).contains_key('X-Dm-Auth-Token')
