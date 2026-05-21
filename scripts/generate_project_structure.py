#!/usr/bin/env python3
"""
Генератор структуры проекта для LLM.
Создаёт текстовое представление всей файловой системы проекта.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Set, Optional


class ProjectStructureGenerator:
    """Генератор структуры проекта."""
    
    # Папки и файлы для исключения
    DEFAULT_IGNORES = {
        '.git', '.idea', '.vscode', '__pycache__', 'node_modules',
        'target', 'bin', 'obj', '.cargo', 'docs', 'assets',
        '.DS_Store', 'Thumbs.db'
    }
    
    # Расширения файлов для включения
    INCLUDE_EXTENSIONS = {
        '.rs', '.toml', '.py', '.md', '.txt', '.json', '.yaml', '.yml',
        '.sh', '.bash', '.gitignore', '.env.example'
    }
    
    def __init__(self, 
                 root_path: str,
                 output_file: Optional[str] = None,
                 ignores: Optional[Set[str]] = None,
                 include_extensions: Optional[Set[str]] = None):
        self.root_path = Path(root_path).resolve()
        self.output_file = output_file
        self.ignores = ignores or self.DEFAULT_IGNORES
        self.include_extensions = include_extensions or self.INCLUDE_EXTENSIONS
        
    def should_ignore(self, path: Path) -> bool:
        """Проверка, нужно ли игнорировать файл/папку."""
        for part in path.parts:
            if part in self.ignores:
                return True
            if part.startswith('.'):
                return True
        return False
    
    def should_include_file(self, path: Path) -> bool:
        """Проверка, нужно ли включить файл."""
        if path.is_file():
            ext = path.suffix.lower()
            name = path.name.lower()
            return ext in self.include_extensions or name in self.include_extensions
        return True
    
    def get_tree_structure(self, 
                          path: Optional[Path] = None, 
                          prefix: str = "", 
                          max_depth: int = 10,
                          current_depth: int = 0) -> str:
        """Рекурсивная генерация дерева структуры."""
        if path is None:
            path = self.root_path
            
        if current_depth >= max_depth:
            return f"{prefix}... (max depth reached)\n"
        
        if self.should_ignore(path):
            return ""
        
        result = ""
        
        if current_depth == 0:
            result += f"📁 {path.name}/\n"
        else:
            if path.is_file():
                size = path.stat().st_size
                size_str = self._format_size(size)
                result += f"{prefix}📄 {path.name} ({size_str})\n"
            else:
                result += f"{prefix}📁 {path.name}/\n"
        
        if path.is_dir():
            try:
                entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                entries = [e for e in entries if not self.should_ignore(e)]
                
                for i, entry in enumerate(entries):
                    if entry.is_file() and not self.should_include_file(entry):
                        continue
                    
                    is_last = (i == len(entries) - 1)
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    connector = "└── " if is_last else "├── "
                    
                    result += f"{prefix}{connector}"
                    result += self.get_tree_structure(
                        entry, 
                        new_prefix, 
                        max_depth, 
                        current_depth + 1
                    ).lstrip()
                    
            except PermissionError:
                result += f"{prefix}    └── [Permission Denied]\n"
        
        return result
    
    def _format_size(self, size: int) -> str:
        """Форматирование размера файла."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def generate_summary(self) -> str:
        """Генерация сводной информации о проекте."""
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': {},
            'largest_files': []
        }
        
        for root, dirs, files in os.walk(self.root_path):
            root_path = Path(root)
            
            if self.should_ignore(root_path):
                dirs.clear()
                continue
            
            stats['total_dirs'] += 1
            
            for file in files:
                file_path = root_path / file
                
                if self.should_ignore(file_path):
                    continue
                
                if not self.should_include_file(file_path):
                    continue
                
                stats['total_files'] += 1
                
                try:
                    size = file_path.stat().st_size
                    stats['total_size'] += size
                    
                    ext = file_path.suffix.lower() or '(no extension)'
                    stats['by_extension'][ext] = stats['by_extension'].get(ext, 0) + 1
                    
                    stats['largest_files'].append({
                        'path': str(file_path.relative_to(self.root_path)),
                        'size': size
                    })
                except (OSError, ValueError):
                    pass
        
        stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
        stats['largest_files'] = stats['largest_files'][:10]
        
        return stats
    
    def generate(self, include_summary: bool = True, max_depth: int = 10) -> str:
        """Генерация полной структуры проекта."""
        output = []
        
        # Заголовок
        output.append("=" * 80)
        output.append("PROJECT STRUCTURE FOR LLM")
        output.append(f"Root: {self.root_path}")
        output.append("=" * 80)
        output.append("")
        
        # Дерево структуры
        output.append("📁 DIRECTORY STRUCTURE:")
        output.append("-" * 80)
        output.append(self.get_tree_structure(max_depth=max_depth))
        output.append("")
        
        # Сводная статистика
        if include_summary:
            stats = self.generate_summary()
            
            output.append("📊 PROJECT STATISTICS:")
            output.append("-" * 80)
            output.append(f"Total Files: {stats['total_files']}")
            output.append(f"Total Directories: {stats['total_dirs']}")
            output.append(f"Total Size: {self._format_size(stats['total_size'])}")
            output.append("")
            
            output.append("Files by Extension:")
            for ext, count in sorted(stats['by_extension'].items(), key=lambda x: x[1], reverse=True):
                output.append(f"  {ext}: {count}")
            output.append("")
            
            output.append("Top 10 Largest Files:")
            for i, file_info in enumerate(stats['largest_files'], 1):
                output.append(f"  {i}. {file_info['path']} ({self._format_size(file_info['size'])})")
            output.append("")
        
        output.append("=" * 80)
        output.append("END OF PROJECT STRUCTURE")
        output.append("=" * 80)
        
        result = "\n".join(output)
        
        # Сохранение в файл
        if self.output_file:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Project structure saved to: {self.output_file}")
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate project structure for LLM"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory of the project (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: print to stdout)"
    )
    parser.add_argument(
        "-d", "--max-depth",
        type=int,
        default=10,
        help="Maximum depth of directory tree (default: 10)"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Don't include summary statistics"
    )
    
    args = parser.parse_args()
    
    generator = ProjectStructureGenerator(
        root_path=args.root,
        output_file=args.output
    )
    
    result = generator.generate(
        include_summary=not args.no_summary,
        max_depth=args.max_depth
    )
    
    if not args.output:
        print(result)


if __name__ == "__main__":
    main()