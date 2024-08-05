<p align="center">
  <img src="https://capsule-render.vercel.app/api?text=Orb%20Controller!🕹&animation=twinkling&type=waving&color=gradient&height=150"/>
</p>


# Orb_Controller
## Background:
Faculty at Oberlin College developed the “Environmental orb”, a colored light that glows different colors depending how much electricity and water are being used in buildings in which it is installed.  Essentially the colors and pulsing patterns of lights displayed on the orb at a given time communicate how much electricity or water is being used by a building at the present time relative to typical use at this time of day. The orb was designed to display two are two color spectra:  red → yellow → green for electricity and pink → purple → aqua for water.  Each minute, the orb receives two numbers through wifi, one for electricity and one for water,  each with one of five values: 0, 1, 2, 3, or 4.   So, for example, if electricity use in the building were at the lowest possible level of use and water consumption was at the highest possible use, the orb would be send a 0 for electricity and a 4 for water.  The orb would respond by alternating between displaying a slowly pulsing green pattern (= lowest level of electricity use) and a rapidly pulsing aqua color (= highest level of water use).  To help distinguish between the two resources, electricity is represented by a heartbeat type of pulsing pattern and water by a shimmering type of pulse.  Over the years we have used several different types of hardware devices to convert the data signal into colored lights.  


# DID:
- Đã lấy được thông tin của mỗi IP
- Đã ping được trong 1 amount of time
- Lưu trữ các thông tin về từng ping một trong dict
- Đã vẽ được graph cho từng IP một với y-axis là speed của từng ping,
    x-axis là thời gian đi và đến của từng ping
- Thực hiện flag: -g --> hiển thị graph, -a --> hiển thị table
- Hiển thị data của nhiều ping lên bokeh bằng nhiều graph (khả năng cái này được rồi)
- giãn cái ping ra, kiểu 5 phút gửi một lần (khả năng làm cái flag)
- nếu có khoảng nào mà hiệu uptime nó âm, tạo Warning
- handle việc Orb bị mất kết nối
- add thêm tool convert từ rgb sang màu --> hiển thị ra một Link để bấm vào hoặc hover ra màu
# TO-DO:
- Đổi size của plot:
https://www.youtube.com/watch?v=rHtQDLRb5O8#:~:text=Bokeh's%20Plot%20objects%20have%20various,calling%20the%20figure()%20function.
- Sau khi đã xong hết nghiên cứu xem có thể thu được live data không.
- Dùng poetry
