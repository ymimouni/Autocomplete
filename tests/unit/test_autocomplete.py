import pytest

from src.autocomplete import *


@pytest.fixture
def populated_ac():
    keywords = ['project runway', 'pinterest', 'river', 'kayak', 'progenex', 'progeria', 'pg&e', 'project free tv',
                'bank', 'proactive', 'progesterone', 'press democrat', 'priceline', 'pandora', 'reprobe', 'paypal']

    autocomplete = Autocomplete()
    autocomplete.populate(keywords)

    return autocomplete


def test_autocomplete(populated_ac):
    data = [('', []),
            ('p', ['pandora', 'paypal', 'pg&e', 'pinterest']),
            ('pr', ['press democrat', 'priceline', 'proactive', 'progenex']),
            ('pro', ['proactive', 'progenex', 'progeria', 'progesterone']),
            ('prog', ['progenex', 'progeria', 'progesterone']),
            ('progenex', ['progenex'])]

    for prefix, expected in data:
        assert populated_ac.get_suggestions(prefix) == expected


def test_precomputation(populated_ac):  # noqa
    data = [('', []),
            ('p', ['pandora', 'paypal', 'pg&e', 'pinterest']),
            ('pr', ['press democrat', 'priceline', 'proactive', 'progenex']),
            ('pro', ['proactive', 'progenex', 'progeria', 'progesterone']),
            ('prog', ['progenex', 'progeria', 'progesterone']),
            ('progenex', ['progenex'])]

    populated_ac.precompute_suggestions()

    for prefix, expected in data:
        assert populated_ac.get_suggestions(prefix) == expected
