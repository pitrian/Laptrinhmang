Lab 2.1 — Xây IDS “tự động” bằng Machine Learning (Anomaly Detection)
1) Khái quát đề bài (Lab 2.1 làm gì?)

Bạn đóng vai Security Analyst và xây một hệ thống IDS dựa trên ML theo đúng tư duy production, gồm 3 ý chính:

Học “normal traffic” → tạo baseline hành vi bình thường của mạng

Giám sát traffic mới liên tục → mô phỏng deployment/production

Cảnh báo khi thấy bất thường → anomaly ⇒ nghi có tấn công

Câu hỏi trọng tâm: “Có cần train lại mỗi khi có traffic mới không?”
➡️ Không. Training tốn tài nguyên và baseline cần ổn định. Thực tế chỉ retrain theo chu kỳ (tuần/tháng) hoặc khi phát hiện data drift.

Workflow đúng kiểu production:

Training (thỉnh thoảng) → fit()

Save model → joblib.dump()

Deployment (liên tục) → predict() trên traffic mới

2) Giải thích từng bước (Pipeline đang làm gì?)
Step 1 — Tạo dữ liệu mô phỏng “thực tế”

Mục tiêu: Có dataset giống log mạng để train/test mô hình.

Tạo 1000 kết nối mạng, gồm:

Normal (95%)

packet_size ~ 70

packets_per_sec ~ 10

duration ~ exp(5)

Attack (5%) gồm 2 kiểu:

DDoS: packets_per_sec cực cao (~200)

Exfiltration: packet_size cực lớn (~5000)

Sau đó concat + shuffle thành DataFrame df.

Ý nghĩa: mô phỏng đúng tình huống thật: tấn công thường hiếm (vài %), nhưng có pattern khác biệt rõ.

Step 2 — Chia Train/Test

Mục tiêu: tách dữ liệu để train và kiểm tra trên dữ liệu “chưa từng thấy”.

Features dùng để học: packet_size, packets_per_sec, duration

Split 70/30

stratify=label để tỉ lệ normal/attack trong train và test giữ ổn định

Ý nghĩa: đánh giá công bằng, tránh test bị lệch tỉ lệ (thiếu attack hoặc quá ít attack).

Step 3 — Train mô hình (Isolation Forest)

Mục tiêu: dạy mô hình hiểu “bình thường” và phát hiện lệch chuẩn.

Dùng: IsolationForest(contamination=0.05)

contamination=0.05 = giả định khoảng 5% traffic là bất thường (phù hợp dataset)

Train bằng: model.fit(train_df[features])

✅ Quan trọng: Đây là unsupervised, nên KHÔNG dùng label khi train.

Ý nghĩa: IDS anomaly-based ngoài đời thường không có label rõ ràng, nên cách làm là “học normal → gặp khác thì báo”.

Step 4 — Lưu model ra file

Mục tiêu: chuẩn production: train xong lưu lại để dùng lâu dài.

joblib.dump(model, "network_ids_model.pkl")

Ý nghĩa: triển khai thật sẽ load model từ file/service, không train lại mỗi lần chạy.

Step 5 — Load model và dự đoán (mô phỏng deployment)

Mục tiêu: giả lập hệ thống chạy thật: nhận traffic mới → dự đoán ngay.

loaded_model = joblib.load(...)

pred = loaded_model.predict(test_df[features])

Isolation Forest trả:

1 = normal

-1 = anomaly

Map lại để dễ dùng:

anomaly → 1 (attack)

normal → 0

Ý nghĩa: chuẩn hoá output để dễ làm alert + so sánh với label khi evaluation.

Step 6 — Đánh giá mô hình (Evaluation)

Mục tiêu: kiểm tra IDS “bắt tấn công” tốt không và có gây báo động giả nhiều không.

Confusion Matrix: TN / FP / FN / TP

Classification Report: precision / recall / f1

Diễn giải theo SOC:

FP cao → báo động giả nhiều → alert fatigue

FN cao → lọt tấn công → nguy hiểm

Chỉ số quan trọng:

Precision: “Alert phát ra thì đúng bao nhiêu %”

Recall: “Tấn công thật bắt được bao nhiêu %”

3) Tóm tắt 1 câu cho từng bước

B1: Tạo dataset giống traffic thật (normal nhiều, attack ít + 2 kiểu attack)

B2: Chia train/test để đánh giá công bằng

B3: Train Isolation Forest để học baseline normal và phát hiện anomaly

B4: Save model để tái sử dụng lâu dài

B5: Load + predict như đang chạy production

B6: Đo FP/FN/precision/recall để biết IDS có hữu dụng không
