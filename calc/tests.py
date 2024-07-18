from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .parcel_3_4_5 import cost_of_parcel_3_4_5


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
    assert cost_of_registered(1000, 0) == [{
            'fiz': '5,70',
            'yur': '5,70',
            'item_vat': '0,95',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб.",
            'notification': ""}]
    assert cost_of_registered(30000, 0) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_value_letter():
    assert cost_of_value_letter(22, 10, 4) == [{
            'fiz': '3,90',
            'yur': '4,26',
            'item_vat': '0,71',
            'for_declared': '0,36',
            'tracking': 'да',
            'sep': '/',
            'rub': " руб.",
            'notification': ""
    }]
    assert cost_of_value_letter(2001, 10, 4) == [{
        'fiz': 'Макс. вес 2 кг', 'sep': ''
    }]
    assert cost_of_value_letter(22, 10, 1) == [{
        'fiz': '4,68',
        'yur': '5,04',
        'item_vat': '0,84',
        'for_declared': '0,36',
        'tracking': 'да',
        'sep': '/',
        'rub': " руб.",
        'notification': "0,78"
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
        'fiz': '3,30',
        'yur': '6,26',
        'item_vat': '1,04',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
    }]
    assert cost_of_parcel(510, '') == [{
        'fiz': '3,30',
        'yur': '5,98',
        'item_vat': '1,00',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
    }]
    assert cost_of_parcel(915, 1.25) == [{
        'fiz': '3,34',
        'yur': '6,34',
        'item_vat': '1,06',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/'
    }]
    assert cost_of_parcel(1150, '') == [{
        'fiz': '4,96',
        'yur': '6,55',
        'item_vat': '1,09',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',

    }]
    assert cost_of_parcel(1152, 10.12) == [{
        'fiz': '5,23',
        'yur': '6,88',
        'item_vat': '1,15',
        'for_declared_fiz': '0,30',
        'for_declared_yur': '0,36',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
    }]
    assert cost_of_parcel(50200, '') == [{
        'fiz': 'Макс. вес 50 кг',
        'sep1': '', 'sep2': ''}]


def test_parcel_3_4_5():
    assert cost_of_parcel_3_4_5(6545, 1.55) == [{
        'fiz': '9,41',
        'for_declared': '0,50',
        'rub': " руб."
    }]
    assert cost_of_parcel_3_4_5(6545, 50.00) == [{
        'fiz': '9,41',
        'for_declared': '0,50',
        'rub': " руб."
    }]
