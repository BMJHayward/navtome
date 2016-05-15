#include <string>
#include <Python.h>

/*
 * basically doing this:
 *
 *  PyRun_SimpleString("from Bio import SeqIO\n"
 *                     "SeqIO.parse('filename.extnsn', 'filetype'");
*/

int getFileData(int argc, char *argv[])
{
    const char *filename, *filetype;
    filename = PyUnicode_DecodeFSDefault(argv[1]);
    filetype = PyUnicode_DecodeFSDefault(argv[2]);
    std::string cmdToRun = "Bio.SeqIO.parse(";
    cmdToRun = cmdToRun + filename + std::string(",") + filetype;
    cmdToRun = (const char*)cmdToRun;

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    
    Py_SetProgramName(program);  /* optional but recommended */
    Py_Initialize();
    PyRun_SimpleString(cmdToRun);
    Py_DECREF(filename);
    Py_DECREF(filetype);
    Py_Finalize();
    PyMem_RawFree(program);
    return 0;
}
