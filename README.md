# Orb_Controller
# DID:
- Đã lấy được thông tin của mỗi IP
- Đã ping được trong 1 amount of time
- Lưu trữ các thông tin về từng ping một trong dict
- Đã vẽ được graph cho từng IP một với y-axis là speed của từng ping,
    x-axis là thời gian đi và đến của từng ping
- Thực hiện flag: -g --> hiển thị graph, -a --> hiển thị table
- Hiển thị data của nhiều ping lên bokeh bằng nhiều graph (khả năng cái này được rồi)
- giãn cái ping ra, kiểu 5 phút gửi một lần (khả năng làm cái flag)
# TO-DO:
- nếu có khoảng nào mà hiệu uptime nó âm, tạo Warning
- add thêm tool convert từ rgb sang màu --> hiển thị ra một Link để bấm vào hoặc hover ra màu
- Đổi size của plot:
https://www.youtube.com/watch?v=rHtQDLRb5O8#:~:text=Bokeh's%20Plot%20objects%20have%20various,calling%20the%20figure()%20function.
- Sau khi đã xong hết nghiên cứu xem có thể thu được live data không.
- Dùng poetry