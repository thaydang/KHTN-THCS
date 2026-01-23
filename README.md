
# Kho tài liệu Khoa học Tự nhiên THCS

Repo này lưu trữ và chia sẻ tài liệu dạy học môn Khoa học Tự nhiên cấp THCS. Bao gồm giáo án, đề kiểm tra, thí nghiệm ảo và tài liệu tham khảo.

## Mục tiêu
- Quản lý tài liệu dạy học có hệ thống.
- Hỗ trợ giáo viên trong tổ cùng xây dựng kho chung.
- Giúp học sinh truy cập tài nguyên học tập trực tuyến.

## Cấu trúc thư mục
- **GiaoAn/**: Giáo án theo từng lớp (6, 7, 8, 9).
- **DeKiemTra/**: Ma trận, bản đặc tả, đề và đáp án (giữa kỳ, cuối kỳ).
- **ThiNghiemAo/**: Thí nghiệm mô phỏng (Hóa, Lý, Sinh).
- **TaiLieu/**: SGK, công văn và tài liệu tham khảo.
- **tools/lesson_planner/**: Ứng dụng tạo kế hoạch bài dạy KHTN và xuất Markdown.

## Hướng dẫn sử dụng
1. Clone repo về máy:
   ```
   git clone https://github.com/<tai-khoan>/KHTN-THCS.git
   cd KHTN-THCS
   ```
2. Thêm hoặc chỉnh sửa tài liệu vào thư mục phù hợp.
3. Commit thay đổi:
   ```
   git add .
   git commit -m "Cập nhật giáo án Lớp 7 - Nồng độ dung dịch"
   git push
   ```

## Công cụ Dữ liệu Chuỗi Thời gian

Module `app/timeseries_data.py` và công cụ CLI `app/timeseries_tool.py` hỗ trợ lưu trữ và xác thực dữ liệu thí nghiệm theo chuỗi thời gian (ví dụ: đo nhiệt độ, áp suất theo thời gian). Xem hướng dẫn chi tiết trong `docs/TIMESERIES_GUIDE.md`.

### Ví dụ sử dụng:
```bash
# Kiểm tra tính hợp lệ của dữ liệu
python app/timeseries_tool.py validate samples/heating_water_experiment.json

# Xem thông tin chi tiết
python app/timeseries_tool.py info samples/heating_water_experiment.json

# Tạo dữ liệu mẫu
python app/timeseries_tool.py create-sample outputs/my_experiment.json \
  --topic "Thí nghiệm của tôi" --device "Nhiệt kế" --num-points 10
```

## KHTN-AI Editor

Bộ công cụ trong `tools/khtn_ai_editor/` cung cấp template Pandoc, XeLaTeX, script build PDF và kho tài nguyên dùng chung lớp 6-9 theo CV7991. Xem chi tiết trong `tools/khtn_ai_editor/README.md`.

### Mẫu đề thi Quarto (tham số hóa seed)
- File mẫu: `resources/khtn_ai_editor/de_ma_tran/exam_template.qmd`
- Render và tạo biến thể mã đề bằng cách thay `seed`/`exam_code`:
  ```bash
  quarto render resources/khtn_ai_editor/de_ma_tran/exam_template.qmd \
    -P seed=202501 -P version=B -P exam_code=GK-KHTN8-2025
  ```
## Ứng dụng tạo kế hoạch bài dạy KHTN

Script `app/lesson_plan_generator.py` hỗ trợ soạn giáo án/bài giảng điện tử từ file JSON
và xuất ra file Markdown hoặc Word (.docx).

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Tính năng mới

- ✨ **Render công thức LaTeX thành ảnh**: Sử dụng Matplotlib để chuyển công thức LaTeX thành ảnh PNG chất lượng cao (300 DPI)
- 📄 **Xuất file Word (.docx)**: Tạo file Word với công thức đã được render, phù hợp để chia sẻ và in ấn
- 🔄 **Xuất nhiều định dạng**: Tạo cả Markdown và Word cùng lúc với tùy chọn `--format both`

### Cách sử dụng

#### Xuất file Markdown (mặc định)
```bash
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json -o outputs/lesson.md
```

#### Xuất file Word với công thức được render
```bash
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json \
  --format word -o outputs/lesson.docx
```

#### Xuất cả Markdown và Word
```bash
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json \
  --format both -o outputs/lesson.md
```

Xem hướng dẫn chi tiết trong `docs/LATEX_WORD_EXPORT.md`.

### Định dạng file JSON

Script sẽ tạo file chứa đầy đủ cấu trúc mục tiêu, học liệu, hoạt động dạy học,
đánh giá... Các công thức viết dạng LaTeX (ví dụ `$F = ma$`) sẽ giữ nguyên trong
file Markdown để sử dụng với các hệ thống hỗ trợ MathJax.

## Đóng góp
- Giáo viên: fork repo, chỉnh sửa và gửi pull request.
- Học sinh: tải tài liệu hoặc gửi đề xuất qua Issues.

## Bản quyền
- Tài liệu tuân thủ Chương trình GDPT 2018 và công văn Bộ GD&ĐT.
- Dùng cho mục đích dạy học, không thương mại hóa.

## Công cụ soạn kế hoạch bài dạy (Markdown)
Ứng dụng dòng lệnh trong thư mục `app/` cho phép tạo giáo án/bài giảng điện tử môn Khoa học Tự nhiên từ tệp JSON và xuất ra Markdown có hỗ trợ công thức LaTeX.

### Cách sử dụng
1. Tạo tệp cấu hình JSON theo mẫu trong `samples/grade6_light_and_shadow.json`.
2. Chạy lệnh:
   ```bash
   python app/lesson_plan_generator.py path/to/config.json -o path/to/output.md
   ```
3. Mở tệp `.md` bằng trình soạn thảo hoặc nền tảng hỗ trợ Markdown/LaTeX để trình chiếu.


> 📌 **Lưu ý:** Khi viết công thức LaTeX trong tệp JSON, hãy dùng hai dấu `\` để biểu diễn một dấu `\` thực tế (ví dụ: `\\dfrac{a}{b}` sẽ hiển thị thành `\dfrac{a}{b}`).

### Cấu trúc tệp JSON
- `metadata`: thông tin bài dạy (tiêu đề, ngày dạy, chủ đề, giáo viên,...).
- `objectives`, `competencies`, `materials`: danh sách mục tiêu, năng lực và học liệu.
- `digital_resources`: học liệu số, bài giảng điện tử.
- `formulas`: danh sách công thức/ký hiệu với trường `latex` giữ nguyên biểu thức.
- `activities`: mỗi hoạt động gồm thời lượng, mục tiêu, các bước (GV/HS) và học liệu số kèm theo.
- `assessment`, `homework`, `reflection`: đánh giá, dặn dò và tự nhận xét sau bài học.

Chạy thử với mẫu:
```bash
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json
```

## Gemini CLI hỗ trợ chỉnh sửa tài liệu

Muốn sử dụng AI Gemini để lập kế hoạch hoặc viết lại nội dung trong kho tài liệu?
Tham khảo hướng dẫn chi tiết và script CLI tại `docs/GEMINI_CLI_GUIDE.md`. Công cụ
`tools/gemini_cli_editor.py` cho phép bạn lấy kế hoạch chỉnh sửa (`plan`) hoặc nhờ
Gemini viết lại toàn bộ một tệp (`edit`) và áp dụng trực tiếp.
