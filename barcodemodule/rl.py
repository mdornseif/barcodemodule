# $Id: rl.py,v 1.1 2002/07/22 22:08:16 drt Exp $ 
 
# Python renderer for GNU barcode intermediate representation to a
# reportlab drawing which can then be further processed to Postscript,
# PDF, SVG or PNG.

from reportlab.lib import colors
from reportlab.graphics.shapes import *

# Based on:
# ps.c -- printing the "partial" bar encoding
#
# Copyright (c) 1999 Alessandro Rubini (rubini@gnu.org)
# Copyright (c) 1999 Prosa Srl. (prosa@prosa.it)
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import re

# shrink the bars to account for ink spreading
SHRINK_AMOUNT = 0.05
#SHRINK_AMOUNT = 0.15

# How do the "partial" and "textinfo" strings work?
# 
# The first char in "partial" tells how much extra space to add to the
# left of the bars. For EAN-13, it is used to leave space to print the
# first digit, other codes may have '0' for no-extra-space-needed.
# 
# The next characters are alternating bars and spaces, as multiples
# of the base dimension which is 1 unless the code is
# rescaled. Rescaling is calculated as the ratio from the requested
# width and the calculated width.  Digits represent bar/space
# dimensions. Lower-case letters represent those bars that should
# extend lower than the others: 'a' is equivalent to '1', 'b' is '2' and
# so on.
# 
# The "textinfo" string is made up of fields "%lf:%lf:%c" separated by
# blank space. The first integer is the x position of the character,
# the second is the font size (before rescaling) and the char item is
# the charcter to be printed.
# 
# Both the "partial" and "textinfo" strings may include "-" or "+" as
# special characters (in "textinfo" the char should be a standalone
# word).  They state where the text should be printed: below the bars
# ("-", default) or above the bars. This is used, for example, to
# print the add-5 and add-2 codes to the right of UPC or EAN codes
# (the add-5 extension is mostly used in ISBN codes.

_rcsid = "$Id: rl.py,v 1.1 2002/07/22 22:08:16 drt Exp $"

from _barcode import *


# This is an 1:1 port of the libbarcode renderer written in C
def draw_barcode(bc):
    """Render the barcode object to a reportlab Drawing.

    The barcode object must be already encoded ans scaled."""
    
    fsav=0
    # text below bars
    mode = '-'

    #if bc.flags & BARCODE_OUT_EPS:
    d = Drawing(bc.width + 2 * bc.margin, bc.height + 2 * bc.margin)

    xpos = bc.margin + int(bc.partial[0]) * bc.scalef
    i = 0
    for c in bc.partial[1:]:
        i = i + 1
	# special cases: '+' and '-' 
        if c  == '+' or c == '-':
            # don't count it
            i = i - 1
	    mode = c
            continue

	# j is the width of this bar/space 
        if c.isdigit():
            j = ord(c) - ord('0')
	else:
            j = ord(c) - ord('a') + 1
        if i % 2:
            # we have a bar
            x0 = bc.xoff + xpos + (j * bc.scalef) / 2.0
            y0 = bc.yoff + bc.margin
            yr = bc.height
            if not (bc.flags & BARCODE_NO_ASCII):
                # leave space for text
                if mode == '-':
                    # text below bars: 10 points or five points 
                    if c.isdigit():
                        y0 += 10 * bc.scalef
                        yr -= 10 * bc.scalef
                    else:
                        y0 += 5 * bc.scalef
                        yr -= 5 * bc.scalef
                elif mode == '+':
                    # text above bars: 10 or 0 from bottom, and 10 from top
                    if c.isdigit():
                        y0 += 10 * bc.scalef
                        yr -= 20 * bc.scalef
                    else:
                        y0 += 0 
                        yr -= 10 * bc.scalef
                    
            d.add(Line(x0, y0, x0, y0 + yr, strokeWidth=((j * bc.scalef) - SHRINK_AMOUNT)))
	xpos += j * bc.scalef



    ########################################

    # Then, the text

    # reinstantiate default
    mode = '-'

    if not (bc.flags & BARCODE_NO_ASCII):
        # k is the "previous font size" 
        k = 0
        for c in bc.textinfo.split(' '):
            c = c.strip()
            if not c:
                continue
            if c == '+' or c == '-':
                mode = c
                continue

            m = re.match(r"(?P<xposition>\d+):(?P<fontsize>\d+):(?P<char>.?)", c)
            if not m:
                raise RuntimeError, "barcodemodule: impossible data: %r" % c
            xposition = int(m.group('xposition'))
            fontsize = int(m.group('fontsize'))
            char = m.group('char')
                
            if mode == '-':
                ytval = bc.yoff + bc.margin
            else:
                ytval = bc.yoff + bc.margin + bc.height - 8 * bc.scalef

            if fsav == fontsize:
                ftval = 0.0
            else:
                ftval = fontsize * bc.scalef
                
            d.add(String((bc.xoff + xposition + 1.5) * bc.scalef + bc.margin, ytval, char, fontsize=ftval, fontName='Helvetica'))
	    fsav = fontsize

    return d

