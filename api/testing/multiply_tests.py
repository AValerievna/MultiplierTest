import pytest

SUCCESS_CODE = 200
ERROR_MSG = 'Something went wrong :('


@pytest.mark.parametrize('first, second',
                         [
                             pytest.param(13, 94,  id='two_double'),
                             pytest.param(33, 9, id='double_single'),
                             pytest.param(2, 2, id='two_single'),
                             pytest.param(0, 2, id='zero'),
                             pytest.param(0, 0, id='two_zero'),
                             pytest.param(-2, 10, id='negative'),
                             pytest.param(-24, -60, id='two_negative'),
                             pytest.param(666, 6, id='first_over_500'),
                             pytest.param(-2, 777, id='second_over_500'),
                             pytest.param(555, 999, id='two_over_500'),
                             pytest.param(500, 3, id='first_500'),
                             pytest.param(-5, 444, id='second_less_500'),
                         ])
def test_multiply_success(api_handler, first, second):
    response = api_handler.request_multiply(first=first, second=second)

    exp_res = first * second
    assert response.status_code == SUCCESS_CODE, "API request was not successfull!"
    assert response.json() == exp_res, "Another result was expected!"


@pytest.mark.parametrize('first, second',
                         [
                             pytest.param("", 94,  id='first_empty_str'),
                             pytest.param(33, "", id='second_empty_str'),
                             pytest.param("some_str", 94,  id='first_some_str'),
                             pytest.param(33, "some_str", id='second_some_str'),
                             pytest.param(0.2, 94,  id='first_float'),
                             pytest.param(33, 4.11, id='second_float')
                         ])
def test_multiply_invalid_param(api_handler, first, second):
    response = api_handler.request_multiply(first=first, second=second)

    assert response.status_code == SUCCESS_CODE, "API request was not successfull!"
    assert response.text == ERROR_MSG, "Another error was expected!"
