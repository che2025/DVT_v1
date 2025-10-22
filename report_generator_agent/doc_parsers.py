import re
import tempfile
import os
from typing import Dict, Any, List, Optional
from fastapi import UploadFile
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


class DocumentParser:
    """
    解析Word文档的层级结构，支持：
    - 主要章节（1.0, 2.0, 3.0等）
    - 子章节（1.1, 1.2等）
    - 混合内容（文字 + 表格按顺序排列）
    """
    
    def __init__(self):
        self.parsed_data = {}
        self.current_section = None
        self.content_counter = {}
        self.stop_parsing = False
    
    async def parse_document(self, file: UploadFile) -> Dict[str, Any]:
        """解析上传的Word文档"""
        try:
            # 读取文件内容
            contents = await file.read()
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(contents)
                tmp_file.flush()
                tmp_file_path = tmp_file.name
            
            try:
                # 加载Word文档
                doc = Document(tmp_file_path)
                
                # 解析文档结构
                self.parsed_data = {}
                self.current_section = None
                self.content_counter = {}
                self.stop_parsing = False  # 停止解析标志
                
                # 遍历文档中的所有元素
                for element in doc.element.body:
                    # 检查是否应该停止解析
                    if self.stop_parsing:
                        print("📋 遇到APPENDICES章节，停止解析")
                        break
                        
                    if element.tag.endswith('p'):  # 段落
                        paragraph = Paragraph(element, doc.element.body)
                        self._process_paragraph(paragraph)
                    elif element.tag.endswith('tbl'):  # 表格
                        table = Table(element, doc.element.body)
                        self._process_table(table)
                
                return self.parsed_data
                
            finally:
                # 清理临时文件
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            raise Exception(f"解析文档失败: {str(e)}")
    
    def _process_paragraph(self, paragraph: Paragraph):
        """处理段落内容"""
        text = paragraph.text.strip()
        if not text:
            return
        
        # 检查是否遇到APPENDICES章节，如果是则停止解析
        if self._should_stop_parsing(text):
            self.stop_parsing = True
            return
            
        # 检查是否为章节标题
        section_match = self._extract_section_number(text)
        
        if section_match:
            section_num, title = section_match
            
            if self._is_main_section(section_num):
                # 主章节 (如 1.0, 2.0)
                self.current_section = section_num
                self.parsed_data[section_num] = {"title": title}
                self.content_counter[section_num] = 0
            else:
                # 子章节 (如 1.1, 1.2)
                self.current_section = section_num
                self.parsed_data[section_num] = text
                self.content_counter[section_num] = 0
        else:
            # 普通内容，归属到当前章节
            if self.current_section:
                self._add_content_to_section(self.current_section, text, "text")
    
    def _process_table(self, table: Table):
        """处理表格内容"""
        if not self.current_section:
            return
            
        # 解析表格数据
        table_data = []
        
        # 获取表头
        if table.rows:
            headers = []
            first_row = table.rows[0]
            for cell in first_row.cells:
                headers.append(cell.text.strip())
            
            # 获取数据行
            for row in table.rows[1:]:
                row_data = {}
                for i, cell in enumerate(row.cells):
                    header = headers[i] if i < len(headers) else f"Column_{i+1}"
                    row_data[header] = cell.text.strip()
                table_data.append(row_data)
        
        # 将表格添加到当前章节
        self._add_content_to_section(self.current_section, table_data, "table")
    
    def _extract_section_number(self, text: str) -> Optional[tuple]:
        """提取章节编号和标题"""
        # 首先尝试标准格式: "1.0 PURPOSE" 或 "1.1 Some content"
        numbered_patterns = [
            r'^(\d+\.\d+)\s+(.*)$',  # 1.0 PURPOSE
            r'^(\d+\.\d+)\.?\s*(.*)$',  # 1.0. PURPOSE  
            r'^(\d+\.\d+)\s*:\s*(.*)$',  # 1.0: PURPOSE
        ]
        
        for pattern in numbered_patterns:
            match = re.match(pattern, text)
            if match:
                section_num = match.group(1)
                title = match.group(2).strip()
                return (section_num, title)
        
        # 如果没有数字格式，尝试识别常见的章节标题
        section_titles = [
            'Purpose', 'Scope', 'Background', 'Test Method Summary', 'References', 
            'Definitions', 'Responsibility', 'Materials', 'Equipment', 
            'General Instructions', 'Procedure', 'Acceptance Criteria',
            'Device Under Test Configuration', 'Test Consumables', 
            'Test Method', 'Test Setup', 'Test Execution', 'Data Analysis'
        ]
        
        # 检查是否为章节标题（单独一行的标题）
        text_clean = text.strip()
        if len(text_clean) < 100 and any(title.lower() in text_clean.lower() for title in section_titles):
            # 如果文本很短且包含章节关键词，认为是章节标题
            # 为这些章节分配一个序号
            section_index = self._get_section_index(text_clean)
            return (f"{section_index}.0", text_clean)
        
        return None
    
    def _is_main_section(self, section_num: str) -> bool:
        """判断是否为主章节 (如 1.0, 2.0)"""
        return section_num.endswith('.0')
    
    def _should_stop_parsing(self, text: str) -> bool:
        """检查是否应该停止解析（遇到APPENDICES章节）"""
        text_lower = text.lower().strip()
        
        # 检查各种APPENDICES的表达方式
        appendices_patterns = [
            'appendices',
            'appendix',
            '附录',
            'attachments'
        ]
        
        # 检查是否为单独的APPENDICES标题行
        for pattern in appendices_patterns:
            if text_lower == pattern or text_lower.startswith(pattern + ' ') or text_lower.startswith(pattern + ':'):
                return True
        
        # 检查带编号的appendices (如 "1.0 APPENDICES")
        if any(pattern in text_lower for pattern in appendices_patterns):
            # 如果包含appendices相关词汇，且文本较短（可能是标题）
            if len(text.strip()) < 50:
                return True
        
        return False
    
    def _get_section_index(self, section_title: str) -> int:
        """为章节标题分配一个索引号"""
        section_mapping = {
            'Purpose': 1,
            'Scope': 2, 
            'Background': 3,
            'Test Method Summary': 4,
            'References': 5,
            'Definitions': 6,
            'Responsibility': 7,
            'Materials': 8,
            'Device Under Test Configuration': 9,
            'Test Consumables': 10,
            'Equipment': 11,
            'General Instructions': 12,
            'Procedure': 13,
            'Test Method': 14,
            'Test Setup': 15,
            'Test Execution': 16,
            'Data Analysis': 17,
            'Acceptance Criteria': 18,
        }
        
        # 查找最匹配的章节标题
        title_lower = section_title.lower()
        for key, value in section_mapping.items():
            if key.lower() in title_lower:
                return value
        
        # 如果没找到，使用哈希值生成一个唯一编号
        return abs(hash(section_title)) % 100 + 20
    
    def _add_content_to_section(self, section_num: str, content: Any, content_type: str):
        """向章节添加内容"""
        # 如果章节还不存在，创建它
        if section_num not in self.parsed_data:
            self.parsed_data[section_num] = {}
        
        # 如果是主章节且只有title，需要添加内容区域
        if isinstance(self.parsed_data[section_num], dict) and "title" in self.parsed_data[section_num]:
            # 这是主章节，保持title，添加内容
            pass
        elif isinstance(self.parsed_data[section_num], str):
            # 这是子章节，将原文本作为第一个内容
            original_text = self.parsed_data[section_num]
            self.parsed_data[section_num] = {"content_1": original_text}
            self.content_counter[section_num] = 1
        elif not isinstance(self.parsed_data[section_num], dict):
            # 初始化为字典
            self.parsed_data[section_num] = {}
            self.content_counter[section_num] = 0
        
        # 添加新内容
        self.content_counter[section_num] += 1
        content_key = f"content_{self.content_counter[section_num]}"
        
        if content_type == "table":
            self.parsed_data[section_num][content_key] = {
                "type": "table",
                "data": content
            }
        else:
            self.parsed_data[section_num][content_key] = content
    
    def format_for_ai_prompt(self) -> str:
        """格式化解析结果为AI可读的提示格式"""
        formatted_sections = []
        
        for section_num in sorted(self.parsed_data.keys(), key=self._sort_section_key):
            section_data = self.parsed_data[section_num]
            
            if isinstance(section_data, str):
                # 简单文本章节
                formatted_sections.append(f"## {section_num}\n{section_data}\n")
                
            elif isinstance(section_data, dict):
                if "title" in section_data:
                    # 主章节有标题
                    formatted_sections.append(f"## {section_num}: {section_data['title']}\n")
                    
                    # 添加其他内容
                    content_items = [(k, v) for k, v in section_data.items() if k != "title"]
                    content_items.sort(key=lambda x: self._extract_content_number(x[0]))
                    
                    for key, value in content_items:
                        formatted_sections.append(self._format_content_item(key, value))
                        
                else:
                    # 子章节或内容章节
                    formatted_sections.append(f"## {section_num}\n")
                    
                    content_items = list(section_data.items())
                    content_items.sort(key=lambda x: self._extract_content_number(x[0]))
                    
                    for key, value in content_items:
                        formatted_sections.append(self._format_content_item(key, value))
        
        return "\n".join(formatted_sections)
    
    def _format_content_item(self, key: str, value: Any) -> str:
        """格式化单个内容项"""
        if isinstance(value, dict) and value.get("type") == "table":
            # 表格内容
            table_data = value.get("data", [])
            if table_data:
                formatted_table = "### 表格内容:\n"
                # 简化表格显示
                for i, row in enumerate(table_data[:3]):  # 只显示前3行作为示例
                    formatted_table += f"行{i+1}: {row}\n"
                if len(table_data) > 3:
                    formatted_table += f"... (共{len(table_data)}行数据)\n"
                return formatted_table
            else:
                return "### 空表格\n"
        else:
            # 文本内容
            return f"{value}\n"
    
    def _sort_section_key(self, section_num: str) -> tuple:
        """生成章节排序的键值"""
        parts = section_num.split('.')
        return (int(parts[0]), int(parts[1]))
    
    def _extract_content_number(self, content_key: str) -> int:
        """从content_N中提取数字N"""
        match = re.search(r'content_(\d+)', content_key)
        return int(match.group(1)) if match else 0


# 工厂函数
async def parse_document(file: UploadFile) -> Dict[str, Any]:
    """解析Word文档并返回结构化数据"""
    parser = DocumentParser()
    return await parser.parse_document(file)


# 快捷格式化函数
async def parse_document_for_ai(file: UploadFile) -> str:
    """解析Word文档并返回AI友好的格式"""
    parser = DocumentParser()
    parsed_data = await parser.parse_document(file)
    return parser.format_for_ai_prompt()


# 测试函数
async def test_document_parser():
    """测试文档解析器"""
    import sys
    import json
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'Inputs/PTL-903900 rev002 G7 GSS Wearable and Transmitter Battery Life Accelerated Aging Protocol.docx'
    
    try:
        # 模拟UploadFile
        class MockUploadFile:
            def __init__(self, file_path):
                self.file_path = file_path
            
            async def read(self):
                with open(self.file_path, 'rb') as f:
                    return f.read()
        
        mock_file = MockUploadFile(file_path)
        parser = DocumentParser()
        
        print("🔍 开始解析文档...")
        parsed_data = await parser.parse_document(mock_file)
        
        print("📊 解析统计:")
        print(f"   总章节数: {len(parsed_data)}")
        
        print(parsed_data)
        # 显示每个章节的详细信息
        
        print("🤖 AI格式化结果 (完整版):")
        print("="*80)
        ai_formatted = parser.format_for_ai_prompt()
        print(ai_formatted)
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_document_parser())
