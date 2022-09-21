import pytest
from my_app import find_user


def test_find_user():
    assert find_user('bob')['lname'] == 'Newby'
    assert find_user('JIM')['lname'] == 'Hopper'
    assert find_user('DuStIn')['lname'] == 'Henderson'
    assert find_user('mIKE')['lname'] == 'Wheeler'
    assert find_user('Bailey') == None
