import tkinter as tk
import requests

def send_push(event=None):  # event参数用于处理事件绑定
    # 获取输入框中的内容
    new_copy = entry.get().strip()  # 去除可能的空白字符

    # 检查内容是否为空
    if not new_copy:
        status_label.config(text="请输入内容后再发送")
        return

    # 构建推送的 URL
    base_url = 'barkurl'
    url = f'{base_url}{new_copy}'

    # 发送推送
    response = requests.get(url)

    if response.status_code == 200:
        status_label.config(text="推送信息成功发送！")
    else:
        status_label.config(text=f"发送失败，错误码: {response.status_code}")

# 创建主窗口
root = tk.Tk()
root.title("推送信息")

# 输入框
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

# 绑定整个窗口的<Return>事件
root.bind('<Return>', send_push)

# 发送按钮
send_button = tk.Button(root, text="发送", command=send_push)
send_button.pack(padx=10, pady=5)

# 显示发送状态
status_label = tk.Label(root, text="")
status_label.pack(padx=10, pady=5)

# 启动主循环
root.mainloop()
