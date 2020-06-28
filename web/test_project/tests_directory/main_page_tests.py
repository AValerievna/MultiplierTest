import pytest

from web.test_project.pages.main_page import MainPage

ERROR_INPUT_MSG = "Only numbers from 0 to 500 and not empty"


def get_opened_main_page():
    main_page = MainPage()
    main_page.open()
    return main_page


def test_main_page_multiply_displayed():
    main_page = get_opened_main_page()
    assert main_page.is_content_displayed()


@pytest.mark.parametrize(
    "first_digit, second_digit",
    [
        pytest.param(13, 94, id='two_double'),
        pytest.param(33, 9, id='double_single'),
        pytest.param(2, 2, id='two_single'),
        pytest.param(0, 2, id='zero'),
        pytest.param(0, 0, id='two_zero')
    ])
def test_main_page_valid_multiply(first_digit, second_digit):
    main_page = get_opened_main_page()
    main_page.input_first_digit(first_digit=first_digit)
    main_page.input_second_digit(second_digit=second_digit)
    main_page.click_multiply_btn()

    exp_res = first_digit * second_digit
    assert main_page.get_result_after_multiply() == "Result: " + str(exp_res), "Another result was expected!"


@pytest.mark.parametrize(
    "first_digit, second_digit",
    [
        pytest.param("", 94, id='empty_str'),
        pytest.param("some_str", 94, id='some_str'),
        pytest.param("0.2", 94, id='float'),
        pytest.param(-2, 10, id='negative')
    ])
def test_main_page_multiply_invalid_params_first(first_digit, second_digit):
    main_page = get_opened_main_page()
    main_page.input_first_digit(first_digit=first_digit)
    main_page.input_second_digit(second_digit=second_digit)
    main_page.click_multiply_btn()

    assert main_page.get_first_error_msg() == ERROR_INPUT_MSG, "Another error was expected!"


@pytest.mark.parametrize(
    "first_digit, second_digit",
    [
        pytest.param(33, "", id='empty_str'),
        pytest.param(33, "some_str", id='some_str'),
        pytest.param(33, "4.11", id='float'),
        pytest.param(44, -10, id='negative')
    ])
def test_main_page_multiply_invalid_params_second(first_digit, second_digit):
    main_page = get_opened_main_page()
    main_page.input_first_digit(first_digit=first_digit)
    main_page.input_second_digit(second_digit=second_digit)
    main_page.click_multiply_btn()

    assert main_page.get_second_error_msg() == ERROR_INPUT_MSG, "Another error was expected!"


@pytest.mark.parametrize(
    "first_digit, second_digit",
    [
        pytest.param("str", "", id='empty_str'),
        pytest.param("0.1", "some_str", id='some_str'),
        pytest.param("", "4.11", id='float'),
        pytest.param(-2, -10, id='two_negative'),
    ])
def test_main_page_multiply_invalid_params_both(first_digit, second_digit):
    main_page = get_opened_main_page()
    main_page.input_first_digit(first_digit=first_digit)
    main_page.input_second_digit(second_digit=second_digit)
    main_page.click_multiply_btn()

    assert main_page.get_first_error_msg() == ERROR_INPUT_MSG, "Another error was expected!"
    assert main_page.get_second_error_msg() == ERROR_INPUT_MSG, "Another error was expected!"
