> 此文为记录python_excel任务中 Python打包的过程

## 本地测试命令

```bash
python main.py <输入的文件路径> <输出路径>

python main.py excel\mock.xlsx excel
```



# 过程

## 下载打包工具pyinstaller

```bash
pip install pyinstaller
```



## 执行打包命令

先进入虚拟环境，执行以下打包命令

打包单个文件：

```bash
pyinstaller -D --clean --win-private-assemblies DepartmentController.py -c --noconfirm 
```

打包多个文件：

```bash
pyinstaller -D --clean --win-private-assemblies DepartmentController.py utils.py main.py -c --noconfirm --noconsole
```

打包完记得把doc放到打包结果里！！！





解释：

这条指令是使用 PyInstaller 打包名为 `test-jieba.py` 的 Python 脚本的命令，并指定了一些选项和参数。以下是各个选项和参数的含义：

- `-D`：生成一个文件夹形式的可执行文件（一个文件夹包含多个文件）。
- `--clean`：在开始打包之前清理之前生成的临时文件。
- `--win-private-assemblies`：在 Windows 上使用私有程序集，将所有依赖项打包到可执行文件中。
- `test-jieba.py`：要打包的 Python 脚本文件名。
- `-c`：将脚本文件打包为一个可执行的命令行程序。
- `--noconfirm`：不要在打包之前询问任何确认问题。
- -p：打包其它文件

通过执行这条指令，PyInstaller 将会根据指定的选项和参数，将 `test-jieba.py` 这个脚本文件及其相关的依赖项打包为一个可执行文件。生成的可执行文件将包含所有必要的文件和依赖项，使其可以在目标系统上独立运行。

请注意，具体的打包结果和行为可能会受到脚本文件的内容、依赖项以及其他相关因素的影响。如果您需要更多关于 PyInstaller 的详细信息和其他选项的解释，请查阅 PyInstaller 的官方文档。



## 验证

打包成功后会有个dist文件，dist有打包好的文件，这里的样例是打包文件为`test-jieba`



## 运行exe执行程序

打开这个`test-jieba`文件夹，里面有一个`test-jieba.exe`执行程序

执行命令：

```bash
test-jieba.exe C:\公司\example.xlsx
```



# 问题

## 问题1

在做`data-analysis-latest`项目的时候，能够成功用pyinstaller成功打包，但是运行的时候报错：

```
configparser.NoSectionError: No section: 'NETWORK_CONFIG'
[5520] Failed to execute script 'main' due to unhandled exception!
```





原因是我在项目中有使用第三方库LAC，但是LAC是没有被打包进来的

解决：

把`from LAC import LAC`改为`import LAC`
把`lac = LAC(mode="lac")` 改为`lac = LAC.LAC(mode="lac")`

执行命令：

```bash
pyinstaller --distpath dist --add-data '.venv/Lib/site-packages/LAC:LAC' -D --clean --win-private-assemblies main.py --noconfirm
```



## 问题2

在做`data-analysis-latest`项目的时候，能够成功用pyinstaller成功打包，但是运行的时候报错：

```
C:\Campany\Projects\data-analysis-latest\dist\main>main.exe C:\Users\gditsec\Desktop\mock.xlsx
W1207 17:31:25.947559  5388 analysis_predictor.cc:2664] Deprecated. Please use CreatePredictor instead.
Traceback (most recent call last):
  File "main.py", line 10, in <module>
  File "LAC\lac.py", line 65, in __init__
    model = LacModel(model_path, mode, use_cuda)
  File "LAC\models.py", line 233, in __init__
    super(LacModel, self).__init__(model_path, mode, use_cuda)
  File "LAC\models.py", line 66, in __init__
    self.predictor = create_paddle_predictor(config)
RuntimeError: (PreconditionNotMet) The third-party dynamic library (mklml.dll) that Paddle depends on is not configured correctly. (error code is 126)
  Suggestions:
  1. Check if the third-party dynamic library (e.g. CUDA, CUDNN) is installed correctly and its version is matched with paddlepaddle you installed.
  2. Configure third-party dynamic library environment variables as follows:
  - Linux: set LD_LIBRARY_PATH by `export LD_LIBRARY_PATH=...`
  - Windows: set PATH by `set PATH=XXX; (at ..\paddle\phi\backends\dynload\dynamic_loader.cc:301)

[6032] Failed to execute script 'main' due to unhandled exception!
```

着重关注这行报错信息：

```
RuntimeError: (PreconditionNotMet) The third-party dynamic library (mklml.dll) that Paddle depends on is not configured correctly. (error code is 126)
```

这个错误通常表示 PaddlePaddle 在加载其依赖的第三方动态库 `mklml.dll` 时出现配置问题。错误代码 126 表示找不到该库。

解决：

把`C:\Campany\Projects\data-analysis-latest\.venv\Lib\site-packages\paddle\libs`下的文件拷贝到

`C:\Campany\Projects\data-analysis-latest\dist\main\paddle\libs`中



# 可参考文章

https://blog.csdn.net/weixin_44858471/article/details/104283174

https://www.cnblogs.com/ronyjay/p/12713078.html

