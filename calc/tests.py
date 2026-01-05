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
            'fiz': '1,84',
            'yur': '1,87',
            'item_vat': '0,31',
            'for_declared': '',
            'tracking': 'нет',
            'rub': " руб.",
            'sep': '/',
    }]
    assert cost_of_simple(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_registered():  # письмо, бандероль, мелкий пакет
    assert cost_of_registered(1000, 4) == [{
            'fiz': '7,88',
            'yur': '8,08',
            'item_vat': '1,35',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб.",
            'notification': ""}]
    assert cost_of_registered(30000, 4) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_value_package():
    assert cost_of_value_package(22, 10, 4) == [{
        'fiz': '5,06',
        'yur': '5,06',
        'item_vat': '0,84',
        'for_declared': '0,36',
        'tracking': 'да',
        'sep': '/',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_value_package(915, 1.25, 4) == [{
        'fiz': '8,27',
        'yur': '8,45',
        'item_vat': '1,41',
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
        'fiz': '6,02',
        'yur': '6,02',
        'item_vat': '1,00',
        'for_declared': '0,36',
        'tracking': 'да',
        'sep': '/',
        'rub': " руб.",
        'notification': "0,96"
    }]


def test_first_class():
    assert cost_of_first_class(155) == [{
            'fiz': '2,94',
            'yur': '2,94',
            'item_vat': '0,49',
            'for_declared': '',
            'tracking': 'да',
            'rub': " руб."}]
    assert cost_of_first_class(2002) == [{
        'fiz': 'Макс. вес 2 кг'
    }]


def test_parcel():
    assert cost_of_parcel(510, '', 4) == [{
        'fiz': '5,00',
        'yur': '6,65',
        'item_vat_yur': '1,11',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(915, 1.25, 4) == [{
        'fiz': '5,04',
        'yur': '7,04',  # Белпочта 7,05 неправильно
        'item_vat_yur': '1,17',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(915, 1.25, 1) == [{
        'fiz': '6,00',
        'yur': '8,00',
        'item_vat_yur': '1,33',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': "0,96"
    }]
    assert cost_of_parcel(1150, '', 4) == [{
        'fiz': '6,08',
        'yur': '7,30',
        'item_vat_yur': '1,22',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(1152, 10.12, 4) == [{
        'fiz': '6,35',
        'yur': '7,61',
        'item_vat_yur': '1,27',
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


def test_parcel2():
    assert cost_of_parcel(3500, '', 4) == [{
        'fiz': '8,15',
        'yur': '9,78',
        'item_vat_yur': '1,63',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(3500, 10, 4) == [{
        'fiz': '8,45',
        'yur': '10,14',
        'item_vat_yur': '1,69',
        'for_declared_fiz': '0,30',
        'for_declared_yur': '0,36',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': ""
    }]


def test_parcel_3_4_5():
    assert cost_of_parcel_3_4_5(6545, 1.55, 4) == [{
        'fiz': '10,90',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(6545, 50.00, 4) == [{
        'fiz': '10,90',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(915, 1.25, 3) == [{
        'fiz': '5,60',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': "0,60"
    }]


def test_parcel_qr():
    assert cost_of_parcel_qr(6545, 1.55, 3) == [{
        'fiz': '6,10',
        'yur': '7,20',
        'item_vat_yur': '1,20',
        'for_declared_fiz': '0,50',
        'for_declared_yur': '0,60',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': '0,60',
        'tracking': 'да',
    }]


def test_internal_transfer():
    assert cost_of_internal_transfer(35.85) == [{
        'fiz': '1,08',
        'yur': '1,30',
        'item_vat': '0,22',
        'fiz_home': '1,48',
        'yur_home': 'нет'
    }]


def test_parcel_int():
    assert cost_of_parcel_int(12, 1000, '') == [[{  # Австрия
        'fiz': '65,65',
        'yur': '78,78',
        'item_vat_yur': '13,13',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'sep1': '', }],
        [{'fiz': '65,65',
          'yur': '78,78',
          'for_declared_fiz': '',
          'for_declared_yur': '',
          'item_vat_yur': '13,13',
          'sep1': '', }]]
    assert cost_of_parcel_int(12, 1045, 1.25) == [[{
        'fiz': '73,04',
        'yur': '87,65',
        'item_vat_yur': '14,61',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'sep1': '/', }],
      [{'fiz': '73,04',
        'yur': '87,65',
        'item_vat_yur': '14,61',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'sep1': '/', }]]


def test_parcel_int2():
    assert cost_of_parcel_int(225, 26000, '') == [[{  # Экваториальная Гвинея
        'fiz': '862,70',
        'yur': '1035,24',
        'item_vat_yur': '172,54',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'sep1': '', }],
        [{'fiz': '1108,40',
            'yur': '1330,08',
            'item_vat_yur': '221,68',
            'for_declared_fiz': '',
            'for_declared_yur': '',
            'sep1': '', }]]


def test_express_parcel():  # 4 зона P12 - P1 Орша - Брест
    """
    (zone, weight, declared_value, delivery, notification, fragile)
    """
    assert find_documents_cost(4, 1750, 0, 1, 4, "None") == [
        [{'fiz': '10,80',
          'for_declared_yur': '-',
          'item_vat': '2,16',
          'notification': '',
          'yur': '12,96'}],
        [{'fiz': '12,50',
          'for_declared_yur': '-',
          'item_vat': '2,50',
          'notification': '',
          'yur': '15,00'}]]
    assert find_documents_cost(4, 1750, 10.75, 1, 4, "None") == [
        [{'fiz': '11,19',
          'for_declared_yur': '0,38',  # С ОЦ физлица также 3,6%
          'item_vat': '2,22',
          'notification': '',
          'yur': '13,34'}],
        [{'fiz': '12,89',
          'for_declared_yur': '0,38',
          'item_vat': '2,56',
          'notification': '',
          'yur': '15,38'}]]
    assert find_goods_cost(5, 21750, 0, 1, 4, "None") == [  # P30-P13 Дубровно-Кобрин
        [{'fiz': '43,75',
          'for_declared_yur': '-',
          'item_vat': '8,75',
          'notification': '',
          'yur': '52,50'}],
        [{'fiz': '47,60',
          'for_declared_yur': '-',
          'item_vat': '9,52',
          'notification': '',
          'yur': '57,12'}]]
    assert find_goods_cost(5, 21750, 12.58, 1, 4, "None") == [  # P30-P13 Дубровно-Кобрин
        [{'fiz': '44,20',
          'for_declared_yur': '0,46',  # сделать ОЦ для физ и юр отдельно?
          'item_vat': '8,83',
          'notification': '',
          'yur': '52,96'}],
        [{'fiz': '48,05',
          'for_declared_yur': '0,46',
          'item_vat': '9,60',
          'notification': '',
          'yur': '57,58'}]]


def test_letter_int():
    assert cost_of_letter_int(1045, 1.25, 12) == [
        [{'fiz': '56,40',
          'yur': '56,40',
          'item_vat_yur': '9,40',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '85,20',
          'yur': '85,20',
          'item_vat_yur': '14,20',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '99,00', 'yur': '99,00', 'item_vat': '16,50'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '101,75',
          'yur': '101,75',
          'for_declared': '0,05',
          'item_vat_yur': '16,96',
          'rub': ' руб.',
          'tracking': 'да',
          }]
    ]

"""
Здесь не должно быть с ОЦ
"""


def test_letter_int2():
    assert cost_of_letter_int(40, 0, 162) == [
        [{'fiz': '4,20',
          'yur': '4,20',
          'item_vat_yur': '0,70',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '5,40',
          'yur': '5,40',
          'item_vat_yur': '0,90',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '18,00', 'yur': '18,00', 'item_vat': '3,00'}],
        [{'fiz': '19,20', 'yur': '19,20', 'item_vat': '3,20'}],
        [{'fiz': '-'}],
        [{'fiz': '-',
          }]
    ]


def test_package_int():
    assert cost_of_package_int(11, 1045) == [  # в Австралию - destination 11
        [{'fiz': '88,35', 'yur': '88,36', 'item_vat': '14,73'}],
        [{'fiz': '88,35', 'yur': '88,36', 'item_vat': '14,73'}],
        [{'fiz': '94,41', 'yur': '94,42', 'item_vat': '15,74'}],  # tracked_priority
    ]


def test_package_int2():
    assert cost_of_package_int(162, 1035) == [  # в Россию - destination 162
        [{'fiz': '29,61', 'yur': '29,62', 'item_vat': '4,94'}],
        [{'fiz': '43,47', 'yur': '43,48', 'item_vat': '7,25'}],
        [{'fiz': '49,53', 'yur': '49,54', 'item_vat': '8,26'}],
    ]


def test_package_int3():
    assert cost_of_package_int(165, 1860) == [  # в США - destination 165
        [{'fiz': '129,75', 'yur': '129,76', 'item_vat': '21,63'}],
        [{'fiz': '140,01', 'yur': '140,02', 'item_vat': '23,34'}],
        [{'fiz': '146,07', 'yur': '146,08', 'item_vat': '24,35'}],
    ]


def test_package_int4():
    assert cost_of_package_int(92, 1860) == [  # в Канаду - destination 92
        [{'fiz': '108,96', 'yur': '108,96', 'item_vat': '18,16'}],
        [{'fiz': '108,96', 'yur': '108,96', 'item_vat': '18,16'}],
        [{'fiz': '115,02', 'yur': '115,02', 'item_vat': '19,17'}],
    ]


def test_package_int5():
    assert cost_of_package_int(132, 1860) == [  # в Мексику - destination 132
        [{'fiz': '106,86', 'yur': '106,86', 'item_vat': '17,81'}],
        [{'fiz': '106,86', 'yur': '106,86', 'item_vat': '17,81'}],
        [{'fiz': '112,92', 'yur': '112,92', 'item_vat': '18,82'}],
    ]


def test_ems_int():
    assert cost_of_ems_int(153, 1035, 12.24) == [  # в Москву- destination 153
        [{'fiz': '61,16', 'yur': '61,16', 'item_vat': '10,19', 'for_declared': '0,44'}],
        [{'fiz': '63,86', 'yur': '63,86', 'item_vat': '10,64', 'for_declared': '0,44'}]
    ]
    assert cost_of_ems_int(194, 1035, 12.24) == [  # Украина - destination 194
        [{'fiz': "отправления не принимаются"}],
        [{'fiz': "отправления не принимаются"}]
    ]
    assert cost_of_ems_int(113, 1520, 12.24) == [  # Ливия - destination 113
        [{'fiz': '128,24', 'yur': '128,24', 'item_vat': '21,37', 'for_declared': '0,44'}],
        [{'fiz': '131,24', 'yur': '131,24', 'item_vat': '21,87', 'for_declared': '0,44'}]
    ]


"""
написать тест емс с весом ниже 500
"""
