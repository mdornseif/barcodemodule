/* $Id: _barcodemodule.c,v 1.2 2002/07/18 21:36:36 drt Exp $ */ 

/* python bindings for the GNU barcode library */

/* barcode objects */

#include "barcode.h"
#include "Python.h"

/* barcode Module functions */

static char module_doc [] = 
"This Module implementes an interface to the GNU barcode library.\n\
\n\
Supported Encodings\n\
\n\
The library encodes text strings. The text representation is\n\
interpreted according to the following rules. When auto-detection of\n\
the encoding is enabled the encoding types are scanned to find one that\n\
can digest the text string. The following list of supported types is\n\
sorted in the same order the library uses when auto-detecting a suitable\n\
encoding for a string.\n\
\n\
EAN\n\
The EAN frontend is similar to UPC; it accepts strings of digits, 12\n\
or 7 characters long. Strings of 13 or 8 characters are accepted if\n\
the provided checksum digit is correct. I expect most users to feed\n\
input without a checksum, though. The add-2 and add-5 extension are\n\
accepted for both the EAN-13 and the EAN-8 encodings. The following\n\
are example of valid input strings: '123456789012' (EAN-13),\n\
'1234567890128' (EAN-13 wih checksum), '1234567' (EAN-8), '12345670\n\
12345' (EAN-8 with checksum and add-5), '123456789012 12' (EAN-13 with\n\
add-2), '123456789012 12345' (EAN-13 with add-5).\n\
\n\
UPC\n\
The UPC frontend accepts only strings made up of digits (and, if a\n\
supplemental encoding is used, a blank to separate it). It accepts\n\
strings of 11 or 12 digits (UPC-A) and 6 or 7 or 8 digits (UPC-E).\n\
\n\
The 12th digit of UPC-A is the checksum and is added by the library if\n\
not specified in the input; if it is specified, it must be the right\n\
checksum or the code is rejected as invalid. For UPC-E, 6 digit are\n\
considered to be the middle part of the code, a leading 0 is assumed and\n\
the checksum is added; 7 digits are either considered the initial part\n\
(leading digit 0 or 1, checksum missing) or the final part (checksum\n\
specified, leading 0 assumed); 8 digits are considered to be the complete\n\
code, with leading 0 or 1 and checksum. For both UPC-A and UPC-E, a\n\
trailing string of 2 digits or 5 digits is accepted as well. Therefore,\n\
the following are examples of valid strings that can be encoded as\n\
UPC: '01234567890' (UPC-A) '012345678905' (UPC-A with checksum),\n\
'012345' (UPC-E), '01234567890 12' (UPC-A, add-2) and '01234567890 12345'\n\
(UPC-A, add-5), '0123456 12' (UPC-E, add-2). Please note that when setting\n\
BARCODE_ANY to auto-detect the encoding to be used, 12-digit strings and\n\
7-digit strings will always be identified as EAN. This because I expect\n\
most user to provide input without a checksum.\n\
\n\
ISBN\n\
ISBN numbers are encoded as EAN-13 symbols, with an optional add-5 trailer.\n\
The ISBN frontend of the library accepts real ISBN numbers and deals with\n\
any hyphen and, if present, the ISBN checksum character before encoding\n\
data. Valid representations for ISBN strings are for example: '1-56592-292-1',\n\
'3-89721-122-X' and '3-89721-122-X 06900'.\n\
\n\
code 128-B\n\
This encoding can represent all of the printing ASCII characters, from the\n\
space (32) to DEL (127). The checksum digit is mandatory in this encoding.\n\
\n\
code 128-C\n\
The 'C' variation of Code-128 uses Code-128 symbols to represent two digit\n\
at a time (Code-128 is made up of 104 symbols whose interpretation is\n\
controlled by the start symbol being used). Code 128-C is thus the most\n\
compact way to represent any even number of digits. The encoder refuses to\n\
deal with an odd number of digits because the caller is expected to provide\n\
proper padding to an even number of digits. (Since Code-128 includes control\n\
symbols to switch charset, it is theoretically possible to represent the odd\n\
digit as a Code 128-A or 128-B symbol, but this tool doesn't currently\n\
implement this option).\n\
\n\
code 128 raw\n\
Code-128 output represented symbol-by-symbol in the input string. To\n\
override part of the problems outlined below in specifying code128\n\
symbols, this pseudo-encoding allows the used to specify a list of\n\
code128 symbols separated by spaces. Each symbol is represented by a\n\
number in the range 0-105. The list should include the leading\n\
character.The checksum and the stop character are automatically added\n\
by the library. Most likely this pseudo-encoding will be used with\n\
BARCODE_NO_ASCII and some external program to supply the printed text.\n\
\n\
code 128\n\
Automatic selection between alphabet A, B and C of the Code-128\n\
standard. This encoding can represent all ASCII symbols, from 0 (NUL)\n\
to 127 (DEL), as well as four special symbols, named F1, F2, F3,\n\
F4. The set of symbols available in this encoding is not easily\n\
represented as input to the barcode library, so the following\n\
convention is used. In the input string, which is a C-language\n\
null-terminated string, the NUL char is represented by the value 128\n\
(0x80, 0200) and the F1-F4 characters are represented by the values\n\
193-196 (0xc1-0xc4, 0301-0304). The values have been chosen to ease\n\
their representation as escape sequences.\n\
\n\
In needed, you can use the 'code 128 raw' pseudo-encoding to\n\
represent code128 symbols by their numerical value. This\n\
encoding is used late in the auto-selection mechanism because (almost)\n\
any input string can be represented using code128.\n\
\n\
code 39\n\
The code-39 standard can encode uppercase letters, digits, the blank\n\
space, plus, minus, dot, star, dollar, slash, percent. Any string that\n\
is only composed of such characters is accepted by the code-39\n\
encoder. To avoid loosing information, the encoder refuses to encode\n\
mixed-case strings (a lowercase string is nonetheless accepted as a\n\
shortcut, but is encoded as uppercase).\n\
\n\
interleaved 2 of 5\n\
This encoding can only represent an even number of digits (odd digits\n\
are represented by bars, and even digits by the interleaving\n\
spaces). The name stresses the fact that two of the five items (bars\n\
or spaces) allocated to each symbol are wide, while the rest are\n\
narrow. The checksum digit is optional (can be disabled via\n\
BARCODE_NO_CHECKSUM). Since the number of digits, including the\n\
checksum, must be even, a leading zero is inserted in the string being\n\
encoded if needed (this is specifically stated in the specs I have\n\
access to).\n\
\n\
Codabar\n\
Codabar can encode the ten digits and a few special symbols (minus, plus,\n\
dollar, colon, bar, dot). The characters 'A', 'B', 'C' and 'D' are used to\n\
represent four different start/stop characters. The input string to the\n\
barcode library can include the start and stop characters or not include them\n\
(in which case 'A' is used as start and 'B' as stop). Start and stop\n\
characters in the input string can be either all lowercase or all uppercase\n\
and are always printed as uppercase.\n\
\n\
Plessey\n\
Plessey barcodes can encode all the hexadecimal digits. Alphabetic\n\
digits in the input string must either be all lowercase or all\n\
uppercase. The output text is always uppercase.\n\
\n\
MSI\n\
MSI can only encode the decimal digits. While the standard specifies\n\
either one or two check digits, the current implementation in this\n\
library only generates one check digit.\n\
\n\
code 93\n\
The code-93 standard can natively encode 48 different characters,\n\
including uppercase letters, digits, the blank space, plus, minus,\n\
dot, star, dollar, slash, percent, as well as five special characters:\n\
a start/stop delimiter and four'shift characters' used for extended encoding.\n\
Using this 'extended encoding' method, any standard 7-bit ASCII character can\n\
be encoded, but it takes up two symbol lengths in barcode if the character is\n\
not natively supported (one of the 48). The encoder here fully implements the\n\
code 93 encoding standard. Any characters natively supported (A-Z, 0-9,\n\
'.+-/$&%') will be encoded as such - for any other characters (such as lower\n\
case letters, brackets, parentheses, etc.), the encoder will revert to\n\
extended encoding. As a note, the option to exclude the checksum will\n\
eliminate the two modulo-47 checksums (called C and K) from the barcode, but\n\
this probably will make it unreadable by 99% of all scanning systems. These\n\
checksums are specified to be used at the firmware level, and their absence\n\
will be interpreted as an invalid barcode.\n\
\n\
";

/*
for some reason "Apple Computer, Inc. version gcc-932.1, based on gcc
version 2.95.2 19991024 (release)" can't compile this while "gcc
version 2.95.3 20010315 (release) [FreeBSD]" can

\n\
Constants for barcode.flags:\n\
BARCODE_128, BARCODE_128B, BARCODE_128C, BARCODE_128RAW, BARCODE_39,\n\
BARCODE_93, BARCODE_ANY, BARCODE_CBR, BARCODE_DEFAULT_FLAGS,\n\
BARCODE_EAN, BARCODE_ENCODING_MASK, BARCODE_I25, BARCODE_ISBN,\n\
BARCODE_MSI, BARCODE_NO_ASCII, BARCODE_NO_CHECKSUM,\n\
BARCODE_OUTPUT_MASK, BARCODE_OUT_EPS, BARCODE_OUT_NOHEADERS,\n\
BARCODE_OUT_PCL, BARCODE_OUT_PCL_III, BARCODE_OUT_PS,BARCODE_PLS,\n\
BARCODE_UPC\n";
*/



static char barcode_version_doc [] = "version()\n\
\n\
Return version of libbarcode as an integer.\n";

static PyObject *
barcode_version(PyObject *self, PyObject *args)
{
  return PyInt_FromLong((long) Barcode_Version(NULL));
}


static char barcode_encode_doc [] =
"encode(flags, ascii)\n\
\n\
Encode ascii to an barcode intermediate representation.\n\
\n\
Return a tuple (partial, textinfom encoding)\n\
\n\
\n\
ascii    -- input to be converted to barcode.\n\
\n\
flags    -- flags used th create the barcodes.\n\
\n\
            BARCODE_ANY\n\
            Choose the best suited encoding type. You also can specify\n\
            any of BARCODE_EAN, BARCODE_UPC, BARCODE_ISBN,\n\
            BARCODE_128B, BARCODE_128C, BARCODE_128, BARCODE_128RAW,\n\
            BARCODE_39, BARCODE_I25, BARCODE_CBR, BARCODE_MSI,\n\
            BARCODE_PLS, BARCODE_93. See module docstring for further\n\
            information.\n\
\n\
            BARCODE_NO_CHECKSUM\n\
            Instructs the engine not to add the checksum character to\n\
            the output. Not all the encoding types can drop the\n\
            checksum; those where the checksum is mandatory (like EAN\n\
            and UPC) just ignore the flag.\n\
\n\
            BARCODE_OUTPUT_MASK\n\
            The mask is used to extract the output-type identifier\n\
            from the flags field.\n\
\n\
partial  -- intermediate representation of the bars. (read-only)\n\
            The first char in partial tells how much extra space to\n\
            add to the left of the bars. For EAN-13, it is used to\n\
            leave space to print the first digit, other codes may have\n\
            '0' for no-extra-space-needed.\n\
\n\
            The next characters are alternating bars and spaces, as\n\
            multiples of the base dimension which is 1 unless the code\n\
            is rescaled. Rescaling is calculated as the ratio from the\n\
            requested width and the calculated width. Digits represent\n\
            bar/space dimensions. Lower-case letters represent those\n\
            bars that should extend lower than the others: 'a' is\n\
            equivalent to '1', 'b' is '2' and so on up to 'i' which is\n\
            equivalent to '9'. Other letters will be used for\n\
            encoding-specific meanings, as soon as I implement them.\n\
\n\
textinfo -- the text to be printed along with the barcode. (read-only)\n\
            The textinfo string is made up of fields %lf:%lf:%c\n\
            separated by blank space. The first integer is the x\n\
            position of the character, the second is the font size\n\
            (before rescaling) and the char item is the character to\n\
            be printed.\n\
\n\
            Both the partial and textinfo strings may include \"-\" or\n\
            \"+\" as special characters (in textinfo the char should\n\
            be a stand-alone word). They state where the text should\n\
            be printed: below the bars (\"-\", default) or above the\n\
            bars. This is used, for example, to print the add-5 and\n\
            add-2 codes to the right of UPC or EAN codes (the add-5\n\
            extension is mostly used in ISBN codes).\n\
\n\
encoding -- type of encoding which was used to produce the barcode. (read-only)\n\
\n\
";

static PyObject * 
barcode_encode(PyObject *self, PyObject *args) 
{
  PyObject *ret = NULL;
  int flags = 0;            /* type of encoding and decoding */
  char *ascii = NULL;       /* malloced */
  struct Barcode_Item *bc;

  if(PyArg_ParseTuple(args, "is", &flags, &ascii) == 0)
    return NULL;
 
  bc = Barcode_Create(ascii);
  if(bc == NULL)
    {
      PyErr_SetString(PyExc_RuntimeError, "can not create barcode structure");
      return NULL;
    }
  
  if(Barcode_Encode(bc, flags) == -1)
    {
      PyErr_SetString(PyExc_RuntimeError, "can not encode barcode");
      return NULL;
    }

  ret = Py_BuildValue("sss", bc->partial, bc->textinfo, bc->encoding);
  
  Barcode_Delete(bc);
  return ret;
}



static char barcode_print_doc [] =
"barcode([arg]) -> md5 object\n\
\n\
Return a barcode md5 object. If arg is present, the method call update(arg)\n\
is made.


            BARCODE_OUT_PS, BARCODE_OUT_EPS, BARCODE_OUT_PCL, BARCODE_OUT_PCL_III\n\
            The currently supported encoding types: full-page\n\
            postscript and encapsulated postscript; PCL (print command\n\
            language, for HP printers) and PCL-III (same as PCL, but\n\
            uses a font not available on older printers).\n\
\n\
            BARCODE_OUT_NOHEADERS\n\
            The flag instructs the printing engine not to print the\n\
            header and footer part of the file. This makes sense for\n\
            the postscript engine but might not make sense for other\n\
            engines; such other engines will silently ignore the flag\n\
            just like the PCL back-end does.\n\
\n\
            BARCODE_NO_ASCII\n\
            Instructs the engine not to print the ascii string on\n\
            output. By default the bar code is accompanied with an\n\
            ascii version of the text it encodes.\n\
\n\
width    -- width for the barcode. (read-write)\n\
\n\
height   -- height for the barcode. (read-write)\n\
\n\
xoff     -- x offset from the origin. (read-write)\n\
\n\
yoff     -- y offset from the origin. (read-write)\n\
\n\
margin   -- margin arround the barcode. (read-write)\n\
\n\
scalef   -- scaling factor. (read-write)\n\
\n\
            Use of the width and scalef fields\n\
            A width unit is the\n\
            width of the thinnest bar and/or space in the chosen code;\n\
            it defaults to 1 point if the output is postscript or\n\
            encapsulated postscript.\n\
\n\
            Either or both the code width and the scale factor can be\n\
            left unspecified (i.e., zero). The library deals with\n\
            defaults in the following way:\n\
\n\
            Both unspecified\n\
            If both the width and the scale factor are unspecified,\n\
            the scale factor will default to 1.0 and the width is\n\
            calculated according to the actual width of the bar code\n\
            being printed.\n\
\n\
            Width unspecified\n\
            If the width is not specified, it is calculated according\n\
            to the values of scalef.\n\
\n\
            Scale factor unspecified\n\
            If the scale factor is not specified, it will be chosen so\n\
            that the generated bar code exactly fits the specified\n\
            width.\n\
\n\
            Both specified\n\
            The code will be printed inside the specified region\n\
            according to the specified scale factor. It will be\n\
            aligned to the left. If, however, the chosen width is too\n\
            small for the specific bar code and scaling factor, then\n\
            the code will extend symmetrically to the left and to the\n\
            right of the chosen region.\n\
\n\
";

static PyObject * 
barcode_print(PyObject *self, PyObject *args) 
{
  PyObject *ret = NULL;
  int flags;         /* type of encoding and decoding */
  char *ascii;       /* malloced */
  char *partial;     /* malloced too */
  char *textinfo;    /* information about text positioning */
  char *encoding;    /* code name, filled by encoding engine */
  int width, height; /* output units */
  int xoff, yoff;    /* output units */
  int margin;        /* output units */
  double scalef;     /* requested scaling for barcode */
  struct Barcode_Item *bc;
  int ok;

  if(PyArg_ParseTuple(args, "isiiiii", &flags, &ascii, &width, 
			   &height, &xoff, &yoff, &margin) == 0)
    return NULL;
 
  bc = Barcode_Create(ascii);
  if(bc == NULL)
    {
      PyErr_SetString(PyExc_RuntimeError, "can not create barcode structure");
      return NULL;
    }
  
    if(Barcode_Position(bc, width, height, xoff, yoff, scalef) == -1)
    {
      PyErr_SetString(PyExc_RuntimeError, "can not set barcode position");
      return NULL;
    }

  if(Barcode_Encode(bc, flags) == -1)
    {
      PyErr_SetString(PyExc_RuntimeError, "can not encode barcode");
      return NULL;
    }

  ret = Py_BuildValue("issssiiiiid", bc->flags, bc->ascii, bc->partial, bc->textinfo, bc->encoding, 
		      bc->width, bc->height, bc->xoff, bc->yoff, bc->margin, bc->scalef);
  
  Barcode_Delete(bc);
  return ret;
}


/* List of functions exported by this module */

static PyMethodDef barcode_functions[] = {
	{"version",		(PyCFunction)barcode_version, METH_NOARGS, barcode_version_doc},
	{"encode",		(PyCFunction)barcode_encode, METH_VARARGS, barcode_encode_doc},
	{NULL,		NULL}	/* Sentinel */
};

/* Initialize this module. */

DL_EXPORT(void)
initbarcode(void)
{
	PyObject *m, *d;

	m = Py_InitModule3("barcode", barcode_functions, module_doc);
	d = PyModule_GetDict(m);
	PyModule_AddIntConstant(m, "BARCODE_ANY", BARCODE_ANY);
	PyModule_AddIntConstant(m, "BARCODE_EAN", BARCODE_EAN);
	PyModule_AddIntConstant(m, "BARCODE_UPC", BARCODE_UPC);
	PyModule_AddIntConstant(m, "BARCODE_ISBN", BARCODE_ISBN);
	PyModule_AddIntConstant(m, "BARCODE_39", BARCODE_39);
	PyModule_AddIntConstant(m, "BARCODE_128" , BARCODE_128);
	PyModule_AddIntConstant(m, "BARCODE_128C", BARCODE_128C);
	PyModule_AddIntConstant(m, "BARCODE_128B", BARCODE_128B);
	PyModule_AddIntConstant(m, "BARCODE_I25", BARCODE_I25);
	PyModule_AddIntConstant(m, "BARCODE_128RAW", BARCODE_128RAW);
	PyModule_AddIntConstant(m, "BARCODE_CBR", BARCODE_CBR);
	PyModule_AddIntConstant(m, "BARCODE_MSI", BARCODE_MSI);
	PyModule_AddIntConstant(m, "BARCODE_PLS", BARCODE_PLS);
	PyModule_AddIntConstant(m, "BARCODE_93", BARCODE_93);   
	PyModule_AddIntConstant(m, "BARCODE_DEFAULT_FLAGS", BARCODE_DEFAULT_FLAGS);
	PyModule_AddIntConstant(m, "BARCODE_ENCODING_MASK", BARCODE_ENCODING_MASK); 
	PyModule_AddIntConstant(m, "BARCODE_NO_ASCII", BARCODE_NO_ASCII);
	PyModule_AddIntConstant(m, "BARCODE_NO_CHECKSUM", BARCODE_NO_CHECKSUM);
	PyModule_AddIntConstant(m, "BARCODE_OUTPUT_MASK", BARCODE_OUTPUT_MASK);
 	PyModule_AddIntConstant(m, "BARCODE_OUT_EPS", BARCODE_OUT_EPS);
 	PyModule_AddIntConstant(m, "BARCODE_OUT_PS", BARCODE_OUT_PS);
 	PyModule_AddIntConstant(m, "BARCODE_OUT_PCL", BARCODE_OUT_PCL);
 	PyModule_AddIntConstant(m, "BARCODE_OUT_PCL_III", BARCODE_OUT_PCL_III);
 	PyModule_AddIntConstant(m, "BARCODE_OUT_NOHEADERS", BARCODE_OUT_NOHEADERS);
}
