# VR_Security_with_GPT
use gpt and other language model's help, to analyse VR app's security problem.

## 项目内容
输入：应用apk、此应用功能的描述。

输出：此应用apk中不应该申请的权限。

运行过程：VR_Security_with_GPT.py中，会使用apk_tool将对应应用安装包进行反编译，提取中其中的AndroidManifest.xml，并通过GPT提取xml文件中申请到的permission和feature。紧接着应用拿提取到的permission和feature继续对GPT提问，根据应用的描述，找到不应该申请的权限，并输出。

## 使用方法
python环境：3.11
### 单个apk处理

1. 打开VR_Security_with_GPT.py，修改openai.api_key为自己的key值。具体如何获得看<https://blog.csdn.net/qq_32265503/article/details/130471485>。

2. 修改main中的apk_src、description分别为自己的应用安装包路径、应用描述，随后运行。

### 多个apk批处理

1. 打开表格app_permission.xlsx
2. 仿照表格中给出的示例填写第一列（安装包名称）和第二列（应用介绍）
3. 将自己需要批处理的apk放到一个统一的文件夹，并修改main.py中的apk_src
4. 运行main.py，脚本会自动分析每一行是否已经生成答案，若没有，则读取对应的apk和描述，运行生成答案，写在表格的第三列（GPT Answer）中，同时把反编译到的xml文件写在第四列。此表格第五列为人工编写的ground truth，以供对比。
