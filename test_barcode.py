import barcode
b = barcode.Barcode("3-930673-57-6 04900")
#b = barcode.Barcode("HUDORA Test Barcode: T1VVVVSS T1KKKKK-DDD")
b.encode()
b.scale()

import barcode.rl
import barcode.postscript
import barcode.pdf
import sys

barcode.pdf.drawToFile(barcode.rl.draw_barcode(b),  'test.pdf')

#barcode.postscript.Barcode_ps_print(b, sys.stdout)
