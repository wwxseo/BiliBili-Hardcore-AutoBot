# ⚡️ BiliBili-Hardcore-AutoBot | B站硬核会员全自动答题助手

> **基于 Google Gemini AI 视觉大模型的全自动答题脚本。不查题库，不盲猜，AI 像人类一样“看”懂屏幕，“思考”后作答。**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 简介

这是一个利用 AI 计算机视觉技术，帮助你通过 Bilibili Lv6 硬核会员进阶试炼的自动化工具。它不是简单的题库搜索，而是通过 ADB 截取手机屏幕，发送给 Google Gemini 1.5 Pro/Flash 大模型进行实时分析，模拟手指点击屏幕，实现 **100% 全自动挂机**。

### ✨ 核心特性

*   **🧠 真·AI 大脑**：接入 Google Gemini 视觉模型，无论是冷门动漫题还是最新的科技参数题，AI 都能现场推理分析。
*   **📱 万能分辨率适配**：内置**百分比坐标算法**，自动读取你手机的分辨率（无论是 1080P、2K 还是平板），自动换算点击位置，**换手机也能用**。
*   **🛡️ 安全防检测**：不注入 APP，不修改数据包。完全模拟真人手指的“按压”操作（Swipe），配合随机坐标抖动，极大降低风控风险。
*   **📝 实时解说**：终端窗口会实时打印 AI 的解题思路和吐槽，挂机过程不再枯燥。
*   **🔒 隐私保护**：API Key 本地配置，敏感信息不上传，由你自己掌控。

---

## 🛠️ 准备工作 (小白必看)

在开始之前，你需要准备：

1.  **一台电脑** (Windows / macOS / Linux)。
2.  **一部安卓手机** (iOS 暂不支持)。
3.  **一根数据线**，将手机连接到电脑。
4.  **Python 环境**：请确保电脑已安装 [Python 3.10](https://www.python.org/downloads/) 或更高版本。

---

## 🚀 快速开始

### 第一步：下载项目
点击右上角的绿色按钮 **Code** -> **Download ZIP**，下载后解压到一个文件夹里。

### 第二步：安装依赖

我们需要告诉电脑安装这个脚本需要的“零件” (库)。你可以选择以下任意一种方式打开终端：

*   **方法 A：如果你用 Visual Studio Code (推荐)**
    1.  用 VS Code 打开本项目的文件夹。
    2.  在顶部菜单栏点击 **“终端 (Terminal)”** -> **“新建终端 (New Terminal)”**。
    3.  在下方弹出的窗口中直接输入命令即可。

*   **方法 B：如果你用 Windows 系统文件夹**
    1.  打开存放本项目的文件夹。
    2.  在文件夹顶部的**地址栏**里输入 `cmd`，然后按回车。会弹出一个黑色的命令框。

*   **方法 C：如果你用 macOS**
    1.  打开“终端” (Terminal) App。
    2.  输入 `cd ` (注意 cd 后面有个空格)，然后把本项目文件夹**拖进**终端窗口，按回车。

**打开终端后，输入以下命令并回车：**

```bash
pip install -r requirements.txt
```

### 第三步：手机设置 (关键)
开启开发者模式：去手机设置 -> 关于手机 -> 连续点击“版本号”7次。
开启 USB 调试：去设置 -> 开发者选项 -> 打开 “USB 调试”。
开启模拟点击权限 (小米/红米用户必做)：在开发者选项里，找到并开启 “USB 调试（安全设置）”。
保持屏幕常亮：建议将自动锁屏时间设置为“永不”或“10分钟”，防止答题中途锁屏。
### 第四步：配置 API Key
你需要一个 Google Gemini 的 API Key (免费申请)。
前往 Google AI Studio 申请 Key。
在项目文件夹里新建一个文本文件，命名为 key.txt。
打开它，只把你的 API Key 粘贴进去，保存关闭。
原理：脚本会自动读取这个文件。这样做的好处是你的 Key 不会写死在代码里，分享代码给别人时不会泄露你的额度。
### 第五步：运行脚本
确保手机已连接电脑，且 B 站 APP 已打开到**“硬核会员答题界面”**。
在终端运行：
```bash
python main.py
```
按回车启动，然后你就可以放手了！
## ❓ 常见问题与故障排除 (FAQ)
### 1. Windows 用户提示 "adb 不是内部或外部命令" 或报错？

> **原因**：本项目默认内置的是 macOS 版的 ADB 工具，Windows 系统无法直接运行。

**解决方法**：你需要下载 Windows 版的 ADB 替换进去。

**📥 官方 ADB 工具包下载地址：**
*   **Windows 版本**：[点击下载](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)
*   **macOS 版本**：[点击下载](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip) (本项目已内置，如损坏可重新下载)
*   **Linux 版本**：[点击下载](https://dl.google.com/android/repository/platform-tools-latest-linux.zip)

**替换步骤 (Windows 用户必做)：**
1.  下载上面的 Windows 版压缩包并解压。
2.  进入解压后的 `platform-tools` 文件夹。
3.  找到 `adb.exe`、`AdbWinApi.dll`、`AdbWinUsbApi.dll` 这三个文件。
4.  **复制**这三个文件。
5.  回到本项目的文件夹，**粘贴并覆盖**原有的 `adb` 文件。
### 2. Mac/Linux 用户提示 "Permission denied"？
原因：下载的文件可能丢失了可执行权限。
解决方法：在终端运行以下命令赋予权限：
```bash
chmod +x adb
```
### 3. 运行后报错 "Connect to ... failed" 或 AI 无响应？
原因：在中国大陆地区，连接 Google API 需要网络代理（梯子）。
解决方法：
打开 main.py 文件。
找到 PROXY_URL 这一行。
根据你的代理软件修改端口号。
Clash 通常是 `http://127.0.0.1:7890`
V2Ray 通常是 `http://127.0.0.1:1087 或 10809`
请查看你代理软件的“设置”界面，找到“本地 HTTP 代理端口”。
## 4. 脚本显示点击了，但手机没反应？
请检查手机**“开发者选项”**里是否开启了 “USB 调试（安全设置）”（尤其是小米/红米手机）。
尝试重新插拔数据线，并在手机弹窗中勾选“始终允许该电脑调试”。
## ⚙️ 高级配置 (可选)
如果你发现 AI 点击的位置稍微有点偏（虽然这很少见），你可以打开 main.py，找到 UI_RATIOS 部分进行微调：
```bash
# 这些数字代表屏幕高度的百分比 (0.0 - 1.0)
UI_RATIOS = {
    'A': 0.469,  # 选项 A 的位置
    'B': 0.550,
    'C': 0.640,
    'D': 0.736,
    'NEXT': 0.916 # 下一题按钮的位置
}
```
如果点高了，把数字改大一点。
如果点低了，把数字改小一点。
## ⚠️ 免责声明
本项目仅供技术研究和 Python 学习使用。
请勿用于商业用途或恶意破坏 Bilibili 社区规则。
使用本工具产生的任何后果（如账号风险）由使用者自行承担。
### Happy Coding & Enjoy Bilibili! ⚡️
## 🤝 贡献与支持

如果你觉得这个脚本帮到了你，请点击右上角的 ⭐️ **Star** 支持一下作者！
欢迎提交 Issue 或 Pull Request。
## 效果图和演示视频（bs拍摄设备有点差谅解一下）

![Screenshot_2025-12-16-03-16-43-70_149003a2d400f6adb210d7e357a3a646](https://github.com/user-attachments/assets/675236e6-c4fe-481d-bb9e-7d6536436370)


https://github.com/user-attachments/assets/ea6096b2-6e25-4572-a984-7cc0d04491de


