#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def print_color(text, color_code):
    """打印带颜色的文本，支持终端 ANSI 转义"""
    # 31=红, 32=绿, 33=黄, 36=青, 90=灰
    print(f"\033[{color_code}m{text}\033[0m")

def main():
    source_dir = Path(__file__).resolve().parent
    
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1]).resolve()
    else:
        target_dir = Path.cwd().resolve()
        
    if target_dir == source_dir:
        print_color("错误: 不能将目标目录设置为当前源码仓库本身。", "31")
        print_color("请在您的目标项目中执行该脚本，或将目标项目路径作为参数传入。例如:", "33")
        print_color(f"python \"{source_dir / 'install.py'}\" /path/to/your-project", "33")
        sys.exit(1)
        
    print_color(f"🚀 开始安装 Antigravity Kit 至: {target_dir}", "36")
    
    # 1. 复制 .agent 目录
    source_agent = source_dir / ".agent"
    target_agent = target_dir / ".agent"
    
    if target_agent.exists():
        print_color("⚠️ 警告: 目标项目已存在 .agent 目录，将进行覆盖...", "33")
        shutil.rmtree(target_agent)
        
    shutil.copytree(source_agent, target_agent)
    print_color("✅ 已复制 .agent 文件夹。", "32")

    # 3. 配置 Git 忽略规则
    git_dir = target_dir / ".git"
    if git_dir.exists() and git_dir.is_dir():
        info_dir = git_dir / "info"
        info_dir.mkdir(exist_ok=True)
        
        exclude_file = info_dir / "exclude"
        exclude_file.touch(exist_ok=True)
        
        with open(exclude_file, "r", encoding="utf-8") as f:
            exclude_content = f.read().splitlines()
            
        with open(exclude_file, "a", encoding="utf-8") as f:
            if ".agent/" not in exclude_content:
                # 确保另起一行
                if exclude_content and not exclude_content[-1] == "":
                    f.write("\n")
                f.write(".agent/\n")
                print_color("✅ 已将 .agent/ 添加至 .git/info/exclude。", "32")
            else:
                print_color("ℹ️ .agent/ 已存在于 .git/info/exclude 中，跳过。", "90")

    else:
        print_color("⚠️ 未检测到 .git 目录，跳过配置 git 忽略规则。", "33")
        print_color("注意: 如果您稍后初始化 git，请记得手动将 .agent/ 添加至 .git/info/exclude!", "33")
        
    print_color("🎉 安装完成！您现在可以在目标项目中使用 Antigravity Kit 的 AI 工作流了。", "32")

if __name__ == "__main__":
    main()
