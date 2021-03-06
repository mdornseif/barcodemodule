import unittest
import _barcode



class moduleFunctionality(unittest.TestCase):

    constants = ['BARCODE_128', 'BARCODE_128B', 'BARCODE_128C',
    'BARCODE_128RAW', 'BARCODE_39', 'BARCODE_93', 'BARCODE_ANY',
    'BARCODE_CBR', 'BARCODE_DEFAULT_FLAGS', 'BARCODE_EAN',
    'BARCODE_ENCODING_MASK', 'BARCODE_I25', 'BARCODE_ISBN',
    'BARCODE_MSI', 'BARCODE_NO_ASCII', 'BARCODE_NO_CHECKSUM',
    'BARCODE_OUTPUT_MASK', 'BARCODE_OUT_EPS', 'BARCODE_OUT_NOHEADERS',
    'BARCODE_OUT_PCL', 'BARCODE_OUT_PCL_III', 'BARCODE_OUT_PS',
    'BARCODE_PLS', 'BARCODE_UPC']

    t = ["123456789012",
         "1234567890128",
         "1234567",
         "12345670 12345",
         "123456789012 12",
         "123456789012 12345",
         "01234567890",
         "012345678905",
         "012345",
         "01234567890 12",
         "01234567890 12345",
         "0123456 12",
         "1-56592-292-1",
         "3-89721-122-X",
         "3-89721-122-X 06900"]
    

    def testModuleConstants(self):
        for x in self.constants:
            self.failUnlessEqual(eval("_barcode.%s" % x), _barcode.__dict__[x])
            
    def testVersionFunction(self):
        self.failUnlessEqual(_barcode.version(), 9800)

    def testEncodeFunction(self):
        someTestValues = {'012345': ('9a1a11232221221214112311a2c11a1a1a',
                                     '0:10:0 12:12:0 19:12:1 26:12:2 33:12:3 40:12:4 47:12:5 64:10:7',
                                     'UPC-E'),
                          '0123456 12': ('0a1a32112221212214111a1a11132123111141231a1a+91122221112122',
                                         '3:12:0 10:12:1 17:12:2 24:12:3 36:12:4 43:12:5 50:12:6 57:12:5 + 77:12:1 86:12:2',
                                         'EAN-8'),
                          '01234567890': ('9a1a3b1a222121221411113212311a1a111141312121331123211a2c1a1a',
                                          '0:10:0 19:12:1 26:12:2 33:12:3 40:12:4 47:12:5 59:12:6 66:12:7 73:12:8 80:12:9 87:12:0 107:10:5',
                                          'UPC-A'),
                          '01234567890 12': ('9a1a3b1a222121221411113212311a1a111141312121331123211a2c1a1a+91122221112122',
                                             '0:10:0 19:12:1 26:12:2 33:12:3 40:12:4 47:12:5 59:12:6 66:12:7 73:12:8 80:12:9 87:12:0 107:10:5 + 117:12:1 126:12:2',
                                             'UPC-A'),
                          '01234567890 12345': ('9a1a3b1a222121221411113212311a1a111141312121331123211a2c1a1a+91121222112122111141111132111231',
                                                '0:10:0 19:12:1 26:12:2 33:12:3 40:12:4 47:12:5 59:12:6 66:12:7 73:12:8 80:12:9 87:12:0 107:10:5 + 117:12:1 126:12:2 135:12:3 144:12:4 153:12:5',
                                                'UPC-A'),
                          '012345678905': ('9a1a2221212214111132123111141a1a1131212133112321112313211a1a',
                                           '0:12:0 12:12:1 19:12:2 26:12:3 33:12:4 40:12:5 47:12:6 59:12:7 66:12:8 73:12:9 80:12:0 87:12:5 94:12:0',
                                           'EAN-13'),
                          '1-56592-292-1': ('9a1a1312312112221231411112311a1a1311221222122311221222221a1a',
                                            '0:12:9 12:12:7 19:12:8 26:12:1 33:12:5 40:12:6 47:12:5 59:12:9 66:12:2 73:12:2 80:12:9 87:12:2 94:12:1',
                                            'ISBN'),
                          '1234567': ('0a1a22212122141111321a1a11231111413123211a1a',
                                      '3:12:1 10:12:2 17:12:3 24:12:4 36:12:5 43:12:6 50:12:7 57:12:0',
                                      'EAN-8'),
                          '12345670 12345': ('0a1a22212122141111321a1a11231111413123211a1a+91121222112122111141111132111231',
                                             '3:12:1 10:12:2 17:12:3 24:12:4 36:12:5 43:12:6 50:12:7 57:12:0 + 77:12:1 86:12:2 95:12:3 104:12:4 113:12:5',
                                             'EAN-8'),
                          '123456789012': ('9a1a2122141123111231411121311a1a1121331123211222121221213a1a',
                                           '0:12:1 12:12:2 19:12:3 26:12:4 33:12:5 40:12:6 47:12:7 59:12:8 66:12:9 73:12:0 80:12:1 87:12:2 94:12:8',
                                           'EAN-13'),
                          '123456789012 12': ('9a1a2122141123111231411121311a1a1121331123211222121221213a1a+91122221112122',
                                              '0:12:1 12:12:2 19:12:3 26:12:4 33:12:5 40:12:6 47:12:7 59:12:8 66:12:9 73:12:0 80:12:1 87:12:2 94:12:8 + 117:12:1 126:12:2',
                                              'EAN-13'),
                          '123456789012 12345': ('9a1a2122141123111231411121311a1a1121331123211222121221213a1a+91121222112122111141111132111231',
                                                 '0:12:1 12:12:2 19:12:3 26:12:4 33:12:5 40:12:6 47:12:7 59:12:8 66:12:9 73:12:0 80:12:1 87:12:2 94:12:8 + 117:12:1 126:12:2 135:12:3 144:12:4 153:12:5',
                                                 'EAN-13'),
                          '1234567890128': ('9a1a2122141123111231411121311a1a1121331123211222121221213a1a',
                                            '0:12:1 12:12:2 19:12:3 26:12:4 33:12:5 40:12:6 47:12:7 59:12:8 66:12:9 73:12:0 80:12:1 87:12:2 94:12:8',
                                            'EAN-13'),
                          '3-89721-122-X': ('9a1a1312312111411213211313121a1a1212222212221212221221411a1a',
                                            '0:12:9 12:12:7 19:12:8 26:12:3 33:12:8 40:12:9 47:12:7 59:12:2 66:12:1 73:12:1 80:12:2 87:12:2 94:12:3',
                                            'ISBN'),
                          '3-89721-122-X 06900': ('9a1a1312312111411213211313121a1a1212222212221212221221411a1a+91121123111114112113113211113211',
                                                  '0:12:9 12:12:7 19:12:8 26:12:3 33:12:8 40:12:9 47:12:7 59:12:2 66:12:1 73:12:1 80:12:2 87:12:2 94:12:3 + 117:12:0 126:12:6 135:12:9 144:12:0 153:12:0',
                                                  'ISBN')}
        
        
        for x, y in someTestValues.items():
            self.failUnlessEqual(_barcode.encode(_barcode.BARCODE_ANY, x), y)

            
    def testLegalEncodings(self):
        someTestValues = {_barcode.BARCODE_EAN: ("123456789012",
                                                "1234567890128",
                                                "1234567",
                                                "12345670 12345",
                                                "123456789012 12",
                                                "123456789012 12345"),
                          _barcode.BARCODE_UPC: ("01234567890",
                                                "012345678905",
                                                "012345",
                                                "01234567890 12",
                                                "01234567890 12345"),
                          _barcode.BARCODE_ISBN: ("1-56592-292-1",
                                                 "3-89721-122-X",
                                                 "3-89721-122-X 06900"),
                          _barcode.BARCODE_128B: ('space (32) to DEL (127)',),
                          #  The encoder refuses to deal with an odd number of digits
                          _barcode.BARCODE_128C: ('1234567890',),
                          _barcode.BARCODE_128: ('\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r',
                                                 '\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19',
                                                 '\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789',
                                                 ':;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`',
                                                 'abcdefghijklmnopqrstuvwxyz{|}~\x7f',
                                                 '\x80\xc1\xc2\xc3\xc4'),
                          # this provokes a vrash in libbarcode 0.98
                          #_barcode.BARCODE_128RAW: ('0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18',
                          #                          '19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34',
                          #                          '35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50',
                          #                          '51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66',
                          #                          '67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82',
                          #                          '83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98',
                          #                          '99 100 101 102 103 104 105'),
                          _barcode.BARCODE_39: ('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ-. *$/+%',),
                          _barcode.BARCODE_93: ('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%',),
                          # This encoding can only represent an even number of digits
                          _barcode.BARCODE_I25: ('1234567890',),
                          _barcode.BARCODE_CBR: ('0123456789-$:/.+', 'A0123456789-$:/.+B', 'C0123456789-$:/.+D'),
                          _barcode.BARCODE_PLS: ('0123456789ABCDEF',),
                          _barcode.BARCODE_MSI: ('0123456789',)}

        for enctype, l in someTestValues.items():
            for x in l:
                _barcode.encode(enctype, x)

    def testOddNrIfDigitsError(self):
        self.failUnlessRaises(RuntimeError, _barcode.encode, _barcode.BARCODE_128C, '12345678901')
        # No Idea why this fails
        #self.failUnlessRaises(RuntimeError, _barcode.encode, _barcode.BARCODE_I25, '12345678901')


 
unittest.main()
