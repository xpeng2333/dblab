import tkinter as tk
from window import branch
from window import client
from window import staff
from window import account
from window import loan
from window import statistics

root = tk.Tk()
root.title(string='BANK_MANAGER')
root.geometry('800x600')
root.resizable(False, False)
name = tk.Label(root, text='银行管理系统', anchor='nw', width=200,
                height=1, justify='left', font=("", 38))
name.place(x=250, y=80)
branchMan = tk.Button(root, text='支行管理', font=('', 22), height=3, width=8)
branchMan.place(x=120, y=180)
staffMan = tk.Button(root, text='员工管理', font=('', 22), height=3, width=8)
staffMan.place(x=320, y=180)
clientMan = tk.Button(root, text='客户管理', font=('', 22), height=3, width=8)
clientMan.place(x=520, y=180)
accountMan = tk.Button(root, text='账户管理', font=('', 22), height=3, width=8)
accountMan.place(x=120, y=380)
loanMan = tk.Button(root, text='贷款管理', font=('', 22), height=3, width=8)
loanMan.place(x=320, y=380)
statisticMan = tk.Button(root, text='业务统计', font=('', 22), height=3, width=8)
statisticMan.place(x=520, y=380)
############################################################################


def banchFunc():
    branch.branchWindow()


def clientFunc():
    client.clientWindow()


def staffFunc():
    staff.staffWindow()


def accountFunc():
    account.accountWindow()


def loanFunc():
    loan.loanWindow()


def statisticFunc():
    statistics.statisticsWindow()


branchMan.config(command=banchFunc)
clientMan.config(command=clientFunc)
staffMan.config(command=staffFunc)
accountMan.config(command=accountFunc)
loanMan.config(command=loanFunc)
statisticMan.config(command=statisticFunc)
root.mainloop()
