/* $Id: _barcodemodule.c,v 1.1 2002/07/13 23:44:00 drt Exp $ */ 

/* barcode objects */

#include "Python.h"
#include "structmember.h"
#include "barcode.h"

typedef struct {
  PyObject_HEAD
  struct Barcode_Item *bc;		/* the context holder */
} barcodeobject;

/* this is needed tu use offsetof - at least on MacOS X */
typedef struct  Barcode_Item barcodeitemtype;

staticforward PyTypeObject barcodetype;

#define is_barcodeobject(v)		((v)->ob_type == &barcodetype)

static barcodeobject *
newbarcodeobject(void)
{
  barcodeobject *barcodep;
  
  barcodep = PyObject_New(barcodeobject, &barcodetype);
  if (barcodep == NULL)
    return NULL;
  
  barcodep->bc = NULL;
  barcodep->bc = Barcode_Create("<unset>");
  if (barcodep->bc == NULL)
    return NULL;
  
  return barcodep;
}


static void
barcode_dealloc(barcodeobject *barcodep)
{
  Barcode_Delete(barcodep->bc);
  barcodep->bc = NULL;
  PyObject_Del(barcodep);
}


/* MD5 methods-as-attributes */

static PyObject *
barcode_encode(barcodeobject *self, PyObject *args)
{
	Barcode_Encode(self->bc, self->bc->flags); 
	Py_INCREF(Py_None);
	return Py_None;
}

static char encode_doc [] =
"encode() - convert input to the the intermediate representation.";

/* todo:
int Barcode_Print(struct Barcode_Item *bc, FILE *f, int flags) 
extern int Barcode_ps_print(struct Barcode_Item *bc, FILE *f); 
extern int Barcode_pcl_print(struct Barcode_Item *bc, FILE *f);
*/

static char barcodetype_doc [] =
"barcode - interface to the GNU barcode library.\n\
\n\
Methods:\n\
\n\
encode() -- convert input to the the intermediate representation.\n\
\n\
Members:\n\
\n\
ascii    -- input to be converted to barcode. (read-write)\n\
\n\
flags    -- flags used th create the barcodes. (read-write)\n\
\n\
            BARCODE_ANY\n\
            Choose the best suited encoding type. You also can specify\n\
            any of BARCODE_EAN, BARCODE_UPC, BARCODE_ISBN,\n\
            BARCODE_128B, BARCODE_128C, BARCODE_128, BARCODE_128RAW,\n\
            BARCODE_39, BARCODE_I25, BARCODE_CBR, BARCODE_MSI,\n\
            BARCODE_PLS, BARCODE_93.\n\
\n\
            BARCODE_NO_ASCII\n\
            Instructs the engine not to print the ascii string on\n\
            output. By default the bar code is accompanied with an\n\
            ascii version of the text it encodes.\n\
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
encoding -- type of encoding which was used to produce the barcode. (read-only)\n\
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
            See attribute for additional documentation.\n\
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
";

static PyMethodDef barcode_methods[] = {
  {"encode",        (PyCFunction)barcode_encode,   METH_VARARGS, encode_doc},
  {NULL,          NULL}           /* sentinel */
};

/* this seems not to work */
static PyMemberDef barcode_members[] = {
  {"flags", T_INT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, flags), READONLY, "docXXX"},
  {"ascii", T_STRING, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, ascii), READONLY, "docbla"},
  {"partial", T_STRING, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, partial), READONLY, "docpartial"},
  {"textinfo", T_STRING, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, textinfo), READONLY, "doctextinfo"},
  {"encoding", T_STRING, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, encoding), READONLY, "docencoding"},
  {"width", T_INT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, width), READONLY, "docw"},
  {"heigth", T_INT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, height), READONLY, "doch"},
  {"xoff", T_INT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, xoff), READONLY, "docx"},
  {"yoff", T_INT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, yoff), READONLY, "docy"},
  {"scalef", T_FLOAT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, scalef), READONLY, "docs"}, 
  {"margin", T_INT, offsetof(barcodeobject, bc) + 
   offsetof(barcodeitemtype, margin), READONLY, "docm"},
  {NULL}
};


static PyObject *
barcode_getattr(barcodeobject *self, char *name)
{
  if(strcmp(name, "ascii") == 0) {
    if (self->bc->ascii != NULL)
      return PyString_FromString(self->bc->ascii);
    else 
      {
	Py_INCREF(Py_None);
	return Py_None;
      }
  } else if(strcmp(name, "partial") == 0) {
    if (self->bc->partial != NULL)
      {    
	return PyString_FromString(self->bc->partial);
      }
    else 
      {
	Py_INCREF(Py_None);
	return Py_None;
      }
  } else if(strcmp(name, "textinfo") == 0) {
    if (self->bc->textinfo != NULL)
      return PyString_FromString(self->bc->textinfo);
    else 
      {
	Py_INCREF(Py_None);
	return Py_None;
      }
  } else if(strcmp(name, "encoding") == 0) {
    if (self->bc->encoding != NULL)
	return PyString_FromString(self->bc->encoding);
    else 
      {
	Py_INCREF(Py_None);
	return Py_None;
      }
  } else if(strcmp(name, "flags") == 0) {
    return PyInt_FromLong(self->bc->flags);
  } else if(strcmp(name, "width") == 0) {
    return PyInt_FromLong(self->bc->width);
  } else if(strcmp(name, "height") == 0) {
    return PyInt_FromLong(self->bc->height);
  } else if(strcmp(name, "xoff") == 0) {
    return PyInt_FromLong(self->bc->xoff);
  } else if(strcmp(name, "yoff") == 0) {
    return PyInt_FromLong(self->bc->yoff);
  } else if(strcmp(name, "margin") == 0) {
    return PyInt_FromLong(self->bc->margin);
  } else if(strcmp(name, "scalef") == 0) {
    return PyFloat_FromDouble(self->bc->scalef);
  }
  return Py_FindMethod(barcode_methods, (PyObject *)self, name);
}

static int
barcode_setattr(barcodeobject *self, char *name, PyObject *v)
{
  char *carg;

  if(strcmp(name, "ascii") == 0) 
    {
      carg = PyString_AsString(v);
      /* free(self->bc->ascii); */
      self->bc->ascii = strdup(carg);
      return 0;
    } 
  else if(strcmp(name, "flags") == 0) 
    {
      self->bc->flags = PyInt_AsLong(v);
      return 0;
    }
  else if(strcmp(name, "margin") == 0) 
    {
      self->bc->margin = PyInt_AsLong(v);
      return 0;
    }

  PyErr_SetString(PyExc_RuntimeError, "this arttibute can not be set");
  return 1;
}

statichere PyTypeObject barcodetype = {
	PyObject_HEAD_INIT(NULL)
	0,			  /*ob_size*/
	"barcode.barcode",	  /*tp_name*/
	sizeof(barcodeobject),	  /*tp_size*/
	0,			  /*tp_itemsize*/
	/* methods */
	(destructor)barcode_dealloc,  /*tp_dealloc*/
	0,			  /*tp_print*/
	(getattrfunc)barcode_getattr, /*tp_gatattr*/  
	(setattrfunc)barcode_setattr,  /*tp_setattr*/
	0,			  /*tp_compare*/
	0,			  /*tp_repr*/
        0,			  /*tp_as_number*/
	0,                        /*tp_as_sequence*/
	0,			  /*tp_as_mapping*/
	0, 			  /*tp_hash*/
	0,			  /*tp_call*/
	0,			  /*tp_str*/
	0,			  /*tp_getattro*/
	0,			  /*tp_setattro*/
	0,	                  /*tp_as_buffer*/
	1,			  /*tp_xxx4*/
	barcodetype_doc,	  /*tp_doc*/
	0,					/* tp_traverse */
	0,					/* tp_clear */
	0,					/* tp_richcompare */
	0,					/* tp_weaklistoffset */
	0,					/* tp_iter */
	0,					/* tp_iternext */
	barcode_methods,			/* tp_methods */
	barcode_members,			/* tp_members */
	0,			  /* tp_getset */
};


/* barcode Module functions */

static char module_doc [] =

"This Module implementes an interface to the GNU barcode library.\n\
\n\
Functions:\n\
\n\
barcode([arg]) -- return a new barcode object, initialized with arg as ascii\n\
version([arg]) -- get version of libbarcode\n\
\n\
Special Objects:\n\
\n\
barcodeType    -- type object for md5 objects\n\
\n\
Constants for barcode.flags:\n\
BARCODE_128, BARCODE_128B, BARCODE_128C BARCODE_128RAW, BARCODE_39,\n\
BARCODE_93, BARCODE_ANY, BARCODE_CBR, BARCODE_DEFAULT_FLAGS,\n\
BARCODE_EAN, BARCODE_ENCODING_MASK, BARCODE_I25, BARCODE_ISBN,\n\
BARCODE_MSI, BARCODE_NO_ASCII, BARCODE_NO_CHECKSUM,\n\
BARCODE_OUTPUT_MASK, BARCODE_OUT_EPS, BARCODE_OUT_NOHEADERS,\n\
BARCODE_OUT_PCL, BARCODE_OUT_PCL_III, BARCODE_OUT_PS, BARCODE_PLS,\n\
BARCODE_UPC\n\
";

static PyObject *
barcode_barcode(PyObject *self, PyObject *args)
{
	barcodeobject *barcodep;
	unsigned char *cp = NULL;
	int len = 0;

	if (!PyArg_ParseTuple(args, "|s#:barcode", &cp, &len))
		return NULL;
	
	if ((barcodep = newbarcodeobject()) == NULL)
		return NULL;

	/* we got an string via initializer */
	if(cp != NULL)
	  {
	    /* free(barcodep->bc->ascii); */
	    barcodep->bc->ascii = strdup(cp);
	  }

	return (PyObject *)barcodep;
}

static char barcode_doc [] =
"barcode([arg]) -> md5 object\n\
\n\
Return a barcode md5 object. If arg is present, the method call update(arg)\n\
is made.";



static PyObject *
barcode_version(PyObject *self, PyObject *args)
{
  return PyInt_FromLong((long) Barcode_Version(NULL));
}


static char version_doc [] =
"barcode([arg]) -> md5 object\n\
\n\
Return a barcode md5 object. If arg is present, the method call update(arg)\n\
is made.";



/* List of functions exported by this module */

static PyMethodDef barcode_functions[] = {
	{"barcode",		(PyCFunction)barcode_barcode, METH_VARARGS, barcode_doc},
	{"version",		(PyCFunction)barcode_version, METH_NOARGS, version_doc},
	{NULL,		NULL}	/* Sentinel */
};

/* Initialize this module. */

DL_EXPORT(void)
initbarcode(void)
{
	PyObject *m, *d;

        barcodetype.ob_type = &PyType_Type;
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
	Py_INCREF(&barcodetype);
	if(PyDict_SetItemString(d, "barcodeType", (PyObject *)&barcodetype) < 0)
	  return;
}
