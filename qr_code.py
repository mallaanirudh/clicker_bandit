import qrcode

data = "https://mallaanirudh-clicker-bandit-app-hap4ud.streamlit.app/"
img = qrcode.make(data)
img.save("clicker_bandit_qr.png")
