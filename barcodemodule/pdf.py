# $Id: pdf.py,v 1.1 2002/07/22 22:08:16 drt Exp $

# Python renderer for GNU barcode intermediate representation to
# PNG - based on reportlab

# --md@hudora.de

from barcode import rl
from reportlab.graphics import renderPDF

_rcsid = "$Id: pdf.py,v 1.1 2002/07/22 22:08:16 drt Exp $"


def drawToFile(bc, filename):
    """Write barcode to PDF file <filename>."""
    renderPDF.drawToFile(barcode.rl.draw_barcode(bc), filename)
