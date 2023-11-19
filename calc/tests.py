# from django.test import TestCase
from . import parcel
from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel


def test_simple():
    assert cost_of_simple(300) == [{
            'fiz': '1,54',
            'yur': '1,54',
            'item_vat': '0,26',
            'for_declared': '',
            'tracking': 'нет',
            'rub': " руб."}]
    assert cost_of_simple(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_registered():
    assert cost_of_registered(1000) == [{
            'fiz': '5,70',
            'yur': '5,70',
            'item_vat': '0,95',
            'for_declared': '',
            'tracking': 'да',
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
            'tracking': 'да',
            'rub': " руб."}]
    assert cost_of_value_letter(2001, 10) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_first_class():
    assert cost_of_first_class(155) == [{
            'fiz': '2,04',
            'yur': '2,04',
            'item_vat': '0,34',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб."}]
    assert cost_of_first_class(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_parcel():
    assert cost_of_parcel(900, '') == [{
        'fiz': '3,00',
        'yur': '6,22',
        'item_vat': '1,04',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep': '/'}]
    assert cost_of_parcel(510, '') == [{
        'fiz': '3,00',
        'yur': '5,94',
        'item_vat': '0,99',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep': '/'}]
    assert cost_of_parcel(915, 1.25) == [{
        'fiz': '3,04',
        'yur': '6,28',
        'item_vat': '1,04',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep': '/'}]
    assert cost_of_parcel(1150, '') == [{
        'fiz': '4,90',
        'yur': '6,48',
        'item_vat': '1,08',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep': '/'}]
    assert cost_of_parcel(1152, 10.12) == [{
        'fiz': '5,17',
        'yur': '6,80',
        'item_vat': '1,13',
        'for_declared_fiz': '0,30',
        'for_declared_yur': '0,36',
        'tracking': 'да',
        'rub': " руб.",
        'sep': '/'}]
    assert cost_of_parcel(50200, '') == [{
        'fiz': 'Макс. вес 50 кг',
        'sep': ''
    }]
