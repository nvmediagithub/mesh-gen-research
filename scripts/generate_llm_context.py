#!/usr/bin/env python3
"""
Комбинированный генератор контекста для LLM.
Запускает оба скрипта и создаёт один полный файл.
"""

import subprocess
import sys
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Generate complete LLM context for the project"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory of the project"
    )
    parser.add_argument(
        "-o", "--output",
        default="LLM_CONTEXT.md",
        help="Output file (default: LLM_CONTEXT.md)"
    )
    
    args = parser.parse_args()
    
    root = Path(args.root).resolve()
    output = Path(args.output)
    
    print("🚀 Generating LLM context...")
    print("")
    
    # Часть 1: Структура проекта
    print("📁 Generating project structure...")
    structure_script = root / "scripts" / "generate_project_structure.py"
    
    if structure_script.exists():
        result = subprocess.run(
            [sys.executable, str(structure_script), str(root), "--no-summary"],
            capture_output=True,
            text=True
        )
        structure_content = result.stdout
    else:
        structure_content = "⚠️ Project structure script not found\n"
    
    # Часть 2: Rust документация
    print("🦀 Extracting Rust documentation...")
    rust_script = root / "scripts" / "extract_rust_docs.py"
    
    if rust_script.exists():
        result = subprocess.run(
            [sys.executable, str(rust_script), str(root), "-f", "markdown"],
            capture_output=True,
            text=True
        )
        rust_content = result.stdout
    else:
        rust_content = "⚠️ Rust documentation script not found\n"
    
    # Объединяем всё
    print("📝 Combining results...")
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write("# LLM CONTEXT FOR PROJECT\n\n")
        f.write(f"**Project Root:** `{root}`\n\n")
        f.write("---\n\n")
        
        f.write("## 📁 PROJECT STRUCTURE\n\n")
        f.write(structure_content)
        f.write("\n\n---\n\n")
        
        f.write("## 🦀 RUST CODE DOCUMENTATION\n\n")
        f.write(rust_content)
    
    print("")
    print(f"✅ Complete LLM context saved to: {output}")
    print(f"📊 File size: {output.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()