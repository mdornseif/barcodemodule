import unittest
import barcode



class moduleFunctionality(unittest.TestCase):

    constants = ['BARCODE_128', 'BARCODE_128B', 'BARCODE_128C',
    'BARCODE_128RAW', 'BARCODE_39', 'BARCODE_93', 'BARCODE_ANY',
    'BARCODE_CBR', 'BARCODE_DEFAULT_FLAGS', 'BARCODE_EAN',
    'BARCODE_ENCODING_MASK', 'BARCODE_I25', 'BARCODE_ISBN',
    'BARCODE_MSI', 'BARCODE_NO_ASCII', 'BARCODE_NO_CHECKSUM',
    'BARCODE_OUTPUT_MASK', 'BARCODE_OUT_EPS', 'BARCODE_OUT_NOHEADERS',
    'BARCODE_OUT_PCL', 'BARCODE_OUT_PCL_III', 'BARCODE_OUT_PS',
    'BARCODE_PLS', 'BARCODE_UPC']

    #'__doc__', '__file__', '__name__',
    #'barcode', 'barcodeType', 'version']

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
            self.failUnlessEqual(eval("barcode.%s" % x), barcode.__dict__[x])
            
    def testVersionFunction(self):
        self.failUnlessEqual(barcode.version(), 9800)

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
            self.failUnlessEqual(barcode.encode(barcode.BARCODE_ANY, x), y)
        
unittest.main()