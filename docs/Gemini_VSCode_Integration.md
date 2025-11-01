# Hướng dẫn tích hợp Gemini CLI với Markdown + LaTeX trong VS Code

Tài liệu này trình bày quy trình từng bước để bạn chuẩn bị môi trường, cấu hình Visual Studio Code và vận hành Gemini CLI nhằm tạo tài liệu Markdown có nhúng công thức LaTeX.

## 1. Chuẩn bị môi trường

1. **Cài đặt Python 3.9+ và `pip`**
   - Windows: tải từ [python.org](https://www.python.org/downloads/) hoặc dùng `winget install Python.Python.3.12`. Khi trình cài đặt hỏi, tick **Add Python to PATH** để dùng được trong PowerShell.
   - macOS: dùng `brew install python@3` hoặc tải trực tiếp từ python.org.
   - Linux (Ubuntu/Debian):
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```
2. **Cài Node.js (tùy chọn)**
   - Cần thiết nếu sử dụng các tiện ích Markdown dựa trên Node cho preview LaTeX.
   - Windows: `winget install OpenJS.NodeJS.LTS` hoặc tải bản `.msi` từ [nodejs.org](https://nodejs.org/). Sau khi cài lại mở PowerShell mới để nhận PATH mới.
   - macOS: dùng `brew install node@18`.
   - Linux: dùng `nvm` hoặc trình quản lý gói của distro.
3. **Cài đặt Gemini CLI**
   - Windows mở **PowerShell** (Admin) hoặc Windows Terminal → chạy:
     ```powershell
     python -m pip install --upgrade google-genai
     google-genai init
     ```
   - macOS/Linux dùng `pip install -U google-genai`.
   - Lệnh `google-genai init` sẽ yêu cầu bạn nhập API key Gemini.
   - API key lấy từ trang [Google AI Studio](https://aistudio.google.com/app/apikey).
4. **Tạo cấu trúc thư mục tài liệu**
   - Ví dụ: `docs/` để lưu Markdown thành phẩm, `prompts/` để lưu prompt đầu vào.
   - Windows có thể dùng `New-Item -ItemType Directory docs` trong PowerShell để tạo thư mục nhanh.
   - Đảm bảo repo đã bật Git để theo dõi phiên bản (`git init` nếu làm mới). Nếu chưa cài Git trên Windows, chạy `winget install Git.Git` rồi đăng nhập tài khoản Git.

## 2. Thiết lập Visual Studio Code

1. **Cài đặt các extension chính**
   - `Markdown All in One`: hỗ trợ preview Markdown và phím tắt.
   - `Markdown Preview Enhanced` *hoặc* `LaTeX Workshop`: render LaTeX trong Markdown.
   - `REST Client` (tùy chọn): gửi prompt Gemini trực tiếp từ VS Code.
   - Windows nên cài thêm `Powershell` extension để dùng terminal tích hợp tiện lợi.
2. **Cấu hình workspace**
   - Mở Command Palette → `Preferences: Open Settings (JSON)` và thêm:
     ```json
     {
       "markdown-preview-enhanced.latexEngine": "xelatex",
       "markdown-preview-enhanced.enableScriptExecution": true
     }
     ```
   - Nếu dùng LaTeX Workshop, trên Windows nên cài [MiKTeX](https://miktex.org/download) hoặc TeX Live (`winget install MiKTeX.MiKTeX`). Sau khi cài, mở MiKTeX Console → Settings → tick **Install missing packages on-the-fly** để không bị lỗi thiếu gói khi build.
3. **Tạo snippets cho LaTeX lặp lại**
   - Vào `Preferences: Configure User Snippets` → `markdown.json` → thêm ví dụ:
     ```json
     "Fraction": {
       "prefix": "frac",
       "body": ["$\\dfrac{${1:a}}{{2:b}}$"]
     }
     ```
   - Lưu ý dùng `\\` kép trong JSON để xuất đúng `\` trong LaTeX.
4. **Đặt Tasks VS Code**
   - Trong thư mục gốc dự án (cùng cấp với `docs/`, `samples/`), tạo thư mục ẩn `.vscode` rồi thêm file `tasks.json`. Trên Windows bạn có thể chạy `New-Item -ItemType Directory .vscode -Force` trong PowerShell trước khi tạo file.
   - Nội dung mẫu của `tasks.json` giúp tự động gọi Gemini CLI và build PDF. Trước khi sử dụng, đảm bảo thư mục `outputs/` tồn tại (có thể tạo bằng `New-Item -ItemType Directory outputs -Force`). Với Windows bạn có thể giữ `"type": "shell"`, VS Code sẽ dùng PowerShell mặc định:
     ```json
     {
       "version": "2.0.0",
       "tasks": [
         {
           "label": "Gemini Generate",
           "type": "shell",
           "command": "google-genai prompt --model gemini-1.5-pro --input ${file} --output docs/${fileBasenameNoExtension}.md"
         },
         {
           "label": "Build PDF",
           "type": "shell",
           "command": "pandoc docs/${fileBasenameNoExtension}.md -o outputs/${fileBasenameNoExtension}.pdf --pdf-engine=xelatex",
           "dependsOn": "Gemini Generate"
         }
       ]
     }
     ```

## 3. Quy trình làm việc từng bước

1. **Soạn prompt Markdown**
   - Tạo tệp `prompts/<chu-de>.prompt.md` chứa yêu cầu, dàn ý, định dạng mong muốn.
   - Nhúng công thức dạng inline `$F = ma$` hoặc block `$$E = mc^2$$` ngay trong prompt.
2. **Chạy Gemini CLI**
   - Thực thi trực tiếp (PowerShell):
     ```powershell
     google-genai prompt `
       --model gemini-1.5-pro `
       --input prompts/luc-dia.prompt.md `
       --output docs/luc-dia.md `
       --temperature 0.6 `
       --top-p 0.9
     ```
   - Sử dụng task trong VS Code bằng `Ctrl+Shift+B` và chọn "Gemini Generate".
3. **Kiểm tra kết quả**
   - Mở file Markdown đầu ra, dùng preview VS Code để xem LaTeX render.
   - Với công thức dài, chuyển sang block `$$ ... $$` để dễ đọc.
   - Chỉnh sửa thủ công nội dung chưa chuẩn trước khi commit.
4. **(Tùy chọn) Xuất PDF**
   - Dùng task "Build PDF" hoặc chạy Pandoc thủ công (PowerShell):
     ```powershell
     pandoc docs/luc-dia.md -o outputs/luc-dia.pdf --pdf-engine=xelatex
     ```
5. **Quản lý phiên bản**
   - Dùng `git diff` để so sánh thay đổi.
   - Commit kèm thông điệp rõ ràng:
     ```bash
     git add docs/luc-dia.md
     git commit -m "Thêm tài liệu lực địa có LaTeX"
     git push origin <branch>
     ```

## 4. Tự động hóa kiểm tra chất lượng

1. **Lint Markdown**
   ```bash
   npm install -g markdownlint-cli
   markdownlint "docs/**/*.md"
   ```
2. **Kiểm tra chính tả** (tùy chọn)
   - Cài `codespell`:
     ```bash
     pip install codespell
     codespell docs/
     ```
3. **Kiểm tra build LaTeX**
   - Nếu dùng LaTeX Workshop: mở command palette → `LaTeX Workshop: Build LaTeX project`.
   - Nếu dùng Pandoc: `pandoc docs/<ten-tai-lieu>.md -o outputs/<ten-tai-lieu>.pdf --pdf-engine=xelatex`.
4. **Chạy script nội bộ repo (nếu dùng)**
   - Ví dụ repo có `app/lesson_plan_generator.py`:
     ```bash
     python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json --output outputs/grade6_lesson.md
     ```
   - Đảm bảo các thay đổi tích hợp vẫn tương thích với workflow hiện tại.

## 5. Mẹo tối ưu

- **Tách prompt và nội dung**: giữ `prompts/` và `docs/` riêng để dễ kiểm soát lịch sử.
- **Ghim cấu trúc mẫu**: sử dụng các template ở `tools/lesson_planner/` để duy trì format thống nhất.
- **Review chéo**: dùng Pull Request để đồng nghiệp kiểm tra nội dung do AI sinh.
- **Bảo mật API key**: lưu trong biến môi trường hoặc file `.env`, không commit lên Git. Với Windows, vào **System Properties → Environment Variables** và thêm biến `GOOGLE_API_KEY` để tiện dùng trong scripts.
- **Theo dõi chi phí**: thử nghiệm với model rẻ hơn (vd. `gemini-1.5-flash`) trước khi dùng `pro`.

Hoàn thành các bước trên, bạn sẽ có quy trình VS Code + Gemini CLI mượt mà để tạo, chỉnh sửa và xuất bản tài liệu Markdown chứa LaTeX cho môn Khoa học Tự nhiên.
