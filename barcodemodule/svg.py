# $Id: svg.py,v 1.1 2002/07/22 22:08:16 drt Exp $

# Python renderer for GNU barcode intermediate representation to
# SVG - based on reportlab

# --md@hudora.de

from barcode import rl
from reportlab.graphics import renderSVG

_rcsid = "$Id: svg.py,v 1.1 2002/07/22 22:08:16 drt Exp $"

def drawToFile(bc, filename):
    """Write barcode to SVG file <filename>."""
    renderSVG.drawToFile(barcode.rl.draw_barcode(bc), filename)
