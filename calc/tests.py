from .letter import cost_of_simple, cost_of_registered, cost_of_value_package
from .first_class import cost_of_first_class
from .parcel import cost_of_parcel
from .parcel_3_4_5 import cost_of_parcel_3_4_5
from .qr_box import cost_of_parcel_qr
from .internal_transfer import cost_of_internal_transfer
from .ems_cost import find_documents_cost, find_goods_cost
from .parcel_int import cost_of_parcel_int
from .letter_int import cost_of_letter_int
from .package_int import cost_of_package_int
from .ems_int import cost_of_ems_int


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


def test_registered():  # письмо, бандероль, мелкий пакет
    assert cost_of_registered(1000, 4) == [{
            'fiz': '6,67',
            'yur': '6,77',
            'item_vat': '1,13',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб.",
            'notification': ""}]
    assert cost_of_registered(30000, 4) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_value_package():
    assert cost_of_value_package(22, 10, 4) == [{
        'fiz': '4,15',
        'yur': '4,27',
        'item_vat': '0,71',
        'for_declared': '0,36',
        'tracking': 'да',
        'sep': '/',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_value_package(915, 1.25, 4) == [{
        'fiz': '6,92',
        'yur': '7,13',
        'item_vat': '1,19',
        'for_declared': '0,05',
        'tracking': 'да',
        'sep': '/',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_value_package(2001, 10, 4) == [{
        'fiz': 'Макс. вес 2 кг', 'sep': ''
    }]
    assert cost_of_value_package(22, 10, 1) == [{
        'fiz': '4,99',
        'yur': '5,11',
        'item_vat': '0,85',
        'for_declared': '0,36',
        'tracking': 'да',
        'sep': '/',
        'rub': " руб.",
        'notification': "0,84"
    }]


def test_first_class():
    assert cost_of_first_class(155) == [{
            'fiz': '2,46',
            'yur': '2,46',
            'item_vat': '0,41',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб."}]
    assert cost_of_first_class(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_parcel():
    assert cost_of_parcel(510, '', 4) == [{
        'fiz': '3,50',
        'yur': '6,01',
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
        'fiz': '3,54',
        'yur': '6,38',  # Белпочта 6,39 неправильно
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
        'fiz': '4,38',
        'yur': '7,22',
        'item_vat_yur': '1,20',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': "0,84"
    }]
    assert cost_of_parcel(1150, '', 4) == [{
        'fiz': '5,02',
        'yur': '6,62',
        'item_vat_yur': '1,10',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(1152, 10.12, 4) == [{
        'fiz': '5,29',
        'yur': '6,95',
        'item_vat_yur': '1,16',
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
        'fiz': '10,07',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(6545, 50.00, 4) == [{
        'fiz': '10,07',
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
        'for_declared_fiz': '0,50',
        'rub': " руб.",
        'notification': '0,54',
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


def test_express_parcel():  # 4 зона P12 - P1 Орша - Брест
    """
    (zone, weight, declared_value, delivery, notification, fragile)
    дописать тест товары
    """
    assert find_documents_cost(4, 1750, 0, 1, 4, "None") == [
        [{'fiz': '8,60',
          'for_declared_yur': '-',
          'item_vat': '1,72',
          'notification': '',
          'yur': '10,32'}],
        [{'fiz': '10,10',
          'for_declared_yur': '-',
          'item_vat': '2,02',
          'notification': '',
          'yur': '12,12'}]]
    assert find_documents_cost(4, 1750, 10.75, 1, 4, "None") == [
        [{'fiz': '8,99',
          'for_declared_yur': '0,38',
          'item_vat': '1,78',
          'notification': '',
          'yur': '10,70'}],
        [{'fiz': '10,49',
          'for_declared_yur': '0,38',
          'item_vat': '2,08',
          'notification': '',
          'yur': '12,50'}]]
    assert find_goods_cost(5, 21750, 0, 1, 4, "None") == [  # P30-P13 Дубровно-Кобрин
        [{'fiz': '36,15',
          'for_declared_yur': '-',
          'item_vat': '7,23',
          'notification': '',
          'yur': '43,38'}],
        [{'fiz': '37,10',
          'for_declared_yur': '-',
          'item_vat': '7,42',
          'notification': '',
          'yur': '44,52'}]]
    assert find_goods_cost(5, 21750, 12.58, 1, 4, "None") == [  # P30-P13 Дубровно-Кобрин
        [{'fiz': '36,60',
          'for_declared_yur': '0,46',
          'item_vat': '7,31',
          'notification': '',
          'yur': '43,84'}],
        [{'fiz': '37,55',
          'for_declared_yur': '0,46',
          'item_vat': '7,50',
          'notification': '',
          'yur': '44,98'}]]


def test_letter_int():
    assert cost_of_letter_int(1045, 1.25, 12) == [
        [{'fiz': '48,48',
          'yur': '48,48',
          'item_vat_yur': '8,08',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '69,54',
          'yur': '69,54',
          'item_vat_yur': '11,59',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '75,30', 'yur': '75,30', 'item_vat': '12,55'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '80,04', 'yur': '80,04', 'item_vat': '13,34'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '82,67',
          'for_declared': '0,05',
          'item_vat_yur': '13,78',
          'rub': ' руб.',
          'tracking': 'да',
          'yur': '82,67'}]
    ]


def test_package_int():
    assert cost_of_package_int(11, 1045) == [  # в Австралию - destination 11
        [{'fiz': '83,92', 'yur': '83,92', 'item_vat': '13,99'}],
        [{'fiz': '83,92', 'yur': '83,92', 'item_vat': '13,99'}],
        [{'fiz': '86,18', 'yur': '86,18', 'item_vat': '14,36'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '90,92', 'yur': '90,92', 'item_vat': '15,15'}]
    ]


def test_package_int2():
    assert cost_of_package_int(161, 1035) == [  # в Россию - destination 161
        [{'fiz': '26,05', 'yur': '26,05', 'item_vat': '4,34'}],
        [{'fiz': '37,14', 'yur': '37,14', 'item_vat': '6,19'}],
        [{'fiz': '41,17', 'yur': '41,17', 'item_vat': '6,86'}],
        [{'fiz': '35,42', 'yur': '35,42', 'item_vat': '5,90'}],
        [{'fiz': '45,91', 'yur': '45,91', 'item_vat': '7,65'}]
    ]


def test_ems_int():
    assert cost_of_ems_int(153, 1035, 12.24) == [  # в Москву- destination 153
        [{'fiz': '51,08', 'yur': '51,08', 'item_vat': '8,51', 'for_declared': '0,44'}],
        [{'fiz': '53,00', 'yur': '53,00', 'item_vat': '8,83', 'for_declared': '0,44'}]
    ]
    assert cost_of_ems_int(194, 1035, 12.24) == [  # Украина - destination 194
        [{'fiz': "отправления не принимаются"}],
        [{'fiz': "отправления не принимаются"}]
    ]
