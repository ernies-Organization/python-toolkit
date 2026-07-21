import os
import re
import tkinter as tk
import webbrowser
from html.parser import HTMLParser
from tkinter import messagebox


# Helper class to strip/parse raw HTML tags inside markdown lines
class HTMLToTextParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return "".join(self.text)


class CompleteMarkdownViewer(tk.Frame):
    """A Tkinter widget that parses and renders Markdown text using only Python standard library modules."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_document_path = None

        # Main Text Widget configuration
        self.text_widget = tk.Text(
            self,
            wrap="word",
            relief="flat",
            padx=15,
            pady=15,
            selectbackground="#cce5ff",  # Highlight color when text is selected for copying
            selectforeground="#000000",
        )

        # Vertical Scrollbar configuration
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.text_widget.yview
        )
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.text_widget.pack(side="left", fill="both", expand=True)

        # Set up all tag styles (Fonts, sizes, margins, colors)
        self._setup_tags()

    def _setup_tags(self):
        """Defines styling tags used for rendering markdown elements."""
        base_font = ("Segoe UI", 11)
        code_font = ("Consolas", 10)

        # Headings (H1 to H6)
        self.text_widget.tag_configure(
            "h1", font=("Segoe UI", 20, "bold"), spacing1=12, spacing3=6
        )
        self.text_widget.tag_configure(
            "h2", font=("Segoe UI", 16, "bold"), spacing1=10, spacing3=5
        )
        self.text_widget.tag_configure(
            "h3", font=("Segoe UI", 14, "bold"), spacing1=8, spacing3=4
        )
        self.text_widget.tag_configure(
            "h4", font=("Segoe UI", 12, "bold"), spacing1=6, spacing3=3
        )
        self.text_widget.tag_configure(
            "h5", font=("Segoe UI", 11, "bold"), spacing1=4, spacing3=2
        )
        self.text_widget.tag_configure(
            "h6",
            font=("Segoe UI", 10, "bold"),
            foreground="#555555",
            spacing1=4,
            spacing3=2,
        )

        # Inline Text Styles
        self.text_widget.tag_configure("body", font=base_font, spacing3=4)
        self.text_widget.tag_configure("bold", font=("Segoe UI", 11, "bold"))
        self.text_widget.tag_configure("italic", font=("Segoe UI", 11, "italic"))
        self.text_widget.tag_configure(
            "bold_italic", font=("Segoe UI", 11, "bold", "italic")
        )
        self.text_widget.tag_configure("strikethrough", overstrike=True)
        self.text_widget.tag_configure(
            "underline", font=("Segoe UI", 11, "underline")
        )
        self.text_widget.tag_configure(
            "highlight", background="#fff59d", foreground="#000000"
        )

        # Block & List Styles
        self.text_widget.tag_configure(
            "list_item", font=base_font, lmargin1=15, lmargin2=30
        )
        self.text_widget.tag_configure(
            "task_list", font=base_font, lmargin1=15, lmargin2=30
        )
        self.text_widget.tag_configure(
            "blockquote",
            font=("Segoe UI", 10, "italic"),
            foreground="#555555",
            lmargin1=20,
            lmargin2=20,
        )
        self.text_widget.tag_configure(
            "hr", font=("Segoe UI", 10), foreground="#a0a0a0", justify="center"
        )
        self.text_widget.tag_configure(
            "table_row", font=code_font, lmargin1=15, lmargin2=15
        )
        self.text_widget.tag_configure(
            "footnote", font=("Segoe UI", 9), foreground="#666666"
        )

        # Code Block Styles
        self.text_widget.tag_configure(
            "inline_code", font=code_font, foreground="#c7254e"
        )
        self.text_widget.tag_configure(
            "code_block",
            font=code_font,
            foreground="#222222",
            lmargin1=25,
            lmargin2=25,
        )

    def load_markdown(self, markdown_text, source_path=None):
        """Parses raw Markdown string line-by-line and renders it into the Text widget."""
        self.current_document_path = (
            os.path.abspath(source_path) if source_path else None
        )

        # Prepare Text widget for updating
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", tk.END)

        lines = markdown_text.splitlines()
        in_code_block = False
        in_html_block = False

        for line in lines:
            # Check for Code Block delimiters (```)
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # Render code block lines directly without parsing inline formatting
            if in_code_block:
                self.text_widget.insert("end", line + "\n", "code_block")
                continue

            # Handle multi-line HTML tags (e.g., <details>, <div>)
            if line.strip().startswith("<details") or line.strip().startswith(
                "<div"
            ):
                in_html_block = True
            if in_html_block:
                parser = HTMLToTextParser()
                parser.feed(line)
                cleaned_text = parser.get_data()
                if cleaned_text.strip():
                    self.text_widget.insert("end", cleaned_text + "\n", "body")
                if "</details>" in line or "</div>" in line:
                    in_html_block = False
                continue

            # Horizontal Divider Rules (---, ***, ___)
            if re.match(r"^(\*|\-|_){3,}$", line.strip()):
                self.text_widget.insert(
                    "end", "─────────────────────────────────────────\n", "hr"
                )
                continue

            # Headings (# to ######)
            if re.match(r"^#{1,6}\s", line):
                level = len(line.split()[0])
                content = line[level + 1 :]
                self.text_widget.insert("end", content + "\n", f"h{level}")
                continue

            # Markdown Pipe Tables (| Column 1 | Column 2 |)
            if line.strip().startswith("|") and line.strip().endswith("|"):
                # Skip divider rows (|---|---|)
                if not re.match(r"^\|[\s\-:|]+\|$", line.strip()):
                    cells = [
                        c.strip() for c in line.strip().strip("|").split("|")
                    ]
                    formatted_row = " | ".join(cells)
                    self.text_widget.insert(
                        "end", f"│ {formatted_row} │\n", "table_row"
                    )
                continue

            # Task Lists (- [ ] or - [x])
            if re.match(r"^\s*[\-\*\+]\s+\[[ xX]\]\s", line):
                checked = "[x]" in line or "[X]" in line
                box = "☑ " if checked else "☐ "
                content = re.sub(r"^\s*[\-\*\+]\s+\[[ xX]\]\s", "", line)
                self._insert_formatted_line(f"{box}{content}\n", "task_list")
                continue

            # Blockquotes (> Quote)
            if line.strip().startswith(">"):
                quote_depth = len(re.match(r"^>+", line.strip()).group(0))
                quote_text = line.strip().lstrip("> ").strip()
                prefix = "│ " * quote_depth
                self._insert_formatted_line(
                    f"{prefix}{quote_text}\n", "blockquote"
                )
                continue

            # Unordered Bullet Lists (- or * or +)
            if re.match(r"^\s*[\-\*\+]\s", line):
                content = re.sub(r"^\s*[\-\*\+]\s", "", line)
                self._insert_formatted_line(f"• {content}\n", "list_item")
                continue

            # Numbered/Ordered Lists (1., 2., etc.)
            if re.match(r"^\s*\d+\.\s", line):
                match = re.match(r"^\s*(\d+\.)\s(.*)", line)
                num, content = match.groups()
                self._insert_formatted_line(f"{num} {content}\n", "list_item")
                continue

            # Footnote Definitions ([^1]: text)
            if re.match(r"^\[\^\d+\]:\s", line):
                self.text_widget.insert("end", line + "\n", "footnote")
                continue

            # Indented Code Blocks (4 spaces or 1 tab)
            if line.startswith("    ") or line.startswith("\t"):
                self.text_widget.insert("end", line[4:] + "\n", "code_block")
                continue

            # Default: Render line as normal body paragraph
            self._insert_formatted_line(line + "\n", "body")

        # Keep widget enabled so the user can select and copy text with Ctrl+C
        self.text_widget.config(state="normal")
        self.text_widget.bind(
            "<Key>", lambda e: "break"
        )  # Blocks editing/typing

    def _insert_formatted_line(self, line, base_tag):
        """Splits a single line into tokens to parse inline markdown elements (bold, links, code, math)."""
        pattern = r"(\[.*?\]\(.*?\)|\[.*?\]\[.*?\]|<https?://\S+>|<[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}>|`.*?`|\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*|~~.*?~~|==.*?==|<u>.*?</u>|\$.*?\$|:[a-zA-Z0-9_]+:)"
        tokens = re.split(pattern, line)

        for token in tokens:
            if not token:
                continue

            # Links: [label](target)
            link_match = re.match(r"^\[(.*?)\]\((.*?)\)$", token)
            if link_match:
                label, target = link_match.groups()
                self._insert_link(label, target, base_tag)
                continue

            # Auto Web Links: <https://...>
            auto_link = re.match(r"^<(https?://\S+)>$", token)
            if auto_link:
                url = auto_link.group(1)
                self._insert_link(url, url, base_tag)
                continue

            # Auto Email Links: <user@email.com>
            email_link = re.match(
                r"^<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>$", token
            )
            if email_link:
                email = email_link.group(1)
                self._insert_link(email, f"mailto:{email}", base_tag)
                continue

            # Inline Code (`code`)
            if token.startswith("`") and token.endswith("`"):
                self.text_widget.insert("end", token[1:-1], "inline_code")
            # Bold + Italic (***text***)
            elif token.startswith("***") and token.endswith("***"):
                self.text_widget.insert(
                    "end", token[3:-3], ("bold_italic", base_tag)
                )
            # Bold (**text**)
            elif token.startswith("**") and token.endswith("**"):
                self.text_widget.insert("end", token[2:-2], ("bold", base_tag))
            # Italic (*text*)
            elif token.startswith("*") and token.endswith("*"):
                self.text_widget.insert("end", token[1:-1], ("italic", base_tag))
            # Strikethrough (~~text~~)
            elif token.startswith("~~") and token.endswith("~~"):
                self.text_widget.insert(
                    "end", token[2:-2], ("strikethrough", base_tag)
                )
            # Highlight (==text==)
            elif token.startswith("==") and token.endswith("=="):
                self.text_widget.insert(
                    "end", token[2:-2], ("highlight", base_tag)
                )
            # HTML Underline (<u>text</u>)
            elif token.startswith("<u>") and token.endswith("</u>"):
                self.text_widget.insert(
                    "end", token[3:-4], ("underline", base_tag)
                )
            # Inline Math ($E=mc^2$)
            elif token.startswith("$") and token.endswith("$"):
                self.text_widget.insert(
                    "end", token[1:-1], ("inline_code", base_tag)
                )
            # Emoji Shortcodes
            elif token == ":smile:":
                self.text_widget.insert("end", "😄 ", base_tag)
            elif token == ":rocket:":
                self.text_widget.insert("end", "🚀 ", base_tag)
            # Plain Text Token
            else:
                self.text_widget.insert("end", token, base_tag)

    def _insert_link(self, label, target, base_tag):
        """Creates a clickable hyperlink tag with hover cursor events."""
        link_tag = f"link_{id(target)}_{hash(label)}"
        self.text_widget.tag_configure(
            link_tag, font=("Segoe UI", 11, "underline"), foreground="#0066cc"
        )
        self.text_widget.tag_bind(
            link_tag,
            "<Button-1>",
            lambda e, url=target: self._handle_link_click(url),
        )
        self.text_widget.tag_bind(
            link_tag, "<Enter>", lambda e: self.text_widget.config(cursor="hand2")
        )
        self.text_widget.tag_bind(
            link_tag, "<Leave>", lambda e: self.text_widget.config(cursor="")
        )
        self.text_widget.insert("end", label, (link_tag, base_tag))

    def _handle_link_click(self, target):
        """Handles hyperlink clicks: opens web URLs in browser or opens local files natively."""
        if target.startswith(("http://", "https://", "mailto:")):
            webbrowser.open(target)
            return

        resolved_target = target
        if not os.path.isabs(resolved_target) and self.current_document_path:
            base_dir = os.path.dirname(self.current_document_path)
            resolved_target = os.path.abspath(
                os.path.join(base_dir, resolved_target)
            )

        if os.path.exists(resolved_target):
            os.startfile(resolved_target)
            return

        messagebox.showerror(
            "Link Not Found",
            f"Could not find local target file:\n\n{target}\n\nResolved path:\n{resolved_target}",
        )


# --- Example standalone application execution ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Markdown Document Viewer")
    root.geometry("700x600")

    viewer = CompleteMarkdownViewer(root)
    viewer.pack(fill="both", expand=True)

    # Optional: Load a local file if available, or load sample string content
    sample_text = """# Markdown Viewer
Welcome to the standard library Markdown viewer script!

## Quick Demonstration
- **Bold**, *Italic*, and `inline code` support.
- Open web links: [Python Official Site](https://www.python.org)
- Code blocks are fully select-and-copyable.

```python
import tkinter as tk
print("Hello from python code block!")
"""

viewer.load_markdown(sample_text)
root.mainloop()
