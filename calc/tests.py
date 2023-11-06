# from django.test import TestCase
from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class


def test_simple():
    assert cost_of_simple(300) == [{
            'fiz': '1,54',
            'yur': '1,54',
            'item_vat': '0,26',
            'rub': " руб."}]
    assert cost_of_simple(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_registered():
    assert cost_of_registered(1000) == [{
            'fiz': '5,70',
            'yur': '5,70',
            'item_vat': '0,95',
            'rub': " руб."}]
    assert cost_of_registered(30000) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_value_letter():
    assert cost_of_value_letter(22, 10) == [{
            'fiz': '3,66',
            'yur': '4,02',
            'item_vat': '0,67',
            'for_declared': '0,36',
            'rub': " руб."}]
    assert cost_of_value_letter(2001, 10) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_first_class():
    assert cost_of_first_class(155) == [{
            'fiz': '2,04',
            'yur': '2,04',
            'item_vat': '0,34',
            'rub': " руб."}]
    assert cost_of_first_class(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]
