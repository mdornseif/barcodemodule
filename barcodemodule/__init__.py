"""Object Oriented Interface to the GNU Barcode Library"""

_rcsid = "$Id: __init__.py,v 1.1 2002/07/22 22:08:16 drt Exp $"

import _barcode
import postscript

flags = {}
for x, y in vars(_barcode).items():
    if x.startswith('BARCODE_'):
        flags[x] = y


class Barcode:
    """Object to wrap arround the GNU barcode library and reportlab.
    
    How do the "partial" and "textinfo" strings work?
    
    The first char in "partial" tells how much extra space to add to the
    left of the bars. For EAN-13, it is used to leave space to print the
    first digit, other codes may have '0' for no-extra-space-needed.
    
    The next characters are alternating bars and spaces, as multiples
    of the base dimension which is 1 unless the code is
    rescaled. Rescaling is calculated as the ratio from the requested
    width and the calculated width.  Digits represent bar/space
    dimensions. Lower-case letters represent those bars that should
    extend lower than the others: 'a' is equivalent to '1', 'b' is '2' and
    so on.

    The "textinfo" string is made up of fields "%lf:%lf:%c" separated by
    blank space. The first integer is the x position of the character,
    the second is the font size (before rescaling) and the char item is
    the charcter to be printed.
    
    Both the "partial" and "textinfo" strings may include "-" or "+" as
    special characters (in "textinfo" the char should be a standalone
    word).  They state where the text should be printed: below the bars
    ("-", default) or above the bars. This is used, for example, to
    print the add-5 and add-2 codes to the right of UPC or EAN codes
    (the add-5 extension is mostly used in ISBN codes.
    """

    def __init__(self, ascii = '', flags = 0):
        self.ascii = ascii
        self.flags = 0
        self.partial = ''
        self.textinfo = ''
        self.encoding = ''
        self.width = 0
        self.height = 0
        self.xoff = 0 
        self.yoff = 0
        self.margin = 10
        self.scalef = 0.0

    def encode(self):
        (self.partial, self.textinfo, self.encoding) = _barcode.encode(self.flags, self.ascii)
        
    def scale(self):
        """Calculate width and height.

        Either or both the code width and the scale factor can be left
        unspecified (i.e., zero). The library deals with defaults in
        the following way:

        Both unspecified
        If both the width and the scale factor are unspecified, the
        scale factor will default to 1.0 and the width is calculated
        according to the actual width of the bar code being printed.

        Width unspecified
        If the width is not specified, it is calculated according to
        the values of scalef.

        Scale factor unspecified
        If the scale factor is not specified, it will be chosen so
        that the generated bar code exactly fits the specified width.

        Both specified
        The code will be printed inside the specified region according
        to the specified scale factor. It will be aligned to the
        left. If, however, the chosen width is too small for the
        specific bar code and scaling factor, then the code will
        extend symmetrically to the left and to the right of the
        chosen region.
        """

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

        

    def __repr__(self):
        return "<barcode object at %s, ascii %r, flags %i>" % (id(self), self.ascii, self.flags)

