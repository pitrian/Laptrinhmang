✅ Session 4 — IDS Mini Project: Scapy + Isolation Forest (Phát hiện bất thường TCP)
📌 Giới thiệu

Đây là bài lab thuộc Week 2 — Practical AI Tools & Protocol Analysis.

Trong session này, mình thực hiện một mô hình IDS đơn giản ngoài đời thực bằng cách kết hợp:

Scapy để bắt gói tin TCP thật từ mạng Wi-Fi

Trích xuất đặc trưng traffic (IP, port, flags…)

Gom packet thành network flows

Dùng mô hình Isolation Forest (ML không giám sát) để phát hiện bất thường

Xuất file kết quả giống workflow của SOC Analyst

👉 Đây chính là cách SOC hiện đại kết hợp Packet Analysis + AI Detection.

🎯 Mục tiêu bài lab

Sau khi làm xong Session 4, mình đã học và thực hiện được:

✅ Bắt gói tin TCP thật từ máy tính
✅ Phân tích các trường quan trọng trong TCP/IP header
✅ Gom traffic thành các flow kết nối
✅ Huấn luyện mô hình ML phát hiện traffic bất thường
✅ Xuất file anomalies để SOC điều tra
✅ Hiểu sâu hơn về TCP handshake và TCP flags

🛠 Công nghệ sử dụng

Python 3.x

Scapy (bắt và phân tích packet)

Pandas (xử lý dữ liệu)

Scikit-learn (Isolation Forest)

Joblib (lưu model)

Npcap (bắt packet trên Windows)
