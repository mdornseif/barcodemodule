# $Id: postscriptrl.py,v 1.1 2002/07/22 22:08:16 drt Exp $ 
 
# Python renderer for GNU barcode intermediate representation to
# Postscript - based on reportlab

# --md@hudora.de

import barcode.rl
from reportlab.graphics import renderPS

_rcsid = "$Id: postscriptrl.py,v 1.1 2002/07/22 22:08:16 drt Exp $"

def drawToFile(bc, filename):
    """Write barcode to Postscript file <filename>."""
    renderPS.drawToFile(barcode.rl.draw_barcode(bc), filename)
