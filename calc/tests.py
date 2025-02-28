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
        'fiz': '4,00',
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
        'fiz': '4,04',
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
        'fiz': '4,88',
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


def test_parcel2():
    assert cost_of_parcel(3500, '', 4) == [{
        'fiz': '6,98',
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
        'fiz': '7,28',
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
        'fiz': '4,54',
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
        [{'fiz': '83,40', 'yur': '83,40', 'item_vat': '13,90'}],  # tracked priority
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
        [{'fiz': '88,10', 'yur': '88,10', 'item_vat': '14,68'}],
        [{'fiz': '88,10', 'yur': '88,10', 'item_vat': '14,68'}],
        [{'fiz': '90,49', 'yur': '90,49', 'item_vat': '15,08'}],  # tracked_priority
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '96,01', 'yur': '96,01', 'item_vat': '16,00'}]
    ]


def test_package_int2():
    assert cost_of_package_int(162, 1035) == [  # в Россию - destination 162
        [{'fiz': '27,41', 'yur': '27,41', 'item_vat': '4,57'}],
        [{'fiz': '42,58', 'yur': '42,58', 'item_vat': '7,10'}],
        [{'fiz': '46,67', 'yur': '46,67', 'item_vat': '7,78'}],
        [{'fiz': '37,80', 'yur': '37,80', 'item_vat': '6,30'}],
        [{'fiz': '52,19', 'yur': '52,19', 'item_vat': '8,70'}]
    ]


def test_package_int3():
    assert cost_of_package_int(165, 1860) == [  # в США - destination 165
        [{'fiz': '136,79', 'yur': '136,79', 'item_vat': '22,80'}],
        [{'fiz': '147,38', 'yur': '147,38', 'item_vat': '24,56'}],
        [{'fiz': '150,65', 'yur': '150,65', 'item_vat': '25,11'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '156,17', 'yur': '156,17', 'item_vat': '26,03'}]
    ]


def test_package_int4():
    assert cost_of_package_int(92, 1860) == [  # в Канаду - destination 92
        [{'fiz': '108,84', 'yur': '108,84', 'item_vat': '18,14'}],
        [{'fiz': '108,84', 'yur': '108,84', 'item_vat': '18,14'}],
        [{'fiz': '112,76', 'yur': '112,76', 'item_vat': '18,79'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '118,28', 'yur': '118,28', 'item_vat': '19,71'}]
    ]


def test_package_int5():
    assert cost_of_package_int(132, 1860) == [  # в Мексику - destination 132
        [{'fiz': '106,98', 'yur': '106,98', 'item_vat': '17,83'}],
        [{'fiz': '106,98', 'yur': '106,98', 'item_vat': '17,83'}],
        [{'fiz': '110,90', 'yur': '110,90', 'item_vat': '18,48'}],
        [{'fiz': 'Отправления не принимаются'}],
        [{'fiz': '116,42', 'yur': '116,42', 'item_vat': '19,40'}]
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
