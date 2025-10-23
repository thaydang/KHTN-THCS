# KHTN-AI Editor

Bộ công cụ hỗ trợ soạn thảo học liệu KHTN theo chuẩn CV7991 trong VS Code, kết hợp Markdown, LaTeX và AI.

## Thành phần

- **templates/**: Kho template Pandoc (YAML metadata, citeproc) và XeLaTeX hỗ trợ tiếng Việt.
- **scripts/**: Script build PDF từ Markdown với Pandoc `--pdf-engine=xelatex --citeproc`.
- **vscode_extensions.json**: Danh sách extension gợi ý cho VS Code.
- **resources/**: Bộ tài nguyên dùng chung (template đề, ma trận, bài giảng KHTN 6–9) nằm trong `resources/khtn_ai_editor/`.

## Quy trình đề xuất trong VS Code

1. Cài đặt các extension trong `vscode_extensions.json`.
2. Tạo file Markdown mới dựa trên `templates/metadata.yml` và các snippet trong `resources/`.
3. Soạn nội dung theo cấu trúc CV7991, sử dụng LaTeX cho công thức, trích dẫn theo CSL.
4. Dùng AI (Copilot/Codeium/ChatGPT) hỗ trợ viết nội dung, nhưng kiểm duyệt và chuẩn hóa bằng template.
5. Chạy script `scripts/build_pdf.sh` để xuất PDF với Pandoc + XeLaTeX.
6. Kiểm tra lỗi biên dịch và cập nhật metadata/bibliography theo yêu cầu.

## Yêu cầu hệ thống

- Pandoc >= 3.1
- TeX Live với XeLaTeX và gói `polyglossia`, `fontspec`, `biblatex`.
- Bộ font hỗ trợ tiếng Việt (ví dụ: Times New Roman, Arial, DejaVu Sans).

Xem chi tiết từng thành phần trong các file tương ứng.
