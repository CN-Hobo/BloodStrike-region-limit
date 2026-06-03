import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class BloodstrikePatcher:
    def __init__(self, root):
        self.root = root
        self.root.title("BloodStrike地区检测补丁工具")
        self.root.geometry("550x325")
        self.root.resizable(False, False)
        
        # 尝试加载同目录下的图标文件，若不存在或加载失败则忽略
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass
        
        # 目标字符串和替换值
        self.target_string = b"aim_info"
        self.replace_bytes = b"\x00" * len(self.target_string)
        
        # 相对路径
        self.dll_relative_path = os.path.join("Engine", "Binaries", "Win64", "NtUniSdkSteam.dll")
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="BloodStrike地区检测补丁工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=15)
        
        # 工具介绍
        intro_text = """本工具用于修改 BloodStrike 游戏的 NtUniSdkSteam.dll 文件以绕过登录时的地区检测。
*使用方法：点击下方按钮选择游戏根目录，文件夹名BLOODSTRIKE，工具会自动定位并处理目标文件。(例：D:\\SteamLibrary\\steamapps\\common\\BLOODSTRIKE)
*本工具开源免费，GitHub地址：CN-Hobo/BloodStrike-region-bypasser
"""
        
        intro_label = tk.Label(self.root, text=intro_text, justify=tk.LEFT, wraplength=500)
        intro_label.pack(pady=10, padx=20)
        
        # 路径显示框架
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10, padx=20, fill=tk.X)
        
        path_label = tk.Label(path_frame, text="当前选择的路径：")
        path_label.pack(anchor=tk.W)
        
        self.path_var = tk.StringVar(value="未选择任何文件夹")
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, state="readonly", width=70)
        path_entry.pack(fill=tk.X, pady=5)
        
        # 选择按钮
        select_button = tk.Button(self.root, text="选择游戏文件夹", command=self.select_folder, 
                                 font=("Arial", 12), width=20, height=5)
        select_button.pack(pady=20)
        
        # 状态标签
        self.status_var = tk.StringVar(value="等待选择文件夹...")
        status_label = tk.Label(self.root, textvariable=self.status_var, fg="blue")
        status_label.pack(pady=5)
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择 BloodStrike 游戏根目录")
        
        if not folder_path:
            return
        
        self.path_var.set(folder_path)
        
        # 验证文件夹名称
        folder_name = os.path.basename(folder_path)
        if folder_name != "BLOODSTRIKE":
            messagebox.showerror("错误", "选择正确的游戏文件夹，请重试\n\n请选择名为 \"BLOODSTRIKE\" 的文件夹。")
            self.status_var.set("文件夹验证失败")
            return
        
        self.status_var.set("文件夹验证成功，正在定位目标文件...")
        self.process_dll(folder_path)
    
    def process_dll(self, game_folder):
        dll_path = os.path.join(game_folder, self.dll_relative_path)
        
        # 检查文件是否存在
        if not os.path.exists(dll_path):
            error_msg = f"找不到目标文件：\n{dll_path}\n\n可能的解决方法：\n1. 确认游戏安装完整\n2. 以管理员身份运行本工具\n3. 游戏更新已修改了文件结构，等待工具更新"
            messagebox.showerror("文件不存在", error_msg)
            self.status_var.set("目标文件不存在")
            return
        
        try:
            # 备份原文件
            backup_path = dll_path + ".bak"
            if not os.path.exists(backup_path):
                shutil.copy2(dll_path, backup_path)
                self.status_var.set("已创建原文件备份")
            
            # 读取文件内容
            with open(dll_path, "rb") as f:
                content = f.read()
            
            # 统计替换次数
            replace_count = content.count(self.target_string)
            
            if replace_count == 0:
                messagebox.showinfo("提示", "在目标文件中未找到 \"aim_info\" 字符串。\n文件可能已经被修改过，或者游戏版本不兼容。")
                self.status_var.set("未找到目标字符串")
                return
            
            # 执行替换
            new_content = content.replace(self.target_string, self.replace_bytes)
            
            # 写入修改后的内容
            with open(dll_path, "wb") as f:
                f.write(new_content)
            
            # 成功提示
            messagebox.showinfo("成功", f"文件处理完成！\n原文件已备份为：\n{backup_path}")
            self.status_var.set(f"处理成功，替换了 {replace_count} 处")
            
            # 结束程序
            self.root.after(1000, self.root.destroy)
            
        except PermissionError:
            error_msg = "权限不足，无法写入文件。\n\n可能的解决方法：\n1. 关闭游戏和所有相关进程\n2. 右键点击本工具，选择\"以管理员身份运行\"\n3. 检查文件是否被杀毒软件锁定"
            messagebox.showerror("权限错误", error_msg)
            self.status_var.set("权限不足")
        except Exception as e:
            error_msg = f"处理文件时发生错误：\n{str(e)}\n\n可能的解决方法：\n1. 确保文件没有被其他程序占用\n2. 检查磁盘空间是否充足\n3. 尝试重新安装游戏"
            messagebox.showerror("未知错误", error_msg)
            self.status_var.set("处理失败")

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodstrikePatcher(root)
    root.mainloop()
