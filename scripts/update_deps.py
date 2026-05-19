#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依赖管理工具 - 更新 requirements.txt"""

import subprocess
import sys
import re
from pathlib import Path


def get_latest_version(package: str) -> str:
    """获取包的最新版本"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", package.split(">=")[0].split("==")[0]],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        versions = re.findall(r'(\d+\.\d+\.\d+)', result.stdout)
        return versions[0] if versions else None
    except Exception:
        return None


def update_requirements(check_only: bool = False):
    """更新依赖版本"""
    req_file = Path(__file__).parent.parent / "requirements.txt"
    backup_file = req_file.with_suffix(".txt.bak")
    
    if not req_file.exists():
        print(f"❌ 找不到 {req_file}")
        return
    
    lines = req_file.read_text().strip().split("\n")
    updated_lines = []
    changed = []
    
    print(f"📦 检查 {len(lines)} 个依赖包...\n")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            updated_lines.append(line)
            continue
        
        package = line.split(">=")[0].split("==")[0]
        current_version = re.search(r'[>=]+([\d.]+)', line)
        current = current_version.group(1) if current_version else "?"
        
        print(f"⏳ 检查 {package}... (当前: {current})", end=" ")
        
        latest = get_latest_version(package)
        
        if latest and latest != current:
            new_line = f"{package}>={latest}"
            updated_lines.append(new_line)
            changed.append((package, current, latest))
            print(f"→ ✅ {latest}")
        else:
            updated_lines.append(line)
            print(f"✓ 已是最新")
    
    if not check_only and changed:
        req_file.write_text("\n".join(updated_lines) + "\n")
        if backup_file.exists():
            backup_file.write_text("\n".join(lines) + "\n")
        print(f"\n✅ 已更新 {len(changed)} 个包:")
        for pkg, old, new in changed:
            print(f"   {pkg}: {old} → {new}")
    elif changed:
        print(f"\n📋 发现 {len(changed)} 个可更新的包（使用 --write 写入）:")
        for pkg, old, new in changed:
            print(f"   {pkg}: {old} → {new}")
    else:
        print("\n✅ 所有依赖已是最新版本")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="更新 Python 依赖")
    parser.add_argument("--write", "-w", action="store_true", help="写入文件")
    args = parser.parse_args()
    
    update_requirements(check_only=not args.write)
