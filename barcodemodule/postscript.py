# $Id: postscript.py,v 1.1 2002/07/22 22:08:16 drt Exp $ 
 
# Python renderer for GNU barcode intermediate representation to Postscript
# --md@hudora.de

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
SHRINK_AMOUNT = 0.15



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

_rcsid = "$Id: postscript.py,v 1.1 2002/07/22 22:08:16 drt Exp $"

from _barcode import *

def drawToFile(bc, filename):
    """Write barcode to Postscript file <filename>."""
    
    fd = open(filename, 'w')
    Barcode_ps_print(bc, fd)
    fd.close()


def Barcode_ps_print(bc, f):
    """This is an 1:1 port of the libbarcode renderer written in C"""

    fsav=0
    # text below bars
    mode = '-'


    scalef = 1.0

    if not self.partial or not self.textinfo:
        raise ValueError, "No data set to be rendered"

    # Maybe this first part can be made common to several printing back-ends,
    # we'll see how that works when other ouput engines are added

    # First, calculate barlen
    barlen = int(self.partial[0])
    for c in self.partial[1:]:
        if c.isdigit():
            barlen += int(c)
        elif c.islower():
            barlen += ord(c) - ord('a') + 1

    # The scale factor depends on bar length 
    #scalef = width_requested / barlen
    if not self.scalef:
        if not self.width:
            # default 
            self.width = barlen
        self.scalef = self.width / float(barlen)

    # The width defaults to "just enough" 
    if not self.width:
        self.width = barlen * scalef + 1

    # But it can be too small, in this case enlarge and center the area 
    if self.width < barlen * scalef:
        wid = barlen * scalef + 1
        self.xoff = self.xoff - ((wid - self.width) / 2)
        self.width = wid
        # Can't extend too far on the left
        if self.xoff < 0:
            self.width = self.width + (-self.xoff)
            self.xoff = 0

    # The height defaults to 80 points (rescaled) 
    height = 80 * scalef
    if not self.height:
        self.height = 80 * scalef

    # alternative implementation
    # /* If too small (5 + text), enlarge and center */
    # i = 5 + 10 * ((bc->flags & BARCODE_NO_ASCII)==0);
    # if (bc->height < i * scalef ) {
    #     int hei = i * scalef;
    #     bc->yoff -= (hei-bc->height)/2;
    #     bc->height = hei;
    #     if (bc->yoff < 0) {
    #         bc->height += -bc->yoff;
    #         bc->yoff = 0;
    #     }
    # }

    # If too small (5 + text), reduce the scale factor and center
    i = 5 + 10 * ((self.flags & _barcode.BARCODE_NO_ASCII)==0)
    if self.height < i * scalef:
        scaleg = float(self.height) / i
        wid = self.width * scaleg / scalef
        self.xoff += self.xoff + ((self.width - wid) / 2)
        self.width = wid
        self.scalef = scaleg


    # Ok, then deal with actual ps (eps) output
    if  not (bc.flags & BARCODE_OUT_NOHEADERS):
        # spit a header first 
	if bc.flags & BARCODE_OUT_EPS:
	    f.write("%%!PS-Adobe-2.0 EPSF-1.2\n")
	else:
            f.write("%%!PS-Adobe-2.0\n")
	f.write("%%%%Creator: libbarcode\n");
        if bc.flags & BARCODE_OUT_EPS:
	    f.write("%%%%%%%%BoundingBox: %i %i %i %i\n" %
		    (bc.xoff,
		    bc.yoff,
		    bc.xoff + bc.width + 2 * bc.margin,
		    bc.yoff + bc.height + 2 * bc.margin))
	f.write("%%%%EndComments\n")
	if bc.flags & BARCODE_OUT_PS:
	    f.write("%%%%EndProlog\n\n")
	    f.write("%%%%Page: 1 1\n\n")

    # some basic information
    f.write("%%%% Printing barcode for %r, scaled %5.2f, encoded using %s\n" % (bc.ascii, bc.scalef, bc.encoding))
    f.write("%% The space/bar succession is represented by the following widths (space first):\n%% ")
    for c in bc.partial:
        if c.isdigit():
            f.write(c)
	if c.islower():
            f.write(str(ord(c) - ord('a') + ord('1')))
	if c.isupper():
            f.write(str(ord(c) - ord('A') + ord('1')))
            
    f.write("\n%%%% Which means in raw encoding:\n%%%% %r\n" % bc.partial)

    # open array for "forall" 
    f.write("\n[\n%%  height  xpos   ypos  width       height  xpos   ypos  width\n")

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
                    
            # Define an array and then use "forall" (Hans Schou) 
            f.write("   [%5.2f %6.2f %6.2f %5.2f]\n" % (yr, x0, y0, (j * bc.scalef) - SHRINK_AMOUNT))
	xpos += j * bc.scalef

    f.write("\n]\t{ {} forall setlinewidth moveto 0 exch rlineto stroke} bind forall\n\n\n")


    ########################################

    # Then, the text

    # reinstantiate default
    mode = '-'

    if not (bc.flags & BARCODE_NO_ASCII):
	f.write("[\n%%%%   char    xpos   ypos fontsize\n")
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
            # if (sscanf(ptr, "%lf:%lf:%c", &f1, &f2, &c) != 3) 
            #f1 = 'xposition'
            #f2 = 'fontsize'
            #c = 'char'
            xposition = int(m.group('xposition'))
            fontsize = int(m.group('fontsize'))
            char = m.group('char')
                
            f.write("    [(")
	    #  Both the backslash and the two parens are special
            if char == '\\' or char == ')' or  char == '(': 
		f.write("\\%s) " % char)
	    else:
		f.write("%s) " % char)
            if mode == '-':
                ytval = bc.yoff + bc.margin
            else:
                ytval = bc.yoff + bc.margin + bc.height - 8 * bc.scalef

            if fsav == fontsize:
                ftval = 0.0
            else:
                ftval = fontsize * bc.scalef
                
            f.write("%6.2f %6.2f %5.2f]\n" % (bc.xoff + xposition * bc.scalef + bc.margin,
                                              ytval, ftval))
	    fsav = fontsize
        f.write("]   { {} forall dup 0.00 ne {\n\t/Helvetica findfont exch scalefont setfont\n    } {pop} ifelse\n    moveto show} bind forall\n")

    f.write("%%%% End barcode for %r\n\n" % bc.ascii)

    if not (bc.flags & BARCODE_OUT_NOHEADERS):
        if bc.flags & BARCODE_OUT_PS:
            f.write("showpage\n")
	    f.write("%%%%%%%%Trailer\n\n")


