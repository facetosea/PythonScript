#include <Python.h>
#include <unistd.h>

int main(int argc, char** argv)
{
    // 在使用Python系统前，必须使用Py_Initialize对其进行初始化。它会载入Python的内建模块并添加系统路
    // 径到模块搜索路径中。这个函数没有返回值，检查系统是否初始化成功需要使用Py_IsInitialized

    Py_Initialize();
    if (!Py_IsInitialized())
    {
        return -1;
    }

    char pPath[256] = { 0 };
    getcwd(pPath, 256);
    printf("filePath:%s  \n", pPath);

    // 添加当前路径
    // 把输入的字符串作为Python代码直接运行，返回0表示成功，-1表示有错。大多时候错误都是因为字符串中有语法错误
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");
    PyObject *pName, *pModule, *pDict, *pFunc, *pArgs;

    // 载入名为pytest的脚本,注意没有后缀
    pName = PyString_FromString("pytest");
    pModule = PyImport_Import(pName);
    if (!pModule)
    {
        printf("can't find pytest.py!\n");
        return -1;
    }
    pDict = PyModule_GetDict(pModule);
    if (!pDict)
    {
        printf("Get pDict failed!");
        return -1;
    }
    // 找出函数名为add的函数
    pFunc = PyDict_GetItemString(pDict, "add");
    if (!pFunc || !PyCallable_Check(pFunc))
    {
        printf("can't find function [add]");
        return -1;
    }
    // // 参数进栈
    printf("push para\n");
    pArgs = PyTuple_New(2);
    //  PyObject* Py_BuildValue(char *format, ...)
    //  把C++的变量转换成一个Python对象。当需要从
    //  C++传递变量到Python时，就会使用这个函数。此函数
    //  有点类似C的printf，但格式不同。常用的格式有
    //  s 表示字符串，
    //  i 表示整型变量，
    //  f 表示浮点数，
    //  O 表示一个Python对象。
    PyTuple_SetItem(pArgs, 0, Py_BuildValue("l", 3));
    PyTuple_SetItem(pArgs, 1, Py_BuildValue("l", 4));
    // // 调用Python函数
    PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pName);
    Py_DECREF(pArgs);
    Py_DECREF(pModule);
    // // 关闭Python
    Py_Finalize();
    return 0;
}
