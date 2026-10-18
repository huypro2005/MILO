# CHƯƠNG 4. KẾT QUẢ NGHIÊN CỨU VÀ THẢO LUẬN

Chương này trình bày kết quả thực nghiệm theo trình tự: mô tả dữ liệu và kiểm tra sơ bộ (Mục 4.1–4.3), kiểm tra tính dừng và đồng liên kết (Mục 4.4), lựa chọn phương pháp ước lượng và xử lý khuyết tật (Mục 4.5–4.6), ước lượng ba mô hình nghiên cứu (Mục 4.7), kiểm định độ vững (Mục 4.8) và thảo luận các giả thuyết H1, H2, H3 (Mục 4.9).

## 4.1. Thống kê mô tả

Bảng 4.1. Thống kê mô tả các biến nghiên cứu

| Biến | N | Trung bình | ĐLC tổng thể | ĐLC between | ĐLC within | Nhỏ nhất | Lớn nhất |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| lnCO2 | 1,533 | −0.0954 | 1.3788 | 1.3627 | 0.2615 | −3.8122 | 2.8569 |
| FDI | 1,533 | 3.7009 | 4.9295 | 2.9802 | 3.9413 | −37.1727 | 55.0729 |
| lnY | 1,533 | 7.7280 | 0.9077 | 0.8932 | 0.1910 | 5.7731 | 9.5662 |
| URB | 1,533 | 49.4763 | 17.2712 | 16.9893 | 3.6643 | 12.2028 | 92.1128 |
| TO | 1,533 | 71.3158 | 32.4156 | 30.1673 | 12.3526 | 2.6988 | 210.3743 |
| Crdt | 1,533 | 33.8573 | 27.3959 | 25.4067 | 10.6519 | 0.4492 | 181.7852 |
| CC | 1,533 | −0.5495 | 0.5606 | 0.5293 | 0.1941 | −1.6643 | 1.4640 |
| GE | 1,533 | −0.4684 | 0.5893 | 0.5439 | 0.2352 | −2.1560 | 1.1141 |
| PV | 1,533 | −0.5011 | 0.7400 | 0.6628 | 0.3378 | −2.7115 | 1.3224 |
| RQ | 1,533 | −0.3839 | 0.5323 | 0.4993 | 0.1933 | −2.1119 | 1.1373 |
| RL | 1,533 | −0.5546 | 0.5204 | 0.4910 | 0.1814 | −2.0462 | 1.0288 |
| VA | 1,533 | −0.3765 | 0.5946 | 0.5562 | 0.2197 | −1.8589 | 0.9689 |

Ghi chú: Mẫu gồm 73 quốc gia đang phát triển, giai đoạn 2002–2022, dữ liệu bảng cân bằng (T = 21). N là số quan sát; ĐLC là độ lệch chuẩn; ĐLC between (giữa các quốc gia) và ĐLC within (trong nội bộ quốc gia) lấy từ lệnh xtsum; giá trị nhỏ nhất và lớn nhất là của chuỗi gốc. Các chỉ số WGI có thang đo xấp xỉ từ −2.5 đến +2.5.

Nguồn: Tác giả tổng hợp từ kết quả lệnh summarize và xtsum trên phần mềm Stata.

Mẫu nghiên cứu gồm 1,533 quan sát của 73 quốc gia trong 21 năm, không có giá trị khuyết. Giá trị trung bình của lnCO2 (−0.0954) tương ứng mức phát thải khoảng 0.91 tấn CO₂/người (trung bình nhân), với khoảng dao động từ khoảng 0.02 đến 17.41 tấn CO₂/người. Thu nhập bình quân đầu người trung bình khoảng 2,271 USD (giá cố định 2015), phù hợp với đặc điểm mẫu gồm các nước thu nhập thấp và trung bình. Dòng vốn FDI ròng bình quân 3.70% GDP; giá trị âm nhỏ nhất (−37.17% GDP) phản ánh những năm dòng vốn rút ra, như thoái vốn hoặc hoàn trả khoản vay nội bộ công ty, vượt quá vốn đầu tư mới, phù hợp với cách đo FDI ròng của WDI (OECD, 2008). Cả sáu chỉ số WGI có trung bình âm (từ −0.5546 đối với RL đến −0.3765 đối với VA). Do WGI được chuẩn hóa với trung bình toàn cầu xấp xỉ bằng 0 (Kaufmann và cộng sự, 2011), chất lượng thể chế của mẫu nhìn chung thấp hơn mặt bằng thế giới, dù giá trị lớn nhất của cả sáu chỉ số đều dương.

Điểm quan trọng hơn đối với phương pháp ước lượng là cấu trúc biến thiên của dữ liệu. Với tất cả các biến trừ FDI, độ lệch chuẩn giữa các quốc gia lớn gấp khoảng hai đến năm lần độ lệch chuẩn trong nội bộ quốc gia: phần lớn khác biệt về phát thải, thu nhập và thể chế là khác biệt bền vững giữa các nước. FDI là ngoại lệ, khi biến thiên trong nội bộ quốc gia (3.94) lớn hơn biến thiên giữa các quốc gia (2.98), tức dòng vốn FDI dao động mạnh qua các năm trong cùng một nước. Đặc điểm này có hai hàm ý. Thứ nhất, nếu áp dụng mô hình hiệu ứng cố định (Mục 4.5), hệ số FDI được nhận diện từ nguồn biến thiên dồi dào, trong khi hệ số của các chỉ số thể chế chỉ dựa trên phần biến thiên trong nội bộ quốc gia tương đối nhỏ (độ lệch chuẩn từ 0.18 đến 0.34), nên dự kiến được ước lượng kém chính xác hơn. Thứ hai, độ lớn kinh tế của các hệ số trong mô hình hiệu ứng cố định cần được đánh giá theo độ lệch chuẩn trong nội bộ quốc gia thay vì độ lệch chuẩn tổng thể, vì đây mới là mức biến động thực tế mà mô hình khai thác.

## 4.2. Ma trận hệ số tương quan

Bảng 4.2. Ma trận hệ số tương quan Pearson

| | lnCO2 | FDI | lnY | URB | TO | Crdt | CC | GE | PV | RQ | RL | VA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| lnCO2 | 1.0000 | | | | | | | | | | | |
| FDI | 0.0744\* | 1.0000 | | | | | | | | | | |
| lnY | 0.8804\* | −0.0156 | 1.0000 | | | | | | | | | |
| URB | 0.6568\* | −0.0067 | 0.7583\* | 1.0000 | | | | | | | | |
| TO | 0.3768\* | 0.3479\* | 0.2542\* | 0.0846\* | 1.0000 | | | | | | | |
| Crdt | 0.5602\* | −0.0034 | 0.5254\* | 0.2829\* | 0.4140\* | 1.0000 | | | | | | |
| CC | 0.3196\* | −0.0154 | 0.4014\* | 0.1971\* | 0.1991\* | 0.4000\* | 1.0000 | | | | | |
| GE | 0.5866\* | −0.0073 | 0.6243\* | 0.3512\* | 0.2806\* | 0.5878\* | 0.7763\* | 1.0000 | | | | |
| PV | 0.3415\* | 0.1133\* | 0.3731\* | 0.1928\* | 0.3938\* | 0.2972\* | 0.6146\* | 0.5342\* | 1.0000 | | | |
| RQ | 0.5451\* | 0.0374 | 0.5827\* | 0.3477\* | 0.3036\* | 0.5061\* | 0.6841\* | 0.8298\* | 0.4794\* | 1.0000 | | |
| RL | 0.4300\* | 0.0220 | 0.4421\* | 0.1878\* | 0.2735\* | 0.4269\* | 0.8571\* | 0.8112\* | 0.6680\* | 0.7899\* | 1.0000 | |
| VA | 0.2898\* | 0.0016 | 0.3713\* | 0.3289\* | 0.0794\* | 0.1283\* | 0.6076\* | 0.5288\* | 0.5471\* | 0.5850\* | 0.7215\* | 1.0000 |

Ghi chú: Dấu (\*) thể hiện hệ số tương quan có ý nghĩa thống kê ở mức 5%.

Nguồn: Tác giả tổng hợp từ kết quả lệnh pwcorr trên phần mềm Stata.

lnCO2 tương quan dương và có ý nghĩa ở mức 5% với tất cả các biến giải thích. Tương quan giữa FDI và lnCO2 dương nhưng rất yếu (0.0744). Mạnh nhất là tương quan của lnCO2 với lnY (0.8804) và URB (0.6568), phù hợp với hiệu ứng quy mô của tăng trưởng (Grossman và Krueger, 1995) và lập luận đô thị hóa làm tăng nhu cầu năng lượng (Poumanyvong và Kaneko, 2010).

Đáng chú ý, cả sáu chỉ số thể chế đều tương quan dương với lnCO2 (từ 0.2898 đến 0.5866), đồng thời tương quan dương với lnY (từ 0.3713 đến 0.6243). Nói cách khác, các nước có thể chế tốt hơn trong mẫu thường cũng có thu nhập cao hơn, nên tương quan dương giữa thể chế và phát thải có thể chủ yếu phản ánh khác biệt về trình độ phát triển. Vì hệ số tương quan chưa kiểm soát các yếu tố khác, chiều tác động của thể chế chỉ có thể được đánh giá trong mô hình hồi quy.

Về đa cộng tuyến, các cặp biến cùng xuất hiện trong một phương trình đều có hệ số tương quan dưới ngưỡng cảnh báo 0.8 (Gujarati và Porter, 2009), cao nhất là lnY–URB (0.7583). Ngược lại, ba cặp chỉ số WGI là CC–RL (0.8571), GE–RQ (0.8298) và GE–RL (0.8112) vượt ngưỡng này. Mức độ đa cộng tuyến được đánh giá chính thức bằng hệ số VIF tại Mục 4.3.

## 4.3. Kiểm định đa cộng tuyến

Bảng 4.3. Hệ số phóng đại phương sai (VIF)

| Biến | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| *Phần A. Mỗi phương trình đưa một chỉ số WGI* | | | | | | |
| FDI | 1.18 | 1.18 | 1.18 | 1.18 | 1.18 | 1.18 |
| lnY | 3.41 | 3.90 | 3.39 | 3.70 | 3.57 | 3.32 |
| URB | 2.54 | 2.57 | 2.52 | 2.53 | 2.60 | 2.51 |
| TO | 1.44 | 1.44 | 1.56 | 1.45 | 1.45 | 1.44 |
| Crdt | 1.69 | 1.84 | 1.63 | 1.72 | 1.68 | 1.64 |
| Chỉ số WGI ở đầu cột | 1.29 | 2.00 | 1.32 | 1.70 | 1.40 | 1.17 |
| VIF trung bình | 1.93 | 2.16 | 1.93 | 2.05 | 1.98 | 1.88 |
| *Phần B. Đưa đồng thời sáu chỉ số WGI (chỉ để đối chiếu)* | | | | | | |
| VIF | RL 8.22 | GE 5.77 | CC 4.33 | RQ 4.16 | VA 2.83 | PV 2.22 |
| | lnY 4.05 | URB 2.89 | Crdt 2.00 | TO 1.64 | FDI 1.18 | Trung bình 3.57 |

Ghi chú: VIF tính từ hồi quy OLS gộp của lnCO2 theo các biến trong bảng (lệnh estat vif). Ở Phần B, mỗi ô ghi tên biến và VIF tương ứng.

Nguồn: Tác giả tổng hợp từ kết quả lệnh estat vif trên phần mềm Stata.

Đa cộng tuyến không làm ước lượng bị chệch nhưng làm tăng sai số chuẩn, khiến khó tách bạch tác động riêng của từng biến (Gujarati và Porter, 2009). Khi đưa đồng thời sáu chỉ số WGI (Phần B), VIF của RL (8.22) và GE (5.77) vượt ngưỡng thận trọng 5 (Sheather, 2009); với RL, phương sai của hệ số lớn gấp 8.22 lần so với trường hợp RL không tương quan với các biến còn lại. Khi mỗi phương trình chỉ chứa một chỉ số (Phần A), VIF của chỉ số thể chế chỉ còn từ 1.17 đến 2.00, VIF lớn nhất thuộc về lnY (3.32–3.90) và VIF trung bình từ 1.88 đến 2.16; VIF của FDI ổn định ở mức 1.18. Kết quả này cho thấy đa cộng tuyến không đáng lo ngại trong cấu trúc mô hình của nghiên cứu, và là cơ sở để Mô hình 2 và Mô hình 3 ước lượng riêng từng khía cạnh thể chế. Cần lưu ý rằng VIF được tính trên dữ liệu gộp; trong mô hình hiệu ứng cố định, độ chính xác của hệ số thể chế còn bị giới hạn bởi biến thiên trong nội bộ quốc gia nhỏ (Mục 4.1), một vấn đề VIF không phản ánh được.

## 4.4. Kiểm định tính dừng và đồng liên kết

Bảng 4.4. Kết quả kiểm định nghiệm đơn vị IPS và CIPS (p-value)

| Biến | IPS – Mức | IPS – Mức + xu thế | IPS – Sai phân | CIPS – Mức | CIPS – Mức + xu thế | CIPS – Sai phân |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| lnCO2 | 0.9991 | 0.0004 | 0.0000 | 0.0000 | 0.1378 | 0.0000 |
| FDI | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0124 | 0.0000 |
| lnY | 0.9992 | 0.9133 | 0.0000 | 0.9524 | 0.9957 | 0.0000 |
| URB | 0.0001 | 1.0000 | 0.0826 | 0.0000 | 0.6124 | 0.9056 |
| TO | 0.1242 | 0.0087 | 0.0000 | 0.9988 | 0.9449 | 0.0000 |
| Crdt | 0.5956 | 0.1101 | 0.0000 | 0.2369 | 0.9998 | 0.0000 |
| CC | 0.0010 | 0.0000 | 0.0000 | 0.9167 | 0.0008 | 0.0000 |
| GE | 0.0001 | 0.0000 | 0.0000 | 0.0000 | 0.0001 | 0.0000 |
| PV | 0.0000 | 0.0000 | 0.0000 | 0.8451 | 0.7746 | 0.0000 |
| RQ | 0.0000 | 0.0000 | 0.0000 | 0.9118 | 0.0327 | 0.0000 |
| RL | 0.0000 | 0.0000 | 0.0000 | 0.1017 | 0.0036 | 0.0000 |
| VA | 0.2261 | 0.0004 | 0.0000 | 0.9751 | 0.4174 | 0.0000 |

Ghi chú: H₀ của cả hai kiểm định là chuỗi có nghiệm đơn vị. IPS (Im và cộng sự, 2003) dùng thống kê W-t-bar, dữ liệu được trừ trung bình chéo theo từng năm (demean), độ trễ chọn theo AIC tối đa 2. CIPS (Pesaran, 2007) dùng 1 độ trễ. “Mức” là dạng mức có hệ số chặn; “Sai phân” là sai phân bậc một (CIPS dùng các năm từ 2003).

Nguồn: Tác giả tổng hợp từ kết quả lệnh xtunitroot ips và pescadf trên phần mềm Stata.

Kết quả cho thấy các biến có bậc tích hợp khác nhau. lnY không dừng ở dạng mức theo cả hai kiểm định, kể cả khi có xu thế, nhưng dừng ở sai phân bậc một, nên có thể xem là I(1): thu nhập bình quân đầu người tăng theo một quỹ đạo bền bỉ. Ngược lại, FDI dừng ở mọi dạng kiểm định, tức I(0): dòng vốn dao động quanh một mức trung bình và các biến động của nó mang tính tạm thời, nhất quán với biến thiên trong nội bộ quốc gia lớn đã ghi nhận ở Mục 4.1. Kết luận về lnCO2 không dứt khoát: IPS không bác bỏ nghiệm đơn vị ở dạng mức (p-value 0.9991) trong khi CIPS bác bỏ (0.0000), và kết quả đảo ngược khi có xu thế. Với các chỉ số thể chế, IPS cho thấy cả sáu chỉ số dừng ở dạng mức, nhưng CIPS, vốn kiểm soát phụ thuộc chéo, không bác bỏ nghiệm đơn vị ở dạng mức của CC, PV, RQ và VA (p-value từ 0.8451 đến 0.9751). Sự khác biệt này gợi ý biến động thể chế giữa các nước có một thành phần chung theo thời gian, ủng hộ việc đưa hiệu ứng cố định năm vào mô hình (Mục 4.5).

URB là trường hợp đặc biệt: biến này không dừng ở sai phân bậc một theo CIPS (p-value 0.9056) và chỉ dừng ở mức 10% theo IPS (0.0826). Kết quả này có thể phản ánh đặc điểm tăng chậm và gần như đều đặn của tỷ lệ đô thị hóa, vốn làm giảm độ mạnh của các kiểm định nghiệm đơn vị. Do một biến có xu hướng mạnh dễ tạo ra tương quan giả, hệ số của URB cần được diễn giải thận trọng và các kết quả chính được kiểm tra lại khi loại URB (Mục 4.8.4).

Bảng 4.5. Kết quả kiểm định đồng liên kết Westerlund

| Nội dung | Kết quả |
|:--|:--|
| Giả thuyết | H₀: không có đồng liên kết; Hₐ: một số quốc gia có đồng liên kết |
| Biến | lnCO2, FDI, lnY, URB, TO, Crdt (Mô hình 1) |
| Số quốc gia / số năm | 73 / 21 |
| Đặc tả | Vector đồng liên kết và tham số AR riêng từng quốc gia; có trung bình theo quốc gia; không có xu thế; loại bỏ trung bình chéo (demean) |
| Thống kê Variance ratio | −2.3225 |
| p-value | 0.0101 |

Nguồn: Tác giả tổng hợp từ kết quả lệnh xtcointtest westerlund trên phần mềm Stata.

Kiểm định Westerlund (2005) bác bỏ giả thuyết không có đồng liên kết ở mức 5% (p-value 0.0101), tức tồn tại quan hệ cân bằng dài hạn giữa các biến của Mô hình 1 ở ít nhất một bộ phận quốc gia trong mẫu. Kết quả này giảm bớt lo ngại rằng quan hệ giữa phát thải và thu nhập ở dạng mức chỉ là hệ quả của việc hai chuỗi cùng tăng theo thời gian (Granger và Newbold, 1974), và là cơ sở để ước lượng các mô hình ở dạng mức.

Tuy vậy, mức độ của bằng chứng này có giới hạn. Thứ nhất, giả thuyết đối chỉ là “một số quốc gia có đồng liên kết”. Thứ hai, kiểm định đồng liên kết giả định các biến là I(1), trong khi FDI là I(0) và URB có dấu hiệu bậc tích hợp cao hơn, nên kết quả nên được xem là bằng chứng hỗ trợ chứ không phải xác nhận chặt chẽ. Thứ ba, các chỉ số thể chế và biến tương tác của Mô hình 2 và 3 không nằm trong vector kiểm định. Ngoài ra, với dữ liệu bảng, ngay cả khi quan hệ đồng liên kết không tồn tại ở mọi quốc gia, ước lượng gộp vẫn có thể được hiểu là một quan hệ trung bình dài hạn giữa các biến (Phillips và Moon, 1999). Vì vậy, nghiên cứu ước lượng ở dạng mức, đồng thời xử lý tự tương quan của sai số bằng sai số chuẩn vững (Mục 4.6) và kiểm tra lại kết quả khi loại URB (Mục 4.8.4).

## 4.5. Lựa chọn mô hình ước lượng

Bảng 4.6. Kết quả ước lượng Pooled OLS, FEM và REM (Mô hình 1)

| Biến | Pooled OLS | FEM | REM |
|:--|:-:|:-:|:-:|
| FDI | 0.0124\*\*\* | 0.0068\*\*\* | 0.0068\*\*\* |
| lnY | 1.1831\*\*\* | 0.7143\*\*\* | 0.7634\*\*\* |
| URB | 0.0024\* | 0.0097\*\*\* | 0.0095\*\*\* |
| TO | 0.0052\*\*\* | 0.0010\*\*\* | 0.0013\*\*\* |
| Crdt | 0.0046\*\*\* | 0.0041\*\*\* | 0.0038\*\*\* |
| Hằng số | −9.9321\*\*\* | −6.3276\*\*\* | −6.7073\*\*\* |
| Số quan sát | 1,533 | 1,533 | 1,533 |
| R² | 0.8065 | | |
| R² within | | 0.5603 | 0.5599 |

Ghi chú: Biến phụ thuộc là lnCO2. \*, \*\*, \*\*\* tương ứng mức ý nghĩa 10%, 5% và 1%, dựa trên sai số chuẩn thông thường chưa điều chỉnh khuyết tật; bảng chỉ dùng để so sánh phương pháp. Ba mô hình chưa có biến giả năm.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Bảng 4.7. Kết quả các kiểm định lựa chọn mô hình

| Kiểm định | Thống kê | Giá trị | p-value | Kết luận |
|:--|:-:|:-:|:-:|:--|
| *Phần A. Mô hình 1* | | | | |
| F test (Pooled OLS và FEM) | F | 227.06 | 0.0000 | Bác bỏ H₀ – chọn FEM |
| Breusch–Pagan LM (Pooled OLS và REM) | chibar2(01) | 12076.40 | 0.0000 | Bác bỏ H₀ – chọn REM |
| Hausman (FEM và REM) | chi2(5) | 33.78 | 0.0000 | Bác bỏ H₀ – chọn FEM |
| Hiệu ứng năm (testparm i.Year) | F(20, 72) | 3.04 | 0.0003 | Bác bỏ H₀ – cần hiệu ứng năm |
| *Phần B. Hausman cho Mô hình 2 / Mô hình 3* | chi2 (M2) | p-value (M2) | chi2 (M3) | p-value (M3) |
| CC | 34.00 | 0.0000 | 36.95 | 0.0000 |
| GE | 30.56 | 0.0000 | 37.99 | 0.0000 |
| PV | 35.09 | 0.0000 | 35.59 | 0.0000 |
| RQ | 34.42 | 0.0000 | 34.20 | 0.0000 |
| RL | 34.15 | 0.0000 | 34.96 | 0.0000 |
| VA | 34.65 | 0.0000 | 33.65 | 0.0000 |

Ghi chú: H₀ của F test: u_i = 0; của Breusch–Pagan LM: Var(u) = 0; của Hausman: khác biệt giữa hệ số FEM và REM không có tính hệ thống (tùy chọn sigmamore); của testparm: hệ số các biến giả năm đồng thời bằng 0 (FEM có biến giả năm, sai số chuẩn cụm theo quốc gia). Thành phần phương sai từ kiểm định LM: Var(u) = 0.3537; Var(e) = 0.0317. Kết luận ở mức ý nghĩa 5%.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Bảng 4.6 cho thấy các hệ số thay đổi đáng kể khi chuyển từ Pooled OLS sang các ước lượng có tính đến đặc điểm riêng của quốc gia: hệ số lnY giảm từ 1.1831 xuống 0.7143 và hệ số FDI giảm từ 0.0124 xuống 0.0068 trong FEM. Pooled OLS so sánh trực tiếp các nước với nhau nên hệ số lẫn cả những khác biệt cố định như cơ cấu năng lượng hay điều kiện tài nguyên; R² cao của Pooled OLS (0.8065) cũng chủ yếu đến từ khác biệt giữa các quốc gia.

Kiểm định F (F = 227.06) và Breusch–Pagan LM (chibar2 = 12076.40) đều bác bỏ H₀ với p-value 0.0000, nên Pooled OLS bị loại. Phương sai thành phần riêng quốc gia (0.3537) gấp khoảng 11 lần phương sai sai số còn lại (0.0317), cho thấy phần phát thải chưa được giải thích chủ yếu là khác biệt bền vững giữa các nước. Kiểm định Hausman bác bỏ H₀ ở Mô hình 1 (chi2(5) = 33.78) và ở cả mười hai phương trình của Mô hình 2 và 3 (chi2 từ 30.56 đến 37.99, p-value 0.0000): hiệu ứng riêng của quốc gia tương quan với các biến giải thích, nên REM cho ước lượng không nhất quán và FEM được lựa chọn. Cần lưu ý rằng các kiểm định này được thực hiện trên mô hình một chiều với sai số chuẩn thông thường, trong khi dữ liệu có phương sai sai số thay đổi (Mục 4.6), điều kiện mà kiểm định Hausman chuẩn không còn hoàn toàn hợp lệ. Tuy vậy, mức bác bỏ rất mạnh và nhất quán ở mọi đặc tả, cùng với việc FEM vẫn nhất quán ngay cả khi REM phù hợp, khiến lựa chọn FEM là an toàn.

Kiểm định đồng thời các biến giả năm bác bỏ H₀ (F(20, 72) = 3.04, p-value 0.0003): phát thải của các nước trong mẫu chịu tác động của những yếu tố chung theo năm mà các biến giải thích chưa nắm bắt, chẳng hạn biến động giá năng lượng hay các cú sốc kinh tế toàn cầu. Kết quả này nhất quán với dấu hiệu về thành phần chung từ kiểm định CIPS (Mục 4.4). Vì vậy, mô hình hiệu ứng cố định hai chiều (quốc gia và năm) được lựa chọn làm mô hình ước lượng cuối cùng cho cả ba mô hình nghiên cứu.

## 4.6. Kiểm định khuyết tật mô hình và lựa chọn sai số chuẩn

Bảng 4.8. Kết quả kiểm định khuyết tật của mô hình FEM hai chiều (Mô hình 1)

| Khuyết tật | Kiểm định | Thống kê | Giá trị | p-value | Kết luận |
|:--|:--|:-:|:-:|:-:|:--|
| Phương sai sai số thay đổi | Modified Wald | chi2(73) | 30441.51 | 0.0000 | Bác bỏ H₀ |
| Phụ thuộc chéo | Pesaran CD | CD | 1.349 | 0.1773 | Không bác bỏ H₀ |
| Tự tương quan bậc một | Wooldridge | F(1, 72) | 102.224 | 0.0000 | Bác bỏ H₀ |

Ghi chú: H₀ của Modified Wald: phương sai sai số như nhau giữa các quốc gia; của Pesaran CD: phần dư giữa các quốc gia độc lập; của Wooldridge: không có tự tương quan bậc một. Modified Wald và Pesaran CD thực hiện trên FEM có biến giả năm; trung bình giá trị tuyệt đối của hệ số tương quan phần dư giữa các quốc gia là 0.454. Kiểm định Wooldridge (lệnh xtserial) thực hiện với các biến của Mô hình 1, không bao gồm biến giả năm.

Nguồn: Tác giả tổng hợp từ kết quả lệnh xttest3, xtcsd và xtserial trên phần mềm Stata.

Mô hình tồn tại hai khuyết tật. Kiểm định Modified Wald bác bỏ mạnh giả thuyết phương sai sai số đồng nhất (chi2(73) = 30441.51), phù hợp với mức độ không đồng nhất cao giữa các nước. Kiểm định Wooldridge bác bỏ giả thuyết không có tự tương quan bậc một (F(1, 72) = 102.224): các cú sốc phát thải có xu hướng kéo dài sang năm sau, nhất quán với tính bền bỉ của lnCO2. Với điều kiện các biến giải thích ngoại sinh chặt, hai khuyết tật này không làm hệ số FEM bị chệch nhưng làm sai số chuẩn thông thường không còn tin cậy, thường theo hướng ước lượng thấp, dẫn đến nguy cơ kết luận sai về ý nghĩa thống kê (Drukker, 2003).

Kiểm định Pesaran CD không bác bỏ giả thuyết độc lập giữa các quốc gia (CD = 1.349, p-value 0.1773), điều có thể lý giải bởi các cú sốc chung đã được biến giả năm hấp thụ. Tuy nhiên, trung bình giá trị tuyệt đối của tương quan phần dư vẫn ở mức 0.454; do thống kê CD được tính từ tổng các hệ số tương quan, các tương quan dương và âm có thể triệt tiêu nhau (Pesaran, 2004), nên khả năng còn phụ thuộc chéo giữa một số nhóm quốc gia chưa thể loại trừ.

Từ các kết quả trên, nghiên cứu áp dụng một quy tắc suy luận thống nhất cho toàn chương. Sai số chuẩn cụm theo quốc gia được dùng làm căn cứ chính, vì cho phép phương sai sai số khác nhau giữa các nước và tương quan tùy ý theo thời gian trong cùng một nước, qua đó xử lý trực tiếp hai khuyết tật đã phát hiện, và dựa trên 73 cụm, đủ lớn cho suy luận tiệm cận (Cameron và Miller, 2015). Sai số chuẩn Driscoll–Kraay (Hoechle, 2007) được dùng để đối chiếu do vững thêm với phụ thuộc chéo; tuy nhiên phương pháp này dựa trên tiệm cận theo chiều thời gian, ở đây chỉ có 21 năm, và chỉ tính tự tương quan đến một số ít bậc trễ, nên có xu hướng ước lượng thấp sai số chuẩn của các biến thay đổi chậm khi sai số tự tương quan mạnh. **Một kết quả được xem là vững khi có ý nghĩa thống kê với cả hai loại sai số chuẩn; kết quả chỉ có ý nghĩa với Driscoll–Kraay được xem là bằng chứng gợi ý, không đủ để kết luận.** Các kiểm định khuyết tật chỉ quyết định cách tính sai số chuẩn, không làm thay đổi hệ số ước lượng.

## 4.7. Kết quả ước lượng mô hình nghiên cứu

Các mô hình được ước lượng bằng FEM hai chiều với sai số chuẩn cụm theo quốc gia. Do biến phụ thuộc ở dạng logarit, hệ số β được hiểu là khi biến giải thích tăng một đơn vị, phát thải CO₂ bình quân đầu người thay đổi xấp xỉ 100×β phần trăm, các yếu tố khác không đổi. Vì FEM chỉ khai thác biến thiên trong nội bộ quốc gia, độ lớn kinh tế được đánh giá theo mức thay đổi một độ lệch chuẩn trong nội bộ quốc gia (Bảng 4.1). Các hệ số phản ánh mối liên hệ có điều kiện giữa các biến; khả năng diễn giải nhân quả được bàn ở Mục 4.9.4.

### 4.7.1. Tác động của FDI đến phát thải CO₂ (Mô hình 1)

Bảng 4.9. Tác động của FDI đến phát thải CO₂ (Mô hình 1)

| Biến | (1) Sai số chuẩn cụm | (2) Driscoll–Kraay |
|:--|:-:|:-:|
| FDI | 0.0080\*\*\* | 0.0080\*\* |
|  | (0.0030) | (0.0029) |
|  | [0.0085] | [0.0110] |
| lnY | 0.5869\*\*\* | 0.5869\*\*\* |
|  | (0.1326) | (0.0474) |
|  | [0.0000] | [0.0000] |
| URB | 0.0025 | 0.0025 |
|  | (0.0073) | (0.0023) |
|  | [0.7296] | [0.2902] |
| TO | 0.0013 | 0.0013\*\*\* |
|  | (0.0012) | (0.0004) |
|  | [0.2732] | [0.0017] |
| Crdt | 0.0041\*\* | 0.0041\*\*\* |
|  | (0.0017) | (0.0008) |
|  | [0.0189] | [0.0000] |
| Số quan sát | 1,533 | 1,533 |
| Số quốc gia | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] |

Ghi chú: Mỗi biến gồm ba dòng: hệ số, (sai số chuẩn) và [p-value]. \*, \*\*, \*\*\* tương ứng mức ý nghĩa 10%, 5% và 1%. Biến phụ thuộc là lnCO2. FEM hai chiều; hằng số và biến giả năm không báo cáo. Cột (1): sai số chuẩn cụm theo quốc gia (kết quả chính, M1_CL); cột (2): sai số chuẩn Driscoll–Kraay (M1_DK). Ghi chú này áp dụng cho các Bảng 4.10–4.15.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Hệ số FDI bằng 0.0080 và có ý nghĩa ở mức 1% (p-value 0.0085; khoảng tin cậy 95% từ 0.0020 đến 0.0140): trong cùng một quốc gia, khi tỷ trọng FDI tăng thêm một điểm phần trăm GDP, phát thải CO₂ bình quân đầu người cao hơn khoảng 0.8%. Mức tăng một độ lệch chuẩn trong nội bộ quốc gia của FDI (3.94 điểm phần trăm) đi kèm phát thải cao hơn khoảng 3.2%. Kết quả giữ ý nghĩa ở mức 5% với sai số chuẩn Driscoll–Kraay (p-value 0.0110). Như vậy, giả thuyết H1 được ủng hộ, với chiều tác động dương. Do mô hình đã kiểm soát lnY, hệ số này phản ánh mối liên hệ giữa FDI và phát thải ngoài phần đi qua tăng trưởng thu nhập.

Trong các biến kiểm soát, lnY có hệ số co giãn 0.5869 (p-value 0.0000): thu nhập bình quân đầu người tăng 1% đi kèm phát thải tăng khoảng 0.59%. Hệ số nhỏ hơn 1 hàm ý cường độ phát thải trên mỗi đơn vị thu nhập giảm dần khi thu nhập tăng trong nội bộ các nước, dù phát thải bình quân đầu người vẫn tăng. Quy đổi theo độ lệch chuẩn trong nội bộ quốc gia, lnY (khoảng 11 điểm phần trăm phát thải) có tác động lớn hơn ba lần FDI (3.2%), nên tăng trưởng thu nhập vẫn là yếu tố gắn với phát thải mạnh nhất. Crdt dương và có ý nghĩa ở mức 5% (p-value 0.0189); URB và TO không có ý nghĩa với sai số chuẩn cụm.

### 4.7.2. Tác động trực tiếp của từng khía cạnh thể chế (Mô hình 2)

Bảng 4.10. Tác động trực tiếp của từng khía cạnh chất lượng thể chế đến phát thải CO₂ (Mô hình 2)

| Biến | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| FDI | 0.0079\*\* | 0.0079\*\*\* | 0.0079\*\*\* | 0.0079\*\*\* | 0.0080\*\*\* | 0.0080\*\*\* |
|  | (0.0030) | (0.0029) | (0.0030) | (0.0030) | (0.0030) | (0.0029) |
|  | [0.0105] | [0.0087] | [0.0091] | [0.0095] | [0.0087] | [0.0083] |
| Chỉ số thể chế k | −0.1108\* | −0.1358\*\* | −0.0313 | −0.0602 | −0.0202 | 0.0061 |
|  | (0.0624) | (0.0608) | (0.0523) | (0.0573) | (0.0729) | (0.0698) |
|  | [0.0800] | [0.0287] | [0.5515] | [0.2966] | [0.7822] | [0.9311] |
| lnY | 0.6468\*\*\* | 0.6777\*\*\* | 0.6053\*\*\* | 0.6241\*\*\* | 0.5948\*\*\* | 0.5860\*\*\* |
|  | (0.1329) | (0.1325) | (0.1352) | (0.1413) | (0.1370) | (0.1342) |
|  | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] |
| URB | 0.0020 | 0.0021 | 0.0023 | 0.0019 | 0.0024 | 0.0026 |
|  | (0.0072) | (0.0073) | (0.0075) | (0.0072) | (0.0073) | (0.0073) |
|  | [0.7859] | [0.7737] | [0.7567] | [0.7908] | [0.7473] | [0.7250] |
| TO | 0.0012 | 0.0011 | 0.0012 | 0.0012 | 0.0013 | 0.0013 |
|  | (0.0011) | (0.0012) | (0.0011) | (0.0012) | (0.0012) | (0.0012) |
|  | [0.3075] | [0.3400] | [0.3044] | [0.3077] | [0.2783] | [0.2696] |
| Crdt | 0.0041\*\* | 0.0040\*\* | 0.0043\*\* | 0.0041\*\* | 0.0042\*\* | 0.0041\*\* |
|  | (0.0017) | (0.0017) | (0.0017) | (0.0017) | (0.0017) | (0.0018) |
|  | [0.0157] | [0.0216] | [0.0135] | [0.0168] | [0.0177] | [0.0215] |
| Số quan sát | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 |
| Số quốc gia (số cụm) | 73 | 73 | 73 | 73 | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] |

Ghi chú: Xem ghi chú Bảng 4.9. Mỗi cột đưa một chỉ số thể chế k ghi ở đầu cột (ước lượng M2CL_CC đến M2CL_VA); sai số chuẩn cụm theo quốc gia.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Khi bổ sung lần lượt từng chỉ số thể chế, hệ số FDI gần như không đổi (0.0079–0.0080) và có ý nghĩa ở mức 5% trong cả sáu phương trình, cho thấy kết quả của Mô hình 1 không do thiếu biến thể chế. Năm trong sáu chỉ số mang dấu âm, nhưng chỉ hiệu quả chính phủ (GE: −0.1358; p-value 0.0287) có ý nghĩa ở mức 5% và kiểm soát tham nhũng (CC: −0.1108; p-value 0.0800) có ý nghĩa ở mức 10%. Về độ lớn, mức cải thiện một độ lệch chuẩn trong nội bộ quốc gia của GE (0.235 điểm) đi kèm phát thải thấp hơn khoảng 3.2%; con số tương ứng của CC (0.194 điểm) là khoảng 2.2%. Dấu âm của GE trái với tương quan thô dương (0.5866, Bảng 4.2): khi đã loại bỏ khác biệt cố định giữa các nước và kiểm soát thu nhập, sự cải thiện hiệu quả chính phủ trong nội bộ một quốc gia gắn với phát thải thấp hơn.

Đối với giả thuyết H2 về tác động khác biệt giữa các khía cạnh, kết quả cần được đọc thận trọng. Việc GE có ý nghĩa trong khi các khía cạnh khác không có ý nghĩa chưa đủ để kết luận GE có tác động mạnh hơn, vì khác biệt giữa một hệ số có ý nghĩa và một hệ số không có ý nghĩa tự nó chưa chắc có ý nghĩa thống kê (Gelman và Stern, 2006). Chẳng hạn, khoảng tin cậy 95% của GE (−0.257 đến −0.015) và RQ (−0.174 đến 0.054) chồng lấn phần lớn. Sai số chuẩn lớn của các chỉ số thể chế (0.052–0.073) phản ánh biến thiên trong nội bộ quốc gia nhỏ của WGI (Mục 4.1), nên các khía cạnh không có ý nghĩa có thể do ước lượng kém chính xác chứ chưa hẳn do không có tác động. Vì vậy, kết luận có thể rút ra là: chỉ hiệu quả chính phủ, và ở mức yếu hơn là kiểm soát tham nhũng, có bằng chứng thống kê về mối liên hệ ngược chiều với phát thải; H2 được ủng hộ một phần.

### 4.7.3. Vai trò điều tiết của từng khía cạnh thể chế (Mô hình 3)

Bảng 4.11. Vai trò điều tiết của chất lượng thể chế trong mối quan hệ FDI – CO₂ (Mô hình 3)

| Biến | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| FDI | 0.0062\*\*\* | 0.0079\*\*\* | 0.0083\*\*\* | 0.0083\*\*\* | 0.0076\*\*\* | 0.0072\*\*\* |
|  | (0.0021) | (0.0022) | (0.0030) | (0.0024) | (0.0026) | (0.0024) |
|  | [0.0045] | [0.0005] | [0.0072] | [0.0008] | [0.0038] | [0.0032] |
| Chỉ số thể chế k | −0.1136\* | −0.1358\*\* | −0.0336 | −0.0603 | −0.0200 | 0.0037 |
|  | (0.0638) | (0.0608) | (0.0517) | (0.0571) | (0.0728) | (0.0695) |
|  | [0.0793] | [0.0286] | [0.5178] | [0.2946] | [0.7848] | [0.9572] |
| FDI × k | −0.0049 | −0.0001 | −0.0053 | 0.0022 | −0.0024 | −0.0039 |
|  | (0.0063) | (0.0056) | (0.0033) | (0.0056) | (0.0055) | (0.0047) |
|  | [0.4366] | [0.9850] | [0.1137] | [0.6946] | [0.6703] | [0.4068] |
| lnY | 0.6562\*\*\* | 0.6779\*\*\* | 0.6147\*\*\* | 0.6247\*\*\* | 0.5945\*\*\* | 0.5934\*\*\* |
|  | (0.1356) | (0.1338) | (0.1349) | (0.1404) | (0.1373) | (0.1364) |
|  | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] |
| URB | 0.0016 | 0.0021 | 0.0021 | 0.0019 | 0.0024 | 0.0025 |
|  | (0.0072) | (0.0073) | (0.0074) | (0.0072) | (0.0073) | (0.0073) |
|  | [0.8234] | [0.7752] | [0.7800] | [0.7906] | [0.7469] | [0.7341] |
| TO | 0.0012 | 0.0011 | 0.0011 | 0.0012 | 0.0012 | 0.0012 |
|  | (0.0011) | (0.0012) | (0.0011) | (0.0012) | (0.0012) | (0.0012) |
|  | [0.3118] | [0.3407] | [0.3447] | [0.3006] | [0.2867] | [0.2928] |
| Crdt | 0.0041\*\* | 0.0040\*\* | 0.0043\*\* | 0.0041\*\* | 0.0042\*\* | 0.0041\*\* |
|  | (0.0017) | (0.0017) | (0.0017) | (0.0017) | (0.0017) | (0.0017) |
|  | [0.0164] | [0.0217] | [0.0133] | [0.0168] | [0.0176] | [0.0214] |
| Số quan sát | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 |
| Số quốc gia (số cụm) | 73 | 73 | 73 | 73 | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] |

Ghi chú: Xem ghi chú Bảng 4.9. Biến tương tác FDI × k được tạo từ FDI và chỉ số k sau khi trừ giá trị trung bình mẫu của từng biến; các số hạng chính FDI và k giữ nguyên thang đo gốc. Do đó, hệ số FDI là tác động của FDI tại mức trung bình của chỉ số k, và hệ số của k là tác động của k tại mức FDI trung bình. Cột (1)–(6) tương ứng M3CL_CC đến M3CL_VA; sai số chuẩn cụm theo quốc gia.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Không biến tương tác nào có ý nghĩa thống kê ở mức 10% (p-value từ 0.1137 đối với FDI × PV đến 0.9850 đối với FDI × GE), nên giả thuyết H3 không được ủng hộ trong mô hình chính. Hệ số FDI, tức tác động tại mức thể chế trung bình của mẫu, vẫn dương và có ý nghĩa ở mức 1% trong cả sáu phương trình (0.0062–0.0083), trong khi hệ số của GE và CC gần như không đổi so với Mô hình 2.

Tuy nhiên, kết quả này cần được hiểu là chưa có bằng chứng về hiệu ứng điều tiết, không phải bằng chứng cho thấy hiệu ứng điều tiết bằng không. Khoảng tin cậy của các hệ số tương tác rất rộng. Với FDI × GE (−0.0001; khoảng tin cậy 95% từ −0.0113 đến 0.0111), dữ liệu không loại trừ khả năng GE cao hơn một độ lệch chuẩn tổng thể (0.589 điểm) làm tác động của FDI giảm khoảng 0.0066, gần bằng toàn bộ tác động trung bình (0.0079), nhưng cũng không loại trừ khả năng ngược lại. Năm trong sáu hệ số tương tác mang dấu âm, cùng chiều kỳ vọng, song độ chính xác của ước lượng không đủ để nhận diện hiệu ứng điều tiết ở quy mô có ý nghĩa kinh tế. Kết quả với sai số chuẩn Driscoll–Kraay, trong đó FDI × PV có ý nghĩa, được trình bày tại Mục 4.8.1.

## 4.8. Kiểm định độ vững

Phần này kiểm tra ba kết luận của Mục 4.7: FDI gắn với phát thải cao hơn (H1); GE, và ở mức yếu hơn CC, gắn với phát thải thấp hơn (H2); không có bằng chứng về vai trò điều tiết của thể chế (H3). Bốn kiểm định độ vững lần lượt thay đổi cách tính sai số chuẩn, cách đo lường thể chế, cấu trúc độ trễ và tập biến kiểm soát. Mô hình động System GMM được trình bày riêng như một phân tích bổ sung (Mục 4.8.5).

### 4.8.1. Sai số chuẩn Driscoll–Kraay

Bảng 4.12. Kiểm định độ vững với sai số chuẩn Driscoll–Kraay

Phần A. Mô hình 2

| Biến | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| FDI | 0.0079\*\* | 0.0079\*\* | 0.0079\*\* | 0.0079\*\* | 0.0080\*\* | 0.0080\*\* |
|  | (0.0029) | (0.0028) | (0.0028) | (0.0028) | (0.0028) | (0.0029) |
|  | [0.0121] | [0.0113] | [0.0105] | [0.0115] | [0.0109] | [0.0110] |
| Chỉ số thể chế k | −0.1108\*\*\* | −0.1358\*\*\* | −0.0313\* | −0.0602\*\* | −0.0202 | 0.0061 |
|  | (0.0286) | (0.0306) | (0.0152) | (0.0249) | (0.0250) | (0.0269) |
|  | [0.0009] | [0.0003] | [0.0530] | [0.0252] | [0.4279] | [0.8242] |
| lnY | 0.6468\*\*\* | 0.6777\*\*\* | 0.6053\*\*\* | 0.6241\*\*\* | 0.5948\*\*\* | 0.5860\*\*\* |
|  | (0.0434) | (0.0444) | (0.0475) | (0.0491) | (0.0419) | (0.0453) |
|  | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] |
| URB | 0.0020 | 0.0021 | 0.0023 | 0.0019 | 0.0024 | 0.0026 |
|  | (0.0024) | (0.0021) | (0.0025) | (0.0022) | (0.0024) | (0.0024) |
|  | [0.4154] | [0.3409] | [0.3579] | [0.3939] | [0.3323] | [0.3023] |
| TO | 0.0012\*\*\* | 0.0011\*\*\* | 0.0012\*\*\* | 0.0012\*\*\* | 0.0013\*\*\* | 0.0013\*\*\* |
|  | (0.0003) | (0.0003) | (0.0004) | (0.0004) | (0.0004) | (0.0004) |
|  | [0.0021] | [0.0045] | [0.0058] | [0.0040] | [0.0025] | [0.0019] |
| Crdt | 0.0041\*\*\* | 0.0040\*\*\* | 0.0043\*\*\* | 0.0041\*\*\* | 0.0042\*\*\* | 0.0041\*\*\* |
|  | (0.0008) | (0.0008) | (0.0009) | (0.0008) | (0.0008) | (0.0009) |
|  | [0.0001] | [0.0001] | [0.0001] | [0.0000] | [0.0001] | [0.0001] |
| Số quan sát | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 |
| Số quốc gia | 73 | 73 | 73 | 73 | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] |

Phần B. Mô hình 3

| Biến | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| FDI | 0.0062\*\* | 0.0079\*\* | 0.0083\*\*\* | 0.0083\*\*\* | 0.0076\*\*\* | 0.0072\*\*\* |
|  | (0.0027) | (0.0028) | (0.0022) | (0.0028) | (0.0026) | (0.0024) |
|  | [0.0345] | [0.0108] | [0.0011] | [0.0072] | [0.0089] | [0.0063] |
| Chỉ số thể chế k | −0.1136\*\*\* | −0.1358\*\*\* | −0.0336\*\* | −0.0603\*\* | −0.0200 | 0.0037 |
|  | (0.0282) | (0.0313) | (0.0156) | (0.0250) | (0.0254) | (0.0270) |
|  | [0.0007] | [0.0003] | [0.0442] | [0.0257] | [0.4413] | [0.8911] |
| FDI × k | −0.0049 | −0.0001 | −0.0053\*\*\* | 0.0022 | −0.0024 | −0.0039 |
|  | (0.0034) | (0.0054) | (0.0012) | (0.0050) | (0.0038) | (0.0028) |
|  | [0.1665] | [0.9843] | [0.0003] | [0.6661] | [0.5436] | [0.1694] |
| lnY | 0.6562\*\*\* | 0.6779\*\*\* | 0.6147\*\*\* | 0.6247\*\*\* | 0.5945\*\*\* | 0.5934\*\*\* |
|  | (0.0429) | (0.0407) | (0.0490) | (0.0494) | (0.0422) | (0.0442) |
|  | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] | [0.0000] |
| URB | 0.0016 | 0.0021 | 0.0021 | 0.0019 | 0.0024 | 0.0025 |
|  | (0.0022) | (0.0019) | (0.0024) | (0.0022) | (0.0024) | (0.0023) |
|  | [0.4769] | [0.2937] | [0.3950] | [0.3945] | [0.3303] | [0.3012] |
| TO | 0.0012\*\*\* | 0.0011\*\*\* | 0.0011\*\*\* | 0.0012\*\*\* | 0.0012\*\*\* | 0.0012\*\*\* |
|  | (0.0003) | (0.0003) | (0.0004) | (0.0004) | (0.0004) | (0.0004) |
|  | [0.0022] | [0.0048] | [0.0089] | [0.0049] | [0.0037] | [0.0037] |
| Crdt | 0.0041\*\*\* | 0.0040\*\*\* | 0.0043\*\*\* | 0.0041\*\*\* | 0.0042\*\*\* | 0.0041\*\*\* |
|  | (0.0008) | (0.0008) | (0.0009) | (0.0008) | (0.0008) | (0.0009) |
|  | [0.0001] | [0.0001] | [0.0001] | [0.0000] | [0.0001] | [0.0002] |
| Số quan sát | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 | 1,533 |
| Số quốc gia | 73 | 73 | 73 | 73 | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] |

Ghi chú: Xem ghi chú Bảng 4.9 và 4.11. Sai số chuẩn Driscoll–Kraay. Phần A tương ứng M2DK_CC đến M2DK_VA; Phần B tương ứng M3DK_CC đến M3DK_VA. Kết quả Driscoll–Kraay của Mô hình 1 ở Bảng 4.9, cột (2).

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Do chỉ thay đổi cách tính sai số chuẩn, hệ số ở Bảng 4.12 trùng với Bảng 4.10 và 4.11; khác biệt nằm ở mức ý nghĩa. FDI tiếp tục dương và có ý nghĩa ở mức 5% trong cả mười hai phương trình. GE và CC có ý nghĩa ở mức 1% (p-value 0.0003 và 0.0009). Bên cạnh đó, RQ (p-value 0.0252) có ý nghĩa ở mức 5%, PV (0.0530) ở mức 10%, và biến tương tác FDI × PV có hệ số âm, có ý nghĩa ở mức 1% (p-value 0.0003); các biến tương tác còn lại vẫn không có ý nghĩa.

Sai số chuẩn Driscoll–Kraay của các chỉ số thể chế chỉ bằng khoảng 30% đến 50% sai số chuẩn cụm (ví dụ với CC: 0.0286 so với 0.0624), phù hợp với nhận định ở Mục 4.6 rằng phương pháp này dễ ước lượng thấp sai số chuẩn của các biến thay đổi chậm khi sai số tự tương quan mạnh. Theo quy tắc suy luận đã nêu, kết quả về FDI và GE là vững. CC có ý nghĩa với cả hai loại sai số chuẩn nhưng chỉ ở mức 10% với sai số chuẩn cụm, nên được xem là bằng chứng yếu hơn. Các kết quả chỉ xuất hiện với Driscoll–Kraay, gồm RQ, PV và FDI × PV, là bằng chứng gợi ý.

### 4.8.2. Chỉ số thể chế tổng hợp IQ_PCA

Chỉ số IQ_PCA là thành phần chính thứ nhất của sáu chỉ số WGI (Phụ lục PL1). Thành phần này có giá trị riêng 4.37394 và giải thích 72.90% tổng phương sai; các trọng số đều dương và tương đối đồng đều (0.35–0.46), nên có thể xem là thước đo chất lượng thể chế chung; hệ số KMO tổng thể 0.8632 cho thấy dữ liệu phù hợp để phân tích thành phần chính. IQ_PCA có độ lệch chuẩn 2.09, nên hệ số của nó không so sánh trực tiếp được với hệ số của từng chỉ số WGI.

Bảng 4.13. Kiểm định độ vững với chỉ số thể chế tổng hợp IQ_PCA

| Biến | M2 – Cụm | M2 – DK | M3 – Cụm | M3 – DK |
|:--|:-:|:-:|:-:|:-:|
| FDI | 0.0079\*\* | 0.0079\*\* | 0.0071\*\*\* | 0.0071\*\*\* |
|  | (0.0030) | (0.0028) | (0.0022) | (0.0025) |
|  | [0.0103] | [0.0114] | [0.0019] | [0.0090] |
| IQ_PCA | −0.0258 | −0.0258\*\*\* | −0.0259 | −0.0259\*\*\* |
|  | (0.0222) | (0.0085) | (0.0222) | (0.0085) |
|  | [0.2485] | [0.0066] | [0.2475] | [0.0062] |
| FDI × IQ_PCA |  |  | −0.0009 | −0.0009 |
|  |  |  | (0.0014) | (0.0010) |
|  |  |  | [0.5380] | [0.3784] |
| lnY | 0.6406\*\*\* | 0.6406\*\*\* | 0.6443\*\*\* | 0.6443\*\*\* |
|  | (0.1391) | (0.0426) | (0.1406) | (0.0411) |
|  | [0.0000] | [0.0000] | [0.0000] | [0.0000] |
| URB | 0.0018 | 0.0018 | 0.0016 | 0.0016 |
|  | (0.0075) | (0.0025) | (0.0075) | (0.0024) |
|  | [0.8155] | [0.4941] | [0.8277] | [0.5022] |
| TO | 0.0011 | 0.0011\*\*\* | 0.0011 | 0.0011\*\*\* |
|  | (0.0011) | (0.0004) | (0.0011) | (0.0004) |
|  | [0.3293] | [0.0061] | [0.3446] | [0.0081] |
| Crdt | 0.0043\*\* | 0.0043\*\*\* | 0.0043\*\* | 0.0043\*\*\* |
|  | (0.0017) | (0.0009) | (0.0017) | (0.0009) |
|  | [0.0133] | [0.0001] | [0.0134] | [0.0001] |
| Số quan sát | 1,533 | 1,533 | 1,533 | 1,533 |
| Số quốc gia | 73 | 73 | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] |

Ghi chú: Xem ghi chú Bảng 4.9. FDI × IQ_PCA là tích của FDI (đã trừ trung bình) và IQ_PCA (có trung bình bằng 0). Các cột tương ứng M2_IQ_CL, M2_IQ, M3_IQ_CL và M3_IQ; DK là sai số chuẩn Driscoll–Kraay.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Đối với H1, FDI dương và có ý nghĩa ở mức 5% trong cả bốn cột. Đối với H3, biến tương tác FDI × IQ_PCA không có ý nghĩa với cả hai loại sai số chuẩn (p-value 0.5380 và 0.3784), nhất quán với kết quả chính. Đối với H2, kết quả chỉ nhất quán một phần: IQ_PCA mang dấu âm, cùng chiều với GE và CC, có ý nghĩa với Driscoll–Kraay (p-value 0.0066) nhưng không có ý nghĩa với sai số chuẩn cụm (p-value 0.2485), nên theo quy tắc của nghiên cứu không được xem là vững. Về độ lớn, một độ lệch chuẩn tổng thể của IQ_PCA tương ứng mức phát thải thấp hơn khoảng 5.4%, không quá khác so với GE (khoảng 8% theo độ lệch chuẩn tổng thể); khác biệt giữa hai kết quả chủ yếu nằm ở độ chính xác của ước lượng. Kết quả này phù hợp với khả năng mối liên hệ giữa thể chế và phát thải tập trung ở một số khía cạnh như GE, nhưng chưa đủ để khẳng định chỉ số tổng hợp đã làm lu mờ tác động của các khía cạnh riêng lẻ.

### 4.8.3. Biến giải thích trễ một năm

Bảng 4.14. Kiểm định độ vững với biến giải thích trễ một năm

Phần A. Sai số chuẩn cụm theo quốc gia

| Biến | M1 | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA | (7) IQ_PCA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| L.FDI | 0.0093\*\*\* | 0.0082\*\*\* | 0.0095\*\*\* | 0.0096\*\*\* | 0.0096\*\*\* | 0.0089\*\*\* | 0.0089\*\*\* | 0.0087\*\*\* |
|  | (0.0030) | (0.0022) | (0.0023) | (0.0031) | (0.0023) | (0.0025) | (0.0025) | (0.0022) |
|  | [0.0027] | [0.0003] | [0.0001] | [0.0030] | [0.0001] | [0.0007] | [0.0006] | [0.0002] |
| L.k |  | −0.1162\* | −0.1287\*\* | −0.0181 | −0.0694 | −0.0026 | 0.0193 | −0.0219 |
|  |  | (0.0659) | (0.0632) | (0.0522) | (0.0599) | (0.0735) | (0.0728) | (0.0223) |
|  |  | [0.0822] | [0.0456] | [0.7299] | [0.2506] | [0.9719] | [0.7912] | [0.3277] |
| L.(FDI × k) |  | −0.0028 | 0.0008 | −0.0040 | 0.0019 | −0.0027 | −0.0023 | −0.0006 |
|  |  | (0.0060) | (0.0055) | (0.0029) | (0.0058) | (0.0059) | (0.0047) | (0.0014) |
|  |  | [0.6401] | [0.8773] | [0.1779] | [0.7408] | [0.6435] | [0.6258] | [0.6651] |
| Số quan sát | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có |

Phần B. Sai số chuẩn Driscoll–Kraay

| Biến | M1 | (1) CC | (2) GE | (3) PV | (4) RQ | (5) RL | (6) VA | (7) IQ_PCA |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| L.FDI | 0.0093\*\*\* | 0.0082\*\* | 0.0095\*\*\* | 0.0096\*\*\* | 0.0096\*\*\* | 0.0089\*\*\* | 0.0089\*\*\* | 0.0087\*\*\* |
|  | (0.0028) | (0.0030) | (0.0032) | (0.0024) | (0.0031) | (0.0029) | (0.0029) | (0.0029) |
|  | [0.0041] | [0.0120] | [0.0082] | [0.0007] | [0.0065] | [0.0062] | [0.0059] | [0.0078] |
| L.k |  | −0.1162\*\*\* | −0.1287\*\*\* | −0.0181 | −0.0694\*\*\* | −0.0026 | 0.0193 | −0.0219\*\* |
|  |  | (0.0326) | (0.0323) | (0.0122) | (0.0205) | (0.0218) | (0.0316) | (0.0082) |
|  |  | [0.0021] | [0.0008] | [0.1557] | [0.0031] | [0.9066] | [0.5482] | [0.0146] |
| L.(FDI × k) |  | −0.0028 | 0.0008 | −0.0040 | 0.0019 | −0.0027 | −0.0023 | −0.0006 |
|  |  | (0.0039) | (0.0061) | (0.0024) | (0.0050) | (0.0048) | (0.0037) | (0.0012) |
|  |  | [0.4771] | [0.8906] | [0.1215] | [0.7068] | [0.5784] | [0.5433] | [0.6242] |
| Số quan sát | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 | 1,460 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có | Có / Có |

Ghi chú: Xem ghi chú Bảng 4.9 và 4.11. Tất cả biến giải thích, kể cả lnY, URB, TO và Crdt, được lấy trễ một năm; biến kiểm soát không được báo cáo. Cột M1 là Mô hình 1; cột (1)–(7) là Mô hình 3 với chỉ số thể chế k ghi ở đầu cột. Mẫu bắt đầu từ năm 2003.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

Khi các biến giải thích được lấy trễ một năm, phát thải hiện tại không thể tác động ngược lại đến giá trị đã xảy ra, nên lo ngại về quan hệ đồng thời được giảm bớt, dù chưa được loại bỏ hoàn toàn do FDI và phát thải đều có tính bền bỉ. L.FDI dương và có ý nghĩa ở mức 1% trong cả tám phương trình với sai số chuẩn cụm (0.0082–0.0096), nên kết luận về H1 không phụ thuộc vào quan hệ cùng thời điểm. Vì mô hình thay FDI cùng kỳ bằng FDI trễ chứ không đưa đồng thời cả hai, kết quả này chưa cho biết tác động kéo dài bao lâu.

Đối với H2, bảng này ước lượng Mô hình 3 nên hệ số L.k là tác động của thể chế tại mức FDI trung bình; ở các ước lượng cùng kỳ, hệ số này gần như trùng với Mô hình 2 (ví dụ GE: −0.1358 ở cả hai mô hình), nên có thể dùng để đối chiếu. L.GE (−0.1287; p-value 0.0456) và L.CC (−0.1162; p-value 0.0822) giữ nguyên dấu và mức ý nghĩa như kết quả chính, đồng thời có ý nghĩa ở mức 1% với Driscoll–Kraay. Đối với H3, toàn bộ biến tương tác trễ không có ý nghĩa với cả hai loại sai số chuẩn; đáng chú ý, L.(FDI × PV) không còn ý nghĩa ngay cả với Driscoll–Kraay (p-value 0.1215), làm suy yếu thêm bằng chứng gợi ý về vai trò điều tiết của ổn định chính trị.

### 4.8.4. Loại biến đô thị hóa (URB)

Bảng 4.15. Kiểm định độ vững khi loại biến đô thị hóa (URB)

| Biến | M1 – Cụm | M1 – DK | M3-IQ – Cụm | M3-IQ – DK |
|:--|:-:|:-:|:-:|:-:|
| FDI | 0.0081\*\*\* | 0.0081\*\* | 0.0072\*\*\* | 0.0072\*\*\* |
|  | (0.0030) | (0.0029) | (0.0022) | (0.0025) |
|  | [0.0087] | [0.0115] | [0.0020] | [0.0089] |
| IQ_PCA |  |  | −0.0266 | −0.0266\*\*\* |
|  |  |  | (0.0223) | (0.0082) |
|  |  |  | [0.2361] | [0.0040] |
| FDI × IQ_PCA |  |  | −0.0009 | −0.0009 |
|  |  |  | (0.0014) | (0.0010) |
|  |  |  | [0.5295] | [0.3779] |
| lnY | 0.5940\*\*\* | 0.5940\*\*\* | 0.6503\*\*\* | 0.6503\*\*\* |
|  | (0.1287) | (0.0478) | (0.1373) | (0.0432) |
|  | [0.0000] | [0.0000] | [0.0000] | [0.0000] |
| TO | 0.0013 | 0.0013\*\*\* | 0.0011 | 0.0011\*\* |
|  | (0.0012) | (0.0004) | (0.0011) | (0.0004) |
|  | [0.2874] | [0.0041] | [0.3600] | [0.0144] |
| Crdt | 0.0044\*\* | 0.0044\*\*\* | 0.0044\*\* | 0.0044\*\*\* |
|  | (0.0020) | (0.0007) | (0.0020) | (0.0007) |
|  | [0.0312] | [0.0000] | [0.0264] | [0.0000] |
| Số quan sát | 1,533 | 1,533 | 1,533 | 1,533 |
| Số quốc gia | 73 | 73 | 73 | 73 |
| Hiệu ứng cố định quốc gia / năm | Có / Có | Có / Có | Có / Có | Có / Có |
| R² within | [bổ sung] | [bổ sung] | [bổ sung] | [bổ sung] |

Ghi chú: Xem ghi chú Bảng 4.9. Mô hình không có URB. Các cột tương ứng M1_noURB_CL, M1_noURB_DK, M3_IQ_noURB_CL và M3_IQ_noURB.

Nguồn: Tác giả tổng hợp từ kết quả Stata.

URB được loại khỏi mô hình do không dừng ở sai phân bậc một theo CIPS (Mục 4.4). Kết quả gần như không đổi: hệ số FDI ở Mô hình 1 là 0.0081 (p-value 0.0087) so với 0.0080 khi có URB, hệ số lnY là 0.5940 so với 0.5869, và biến tương tác FDI × IQ_PCA vẫn không có ý nghĩa (p-value 0.5295). Như vậy, đặc điểm không dừng của URB không chi phối kết luận về H1 và H3 (đo bằng IQ_PCA). Kiểm định này chưa được thực hiện riêng cho các mô hình của GE và CC, nên chưa kiểm chứng được độ vững của H2 khi loại URB; tuy vậy, do hệ số URB nhỏ và không có ý nghĩa trong mọi phương trình của Mô hình 2, khả năng URB làm thay đổi kết luận về GE và CC là thấp.

### 4.8.5. Phân tích bổ sung: mô hình động

Do phát thải có tính bền bỉ cao, nghiên cứu ước lượng thêm mô hình động có biến trễ lnCO2 bằng ba phương pháp (Bảng 4.16; chi tiết System GMM ở Phụ lục PL2).

Bảng 4.16. Kết quả ước lượng mô hình động

| Biến | (1) Pooled OLS động | (2) FE động | (3) System GMM |
|:--|:-:|:-:|:-:|
| L.lnCO2 | 0.9823\*\*\* | 0.8234\*\*\* | 1.0051\*\*\* |
|  | (0.0041) | (0.0256) | (0.0459) |
|  | [0.0000] | [0.0000] | [0.000] |
| FDI | 0.0021\*\* | 0.0028\*\* | 0.0055\*\* |
|  | (0.0010) | (0.0012) | (0.0025) |
|  | [0.0438] | [0.0202] | [0.029] |
| lnY | 0.0094 | 0.1470\*\*\* | 0.1476\* |
|  | (0.0085) | (0.0452) | (0.0884) |
|  | [0.2697] | [0.0017] | [0.099] |
| URB | −0.0002 | 0.0013 | −0.0060\*\* |
|  | (0.0003) | (0.0022) | (0.0030) |
|  | [0.4560] | [0.5607] | [0.047] |
| TO | 0.0001 | 0.0007\* | −0.0007 |
|  | (0.0001) | (0.0003) | (0.0004) |
|  | [0.3354] | [0.0604] | [0.120] |
| Crdt | 0.0003\*\* | 0.0002 | −0.0013 |
|  | (0.0001) | (0.0004) | (0.0010) |
|  | [0.0382] | [0.6261] | [0.199] |
| Số quan sát / số quốc gia | 1,460 / 73 | 1,460 / 73 | 1,460 / 73 |
| Biến giả năm | Có | Có | Có |
| AR(2) – p-value |  |  | 0.169 |
| Hansen – p-value |  |  | 0.531 |
| Số biến công cụ |  |  | 33 |

Ghi chú: Xem ghi chú Bảng 4.9. Cột (1) và (2) dùng sai số chuẩn cụm theo quốc gia. Cột (3): System GMM hai bước, sai số chuẩn hiệu chỉnh (twostep robust small); biến công cụ GMM gồm L.lnCO2 (độ trễ 1–3), FDI và lnY (độ trễ 2–3), dạng collapse; URB, TO, Crdt và biến giả năm là biến công cụ chuẩn.

Nguồn: Tác giả tổng hợp từ kết quả lệnh regress, xtreg và xtabond2 trên phần mềm Stata.

Các kiểm định chẩn đoán của System GMM đạt yêu cầu: AR(2) không có ý nghĩa (p-value 0.169), kiểm định Hansen không bác bỏ tính hợp lệ của biến công cụ (p-value 0.531), và số biến công cụ (33) nhỏ hơn số quốc gia (73) (Roodman, 2009). FDI có hệ số dương và có ý nghĩa ở mức 5% (0.0055; p-value 0.029). Tuy nhiên, hệ số biến trễ lnCO2 bằng 1.0051, với khoảng tin cậy 95% (0.9136 đến 1.0965) bao gồm giá trị 1, và vượt cả cận trên do Pooled OLS động cung cấp (0.9823), trong khi FE động (0.8234) là cận dưới. Một ước lượng GMM đáng tin cậy cần nằm giữa hai cận này (Bond, 2002); việc nằm ngoài khoảng cho thấy biến công cụ có thể yếu, dù các kiểm định chẩn đoán đạt yêu cầu. Bên cạnh đó, hệ số xấp xỉ 1 hàm ý phát thải gần như có nghiệm đơn vị, nên giả định ổn định của mô hình động không được thỏa mãn và tác động dài hạn không xác định được. Vì vậy, System GMM không được dùng để kết luận các giả thuyết. Kết quả của các phương pháp động chỉ cho thấy một điểm chung: hệ số FDI ngắn hạn dương và có ý nghĩa ở mức 5% trong cả ba cột (0.0021–0.0055). Do có biến trễ của biến phụ thuộc, các hệ số này là tác động ngắn hạn và không so sánh trực tiếp được với hệ số của mô hình tĩnh.

### 4.8.6. Tổng hợp kết quả kiểm định độ vững

Bảng 4.17. Tổng hợp kết quả kiểm định độ vững

| Kết luận | Mô hình chính (cụm) | Driscoll–Kraay | IQ_PCA | Biến trễ (cụm) | Loại URB | Đánh giá |
|:--|:-:|:-:|:-:|:-:|:-:|:--|
| H1: FDI (+) | 1% | 5% | 5% | 1% | 1% | Vững |
| H2: GE (−) | 5% | 1% | — | 5% | Chưa kiểm định | Vững |
| H2: CC (−) | 10% | 1% | — | 10% | Chưa kiểm định | Bằng chứng yếu |
| H2: RQ, PV (−) | Không | 5%; 10% | — | Không | Chưa kiểm định | Gợi ý |
| H2: IQ_PCA (−) | — | — | Không (cụm); 1% (DK) | Không | Không (cụm) | Gợi ý |
| H3: FDI × PV (−) | Không | 1% | — | Không | — | Gợi ý, không duy trì khi lấy trễ |
| H3: các tương tác khác | Không | Không | Không | Không | Không | Không có bằng chứng |

Ghi chú: Ô ghi mức ý nghĩa cao nhất đạt được; “Không” là không có ý nghĩa ở mức 10%; “—” là không áp dụng. Với H1, cột Driscoll–Kraay ghi mức ý nghĩa thấp nhất trong các phương trình của Mô hình 1–3. Đánh giá theo quy tắc suy luận ở Mục 4.6.

Nguồn: Tác giả tổng hợp từ Bảng 4.9–4.15.

Qua bốn kiểm định độ vững, hệ số FDI dương và có ý nghĩa ở mức tối thiểu 5% trong mọi đặc tả với cả hai loại sai số chuẩn, nên H1 được ủng hộ nhất quán. Đối với H2, chỉ GE âm và có ý nghĩa với cả hai loại sai số chuẩn, ở cả dạng cùng kỳ và dạng trễ; CC cùng chiều nhưng chỉ đạt mức 10% với sai số chuẩn cụm, còn RQ, PV và chỉ số tổng hợp chỉ có ý nghĩa với Driscoll–Kraay, nên H2 được ủng hộ một phần, tập trung ở khía cạnh hiệu quả chính phủ. Đối với H3, không biến tương tác nào có ý nghĩa với sai số chuẩn cụm trong bất kỳ đặc tả nào; FDI × PV chỉ có ý nghĩa với Driscoll–Kraay ở dạng cùng kỳ và mất ý nghĩa khi lấy trễ, nên chưa có bằng chứng ủng hộ H3.

## 4.9. Thảo luận kết quả

### 4.9.1. FDI và phát thải CO₂ (H1)

Kết quả ủng hộ giả thuyết H1: FDI có mối liên hệ cùng chiều và có ý nghĩa với phát thải CO₂ bình quân đầu người tại các quốc gia đang phát triển. Một điểm phần trăm FDI/GDP tăng thêm đi kèm phát thải cao hơn khoảng 0.8%, và kết quả vững qua mọi kiểm định độ vững. Về độ lớn, đây là một chi phí môi trường đo lường được nhưng không phải động lực chính của phát thải: quy đổi theo biến động thực tế trong nội bộ quốc gia, mối liên hệ của thu nhập với phát thải lớn hơn ba lần của FDI.

Về lý thuyết, kết quả phù hợp với giả thuyết thiên đường ô nhiễm (Copeland và Taylor, 2004), theo đó các nước đang phát triển với tiêu chuẩn môi trường thấp hơn có thể thu hút các hoạt động sản xuất có cường độ phát thải cao. Do mô hình đã kiểm soát thu nhập, hệ số FDI không đơn thuần phản ánh hiệu ứng quy mô của tăng trưởng mà gợi ý vai trò của hiệu ứng cơ cấu, tức dòng vốn tập trung vào các ngành phát thải cao, hoặc của công nghệ sản xuất đi kèm. Đồng thời, kết quả không ủng hộ giả thuyết vầng hào quang ô nhiễm (Zarsky, 1999) như một xu hướng chiếm ưu thế, dù không loại trừ việc hiệu ứng lan tỏa công nghệ sạch tồn tại nhưng bị lấn át. Do mô hình chỉ xác định được tác động ròng và không có dữ liệu theo ngành, nghiên cứu chưa tách được các kênh này; kết quả vì vậy nhất quán với giả thuyết thiên đường ô nhiễm nhưng chưa phải bằng chứng trực tiếp cho cơ chế đó.

Về thực nghiệm, kết quả tương đồng với Pao và Tsai (2011) cho nhóm BRIC và Shahbaz và cộng sự (2015) cho các nhóm quốc gia theo mức thu nhập, đều ghi nhận FDI làm gia tăng phát thải CO₂; ngược lại, Zhu và cộng sự (2016) cho thấy FDI làm giảm phát thải tại ASEAN-5. Sự khác biệt có thể xuất phát từ đặc điểm mẫu: nghiên cứu này bao gồm 73 quốc gia có chất lượng thể chế trung bình thấp hơn mặt bằng thế giới, nơi khả năng áp đặt tiêu chuẩn môi trường đối với dòng vốn nước ngoài còn hạn chế.

### 4.9.2. Chất lượng thể chế và phát thải CO₂ (H2)

Giả thuyết H2 được ủng hộ một phần. Trong sáu khía cạnh, chỉ hiệu quả chính phủ có mối liên hệ ngược chiều với phát thải một cách vững chắc: mức cải thiện một độ lệch chuẩn trong nội bộ quốc gia của GE đi kèm phát thải thấp hơn khoảng 3.2%, tương đương về độ lớn với tác động của một độ lệch chuẩn FDI nhưng ngược chiều. Kiểm soát tham nhũng cùng chiều nhưng bằng chứng yếu hơn (mức 10%). Các khía cạnh còn lại và chỉ số tổng hợp không có ý nghĩa với sai số chuẩn cụm.

Phát hiện đáng chú ý là sự đảo chiều của GE: tương quan thô dương (0.5866) nhưng hệ số trong FEM âm. Khi so sánh giữa các quốc gia, nước có thể chế tốt hơn thường giàu hơn và phát thải nhiều hơn; khi loại bỏ khác biệt cố định và kiểm soát thu nhập, cải thiện hiệu quả chính phủ trong nội bộ một quốc gia lại gắn với phát thải thấp hơn. Như vậy, tương quan thô giữa thể chế và phát thải chủ yếu phản ánh trình độ phát triển, và vai trò của thể chế chỉ được nhận diện đúng chiều khi tách được yếu tố này.

Về lý thuyết, kết quả phù hợp với lý thuyết thể chế (North, 1990), theo đó thể chế quyết định cách các quy tắc được thực thi trong thực tế. GE phản ánh năng lực xây dựng và thực thi chính sách của bộ máy nhà nước, còn CC phản ánh mức độ lạm dụng quyền lực công; cả hai đều liên quan trực tiếp đến việc quy định môi trường có được áp dụng nghiêm túc hay không. Trong khi đó, RQ trong WGI chủ yếu đo khả năng ban hành chính sách hỗ trợ khu vực tư nhân phát triển, không phải mức độ nghiêm ngặt của quy định môi trường. Tuy nhiên, như đã phân tích ở Mục 4.7.2, khoảng tin cậy của các khía cạnh chồng lấn nhau, nên kết quả chưa cho phép xếp hạng tầm quan trọng của từng khía cạnh; các giải thích trên dựa trên định nghĩa của chỉ số và chưa được kiểm định trực tiếp. Sai số chuẩn lớn của các khía cạnh không có ý nghĩa cũng có thể bắt nguồn từ biến thiên trong nội bộ quốc gia nhỏ của WGI và sai số đo lường của các chỉ số dựa trên cảm nhận (Kaufmann và cộng sự, 2011).

Về thực nghiệm, kết quả về GE và CC cùng chiều với Lau và cộng sự (2014), nghiên cứu tại Malaysia cho thấy chất lượng thể chế tốt hơn góp phần hạn chế phát thải. Khác biệt của nghiên cứu này là mối liên hệ chỉ được nhận diện vững chắc ở khía cạnh hiệu quả chính phủ, trong khi chỉ số tổng hợp chỉ cho bằng chứng gợi ý. Hàm ý là các nỗ lực giảm phát thải có cơ sở thực nghiệm rõ nhất khi gắn với nâng cao năng lực thực thi chính sách của chính phủ.

### 4.9.3. Vai trò điều tiết của chất lượng thể chế (H3)

Giả thuyết H3 không được ủng hộ. Trong mô hình chính, cả sáu biến tương tác đều không có ý nghĩa thống kê (p-value từ 0.1137 đến 0.9850), và kết quả tương tự khi dùng chỉ số tổng hợp, khi loại URB và khi lấy trễ một năm. Biến tương tác duy nhất có ý nghĩa, FDI × PV với sai số chuẩn Driscoll–Kraay, không xuất hiện với sai số chuẩn cụm và mất ý nghĩa khi lấy trễ, nên không đủ vững để làm căn cứ ủng hộ H3. Như vậy, FDI gắn với phát thải cao hơn ở mức thể chế điển hình của mẫu, nhưng không có bằng chứng cho thấy mức độ của mối liên hệ này thay đổi theo chất lượng thể chế.

Kết quả này khác với Bakhsh và cộng sự (2021), nghiên cứu cho rằng chất lượng thể chế làm giảm tác động gây ô nhiễm của FDI. Có thể đưa ra bốn cách giải thích, đều chưa được kiểm định trực tiếp. Thứ nhất, độ chính xác của ước lượng thấp: khoảng tin cậy của các hệ số tương tác đủ rộng để chứa cả những hiệu ứng điều tiết lớn về mặt kinh tế (Mục 4.7.3), nên kiểm định có độ mạnh hạn chế. Thứ hai, FDI biến động mạnh và có những giá trị cực đoan (từ −37% đến 55% GDP), làm tăng nhiễu của biến tương tác. Thứ ba, WGI là chỉ số dựa trên cảm nhận về quản trị nói chung, có sai số đo lường và không trực tiếp đo tiêu chuẩn môi trường hay cơ cấu ngành của dòng vốn, vốn là những yếu tố quyết định hành vi môi trường của doanh nghiệp FDI; sai số đo lường có xu hướng kéo hệ số tương tác về không. Thứ tư, chất lượng thể chế của mẫu thấp hơn mặt bằng thế giới ở cả sáu khía cạnh; nếu vai trò điều tiết chỉ phát huy khi thể chế vượt một ngưỡng nhất định, phần lớn quan sát có thể chưa đạt ngưỡng đó.

Kết quả về H3 cũng bổ sung một sắc thái cho thảo luận về H1. Trong các lập luận về thiên đường ô nhiễm gắn với thể chế, thể chế yếu là điều kiện để FDI làm tăng phát thải; việc không nhận diện được hiệu ứng điều tiết vì vậy chưa ủng hộ kênh “thể chế yếu dẫn đến thiên đường ô nhiễm”. Kết hợp với kết quả H2, bằng chứng gợi ý rằng hiệu quả chính phủ gắn với mức phát thải chung thấp hơn của nền kinh tế, nhưng chưa cho thấy nó làm thay đổi tác động môi trường của dòng vốn FDI. Hàm ý thận trọng là cải thiện quản trị nói chung có thể chưa đủ để tự động hạn chế tác động môi trường của FDI; các công cụ chuyên biệt như tiêu chuẩn môi trường đối với dự án đầu tư có thể cần thiết. Hàm ý này mang tính gợi mở và cần được kiểm chứng bằng các thước đo thể chế môi trường cụ thể hơn.

### 4.9.4. Giới hạn trong diễn giải kết quả

Các kết quả trên cần được đọc trong ba giới hạn. Thứ nhất, mô hình hiệu ứng cố định hai chiều loại bỏ được khác biệt cố định giữa các nước và các cú sốc chung theo năm, nhưng chưa xử lý triệt để khả năng nội sinh do quan hệ nhân quả ngược hoặc các yếu tố thay đổi theo thời gian bị bỏ sót, như cơ cấu năng lượng hay tỷ trọng công nghiệp; biến trễ chỉ giảm nhẹ vấn đề này, và System GMM không cho kết quả đủ tin cậy. Vì vậy, thuật ngữ “tác động” trong chương này được hiểu là mối liên hệ có điều kiện, nhất quán với một quan hệ nhân quả nhưng chưa phải bằng chứng nhân quả chặt chẽ. Thứ hai, bằng chứng về đồng liên kết chỉ mang tính hỗ trợ do các biến có bậc tích hợp khác nhau. Thứ ba, các kiểm định lựa chọn mô hình được thực hiện trên đặc tả một chiều với sai số chuẩn thông thường. Những giới hạn này được tổng hợp và đề xuất hướng khắc phục tại Mục 5.3.

## Tóm tắt Chương 4

Chương 4 trình bày kết quả thực nghiệm trên dữ liệu bảng cân bằng gồm 73 quốc gia đang phát triển giai đoạn 2002–2022. Dữ liệu cho thấy phát thải, thu nhập và chất lượng thể chế khác biệt chủ yếu giữa các quốc gia, trong khi FDI biến động mạnh qua thời gian trong từng nước. Ma trận tương quan và hệ số VIF ủng hộ việc ước lượng riêng từng khía cạnh thể chế. Các biến có bậc tích hợp khác nhau, và kiểm định Westerlund cho thấy tồn tại đồng liên kết ở một bộ phận quốc gia. Các kiểm định F, Breusch–Pagan LM, Hausman và kiểm định hiệu ứng năm dẫn đến lựa chọn mô hình hiệu ứng cố định hai chiều; do mô hình có phương sai sai số thay đổi và tự tương quan, sai số chuẩn cụm theo quốc gia được dùng làm căn cứ suy luận chính, sai số chuẩn Driscoll–Kraay dùng để đối chiếu.

Kết quả cho thấy FDI có mối liên hệ cùng chiều và vững với phát thải CO₂: một điểm phần trăm FDI/GDP tăng thêm đi kèm phát thải cao hơn khoảng 0.8%, ủng hộ H1. Đối với H2, chỉ hiệu quả chính phủ có mối liên hệ ngược chiều vững chắc với phát thải, kiểm soát tham nhũng cho bằng chứng yếu hơn, nên giả thuyết được ủng hộ một phần. Đối với H3, không có bằng chứng vững về vai trò điều tiết của chất lượng thể chế, dù độ chính xác của ước lượng chưa cho phép loại trừ hiệu ứng này. Mô hình động System GMM cho hệ số FDI cùng chiều nhưng hệ số biến trễ của phát thải nằm ngoài khoảng tin cậy hợp lý, nên chỉ được dùng để tham khảo. Những kết quả này là cơ sở cho kết luận và hàm ý chính sách tại Chương 5.

## PHỤ LỤC

### Phụ lục PL1. Kết quả phân tích thành phần chính (PCA) sáu chỉ số WGI

Phần A. Giá trị riêng và tỷ lệ phương sai giải thích

| Thành phần | Giá trị riêng | Chênh lệch | Tỷ lệ | Tích lũy |
|:--|:-:|:-:|:-:|:-:|
| Comp1 | 4.37394 | 3.75076 | 0.7290 | 0.7290 |
| Comp2 | 0.623174 | 0.158574 | 0.1039 | 0.8329 |
| Comp3 | 0.4646 | 0.172583 | 0.0774 | 0.9103 |
| Comp4 | 0.292017 | 0.150057 | 0.0487 | 0.9590 |
| Comp5 | 0.14196 | 0.0376478 | 0.0237 | 0.9826 |
| Comp6 | 0.104312 | . | 0.0174 | 1.0000 |

Phần B. Vector riêng (trọng số thành phần) và hệ số KMO

| Biến | Comp1 | Comp2 | Comp3 | Comp4 | Comp5 | Comp6 | KMO |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| CC | 0.4274 | −0.0486 | −0.1788 | −0.7355 | −0.1878 | 0.4546 | 0.8749 |
| GE | 0.4230 | −0.4260 | −0.1942 | 0.0975 | 0.7684 | −0.0445 | 0.8428 |
| PV | 0.3534 | 0.6713 | −0.5414 | 0.3502 | 0.0018 | 0.0938 | 0.9353 |
| RQ | 0.4116 | −0.4465 | 0.1115 | 0.5410 | −0.4985 | 0.2784 | 0.8420 |
| RL | 0.4556 | −0.0066 | 0.0268 | −0.1829 | −0.2724 | −0.8270 | 0.8360 |
| VA | 0.3694 | 0.4075 | 0.7900 | 0.0273 | 0.2272 | 0.1450 | 0.8909 |
| Tổng thể | | | | | | | 0.8632 |

Ghi chú: IQ_PCA là điểm của thành phần thứ nhất (lệnh predict, score): trung bình 0, độ lệch chuẩn 2.0914, nhỏ nhất −6.2943, lớn nhất 5.8043. Số quan sát: 1,533.

Nguồn: Tác giả tổng hợp từ kết quả lệnh pca, estat kmo và summarize trên phần mềm Stata.

### Phụ lục PL2. Kết quả ước lượng System GMM

| Biến | Hệ số | Sai số chuẩn | t | P>\|t\| | KTC 95% (dưới) | KTC 95% (trên) |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| L.lnCO2 | 1.0051 | 0.0459 | 21.91 | 0.000 | 0.9136 | 1.0965 |
| FDI | 0.0055 | 0.0025 | 2.23 | 0.029 | 0.0006 | 0.0104 |
| lnY | 0.1476 | 0.0884 | 1.67 | 0.099 | −0.0287 | 0.3239 |
| URB | −0.0060 | 0.0030 | −2.02 | 0.047 | −0.0119 | −0.0001 |
| TO | −0.0007 | 0.0004 | −1.57 | 0.120 | −0.0016 | 0.0002 |
| Crdt | −0.0013 | 0.0010 | −1.30 | 0.199 | −0.0033 | 0.0007 |
| yr2 | 0.0274 | 0.0159 | 1.73 | 0.089 | −0.0042 | 0.0590 |
| yr3 | 0.0016 | 0.0154 | 0.10 | 0.920 | −0.0292 | 0.0323 |
| yr4 | 0.0059 | 0.0182 | 0.32 | 0.748 | −0.0304 | 0.0422 |
| yr6 | −0.0100 | 0.0176 | −0.57 | 0.572 | −0.0452 | 0.0251 |
| yr7 | −0.0156 | 0.0201 | −0.78 | 0.440 | −0.0557 | 0.0245 |
| yr8 | −0.0219 | 0.0182 | −1.20 | 0.234 | −0.0582 | 0.0145 |
| yr9 | 0.0330 | 0.0169 | 1.95 | 0.056 | −0.0008 | 0.0667 |
| yr10 | 0.0094 | 0.0154 | 0.61 | 0.543 | −0.0213 | 0.0401 |
| yr11 | 0.0090 | 0.0179 | 0.50 | 0.618 | −0.0267 | 0.0446 |
| yr12 | −0.0046 | 0.0178 | −0.26 | 0.796 | −0.0400 | 0.0308 |
| yr13 | 0.0144 | 0.0209 | 0.69 | 0.492 | −0.0272 | 0.0561 |
| yr14 | 0.0043 | 0.0196 | 0.22 | 0.826 | −0.0347 | 0.0434 |
| yr15 | 0.0147 | 0.0177 | 0.83 | 0.410 | −0.0206 | 0.0499 |
| yr16 | −0.0001 | 0.0177 | −0.00 | 0.997 | −0.0353 | 0.0351 |
| yr17 | −0.0009 | 0.0152 | −0.06 | 0.952 | −0.0311 | 0.0293 |
| yr18 | 0.0117 | 0.0162 | 0.72 | 0.474 | −0.0207 | 0.0440 |
| yr19 | −0.0496 | 0.0190 | −2.61 | 0.011 | −0.0876 | −0.0117 |
| yr20 | 0.0481 | 0.0189 | 2.54 | 0.013 | 0.0103 | 0.0858 |
| yr21 | 0.0113 | 0.0209 | 0.54 | 0.592 | −0.0304 | 0.0529 |
| Hằng số | −0.7498 | 0.5679 | −1.32 | 0.191 | −1.8819 | 0.3823 |

| Thông tin và kiểm định | Kết quả |
|:--|:--|
| Số quan sát / số quốc gia | 1,460 / 73 |
| Số biến công cụ | 33 |
| F(25, 72) | 1528.42 (Prob > F = 0.000) |
| Arellano–Bond AR(1) | z = −4.80; Pr > z = 0.000 |
| Arellano–Bond AR(2) | z = −1.38; Pr > z = 0.169 |
| Sargan chi2(7) | 10.15; Prob > chi2 = 0.180 |
| Hansen chi2(7) | 6.08; Prob > chi2 = 0.531 |
| Difference-in-Hansen (GMM cho phương trình mức) | chi2(3) = 3.28; Prob > chi2 = 0.351 |
| Cận của hệ số biến trễ | Pooled OLS động: 0.9823 (cận trên); FE động: 0.8234 (cận dưới) |

Ghi chú: System GMM hai bước (twostep robust small), sai số chuẩn hiệu chỉnh. Biến công cụ GMM: L.lnCO2 với độ trễ 1–3, FDI và lnY với độ trễ 2–3 (collapse); URB, TO, Crdt và biến giả năm là biến công cụ chuẩn. yr5 bị loại do đa cộng tuyến; Stata cảnh báo ma trận hiệp phương sai của các điều kiện mômen ở bước hai suy biến và dùng nghịch đảo tổng quát. Hệ số và khoảng tin cậy làm tròn đến bốn chữ số thập phân; t, P>|t| và các thống kê kiểm định giữ như output.

Nguồn: Tác giả tổng hợp từ kết quả lệnh xtabond2 trên phần mềm Stata.

## Tài liệu được trích dẫn trong Chương 4 (chuyển vào danh mục Tài liệu tham khảo)

Antweiler, W., Copeland, B. R., & Taylor, M. S. (2001). Is free trade good for the environment? *American Economic Review, 91*(4), 877–908.

Bakhsh, S., Yin, H., & Shabir, M. (2021). Foreign investment and CO2 emissions: Do technological innovation and institutional quality matter? Evidence from system GMM approach. *Environmental Science and Pollution Research, 28*(15), 19424–19438.

Bond, S. R. (2002). Dynamic panel data models: A guide to micro data methods and practice. *Portuguese Economic Journal, 1*(2), 141–162.

Cameron, A. C., & Miller, D. L. (2015). A practitioner’s guide to cluster-robust inference. *Journal of Human Resources, 50*(2), 317–372.

Copeland, B. R., & Taylor, M. S. (2004). Trade, growth, and the environment. *Journal of Economic Literature, 42*(1), 7–71.

Drukker, D. M. (2003). Testing for serial correlation in linear panel-data models. *The Stata Journal, 3*(2), 168–177.

Gelman, A., & Stern, H. (2006). The difference between “significant” and “not significant” is not itself statistically significant. *The American Statistician, 60*(4), 328–331.

Granger, C. W. J., & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics, 2*(2), 111–120.

Grossman, G. M., & Krueger, A. B. (1995). Economic growth and the environment. *The Quarterly Journal of Economics, 110*(2), 353–377.

Gujarati, D. N., & Porter, D. C. (2009). *Basic Econometrics* (5th ed.). New York: McGraw-Hill/Irwin.

Hoechle, D. (2007). Robust standard errors for panel regressions with cross-sectional dependence. *The Stata Journal, 7*(3), 281–312.

Im, K. S., Pesaran, M. H., & Shin, Y. (2003). Testing for unit roots in heterogeneous panels. *Journal of Econometrics, 115*(1), 53–74.

Kaufmann, D., Kraay, A., & Mastruzzi, M. (2011). The Worldwide Governance Indicators: Methodology and analytical issues. *Hague Journal on the Rule of Law, 3*(2), 220–246.

Lau, L. S., Choong, C. K., & Eng, Y. K. (2014). Carbon dioxide emission, institutional quality, and economic growth: Empirical evidence in Malaysia. *Renewable Energy, 68*, 276–281.

North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge: Cambridge University Press.

OECD. (2008). *OECD Benchmark Definition of Foreign Direct Investment* (4th ed.). Paris: OECD Publishing.

Pao, H. T., & Tsai, C. M. (2011). Multivariate Granger causality between CO2 emissions, energy consumption, FDI and GDP: Evidence from a panel of BRIC countries. *Energy, 36*(1), 685–693.

Pesaran, M. H. (2004). General diagnostic tests for cross section dependence in panels. *CESifo Working Paper No. 1229*.

Pesaran, M. H. (2007). A simple panel unit root test in the presence of cross-section dependence. *Journal of Applied Econometrics, 22*(2), 265–312.

Phillips, P. C. B., & Moon, H. R. (1999). Linear regression limit theory for nonstationary panel data. *Econometrica, 67*(5), 1057–1111.

Poumanyvong, P., & Kaneko, S. (2010). Does urbanization lead to less energy use and lower CO2 emissions? A cross-country analysis. *Ecological Economics, 70*(2), 434–444.

Roodman, D. (2009). How to do xtabond2: An introduction to difference and system GMM in Stata. *The Stata Journal, 9*(1), 86–136.

Shahbaz, M., Nasreen, S., Abbas, F., & Anis, O. (2015). Does foreign direct investment impede environmental quality in high-, middle-, and low-income countries? *Energy Economics, 51*, 275–287.

Sheather, S. J. (2009). *A Modern Approach to Regression with R*. New York: Springer.

Westerlund, J. (2005). New simple tests for panel cointegration. *Econometric Reviews, 24*(3), 297–316.

Zarsky, L. (1999). Havens, halos and spaghetti: Untangling the evidence about foreign direct investment and the environment. In *Foreign Direct Investment and the Environment* (pp. 47–74). Paris: OECD.

Zhu, H., Duan, L., Guo, Y., & Yu, K. (2016). The effects of FDI, economic growth and energy consumption on carbon emissions in ASEAN-5: Evidence from panel quantile regression. *Economic Modelling, 58*, 237–248.
