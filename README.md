# Orb_Controller
# DID:
- Đã lấy được thông tin của mỗi IP
- Đã ping được trong 1 amount of time
- Lưu trữ các thông tin về từng ping một trong dict
# TO-DO:
- dùng poetry như build system để quản lý dependencies cho người dùng
--> auto tải dependencies cho người dùng khi chạy
- Hiển thị data lên bokeh
- Thực hiện flag: -g --> hiển thị graph, -a --> hiển thị table
- Graph sẽ có dạng: x-axis thì là khoảng thời gian 
                    từ lúc gửi đến lúc nhận ping --> string
                    y-axis thì là speed của ping
                    Nếu request timed out --> để là 0 hoặc cái gì đó khác (hiện tại đang để ip nan chưa có mục đích)
                    Point-to-point graph, khi bấm vào (hover) phải hiển thị ra các thông tin khác (ví dụ như trong info_dict)
- Table sẽ có dạng csv, bố cục dict thế nào thì trình bày table như thế
- Sau khi đã xong hết nghiên cứu xem có thể thu được live data không.