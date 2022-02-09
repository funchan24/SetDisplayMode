## 说明

* *为 **Python** 程序创建统一的目录结构、样板代码。程序编写完成后，将python代码打包为 **zip** 或 **exe** 文件进行分发*

### 用法

* 创建程序根目录 **mkdir Example**
* 进入程序根目录 **cd Example**
* 创建Python虚拟运行环境 **python -m venv .venv**
* 激活Python虚拟运行环境 **.venv\scripts\activate.bat**
* 将 **init** 复制到根目录 **Example\init**
* 创建统一的目录结构、样板代码 **python init\pre.py**
* 在 **Example\core\main.py** 编写代码
* 使用 **start.bat** 运行程序
* 打包命令帮助 **python init\pack.py -h**

### 注意

* 使用 **Nuitka** 打包 **exe** 文件，详细选项参考 **Nuitka** 用法

### 文件

* start.bat： Windows启动程序
* start.sh： Linux启动程序

### 目录

<table>
    <tr>
        <th>序号</th>
        <th>名称</th>
        <th>说明</th>
    </tr>
    <tr>
        <td>1</td>
        <td>.venv</td>
        <td>Python虚拟环境</td>
    </tr>
    <tr>
        <td>2</td>
        <td>bin</td>
        <td>依赖的可执行程序</td>
    </tr>
    <tr>
        <td>3</td>
        <td>conf</td>
        <td>配置信息</td>
    </tr>
    <tr>
        <td>4</td>
        <td>core</td>
        <td>核心代码</td>
    </tr>
    <tr>
        <td>5</td>
        <td>db</td>
        <td>数据库文件</td>
    </tr>
    <tr>
        <td>6</td>
        <td>docs</td>
        <td>说明文档</td>
    </tr>
    <tr>
        <td>7</td>
        <td>init</td>
        <td>程序初始化、打包</td>
    </tr>
    <tr>
        <td>8</td>
        <td>input</td>
        <td>用户输入文件</td>
    </tr>
    <tr>
        <td>9</td>
        <td>log</td>
        <td>运行日志</td>
    </tr>
    <tr>
        <td>10</td>
        <td>output</td>
        <td>运行结果</td>
    </tr>
    <tr>
        <td>11</td>
        <td>res</td>
        <td>引用资源</td>
    </tr>
    <tr>
        <td>12</td>
        <td>tests</td>
        <td>测试代码</td>
    </tr>
</table>