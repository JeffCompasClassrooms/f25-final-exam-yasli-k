import pytest
from brute import Brute


def describe_brute_class():
    def describe_init():
        def it_hashes_the_secret_string_correctly():
            secret = "test123"
            brute = Brute(secret)
            assert brute.target == brute.hash(secret)

    def describe_hash():
        def it_produces_sha512_hexdigest():
            brute = Brute("test")
            assert len(brute.hash("test")) == 128

        def it_handles_empty_string():
            brute = Brute("")
            assert brute.hash("") is not None

    def describe_random_guess():
        def it_returns_string_of_length_1_to_8():
            brute = Brute("test")
            guess = brute.randomGuess()
            assert 1 <= len(guess) <= 8
            assert all(c.isalnum() for c in guess)

    def describe_brute_once_no_mocks():
        def it_returns_true_on_correct_guess():
            secret = "abc123"
            brute = Brute(secret)
            assert brute.bruteOnce(secret) is True

        def it_returns_false_on_wrong_guess():
            secret = "abc123"
            brute = Brute(secret)
            assert brute.bruteOnce("wrong") is False

        def it_handles_empty_attempt():
            brute = Brute("hello")
            assert brute.bruteOnce("") is False

    def describe_brute_many_with_mocks():
        # mocker is passed automatically to every test function inside this block
        def it_returns_time_when_successful(mocker):
            secret = "win"
            brute = Brute(secret)
            mocker.patch.object(brute, 'randomGuess', return_value=secret)
            mocker.patch('time.time', side_effect=[100.0, 100.7])

            result = brute.bruteMany(limit=10)
            assert result == pytest.approx(0.7)

        def it_returns_negative_1_when_fails_all_attempts(mocker):
            brute = Brute("secret")
            mocker.patch.object(brute, 'randomGuess', return_value="wrong")

            result = brute.bruteMany(limit=5)
            assert result == -1

        def it_calls_brute_once_exactly_limit_times(mocker):
            brute = Brute("any")
            mocker.patch.object(brute, 'randomGuess', return_value="wrong")
            spy = mocker.spy(brute, 'bruteOnce')

            brute.bruteMany(limit=6)
            assert spy.call_count == 6

        def it_handles_limit_zero(mocker):
            brute = Brute("any")
            mocker.patch('time.time')

            result = brute.bruteMany(limit=0)
            assert result == -1