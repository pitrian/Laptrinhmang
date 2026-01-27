Khái quát đề bài (Lab 2.1 làm gì?)

Bạn đóng vai security analyst và xây một IDS “tự động” bằng ML có 3 ý chính:

Học “normal traffic” (baseline hành vi bình thường của mạng)

Giám sát traffic mới liên tục (deployment/production)

Cảnh báo khi thấy bất thường (anomaly → nghi tấn công)

Câu hỏi trọng tâm: “Có cần train lại mỗi khi có traffic mới không?”
→ Không. Vì training tốn tài nguyên + cần baseline ổn định. Thường chỉ retrain theo chu kỳ (tuần/tháng) hoặc khi có drift.

Workflow đúng kiểu production:

Training (thỉnh thoảng) → fit()

Save model → joblib.dump()

Deployment (liên tục) → predict() trên traffic mới

2) Từng bước đang làm gì?
Step 1 — Tạo dữ liệu mô phỏng “thực tế”

Mục tiêu: Có dataset giống network log để học/thử nghiệm.

Bạn tạo 1000 “kết nối mạng”, gồm:

Normal (95%): packet_size ~ 70, packets_per_sec ~ 10, duration ~ exp(5)

Attack (5%) gồm 2 kiểu:

DDoS: packets_per_sec cực cao (~200)

Exfiltration: packet_size cực lớn (~5000)

Cuối cùng concat + shuffle thành df.

Ý nghĩa: mô phỏng tình huống thật: tấn công thường hiếm (khoảng vài %), nhưng có pattern khác rõ.

Step 2 — Chia Train/Test

Mục tiêu: Tách dữ liệu để train và kiểm tra trên dữ liệu “chưa từng thấy”.

Chọn features: packet_size, packets_per_sec, duration

Split 70/30

stratify=label để tỉ lệ normal/attack ở train và test giữ giống nhau.

Ý nghĩa: đánh giá công bằng, tránh tình trạng test thiếu attack hoặc lệch tỉ lệ.

Step 3 — Train mô hình (Isolation Forest)

Mục tiêu: Dạy mô hình hiểu “bình thường là gì” và phát hiện lệch chuẩn.

Dùng IsolationForest(contamination=0.05)

contamination=0.05 = giả định khoảng 5% traffic là bất thường (gần giống bạn tạo data)

Train bằng: model.fit(train_df[features])

Quan trọng: Đây là unsupervised, nên KHÔNG dùng label khi train.

Ý nghĩa: IDS anomaly-based thường không có label ngoài đời, nên dùng model kiểu “học normal → thấy khác thì báo”.

Step 4 — Lưu model ra file

Mục tiêu: Chuẩn production: train xong lưu lại để dùng lâu dài.

joblib.dump(model, 'network_ids_model.pkl')

Ý nghĩa: triển khai thật sẽ load model từ disk/service, không train lại mỗi lần chạy.

Step 5 — Load model và dự đoán (mô phỏng deployment)

Mục tiêu: Giả lập hệ thống chạy thật: nhận traffic mới → dự đoán ngay.

loaded_model = joblib.load(...)

predict(test_df[features])

IsolationForest trả:

1 = normal

-1 = anomaly
Bạn map lại thành:

anomaly → 1 (attack)

normal → 0

Ý nghĩa: chuẩn hoá output để so với label (và để code alert dễ hiểu).

Step 6 — Đánh giá (evaluation)

Mục tiêu: Xem IDS “bắt tấn công” tốt không và có gây nhiều báo động giả không.

Confusion Matrix: TN/FP/FN/TP

Report: precision/recall/f1

Diễn giải nhanh trong ngữ cảnh SOC:

FP cao → báo động giả nhiều → alert fatigue (mệt vì toàn báo sai)

FN cao → lọt tấn công → nguy hiểm

Precision: “báo động thì đúng bao nhiêu %”

Recall: “tấn công thật bắt được bao nhiêu %”

3) Tóm lại 1 câu cho từng bước

B1: tạo data giống mạng thật (normal nhiều, attack ít + 2 kiểu attack)

B2: chia train/test để kiểm tra công bằng

B3: train IsolationForest học baseline normal

B4: save model để dùng lâu dài

B5: load + predict như đang chạy production

B6: đo FP/FN/precision/recall để biết IDS có “hữu dụng” không
