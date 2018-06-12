import tkinter as tk
from tkinter import ttk
from db import dbop
import tkinter.messagebox
from SQl.sql import *


def accountWindow():
    accountTop = tk.Toplevel(width=900, height=550)
    accountTop.title(string='accountTop')
    accountTop.resizable(False, False)
    addDataBtn = tk.Button(accountTop, text='新建', height=4, width=10)
    addDataBtn.place(x=40, y=40)
    attrCombo = ttk.Combobox(
        accountTop, width=14, state='readonly')
    attrCombo['values'] = ('账户号', '账户类型', '支行名', '余额', '开户日期',
                           '最近访问日期', '利率', '货币类型', '透支额')
    attrCombo.place(x=220, y=20)
    attrCombo.current(0)
    conditionEntry = tk.Entry(accountTop, width=30)
    conditionEntry.place(x=380, y=20)
    cacheBtn = tk.Button(accountTop, text='添加', width=10)
    cacheBtn.place(x=650, y=20)
    searchBtn = tk.Button(accountTop, text='查找', width=10)
    searchBtn.place(x=750, y=20)
    conditionList = tk.Listbox(accountTop, width=52, height=5)
    conditionList.place(x=220, y=50)
    tree = ttk.Treeview(accountTop, height=13, columns=(
        'accountID', 'type', 'balance', 'createDate', 'creator', 'lastVisit', 'rate', 'currencyType', 'overdraft'))
    tree.column('accountID', width=100, anchor='center')
    tree.column('type', width=70, anchor='center')
    tree.column('balance', width=50, anchor='center')
    tree.column('createDate', width=100, anchor='center')
    tree.column('creator', width=150, anchor='center')
    tree.column('lastVisit', width=100, anchor='center')
    tree.column('rate', width=50, anchor='center')
    tree.column('currencyType', width=70, anchor='center')
    tree.column('overdraft', width=100, anchor='center')
    tree.heading('accountID', text='账户号')
    tree.heading('type', text='账户类型')
    tree.heading('balance', text='余额')
    tree.heading('createDate', text='开户日期')
    tree.heading('creator', text='支行名')
    tree.heading('lastVisit', text='最近访问日期')
    tree.heading('rate', text='利率')
    tree.heading('currencyType', text='货币类型')
    tree.heading('overdraft', text='透支额')
    tree["show"] = "headings"
    tree.place(x=40, y=200)
    # accountTop.overrideredirect(1)

    def addData():
        newTop = tk.Toplevel(accountTop, width=1050, height=300)
        newTop.resizable(False, False)
        newTop.overrideredirect(1)
        accountFlag = tk.BooleanVar()
        accountFlag.set(True)
        tk.Radiobutton(newTop, variable=accountFlag, text='储蓄账户',
                       value=True).place(x=240, y=10)
        tk.Radiobutton(newTop, variable=accountFlag, text='支票账户',
                       value=False).place(x=480, y=10)
        label1 = tk.Label(newTop, text='账户号')
        label1.place(x=40, y=50)
        entry1 = tk.Entry(newTop, width=8)
        entry1.place(x=40, y=100)
        label2 = tk.Label(newTop, text='余额')
        label2.place(x=120, y=50)
        entry2 = tk.Entry(newTop, width=12)
        entry2.place(x=120, y=100)
        label3 = tk.Label(newTop, text='开户日期')
        label3.place(x=240, y=50)
        entry3 = tk.Entry(newTop, width=12)
        entry3.place(x=240, y=100)
        label4 = tk.Label(newTop, text='支行名')
        label4.place(x=360, y=50)
        entry4 = tk.Entry(newTop, width=12)
        entry4.place(x=360, y=100)
        label5 = tk.Label(newTop, text='利率')
        label5.place(x=480, y=50)
        entry5 = tk.Entry(newTop, width=12)
        entry5.place(x=480, y=100)
        label6 = tk.Label(newTop, text='货币类型')
        label6.place(x=600, y=50)
        entry6 = tk.Entry(newTop, width=8)
        entry6.place(x=600, y=100)
        label7 = tk.Label(newTop, text='透支额')
        label7.place(x=680, y=50)
        entry7 = tk.Entry(newTop, width=8)
        entry7.place(x=680, y=100)
        label8 = tk.Label(newTop, text='客户')
        label8.place(x=760, y=50)
        entry8 = tk.Entry(newTop, width=12)
        entry8.place(x=760, y=100)
        label9 = tk.Label(newTop, text='负责人')
        label9.place(x=880, y=50)
        entry9 = tk.Entry(newTop, width=12)
        entry9.place(x=880, y=100)
        confirmBtn = tk.Button(newTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(newTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            if(accountFlag.get()):
                accountType = "储蓄账户"
                accountID = entry1.get().strip()
                balance = entry2.get().strip()
                createDate = entry3.get().strip()
                branchName = entry4.get().strip()
                rate = entry5.get().strip()
                currencyType = entry6.get().strip()
                overdraft = entry7.get().strip()
                client = entry8.get().strip()
                staff = entry9.get().strip()
                sql1 = "insert into bank.账户(`账户号`,`支行名`,`余额`,`开户日期`) values(%s,%s,%s,%s);"
                sql2 = "insert into bank.储蓄账户(`账户号`,`支行名`,`余额`,`开户日期`,`利率`,`货币类型`) values(%s,%s,%s,%s,%s,%s);"
                sql3 = "insert into bank.拥有(`客户身份证号`,`账户号`,`最近访问日期`) values(%s,%s,%s);"
                sql4 = "insert into bank.负责(`员工身份证号`,`客户身份证号`,`负责人类型`) values(%s,%s,%s);"
                sql5 = "update bank.支行 set `资产`=`资产`+%s where `支行名`=%s;"
                try:
                    connAccount.execSQL(
                        sql1, (accountID, branchName, balance, createDate))
                    connAccount.execSQL(sql2, (accountID, branchName, balance, createDate,
                                               rate, currencyType))
                    connAccount.execSQL(sql3, (client, accountID, createDate))
                    connAccount.execSQL(
                        sql4, (staff, client, "银行账户负责人_"+accountID))
                    connAccount.execCommit(sql5, (balance, branchName))
                    closeWindow()
                except Exception as e:
                    tk.messagebox.showerror(
                        "警告", "无法添加 %s,%s,%s,%s,%s,%s,%s！" % (accountID, accountType, balance, createDate, branchName, rate, currencyType))
                    print("Fail", e)
            else:
                accountType = "支票账户"
                accountID = entry1.get().strip()
                balance = entry2.get().strip()
                createDate = entry3.get().strip()
                branchName = entry4.get().strip()
                rate = entry5.get().strip()
                currencyType = entry6.get().strip()
                overdraft = entry7.get().strip()
                client = entry8.get().strip()
                staff = entry9.get().strip()
                sql1 = "insert into bank.账户(`账户号`,`支行名`,`余额`,`开户日期`) values(%s,%s,%s,%s);"
                sql2 = "insert into bank.支票账户(`账户号`,`支行名`,`余额`,`开户日期`,`利率`,`货币类型`,`透支额`) values(%s,%s,%s,%s,%s,%s,%s);"
                sql3 = "insert into bank.拥有(`客户身份证号`,`账户号`,`最近访问日期`) values(%s,%s,%s);"
                sql4 = "insert into bank.负责(`员工身份证号`,`客户身份证号`,`负责人类型`) values(%s,%s,%s);"
                sql5 = "update bank.支行 set `资产`=`资产`+%s where `支行名`=%s;"
                try:
                    connAccount.execSQL(
                        sql1, (accountID, branchName, balance, createDate))
                    connAccount.execSQL(
                        sql2, (accountID, branchName, balance, createDate, rate, currencyType, overdraft))
                    connAccount.execSQL(sql3, (client, accountID, createDate))
                    connAccount.execSQL(
                        sql4, (staff, client, "银行账户负责人_"+accountID))
                    connAccount.execCommit(sql5, (balance, branchName))
                    closeWindow()
                except Exception as e:
                    tk.messagebox.showerror(
                        "警告", "无法添加 %s,%s,%s,%s,%s,%s！" % (accountID, accountType, balance, createDate, branchName, overdraft))
                    print("Fail", e)

        def closeWindow():
            newTop.destroy()
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        newTop.mainloop()

    def saveCondition():
        attr = attrCombo.get()
        condition = conditionEntry.get().strip()
        conditionList.insert('end', attr+':'+condition)

    def seachData():
        olditems = tree.get_children()
        [tree.delete(olditem) for olditem in olditems]
        rawCondition = conditionList.get(0, 'end')
        if len(rawCondition) == 0:
            sql1 = "select * from bank.储蓄账户;"
            sql2 = "select * from bank.支票账户;"
        else:
            sql1 = genSQL("储蓄账户", rawCondition)
            sql2 = genSQL("支票账户", rawCondition)
        try:
            alldata1 = connAccount.execSQL(sql1, None)
        except:
            alldata1 = False
        if(alldata1 != False):
            for item in alldata1.fetchall():
                print(item)
                tmp = connAccount.execSQL(
                    "select * from bank.拥有 where `账户号`=%s;", item[0])
                tmpdata = tmp.fetchall()[0]
                tree.insert('', 'end', values=(
                    item[0], "储蓄账户", item[2], item[3], item[1], tmpdata[2], item[4], item[5], "/"))
        try:
            alldata2 = connAccount.execSQL(sql2, None)
        except:
            alldata2 = False

        if(alldata1 != False):
            for item in alldata1.fetchall():
                print(item)
                tmp = connAccount.execSQL(
                    "select * from bank.拥有 where `账户号`=%s;", item[0])
                tmpdata = tmp.fetchall()[0]
                tree.insert('', 'end', values=(
                    item[0], "支票账户", item[2], item[3], item[1], tmpdata[2], item[4], item[5], item[6]))

    def removeCondition(*args):
        conditionList.delete(conditionList.curselection()[0])

    def removeData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        sql1 = "delete from bank.账户 where `账户号`=%s;"
        sql2 = "delete from bank.储蓄账户 where `账户号`=%s;"
        sql3 = "delete from bank.支票账户 where `账户号`=%s;"
        sql4 = "delete from bank.拥有 where `账户号`=%s;"
        sql5 = "delete from bank.负责 where `负责人类型`=%s;"
        try:
            connAccount.execSQL(sql2, data[0])
            connAccount.execSQL(sql3, data[0])
            connAccount.execSQL(sql1, data[0])
            connAccount.execSQL(sql4, data[0])
            connAccount.execCommit(sql5, "银行账户负责人_"+data[0])
            tree.delete(tree.selection())
        except Exception as e:
            tk.messagebox.showerror("警告", "无法删除！")
            print("Fail", e)

    def editData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        editTop = tk.Toplevel(accountTop, width=900, height=300)
        editTop.resizable(False, False)
        editTop.overrideredirect(1)
        label1 = tk.Label(editTop, text='账户号')
        label1.place(x=40, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(editTop, width=18, textvariable=text1)
        entry1.place(x=40, y=100)
        label2 = tk.Label(editTop, text='账户类型')
        label2.place(x=190, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(editTop, width=6, textvariable=text2)
        entry2.place(x=190, y=100)
        label3 = tk.Label(editTop, text='余额')
        label3.place(x=240, y=50)
        text3 = tk.StringVar()
        entry3 = tk.Entry(editTop, width=12, textvariable=text3)
        entry3.place(x=240, y=100)
        label4 = tk.Label(editTop, text='开户日期')
        label4.place(x=340, y=50)
        text4 = tk.StringVar()
        entry4 = tk.Entry(editTop, width=12, textvariable=text4)
        entry4.place(x=340, y=100)
        label5 = tk.Label(editTop, text='支行名')
        label5.place(x=440, y=50)
        text5 = tk.StringVar()
        entry5 = tk.Entry(editTop, width=18, textvariable=text5)
        entry5.place(x=440, y=100)
        label6 = tk.Label(editTop, text='利率')
        label6.place(x=590, y=50)
        text6 = tk.StringVar()
        entry6 = tk.Entry(editTop, width=12, textvariable=text6)
        entry6.place(x=590, y=100)
        label7 = tk.Label(editTop, text='货币类型')
        label7.place(x=690, y=50)
        text7 = tk.StringVar()
        entry7 = tk.Entry(editTop, width=6, textvariable=text7)
        entry7.place(x=690, y=100)
        label8 = tk.Label(editTop, text='透支额')
        label8.place(x=740, y=50)
        text8 = tk.StringVar()
        entry8 = tk.Entry(editTop, width=12, textvariable=text8)
        entry8.place(x=740, y=100)
        confirmBtn = tk.Button(editTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(editTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            accountID = entry1.get().strip()
            accountType = entry2.get().strip()
            balance = entry3.get().strip()
            createDate = entry4.get().strip()
            branchName = entry5.get().strip()
            rate = entry6.get().strip()
            currencyType = entry7.get().strip()
            overdraft = entry8.get().strip()
            if(accountType == '储蓄账户'):
                sql = "update bank.储蓄账户 set `利率`=%s , `货币类型`=%s where `账户号`='%s';"
                try:
                    connAccount.execCommit(
                        sql, (rate, currencyType, data[0]))
                    print(sql % (rate, currencyType, data[0]))
                    closeWindow()
                except Exception as e:
                    tk.messagebox.showerror("警告", "修改失败！")
                    print("Fail", e)
            else:
                sql = "update bank.支票账户 set `透支额`=%s where `账户号`=%s;"
                try:
                    connAccount.execCommit(
                        sql, (overdraft, data[0]))
                    closeWindow()
                except Exception as e:
                    tk.messagebox.showerror("警告", "修改失败！")
                    print("Fail", e)

        def closeWindow():
            editTop.destroy()

        text1.set(data[0])
        text2.set(data[1])
        text3.set(data[2])
        text4.set(data[3])
        text5.set(data[4])
        text6.set(data[6])
        text7.set(data[7])
        text8.set(data[8])
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        editTop.mainloop()

    def addUser():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        adduserTop = tk.Toplevel(accountTop, width=810, height=300)
        adduserTop.resizable(False, False)
        adduserTop.overrideredirect(1)
        label1 = tk.Label(adduserTop, text='账户号')
        label1.place(x=100, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(adduserTop, width=30, textvariable=text1)
        entry1.place(x=60, y=100)
        label2 = tk.Label(adduserTop, text='客户身份证号')
        label2.place(x=350, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(adduserTop, width=18, textvariable=text2)
        entry2.place(x=300, y=100)
        label3 = tk.Label(adduserTop, text='员工身份证号')
        label3.place(x=500, y=50)
        text3 = tk.StringVar()
        entry3 = tk.Entry(adduserTop, width=18, textvariable=text3)
        entry3.place(x=450, y=100)
        label4 = tk.Label(adduserTop, text='添加日期')
        label4.place(x=650, y=50)
        text4 = tk.StringVar()
        entry4 = tk.Entry(adduserTop, width=18, textvariable=text4)
        entry4.place(x=600, y=100)
        confirmBtn = tk.Button(adduserTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(adduserTop, text='取消')
        cancelBtn.place(x=350, y=250)
        #########################################

        def confirmFunc():
            #loanID = entry1.get().strip()
            accountID = data[0]
            clientID = entry2.get().strip()
            staffID = entry3.get().strip()
            addDate = entry4.get().strip()
            sql1 = "insert into bank.负责(`员工身份证号`,`客户身份证号`,`负责人类型`) values(%s,%s,%s);"
            sql2 = "insert into bank.拥有(`账户号`,`客户身份证号`,`最近访问日期`) values(%s,%s,%s);"
            try:
                connAccount.execSQL(
                    sql1, (staffID, clientID, "银行账户负责人_"+accountID))
                connAccount.execCommit(sql2, (accountID, clientID, addDate))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror("警告", "添加失败！")
                print("Fail", e)

        def closeWindow():
            adduserTop.destroy()
        text1.set(data[0])
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        adduserTop.mainloop()

    def saveAndget():
        pass

    rightMenu = tk.Menu(accountTop)
    rightMenu.add_command(label='编辑', command=editData)
    rightMenu.add_command(label='删除', command=removeData)
    rightMenu.add_command(label='添加客户', command=addUser)
    rightMenu.add_command(label='存取款', command=saveAndget)

    def popupmenu(event):
        try:
            rightMenu.post(event.x_root, event.y_root)
        except:
            pass

    def closePop(*args):
        rightMenu.unpost()
    connAccount = dbop.mysqlConn()
    conditionList.bind('<Button-3>', removeCondition)
    tree.bind('<Button-3>', popupmenu)
    tree.bind('<Button-1>', closePop)
    conditionList.bind('<Double-Button-1>', removeCondition)
    cacheBtn.config(command=saveCondition)
    addDataBtn.config(command=addData)
    searchBtn.config(command=seachData)
    accountTop.mainloop()
