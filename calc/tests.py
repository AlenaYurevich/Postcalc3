from .letter import cost_of_simple, cost_of_registered, cost_of_value_letter
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .parcel_3_4_5 import cost_of_parcel_3_4_5
from .qr_box import cost_of_parcel_qr
from .internal_transfer import cost_of_internal_transfer
from .parcel_int import cost_of_parcel_int
from .letter_int import cost_of_letter_int


def test_simple():
    assert cost_of_simple(300) == [{
            'fiz': '1,54',
            'yur': '1,54',
            'item_vat': '0,26',
            'for_declared': '',
            'tracking': 'нет',
            'rub': " руб.",
    }]
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
            'fiz': '2,22',
            'yur': '2,22',
            'item_vat': '0,37',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб."}]
    assert cost_of_first_class(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_parcel():
    assert cost_of_parcel(510, '', 4) == [{
        'fiz': '3,30',
        'yur': '5,98',
        'item_vat_yur': '1,00',
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
        'item_vat_yur': '1,06',
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
        'item_vat_yur': '1,19',
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
        'item_vat_yur': '1,09',
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
        'item_vat_yur': '1,15',
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
        'fiz': '9,74',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(6545, 50.00, 4) == [{
        'fiz': '9,74',
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


def test_parcel_qr():
    assert cost_of_parcel_qr(6545, 1.55, 3) == [{
        'fiz': '5,54',
        'yur': '6,54',
        'for_declared_fiz': '0,50',
        'for_declared_yur': '0,60',
        'item_vat_yur': '1,09',
        'rub': " руб.",
        'notification': '0,54',
        'sep1': '/',
        'sep2': '/',
        'tracking': 'да',
    }]


def test_internal_transfer():
    assert cost_of_internal_transfer(35.85) == [{
        'fiz': '1,08',
        'yur': '1,30',
        'item_vat': '0,22',
        'fiz_home': '1,40',
        'yur_home': 'нет'
    }]


def test_parcel_int():
    assert cost_of_parcel_int(12, 1000, '') == [[{
        'fiz': '59,15',
        'yur': '70,98',
        'item_vat_yur': '11,83',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': "да",
        'sep1': '',
        'sep2': '/',
        'rub': " руб."}],
        [{'fiz': '60,60',
          'for_declared_fiz': '',
          'for_declared_yur': '',
          'item_vat_yur': '12,12',
          'rub': ' руб.',
          'sep1': '',
          'sep2': '/',
          'tracking': 'да',
          'yur': '72,72'}]]
    assert cost_of_parcel_int(12, 1045, 1.25) == [[{
        'fiz': '65,57',
        'yur': '78,68',  # на сайте Белпочта неправильно, 78,70
        'item_vat_yur': '13,11',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'sep1': '/',
        'sep2': '/',
        'tracking': "да",
        'rub': " руб."
    }],
      [{'fiz': '67,02',
        'yur': '80,42',  # на сайте Белпочта неправильно, 80,44
        'item_vat_yur': '13,40',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'sep1': '/',
        'sep2': '/',
        'tracking': "да",
        'rub': " руб."}]]


"""
Добавить тест на ЕМS
"""


def test_letter_int():
    assert cost_of_letter_int(1045, 1.25) == [
        [{'fiz': '48,48',
          'yur': '48,48',
          'item_vat_yur': '8,08',
          'for_declared_fiz': '',
          'for_declared_yur': '',
          'rub': " руб.",
          'tracking': "нет",
          'sep1': "",
          'sep2': "/", }],
        [{'fiz': '69,54',
          'yur': '69,54',
          'item_vat_yur': '11,59',
          'for_declared_fiz': '',
          'for_declared_yur': '',
          'rub': " руб.",
          'tracking': "нет",
          'sep1': "",
          'sep2': "/", }],
        [{'fiz': '61,61',
          'yur': '61,61',
          'item_vat_yur': '10,27',
          'for_declared_fiz': '0,05',
          'for_declared_yur': '0,05',
          'rub': " руб.",
          'tracking': "да",
          'sep1': "/",
          'sep2': "/", }],
        [{'fiz': '82,67',
          'yur': '82,67',
          'item_vat_yur': '13,78',
          'for_declared_fiz': '0,05',
          'for_declared_yur': '0,05',
          'rub': " руб.",
          'tracking': "да",
          'sep1': "/",
          'sep2': "/", }]
    ]
