# Hướng dẫn sử dụng Gemini CLI để chỉnh sửa kho KHTN-THCS

Tài liệu này giúp bạn thiết lập và vận hành công cụ dòng lệnh dùng mô hình
Gemini để lên kế hoạch hoặc viết lại nội dung trong repo. Đây là cách thuận
tiện khi bạn muốn "chỉnh sửa toàn bộ" nhiều tài liệu với sự hỗ trợ của AI.

## 1. Chuẩn bị môi trường

1. Cài Python 3.10+.
2. Cài đặt thư viện cần thiết:
   ```bash
   pip install google-generativeai
   ```
3. Tạo API key trong [Google AI Studio](https://aistudio.google.com/) và đặt vào
   biến môi trường:
   ```bash
   export GEMINI_API_KEY="your_api_key"
   ```

> 💡 Bạn có thể lưu biến môi trường này trong `~/.bashrc` hoặc `.zshrc` để tự
> động kích hoạt mỗi lần mở terminal.

## 2. Tổng quan công cụ `gemini_cli_editor.py`

Script nằm tại `tools/gemini_cli_editor.py` và cung cấp hai nhóm chức năng:

| Lệnh | Mô tả |
|------|-------|
| `plan` | Sinh kế hoạch chỉnh sửa dựa trên prompt và các tệp ngữ cảnh. |
| `edit` | Gửi nội dung tệp cùng hướng dẫn để Gemini trả về phiên bản đã viết lại. |

Cấu trúc chung:
```bash
python tools/gemini_cli_editor.py <command> [tùy chọn]
```

### 2.1. Lệnh `plan`
Dùng khi bạn muốn Gemini phân tích nhiều tệp và đề xuất lộ trình chỉnh sửa.

```bash
python tools/gemini_cli_editor.py plan "Chuẩn hóa các file README" \
    --files README.md docs/TIMESERIES_GUIDE.md
```

Tùy chọn hữu ích:
- `--files`: danh sách tệp được đọc làm ngữ cảnh (ưu tiên tối đa ~12.000 ký tự).
- `--max-chars`: điều chỉnh giới hạn ký tự để tránh prompt quá dài.
- `--model`: đổi sang mô hình khác, ví dụ `gemini-1.5-pro` nếu cần chất lượng cao.

### 2.2. Lệnh `edit`
Dùng khi bạn muốn Gemini trả về toàn bộ nội dung mới của một tệp.

```bash
python tools/gemini_cli_editor.py edit docs/huong_dan.md \
    --instruction "Rút gọn nội dung, thêm phần mở đầu" --apply
```

- `--instruction`: mô tả rõ ràng thay đổi mong muốn.
- `--apply`: nếu có cờ này, script sẽ ghi đè file bằng nội dung Gemini trả về.
  Nếu không, nội dung chỉ được in ra terminal để bạn xem trước.

Phản hồi phải chứa nội dung trong code fence. Nếu mô hình không trả về đúng
định dạng, script sẽ dừng và hiển thị thông báo để bạn yêu cầu lại.

## 3. Quy trình chỉnh sửa nhiều tệp

1. **Lập kế hoạch**: chạy `plan` với danh sách tệp quan trọng để Gemini đề xuất
   các bước chỉnh sửa.
2. **Thực hiện từng tệp**: dùng `edit` cho từng tệp theo hướng dẫn cụ thể.
3. **Kiểm tra**: chạy lại test/CI hoặc review thủ công.
4. **Commit & PR**: `git add`, `git commit`, rồi tạo pull request như thông lệ.

## 4. Mẹo sử dụng hiệu quả

- Ghi rõ yêu cầu, bao gồm giọng văn, cấu trúc mong muốn hoặc đoạn nội dung bắt
  buộc giữ lại.
- Với các tệp dài, hãy chia thành nhiều phần và chạy `edit` từng lần để kiểm
  soát chất lượng tốt hơn.
- Kết hợp với `git diff` sau mỗi bước để xem chính xác thay đổi trước khi commit.
- Lưu prompt quan trọng vào thư mục `docs/` hoặc `tools/` để tái sử dụng.

## 5. Xử lý lỗi thường gặp

| Vấn đề | Cách khắc phục |
|--------|----------------|
| `Gemini API key không được tìm thấy` | Kiểm tra biến môi trường `GEMINI_API_KEY` hoặc truyền trực tiếp `--api-key`. |
| Không thấy code fence trong phản hồi | Yêu cầu lại mô hình, nhấn mạnh phải trả kết quả trong ```markdown```. |
| Prompt quá dài | Giảm số lượng tệp trong `--files` hoặc hạ `--max-chars`. |

---
Với công cụ này, bạn có thể kết hợp quy trình Git truyền thống cùng sức mạnh
của Gemini để chỉnh sửa hàng loạt tài liệu trong kho KHTN-THCS một cách an
 toàn và có kiểm soát.
