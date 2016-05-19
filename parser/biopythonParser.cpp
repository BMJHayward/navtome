#include <string>
#include <Python.h>

/*
 * basically doing this:
 *
 *  PyRun_SimpleString("from Bio import SeqIO\n"
 *                     "SeqIO.parse('filename.extnsn', 'filetype'");
*/

PyObject* getFileData(int argc, char *argv[])
{
    PyObject *BioModule = PyImport_ImportModule("Bio");
    const char *filename, *filetype, *pycmdToRun;
    filename = (const char *)PyUnicode_DecodeFSDefault(argv[1]);
    filetype = (const char *)PyUnicode_DecodeFSDefault(argv[2]);
    std::string cmdToRun = "import Bio\nBio.SeqIO.parse(";
    cmdToRun = cmdToRun + filename + std::string(",") + filetype;
    pycmdToRun = cmdToRun.c_str();

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    
    Py_SetProgramName(program);  /* optional but recommended */
    Py_Initialize();
    PyObject* filedata;
    filedata = PyRun_String(pycmdToRun, 0, NULL, NULL);
    Py_DECREF(filename);
    Py_DECREF(filetype);
    Py_Finalize();
    PyMem_RawFree(program);

    return filedata;
}
