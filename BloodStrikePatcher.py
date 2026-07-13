import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import webbrowser

class BloodstrikePatcher:
    def __init__(self, root):
        self.root = root
        self.root.title("BloodStrike地区检测补丁工具")
        self.root.geometry("560x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        # 配置ttk样式
        style = ttk.Style()
        style.theme_use('vista')
        style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'), foreground="#1221ac", background='#f5f5f5')
        style.configure('Desc.TLabel', font=('Microsoft YaHei', 9), foreground='#555555', background='#f5f5f5')
        style.configure('Path.TLabel', font=('Microsoft YaHei', 9), foreground='#333333', background='#f5f5f5')
        style.configure('Status.TLabel', font=('Microsoft YaHei', 9), foreground='#2980b9', background='#f5f5f5')
        style.configure('Accent.TFrame', background="#4b5dff")
        style.configure('Card.TFrame', background='#ffffff', relief='solid', borderwidth=1)
        style.configure('Action.TButton', font=('Microsoft YaHei', 11), padding=(10, 8))
        style.map('Action.TButton', background=[('active', "#00ff00")])
        
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
        
        # 可能的DLL文件名（通常只会存在其中一个）
        self.dll_names = ["NtUniSdkSteam.dll", "NtUniSdkMpayOversea.dll"]
        self.dll_subdir = os.path.join("Engine", "Binaries", "Win64")
        
        self.create_widgets()
    
    def create_widgets(self):
        # 顶部红色装饰条
        accent = ttk.Frame(self.root, style='Accent.TFrame', height=4)
        accent.pack(fill=tk.X)
        
        # 主内容区用白色卡片包裹
        card = ttk.Frame(self.root, style='Card.TFrame')
        card.pack(padx=20, pady=(20, 10), fill=tk.X)
        
        # 标题
        title_label = ttk.Label(card, text="BloodStrike 地区检测补丁工具", style='Title.TLabel')
        title_label.pack(pady=(15, 10))
        
        # 分隔线
        sep = ttk.Separator(card, orient='horizontal')
        sep.pack(fill=tk.X, padx=20, pady=5)
        
        # 工具介绍
        intro_text = """本工具用于补丁 BloodStrike 游戏的 DLL 以绕过登录时的地区检测。
目前测试支持的游戏下载来源有：Steam端 & 官网Win端。
使用方法：选择游戏根目录，工具会自动定位并处理目标文件。
（通常默认文件夹名 BloodStrike 的全大小写形式）"""
        
        intro_label = ttk.Label(card, text=intro_text, style='Desc.TLabel', justify=tk.LEFT)
        intro_label.pack(pady=(10, 5), padx=25)
        
        # 可点击的GitHub链接
        link_frame = ttk.Frame(card)
        link_frame.pack(pady=(0, 10), padx=100, anchor=tk.W)
        ttk.Label(link_frame, text="GitHub：", style='Desc.TLabel').pack(side=tk.LEFT)
        github_link = tk.Label(link_frame, text="CN-Hobo/BloodStrike-region-limit",
                               font=("Microsoft YaHei", 9, "bold"), fg="#555555",
                               cursor="hand2", bg="#ffffff")
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/CN-Hobo/BloodStrike-region-limit"))
        
        # 路径显示区域
        path_frame = ttk.Frame(card)
        path_frame.pack(pady=(5, 15), padx=25, fill=tk.X)
        
        path_label = ttk.Label(path_frame, text="已选择的路径：", style='Path.TLabel')
        path_label.pack(anchor=tk.W)
        
        self.path_var = tk.StringVar(value="尚未选择文件夹")
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=70)
        path_entry.configure(state='readonly')
        path_entry.pack(fill=tk.X, pady=(3, 0))
        
        # 选择按钮
        select_button = ttk.Button(self.root, text="选择游戏文件夹", command=self.select_folder, style='Action.TButton')
        select_button.pack(pady=(5, 15))
        
        # 状态标签
        self.status_var = tk.StringVar(value="等待操作...")
        status_label = ttk.Label(self.root, textvariable=self.status_var, style='Status.TLabel')
        status_label.pack(pady=(0, 15))
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择 BloodStrike 游戏根目录")
        
        if not folder_path:
            return
        
        self.path_var.set(folder_path)
        
        # 验证文件夹名称
        folder_name = os.path.basename(folder_path)
        if folder_name.lower() != "bloodstrike":
            ret = messagebox.askyesno("文件夹名称不符", f"当前文件夹名称为 \"{folder_name}\"，不是 \"BLOODSTRIKE\" 或它的小写。\n*如果你确认这是重命名过的游戏根目录，请点击“是”继续。*\n\n仍然使用这个文件夹继续吗？")
            if not ret:
                self.status_var.set("已取消选择")
                return
        
        self.status_var.set("文件夹验证成功，正在定位目标文件...")
        self.process_dll(folder_path)
    
    def process_dll(self, game_folder):
        dll_dir = os.path.join(game_folder, self.dll_subdir)
        
        # 查找存在的DLL
        dll_path = None
        found_name = None
        for name in self.dll_names:
            path = os.path.join(dll_dir, name)
            if os.path.exists(path):
                dll_path = path
                found_name = name
                break
        
        if dll_path is None:
            searched = "\n".join(os.path.join(dll_dir, n) for n in self.dll_names)
            error_msg = f"找不到目标文件，已尝试：\n{searched}\n\n可能的解决方法：\n①确认游戏安装完整\n②以管理员身份运行本工具\n③游戏更新已修改了文件结构，等待工具更新"
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
                messagebox.showinfo("提示", "在该目录的DLL文件中未找到目标字符串。\n①目标文件可能已经打过补丁了\n②游戏可能更了文件结构，等工具更新")
                self.status_var.set("未找到目标字符串")
                return
            
            # 执行替换
            new_content = content.replace(self.target_string, self.replace_bytes)
            
            # 写入修改后的内容
            with open(dll_path, "wb") as f:
                f.write(new_content)
            
            # 成功提示
            messagebox.showinfo("成功", f"文件处理完成！\n原文件已备份为：\n{backup_path}")
            self.status_var.set(f"处理成功，替换了 {replace_count} 处。\n你现在可以尝试启动游戏了！")
            
            # 结束程序
            self.root.after(1000, self.root.destroy)
            
        except PermissionError:
            error_msg = "权限不足，无法写入文件。\n\n可能的解决方法：\n①关闭游戏后再尝试补丁操作\n②右键点击本工具，选择\"以管理员身份运行\"\n③检查文件是否被杀毒软件锁定"
            messagebox.showerror("权限错误", error_msg)
            self.status_var.set("权限不足")
        except Exception as e:
            error_msg = f"处理文件时发生错误：\n{str(e)}\n\n可能的解决方法：\n①确保文件没有被其他程序占用\n②检查磁盘空间是否充足\n③尝试重新安装游戏"
            messagebox.showerror("未知错误", error_msg)
            self.status_var.set("处理失败")

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodstrikePatcher(root)
    root.mainloop()
