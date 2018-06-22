import tkinter as tk
from tkinter import ttk
from db import dbop
import tkinter.messagebox
from SQl.sql import *


def statisticsWindow():
    statTop = tk.Toplevel(width=900, height=550)
    statTop.title("数据分析")
    lable1 = tk.Label(statTop, text='总资产')
    lable1.place(x=130, y=30)
    text1 = tk.StringVar()
    data1 = tk.Label(statTop, textvariable=text1)
    data1.place(x=230, y=30)
    lable2 = tk.Label(statTop, text='总员工数')
    lable2.place(x=330, y=30)
    text2 = tk.StringVar()
    data2 = tk.Label(statTop, textvariable=text2)
    data2.place(x=430, y=30)
    lable3 = tk.Label(statTop, text='总客户数')
    lable3.place(x=530, y=30)
    text3 = tk.StringVar()
    data3 = tk.Label(statTop, textvariable=text3)
    data3.place(x=630, y=30)
    tree = ttk.Treeview(statTop, height=20, columns=(
        'branchName', 'asset', 'saveAccount', 'loanAccount', 'staff', 'loan'))
    tree.column('branchName', width=130, anchor='center')
    tree.column('asset', width=100, anchor='center')
    tree.column('saveAccount', width=100, anchor='center')
    tree.column('loanAccount', width=100, anchor='center')
    tree.column('staff', width=100, anchor='center')
    tree.column('loan', width=130, anchor='center')
    tree.heading('branchName', text='支行名')
    tree.heading('asset', text='资产')
    tree.heading('saveAccount', text='储蓄账户数')
    tree.heading('loanAccount', text='支票账户数')
    tree.heading('staff', text='员工数')
    tree.heading('loan', text='贷款')
    tree["show"] = "headings"
    tree.place(x=110, y=80)
    sql1 = "select `支行名`, `资产` from bank.支行;"
    sql2 = "select count(*) from bank.储蓄账户 where `支行名`=%s;"
    sql3 = "select count(*) from bank.支票账户 where `支行名`=%s;"
    sql4 = "select count(*) from bank.员工 where `支行名`=%s;"
    sql5 = "select sum(`总金额`) from bank.贷款 where `支行名`=%s;"
    sql6 = "select sum(`资产`) from bank.支行;"
    sql7 = "select count(*) from bank.客户;"
    sql8 = "select count(*) from bank.员工;"
    connStat = dbop.mysqlConn()
    allAsset = connStat.execSQL(sql6, None)
    text1.set(allAsset.fetchone())
    allClient = connStat.execSQL(sql7, None)
    text2.set(allClient.fetchone())
    allStaff = connStat.execSQL(sql8, None)
    text3.set(allStaff.fetchone())
    branchList = []
    saveAccountList = []
    loanAccountList = []
    staffList = []
    loanList = []
    getBranch = connStat.execSQL(sql1, None)
    while True:
        item = getBranch.fetchone()
        if not item:
            break
        item = list(item)
        branchList.append(item)
    for item in branchList:
        getSaveAccount = connStat.execSQL(sql2, item[0])
        while True:
            num = getSaveAccount.fetchone()
            if not num:
                break
            saveAccountList.append(num)
    for item in branchList:
        getLoanAccount = connStat.execSQL(sql3, item[0])
        while True:
            num = getLoanAccount.fetchone()
            if not num:
                break
            loanAccountList.append(num)
    for item in branchList:
        staff = connStat.execSQL(sql4, item[0])
        while True:
            num = staff.fetchone()
            if not num:
                break
            staffList.append(num)
    for item in branchList:
        getLoan = connStat.execSQL(sql5, item[0])
        while True:
            num = getLoan.fetchone()
            if not num:
                break
            loanList.append(num)
    index = 0
    for item in branchList:
        tree.insert('', 'end', values=[item[0], item[1], saveAccountList[index],
                                       loanAccountList[index], staffList[index], loanList[index]])
        index += 1
    statTop.mainloop()
