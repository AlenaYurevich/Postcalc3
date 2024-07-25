from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .parcel_3_4_5 import cost_of_parcel_3_4_5
from .internal_transfer import cost_of_internal_transfer


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
    assert cost_of_registered(1000, 4) == [{
            'fiz': '5,94',
            'yur': '5,94',
            'item_vat': '0,99',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб.",
            'notification': ""}]
    assert cost_of_registered(30000, 4) == [{
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
    assert cost_of_value_letter(915, 1.25, 4) == [{
        'fiz': '6,23',
        'yur': '6,59',
        'item_vat': '1,10',
        'for_declared': '0,05',
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
    assert cost_of_parcel(900, '', 4) == [{
        'fiz': '3,30',
        'yur': '6,26',
        'item_vat': '1,04',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(510, '', 4) == [{
        'fiz': '3,30',
        'yur': '5,98',
        'item_vat': '1,00',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(915, 1.25, 4) == [{
        'fiz': '3,34',
        'yur': '6,34',
        'item_vat': '1,06',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(915, 1.25, 1) == [{
        'fiz': '4,12',
        'yur': '7,12',
        'item_vat': '1,19',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': "0,78"
    }]
    assert cost_of_parcel(1150, '', 4) == [{
        'fiz': '4,96',
        'yur': '6,55',
        'item_vat': '1,09',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(1152, 10.12, 4) == [{
        'fiz': '5,23',
        'yur': '6,88',
        'item_vat': '1,15',
        'for_declared_fiz': '0,30',
        'for_declared_yur': '0,36',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(50200, '', 4) == [{
        'fiz': 'Макс. вес 50 кг',
        'sep1': '', 'sep2': ''}]


def test_parcel_3_4_5():
    assert cost_of_parcel_3_4_5(6545, 1.55, 4) == [{
        'fiz': '9,41',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(6545, 50.00, 4) == [{
        'fiz': '9,41',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(915, 1.25, 3) == [{
        'fiz': '4,04',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': "0,54"
    }]


def test_internal_transfer():
    assert cost_of_internal_transfer(35.85) == [{
        'fiz': '1,08',
        'yur': '1,30',
        'item_vat': '0,22',
        'fiz_home': '1,40',
        'yur_home': 'нет'
    }]


"""
Добавить тест на ЕМS
"""
