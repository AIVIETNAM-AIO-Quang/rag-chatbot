# RAG Chatbot

Đây là ứng dụng chatbot đơn giản sử dụng phương pháp Retrieval-Augmented Generation. Ứng dụng cho phép người dùng upload file PDF, xử lý nội dung tài liệu và đặt câu hỏi dựa trên nội dung trong file đã upload.

## Chức năng chính

- Upload và xử lý file PDF.
- Trích xuất văn bản từ tài liệu PDF.
- Chia văn bản dài thành các đoạn nhỏ.
- Chuyển các đoạn văn bản thành embedding.
- Lưu embedding vào ChromaDB.
- Truy xuất các đoạn tài liệu liên quan đến câu hỏi của người dùng.
- Sinh câu trả lời dựa trên context được truy xuất.
- Cung cấp giao diện chatbot đơn giản bằng Streamlit.

## Ngôn ngữ và các thư viện được dùng

- Python
- Streamlit
- ChromaDB
- PyPDF
- Google Gemini API
- Gemini Embedding Model

## Cấu trúc project

```text
rag-chatbot/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Cách hoạt động

Ứng dụng hoạt động theo pipeline RAG cơ bản:

```text
PDF Upload
→ Text Extraction
→ Text Chunking
→ Embedding
→ Vector Storage
→ Retrieval
→ Answer Generation
```

Đầu tiên, file PDF được chuyển thành văn bản thô. Sau đó, văn bản được chia thành nhiều đoạn nhỏ. Mỗi đoạn được chuyển thành vector embedding và lưu vào ChromaDB. Khi người dùng đặt câu hỏi, ứng dụng sẽ truy xuất các đoạn văn bản liên quan nhất, đưa chúng vào prompt dưới dạng context, rồi dùng mô hình ngôn ngữ để sinh câu trả lời.

## Cách chạy trên máy cá nhân

Clone repository:

```bash
git clone https://github.com/AIVIETNAM-AIO-Quang/rag-chatbot.git
cd rag-chatbot
```

Cài đặt thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Tạo file secrets cho Streamlit:

```text
.streamlit/secrets.toml
```

Thêm Gemini API key vào file secrets:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Chạy ứng dụng Streamlit:

```bash
streamlit run app.py
```

## Deploy

Ứng dụng có thể được deploy bằng Streamlit Community Cloud.

Thiết lập deploy:

```text
Repository: AIVIETNAM-AIO-Quang/rag-chatbot
Branch: main
Main file path: app.py
```

Trong phần Secrets của Streamlit Cloud, thêm:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Không đưa API key lên GitHub.

## Hạn chế

- Nếu app restart, người dùng cần upload và xử lý lại file PDF.
- File PDF quá dài có thể tiêu tốn nhiều API quota hơn.
- Chất lượng câu trả lời phụ thuộc vào chất lượng trích xuất văn bản, cách chia chunk và khả năng truy xuất context liên quan.

## Ghi chú

Project này được xây dựng nhằm thực hành quy trình cơ bản của một hệ thống RAG. Ứng dụng minh họa cách kết hợp truy xuất tài liệu và mô hình ngôn ngữ để tạo ra chatbot có khả năng trả lời dựa trên nội dung tài liệu.
