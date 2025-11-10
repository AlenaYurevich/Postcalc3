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
        'fiz': '4,40',
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
        'fiz': '4,44',
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
        'fiz': '5,28',
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
        'fiz': '5,42',
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
        'fiz': '5,69',
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


def test_parcel2():
    assert cost_of_parcel(3500, '', 4) == [{
        'fiz': '7,38',
        'yur': '8,98',
        'item_vat_yur': '1,50',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'tracking': 'да',
        'rub': " руб.",
        'sep1': '',
        'sep2': '/',
        'notification': ""
    }]
    assert cost_of_parcel(3500, 10, 4) == [{
        'fiz': '7,68',
        'yur': '9,34',
        'item_vat_yur': '1,56',
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
        'fiz': '10,17',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(6545, 50.00, 4) == [{
        'fiz': '10,17',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': ""
    }]
    assert cost_of_parcel_3_4_5(915, 1.25, 3) == [{
        'fiz': '5,04',
        'for_declared': '0,50',
        'rub': " руб.",
        'notification': "0,54"
    }]


def test_parcel_qr():
    assert cost_of_parcel_qr(6545, 1.55, 3) == [{
        'fiz': '5,54',
        'yur': '6,54',
        'item_vat_yur': '1,09',
        'for_declared_fiz': '0,50',
        'for_declared_yur': '0,60',
        'rub': " руб.",
        'sep1': '/',
        'sep2': '/',
        'notification': '0,54',
        'tracking': 'да',
    }]


def test_internal_transfer():
    assert cost_of_internal_transfer(35.85) == [{
        'fiz': '1,08',
        'yur': '1,30',
        'item_vat': '0,22',
        'fiz_home': '1,43',
        'yur_home': 'нет'
    }]


def test_parcel_int():
    assert cost_of_parcel_int(12, 1000, '') == [[{
        'fiz': '62,10',
        'yur': '74,52',
        'item_vat_yur': '12,42',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'sep1': '', }],
        [{'fiz': '63,65',
          'yur': '76,38',
          'for_declared_fiz': '',
          'for_declared_yur': '',
          'item_vat_yur': '12,73',
          'sep1': '', }]]
    assert cost_of_parcel_int(12, 1045, 1.25) == [[{
        'fiz': '68,85',
        'yur': '82,62',
        'item_vat_yur': '13,77',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'sep1': '/', }],
      [{'fiz': '70,40',
        'yur': '84,48',
        'item_vat_yur': '14,08',
        'for_declared_fiz': '0,04',
        'for_declared_yur': '0,05',
        'sep1': '/', }]]


def test_parcel_int2():
    assert cost_of_parcel_int(225, 26000, '') == [[{  # Экваториальная Гвинея
        'fiz': '788,60',
        'yur': '946,32',
        'item_vat_yur': '157,72',
        'for_declared_fiz': '',
        'for_declared_yur': '',
        'sep1': '', }],
        [{'fiz': "Макс. вес 20 кг", 'yur': "-", 'item_vat_yur': "-", 'for_declared': "-"}]]


def test_express_parcel():  # 4 зона P12 - P1 Орша - Брест
    """
    (zone, weight, declared_value, delivery, notification, fragile)
    """
    assert find_documents_cost(4, 1750, 0, 1, 4, "None") == [
        [{'fiz': '9,80',
          'for_declared_yur': '-',
          'item_vat': '1,96',
          'notification': '',
          'yur': '11,76'}],
        [{'fiz': '11,35',
          'for_declared_yur': '-',
          'item_vat': '2,27',
          'notification': '',
          'yur': '13,62'}]]
    assert find_documents_cost(4, 1750, 10.75, 1, 4, "None") == [
        [{'fiz': '10,19',
          'for_declared_yur': '0,38',  # С ОЦ физлица также 3,6%
          'item_vat': '2,02',
          'notification': '',
          'yur': '12,14'}],
        [{'fiz': '11,74',
          'for_declared_yur': '0,38',
          'item_vat': '2,33',
          'notification': '',
          'yur': '14,00'}]]
    assert find_goods_cost(5, 21750, 0, 1, 4, "None") == [  # P30-P13 Дубровно-Кобрин
        [{'fiz': '39,75',  # не поменялось
          'for_declared_yur': '-',
          'item_vat': '7,95',
          'notification': '',
          'yur': '47,70'}],
        [{'fiz': '43,25',
          'for_declared_yur': '-',
          'item_vat': '8,65',
          'notification': '',
          'yur': '51,90'}]]
    assert find_goods_cost(5, 21750, 12.58, 1, 4, "None") == [  # P30-P13 Дубровно-Кобрин
        [{'fiz': '40,20',
          'for_declared_yur': '0,46',  # сделать ОЦ для физ и юр отдельно?
          'item_vat': '8,03',
          'notification': '',
          'yur': '48,16'}],
        [{'fiz': '43,70',
          'for_declared_yur': '0,46',
          'item_vat': '8,73',
          'notification': '',
          'yur': '52,36'}]]


def test_letter_int():
    assert cost_of_letter_int(1045, 1.25, 12) == [
        [{'fiz': '50,88',
          'yur': '50,88',
          'item_vat_yur': '8,48',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '77,34',
          'yur': '77,34',
          'item_vat_yur': '12,89',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '88,92', 'yur': '88,92', 'item_vat': '14,82'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '91,13',
          'yur': '91,13',
          'for_declared': '0,05',
          'item_vat_yur': '15,19',
          'rub': ' руб.',
          'tracking': 'да',
          }]
    ]


def test_letter_int2():
    assert cost_of_letter_int(40, 0, 162) == [
        [{'fiz': '50,88',
          'yur': '50,88',
          'item_vat_yur': '8,48',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': '77,34',
          'yur': '77,34',
          'item_vat_yur': '12,89',
          'for_declared': '',
          'rub': " руб.",
          'tracking': "нет", }],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '88,92', 'yur': '88,92', 'item_vat': '14,82'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '91,13',
          'yur': '91,13',
          'for_declared': '0,05',
          'item_vat_yur': '15,19',
          'rub': ' руб.',
          'tracking': 'да',
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
        [{'fiz': '55,64', 'yur': '55,64', 'item_vat': '9,27', 'for_declared': '0,44'}],
        [{'fiz': '58,10', 'yur': '58,10', 'item_vat': '9,68', 'for_declared': '0,44'}]
    ]
    assert cost_of_ems_int(194, 1035, 12.24) == [  # Украина - destination 194
        [{'fiz': "отправления не принимаются"}],
        [{'fiz': "отправления не принимаются"}]
    ]
    assert cost_of_ems_int(113, 1520, 12.24) == [  # Ливия - destination 113
        [{'fiz': '128,24', 'yur': '128,24', 'item_vat': '21,37', 'for_declared': '0,44'}],
        [{'fiz': '131,24', 'yur': '131,24', 'item_vat': '21,87', 'for_declared': '0,44'}]
    ]
