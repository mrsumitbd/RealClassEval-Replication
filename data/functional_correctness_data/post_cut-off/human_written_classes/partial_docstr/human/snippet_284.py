import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser

class VirtualLogDisplay:
    """虚拟滚动日志显示组件"""

    def __init__(self, parent, formatter):
        self.parent = parent
        self.formatter = formatter
        self.line_height = 20
        self.visible_lines = 30
        self.main_frame = ttk.Frame(parent)
        self.scrollbar = ttk.Scrollbar(self.main_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget = tk.Text(self.main_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, background='#1e1e1e', foreground='#ffffff', insertbackground='#ffffff', selectbackground='#404040', font=('Consolas', 10))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_widget.yview)
        self.configure_text_tags()
        self.log_index = None
        self.current_page = 0
        self.page_size = 500
        self.max_display_lines = 2000

    def pack(self, **kwargs):
        """包装pack方法"""
        self.main_frame.pack(**kwargs)

    def configure_text_tags(self):
        """配置文本标签样式"""
        self.text_widget.tag_configure('timestamp', foreground='#808080')
        self.text_widget.tag_configure('level', foreground='#808080')
        self.text_widget.tag_configure('module', foreground='#808080')
        self.text_widget.tag_configure('message', foreground='#ffffff')
        self.text_widget.tag_configure('extras', foreground='#808080')
        for level, color in self.formatter.level_colors.items():
            self.text_widget.tag_configure(f'level_{level}', foreground=color)
        for module, color in self.formatter.module_colors.items():
            self.text_widget.tag_configure(f'module_{module}', foreground=color)

    def set_log_index(self, log_index):
        """设置日志索引数据源"""
        self.log_index = log_index
        self.current_page = 0
        self.refresh_display()

    def refresh_display(self):
        """刷新显示"""
        if not self.log_index:
            self.text_widget.delete(1.0, tk.END)
            return
        self.text_widget.delete(1.0, tk.END)
        total_count = self.log_index.get_filtered_count()
        if total_count == 0:
            self.text_widget.insert(tk.END, '没有符合条件的日志记录\n')
            return
        start_index = 0
        end_index = min(total_count, self.max_display_lines)
        batch_size = 100
        for batch_start in range(start_index, end_index, batch_size):
            batch_end = min(batch_start + batch_size, end_index)
            self.display_batch(batch_start, batch_end)
            self.parent.update_idletasks()
        self.text_widget.see(tk.END)

    def display_batch(self, start_index, end_index):
        """批量显示日志条目"""
        for i in range(start_index, end_index):
            log_entry = self.log_index.get_entry_at_filtered_position(i)
            if log_entry:
                self.append_entry(log_entry, scroll=False)

    def append_entry(self, log_entry, scroll=True):
        """将单个日志条目附加到文本小部件"""
        should_scroll = scroll and self.text_widget.yview()[1] > 0.99
        parts, tags = self.formatter.format_log_entry(log_entry)
        line_text = ' '.join(parts) + '\n'
        start_pos = self.text_widget.index(tk.END + '-1c')
        self.text_widget.insert(tk.END, line_text)
        current_len = 0
        for part, tag_name in zip(parts, tags, strict=False):
            start_index = f'{start_pos}+{current_len}c'
            end_index = f'{start_pos}+{current_len + len(part)}c'
            self.text_widget.tag_add(tag_name, start_index, end_index)
            current_len += len(part) + 1
        if should_scroll:
            self.text_widget.see(tk.END)