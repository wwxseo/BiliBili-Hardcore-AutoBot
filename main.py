import subprocess
import time
import os
import re
import random
import sys

# 尝试导入依赖，如果没装则提示
try:
    import google.generativeai as genai
except ImportError:
    print("❌ 缺少依赖库！请运行: pip install google-generativeai")
    sys.exit(1)

# ==========================================
# ⚙️ 用户配置区 (User Configuration)
# ==========================================

# 1. Google Gemini API Key
# 建议：不要直接在这里贴 Key，而是去同目录下新建一个 key.txt 文件填入 Key
# 或者直接修改下面这就行
API_KEY = "" 

# 2. 网络代理 (Proxy)
# 中国大陆用户通常需要配置，例如: "http://127.0.0.1:7890"
# 如果不需要代理，请留空 ""
PROXY_URL = "http://127.0.0.1:4780" 

# 3. 点击坐标比例 (基于 1080x2400 的完美比例)
# 如果你的手机点击位置不准，微调这里的数字 (0.0 - 1.0)
UI_RATIOS = {
    'A': 0.469,  # 选项 A 高度
    'B': 0.550,  # 选项 B 高度
    'C': 0.640,  # 选项 C 高度
    'D': 0.736,  # 选项 D 高度
    'NEXT': 0.916 # 下一题按钮高度
}

# ==========================================

# 配置网络
if PROXY_URL:
    os.environ["http_proxy"] = PROXY_URL
    os.environ["https_proxy"] = PROXY_URL

# 配置 API Key
def load_api_key():
    # 优先读取文件
    if os.path.exists("key.txt"):
        with open("key.txt", "r") as f:
            return f.read().strip()
    return API_KEY

final_key = load_api_key()
if not final_key:
    print("❌ 错误：未找到 API Key！")
    print("请在代码中填写 API_KEY，或在同目录下新建 key.txt 文件。")
    sys.exit(1)

genai.configure(api_key=final_key)

# --- 核心类 ---
class AndroidBot:
    def __init__(self):
        self.adb_path = self._detect_adb()
        self.width, self.height = self._get_screen_size()
        print(f"📱 设备分辨率: {self.width} x {self.height}")

    def _detect_adb(self):
        # 优先检测当前目录下的 adb
        if os.path.exists("./adb"):
            return "./adb"
        # 其次检测系统环境变量里的 adb
        return "adb"

    def run_cmd(self, args, timeout=5):
        try:
            cmd = [self.adb_path] + args
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            return proc.stdout
        except: return None

    def _get_screen_size(self):
        out = self.run_cmd(['shell', 'wm', 'size'])
        if out:
            try:
                txt = out.decode()
                match = re.search(r'(\d+)x(\d+)', txt)
                if match: return int(match.group(1)), int(match.group(2))
            except: pass
        print("⚠️ 无法获取分辨率，默认使用 1080x2400")
        return 1080, 2400

    def capture_screen(self):
        try:
            # 使用 exec-out 直接获取二进制流，速度快
            proc = subprocess.Popen([self.adb_path, 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data, _ = proc.communicate(timeout=5)
            return data if len(data) > 0 else None
        except: return None

    def tap_ratio(self, ratio_name):
        ratio = UI_RATIOS.get(ratio_name)
        if not ratio: return
        
        # 计算绝对坐标
        x = int(self.width * 0.5) # 水平居中
        y = int(self.height * ratio)
        
        # 随机抖动防检测
        x += random.randint(-5, 5)
        y += random.randint(-5, 5)
        
        print(f"👉 点击 [{ratio_name}] -> ({x}, {y})")
        # 使用 Swipe 模拟按压 (比 Tap 更稳)
        self.run_cmd(['shell', 'input', 'swipe', str(x), str(y), str(x), str(y), '100'])

# --- AI 逻辑 ---
def get_ai_model():
    print("🧠 正在初始化 AI...", end=" ")
    try:
        # 自动寻找可用模型
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                print(f"✅ 使用模型: {m.name}")
                return genai.GenerativeModel(m.name)
        print("✅ 使用默认 Flash")
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"\n❌ AI 连接失败: {e}")
        return None

def analyze_and_act(bot, model, image_bytes):
    print("🤖 思考中...", end="\r")
    try:
        prompt = """
        B站硬核会员答题。
        请输出两行：
        1. 【结论】：【选X】
        2. 【分析】：(一句话解释，幽默风格)
        """
        response = model.generate_content([{"mime_type": "image/jpeg", "data": image_bytes}, prompt])
        text = response.text.strip()
        
        # 打印分析
        print(" " * 20, end="\r")
        print("-" * 40)
        print(text.replace("\n\n", "\n"))
        print("-" * 40)
        
        # 提取选项
        choice = 'C'
        match = re.search(r'【选\s*([ABCD])\s*】', text)
        if match:
            choice = match.group(1).upper()
        else:
            # 模糊匹配
            fallback = re.findall(r'[ABCD]', text.upper())
            if fallback: choice = fallback[-1]
            
        # 执行点击
        bot.tap_ratio(choice)
        return True
    except Exception as e:
        print(f"❌ AI 错误: {e}")
        return False

# --- 主程序 ---
def main():
    print("=" * 40)
    print("   BiliBili Hardcore AutoBot (Open Source)")
    print("   全自动硬核会员答题助手")
    print("=" * 40)

    bot = AndroidBot()
    model = get_ai_model()
    
    if not model:
        print("请检查网络代理或 API Key 配置。")
        return

    input("\n👉 请打开 B站答题界面，按【回车】开始挂机...")
    
    count = 1
    while True:
        print(f"\n>>>>>> 第 {count} 题 <<<<<<")
        
        # 1. 截图
        img = bot.capture_screen()
        if not img:
            print("⚠️ 截图失败，请检查 USB 连接")
            time.sleep(2)
            continue
            
        # 2. AI 答题
        if analyze_and_act(bot, model, img):
            # 3. 翻页逻辑
            time.sleep(0.5) # 等待选中
            bot.tap_ratio('NEXT') # 点击下一题
            
            print("🌊 加载下一题...", end=" ")
            # 倒计时等待加载
            for i in range(3, 0, -1):
                print(i, end=" ", flush=True)
                time.sleep(1)
            print("Go!")
            
            count += 1
        else:
            time.sleep(3)

if __name__ == "__main__":
    main()