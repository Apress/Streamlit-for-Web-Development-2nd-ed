from streamlit.testing.v1 import AppTest

def test_main():
    at = AppTest.from_file('../main.py').run()

    at.number_input[0].set_value(10).run()
    at.number_input[1].set_value(4).run()
    at.selectbox[0].set_value('-').run()
    at.button[0].click().run()
    assert at.markdown[0].value == 'Result: 6.0'

    at.number_input[0].set_value(2).run()
    at.number_input[1].set_value(6).run()
    at.selectbox[0].set_value('*').run()
    at.button[0].click().run()
    assert at.markdown[0].value == 'Result: 12.0'

    at.number_input[0].set_value(10).run()
    at.number_input[1].set_value(2).run()
    at.selectbox[0].set_value('/').run()
    at.button[0].click().run()
    assert at.markdown[0].value == 'Result: 5.0'

    at.number_input[0].set_value(10).run()
    at.number_input[1].set_value(0).run()
    at.selectbox[0].set_value('/').run()
    at.button[0].click().run()
    assert at.error

    at.number_input[0].set_value(-5).run()
    at.number_input[1].set_value(3).run()
    at.selectbox[0].set_value('+').run()
    at.button[0].click().run()
    assert at.markdown[0].value == 'Result: -2.0'
