#!/usr/bin/env python3
"""
Экстрактор документации из Rust файлов.
Извлекает функции, структуры, трейты и их документацию для LLM.
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class RustItem:
    """Базовый класс для Rust элементов."""
    name: str
    kind: str  # 'function', 'struct', 'enum', 'trait', 'impl', 'mod', 'const', 'static', 'type'
    visibility: str  # 'pub', 'pub(crate)', 'pub(super)', 'private'
    doc_comments: List[str]
    signature: str
    line_number: int
    file_path: str
    children: List['RustItem'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class RustDocExtractor:
    """Экстрактор документации из Rust кода."""
    
    # Паттерны для поиска элементов
    PATTERNS = {
        'function': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?(?:\s+crate|\s+super)?\s+)?'
            r'(?:const\s+|unsafe\s+|async\s+|extern\s+(?:"[^"]*"\s+)?)?'
            r'fn\s+(\w+)\s*\((.*?)\)(?:\s*->\s*([^{\n]+))?\s*\{',
            re.MULTILINE
        ),
        'struct': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?'
            r'struct\s+(\w+)(?:<[^>]+>)?(?:\([^)]*\)|\s*\{)',
            re.MULTILINE
        ),
        'enum': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?'
            r'enum\s+(\w+)(?:<[^>]+>)?\s*\{',
            re.MULTILINE
        ),
        'trait': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?'
            r'(?:unsafe\s+)?trait\s+(\w+)',
            re.MULTILINE
        ),
        'impl': re.compile(
            r'^(\s*)(?:pub(?:\([^)]*\))?\s+)?'
            r'(?:unsafe\s+)?impl(?:<[^>]+>)?\s+(?:for\s+)?(\w+(?:<[^>]+>)?)',
            re.MULTILINE
        ),
        'mod': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?mod\s+(\w+);',
            re.MULTILINE
        ),
        'const': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?const\s+(\w+)\s*:\s*([^=]+)\s*=\s*([^;]+);',
            re.MULTILINE
        ),
        'static': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?static\s+(\w+)\s*:\s*([^=]+)\s*=\s*([^;]+);',
            re.MULTILINE
        ),
        'type_alias': re.compile(
            r'^(\s*)(pub(?:\([^)]*\))?\s+)?type\s+(\w+)(?:<[^>]+>)?\s*=\s*([^;]+);',
            re.MULTILINE
        ),
    }
    
    def __init__(self, root_path: str, output_file: Optional[str] = None):
        self.root_path = Path(root_path).resolve()
        self.output_file = output_file
        self.items: List[RustItem] = []
        
    def extract_doc_comments(self, content: str, pos: int) -> List[str]:
        """Извлечение комментариев документации перед элементом."""
        docs = []
        
        # Ищем строку перед элементом
        before = content[:pos].rstrip()
        lines = before.split('\n')
        
        # Идём снизу вверх, собираем doc комментарии
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('///'):
                docs.insert(0, line[3:].strip())
            elif line.startswith('//!'):
                docs.insert(0, line[3:].strip())
            elif line.startswith('/*') or line.startswith('*'):
                # Block doc comments
                if '*/' in line:
                    break
                docs.insert(0, line.strip('* ').strip())
            elif line and not line.startswith('#['):
                # Непустая строка, не атрибут - конец документации
                break
        
        return docs
    
    def get_visibility(self, pub_match: Optional[str]) -> str:
        """Определение видимости элемента."""
        if pub_match is None:
            return 'private'
        
        pub_match = pub_match.strip()
        
        if pub_match == 'pub':
            return 'pub'
        elif pub_match.startswith('pub('):
            return pub_match
        else:
            return 'pub'
    
    def extract_functions(self, content: str, file_path: str) -> List[RustItem]:
        """Извлечение функций."""
        items = []
        
        for match in self.PATTERNS['function'].finditer(content):
            indent, visibility, name, params, return_type = match.groups()
            
            pos = match.start()
            docs = self.extract_doc_comments(content, pos)
            
            # Формируем полную сигнатуру
            signature = f"fn {name}({params})"
            if return_type:
                signature += f" -> {return_type.strip()}"
            
            line_number = content[:pos].count('\n') + 1
            
            items.append(RustItem(
                name=name,
                kind='function',
                visibility=self.get_visibility(visibility),
                doc_comments=docs,
                signature=signature,
                line_number=line_number,
                file_path=str(file_path)
            ))
        
        return items
    
    def extract_structs(self, content: str, file_path: str) -> List[RustItem]:
        """Извлечение структур."""
        items = []
        
        for match in self.PATTERNS['struct'].finditer(content):
            indent, visibility, name = match.groups()
            
            pos = match.start()
            docs = self.extract_doc_comments(content, pos)
            
            # Пытаемся извлечь полное определение
            brace_pos = content.find('{', match.end())
            paren_pos = content.find('(', match.end())
            
            if paren_pos != -1 and (brace_pos == -1 or paren_pos < brace_pos):
                # Tuple struct
                end_pos = content.find(')', paren_pos)
                signature = content[match.start():end_pos+1].strip()
                signature = re.sub(r'\s+', ' ', signature)
            elif brace_pos != -1:
                # Regular struct
                end_pos = self._find_matching_brace(content, brace_pos)
                signature = content[match.start():brace_pos].strip()
                signature = re.sub(r'\s+', ' ', signature)
            else:
                signature = f"struct {name}"
            
            line_number = content[:pos].count('\n') + 1
            
            items.append(RustItem(
                name=name,
                kind='struct',
                visibility=self.get_visibility(visibility),
                doc_comments=docs,
                signature=signature,
                line_number=line_number,
                file_path=str(file_path)
            ))
        
        return items
    
    def extract_enums(self, content: str, file_path: str) -> List[RustItem]:
        """Извлечение enum'ов."""
        items = []
        
        for match in self.PATTERNS['enum'].finditer(content):
            indent, visibility, name = match.groups()
            
            pos = match.start()
            docs = self.extract_doc_comments(content, pos)
            
            # Извлекаем полное определение
            brace_pos = content.find('{', match.end())
            if brace_pos != -1:
                end_pos = self._find_matching_brace(content, brace_pos)
                signature = content[match.start():brace_pos].strip()
                signature = re.sub(r'\s+', ' ', signature)
            else:
                signature = f"enum {name}"
            
            line_number = content[:pos].count('\n') + 1
            
            items.append(RustItem(
                name=name,
                kind='enum',
                visibility=self.get_visibility(visibility),
                doc_comments=docs,
                signature=signature,
                line_number=line_number,
                file_path=str(file_path)
            ))
        
        return items
    
    def extract_traits(self, content: str, file_path: str) -> List[RustItem]:
        """Извлечение трейтов."""
        items = []
        
        for match in self.PATTERNS['trait'].finditer(content):
            indent, visibility, name = match.groups()
            
            pos = match.start()
            docs = self.extract_doc_comments(content, pos)
            
            signature = f"trait {name}"
            line_number = content[:pos].count('\n') + 1
            
            items.append(RustItem(
                name=name,
                kind='trait',
                visibility=self.get_visibility(visibility),
                doc_comments=docs,
                signature=signature,
                line_number=line_number,
                file_path=str(file_path)
            ))
        
        return items
    
    def extract_impls(self, content: str, file_path: str) -> List[RustItem]:
        """Извлечение impl блоков."""
        items = []
        
        for match in self.PATTERNS['impl'].finditer(content):
            indent, name = match.groups()
            
            pos = match.start()
            docs = self.extract_doc_comments(content, pos)
            
            # Определяем, это impl Trait for Type или impl Type
            for_match = re.search(r'\bfor\s+(\w+)', match.group(0))
            if for_match:
                signature = f"impl {name} for {for_match.group(1)}"
            else:
                signature = f"impl {name}"
            
            line_number = content[:pos].count('\n') + 1
            
            items.append(RustItem(
                name=name,
                kind='impl',
                visibility='pub',
                doc_comments=docs,
                signature=signature,
                line_number=line_number,
                file_path=str(file_path)
            ))
        
        return items
    
    def _find_matching_brace(self, content: str, start: int) -> int:
        """Поиск закрывающей скобки с учётом вложенности."""
        count = 1
        pos = start + 1
        
        while pos < len(content) and count > 0:
            if content[pos] == '{':
                count += 1
            elif content[pos] == '}':
                count -= 1
            pos += 1
        
        return pos - 1
    
    def extract_from_file(self, file_path: Path) -> List[RustItem]:
        """Извлечение всех элементов из файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, IOError) as e:
            print(f"⚠️  Warning: Could not read {file_path}: {e}")
            return []
        
        items = []
        items.extend(self.extract_functions(content, file_path))
        items.extend(self.extract_structs(content, file_path))
        items.extend(self.extract_enums(content, file_path))
        items.extend(self.extract_traits(content, file_path))
        items.extend(self.extract_impls(content, file_path))
        
        return items
    
    def find_rust_files(self) -> List[Path]:
        """Поиск всех Rust файлов в проекте."""
        rust_files = []
        
        for root, dirs, files in os.walk(self.root_path):
            # Пропускаем target и другие служебные директории
            dirs[:] = [d for d in dirs if d not in ('target', '.git', 'node_modules')]
            
            for file in files:
                if file.endswith('.rs'):
                    rust_files.append(Path(root) / file)
        
        return sorted(rust_files)
    
    def generate_summary(self) -> Dict[str, Any]:
        """Генерация сводной статистики."""
        stats = {
            'total_files': 0,
            'total_items': 0,
            'by_kind': {},
            'by_visibility': {},
            'by_file': {}
        }
        
        for item in self.items:
            stats['total_items'] += 1
            
            # По типу
            stats['by_kind'][item.kind] = stats['by_kind'].get(item.kind, 0) + 1
            
            # По видимости
            stats['by_visibility'][item.visibility] = stats['by_visibility'].get(item.visibility, 0) + 1
            
            # По файлам
            stats['by_file'][item.file_path] = stats['by_file'].get(item.file_path, 0) + 1
        
        stats['total_files'] = len(stats['by_file'])
        
        return stats
    
    def format_item(self, item: RustItem, indent: int = 0) -> str:
        """Форматирование элемента для вывода."""
        lines = []
        prefix = "  " * indent
        
        # Заголовок
        visibility_icon = "🌍" if item.visibility == 'pub' else "🔒"
        kind_icon = {
            'function': '📦',
            'struct': '📋',
            'enum': '🔀',
            'trait': '🎯',
            'impl': '🔧',
            'mod': '📁',
            'const': '🔢',
            'static': '📌',
            'type': '🏷️'
        }.get(item.kind, '📄')
        
        lines.append(f"{prefix}{kind_icon} {visibility_icon} {item.kind.upper()}: {item.name}")
        lines.append(f"{prefix}   📍 {item.file_path}:{item.line_number}")
        
        # Сигнатура
        if item.signature:
            sig_lines = item.signature.split('\n')
            for sig_line in sig_lines[:3]:  # Первые 3 строки
                lines.append(f"{prefix}   {sig_line.strip()}")
            if len(sig_lines) > 3:
                lines.append(f"{prefix}   ...")
        
        # Документация
        if item.doc_comments:
            lines.append(f"{prefix}   📝 Documentation:")
            for doc_line in item.doc_comments[:5]:  # Первые 5 строк документации
                lines.append(f"{prefix}      {doc_line}")
            if len(item.doc_comments) > 5:
                lines.append(f"{prefix}      ... ({len(item.doc_comments) - 5} more lines)")
        
        # Дети
        if item.children:
            lines.append(f"{prefix}   👶 Children ({len(item.children)}):")
            for child in item.children[:5]:
                lines.append(f"{prefix}      - {child.kind}: {child.name}")
            if len(item.children) > 5:
                lines.append(f"{prefix}      ... ({len(item.children) - 5} more)")
        
        return "\n".join(lines)
    
    def generate(self, format: str = 'text') -> str:
        """Генерация полной документации."""
        # Находим все Rust файлы
        rust_files = self.find_rust_files()
        print(f"🔍 Found {len(rust_files)} Rust files")
        
        # Извлекаем элементы из каждого файла
        for file_path in rust_files:
            items = self.extract_from_file(file_path)
            self.items.extend(items)
            print(f"  ✅ {file_path.relative_to(self.root_path)}: {len(items)} items")
        
        print(f"\n📊 Total: {len(self.items)} items extracted")
        
        # Генерируем вывод в зависимости от формата
        if format == 'json':
            return self._generate_json()
        elif format == 'markdown':
            return self._generate_markdown()
        else:
            return self._generate_text()
    
    def _generate_text(self) -> str:
        """Генерация текстового вывода."""
        output = []
        
        output.append("=" * 80)
        output.append("RUST CODE DOCUMENTATION FOR LLM")
        output.append(f"Root: {self.root_path}")
        output.append("=" * 80)
        output.append("")
        
        # Группируем по файлам
        by_file = {}
        for item in self.items:
            if item.file_path not in by_file:
                by_file[item.file_path] = []
            by_file[item.file_path].append(item)
        
        for file_path, items in sorted(by_file.items()):
            rel_path = Path(file_path).relative_to(self.root_path)
            output.append(f"\n{'=' * 80}")
            output.append(f"📄 FILE: {rel_path}")
            output.append(f"{'=' * 80}")
            output.append("")
            
            for item in items:
                output.append(self.format_item(item))
                output.append("")
        
        # Статистика
        stats = self.generate_summary()
        output.append("\n" + "=" * 80)
        output.append("📊 STATISTICS")
        output.append("=" * 80)
        output.append(f"Total Files: {stats['total_files']}")
        output.append(f"Total Items: {stats['total_items']}")
        output.append("")
        output.append("By Kind:")
        for kind, count in sorted(stats['by_kind'].items(), key=lambda x: x[1], reverse=True):
            output.append(f"  {kind}: {count}")
        output.append("")
        output.append("By Visibility:")
        for vis, count in sorted(stats['by_visibility'].items(), key=lambda x: x[1], reverse=True):
            output.append(f"  {vis}: {count}")
        
        output.append("\n" + "=" * 80)
        output.append("END OF DOCUMENTATION")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def _generate_json(self) -> str:
        """Генерация JSON вывода."""
        data = {
            'root_path': str(self.root_path),
            'statistics': self.generate_summary(),
            'items': [asdict(item) for item in self.items]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _generate_markdown(self) -> str:
        """Генерация Markdown вывода."""
        output = []
        
        output.append("# Rust Code Documentation\n")
        output.append(f"**Root:** `{self.root_path}`\n")
        output.append(f"**Total Items:** {len(self.items)}\n")
        output.append("")
        
        # Группируем по файлам
        by_file = {}
        for item in self.items:
            if item.file_path not in by_file:
                by_file[item.file_path] = []
            by_file[item.file_path].append(item)
        
        for file_path, items in sorted(by_file.items()):
            rel_path = Path(file_path).relative_to(self.root_path)
            output.append(f"\n## 📄 {rel_path}\n")
            
            for item in items:
                visibility_badge = "🌍 `pub`" if item.visibility == 'pub' else "🔒 `private`"
                output.append(f"\n### {item.kind.capitalize()}: `{item.name}` {visibility_badge}\n")
                output.append(f"**Location:** `{rel_path}:{item.line_number}`\n")
                
                if item.signature:
                    output.append(f"\n```rust\n{item.signature}\n```\n")
                
                if item.doc_comments:
                    output.append("\n**Documentation:**\n")
                    output.append("\n".join(f"> {doc}" for doc in item.doc_comments))
                    output.append("")
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Extract documentation from Rust files for LLM"
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
        "-f", "--format",
        choices=['text', 'json', 'markdown'],
        default='text',
        help="Output format (default: text)"
    )
    
    args = parser.parse_args()
    
    extractor = RustDocExtractor(
        root_path=args.root,
        output_file=args.output
    )
    
    result = extractor.generate(format=args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n✅ Documentation saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()