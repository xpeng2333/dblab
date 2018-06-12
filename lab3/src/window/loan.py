import tkinter as tk
from tkinter import ttk
from db import dbop
import tkinter.messagebox
from SQl.sql import *


def loanWindow():
    loanTop = tk.Toplevel(width=900, height=550)
    loanTop.title(string='loanTop')
    loanTop.resizable(False, False)
    addDataBtn = tk.Button(loanTop, text='新建', height=4, width=10)
    addDataBtn.place(x=40, y=40)
    attrCombo = ttk.Combobox(
        loanTop, width=14, state='readonly')
    attrCombo['values'] = ('贷款号', '支行名', '总金额', '当前状态')
    attrCombo.place(x=220, y=20)
    attrCombo.current(0)
    conditionEntry = tk.Entry(loanTop, width=30)
    conditionEntry.place(x=380, y=20)
    cacheBtn = tk.Button(loanTop, text='添加', width=10)
    cacheBtn.place(x=650, y=20)
    searchBtn = tk.Button(loanTop, text='查找', width=10)
    searchBtn.place(x=750, y=20)
    conditionList = tk.Listbox(loanTop, width=52, height=5)
    conditionList.place(x=220, y=50)
    tree = ttk.Treeview(loanTop, height=13, columns=(
        'loanID', 'branchName', 'balance', 'status'))
    tree.column('loanID', width=200, anchor='center')
    tree.column('branchName', width=300, anchor='center')
    tree.column('balance', width=150, anchor='center')
    tree.column('status', width=150, anchor='center')
    tree.heading('loanID', text='贷款号')
    tree.heading('branchName', text='支行名')
    tree.heading('balance', text='总金额')
    tree.heading('status', text='当前状态')
    tree["show"] = "headings"
    tree.place(x=40, y=200)
    # loanTop.overrideredirect(1)

    def addData():
        newTop = tk.Toplevel(loanTop, width=660, height=300)
        newTop.resizable(False, False)
        newTop.overrideredirect(1)
        label1 = tk.Label(newTop, text='贷款号')
        label1.place(x=40, y=50)
        entry1 = tk.Entry(newTop, width=20)
        entry1.place(x=40, y=100)
        label2 = tk.Label(newTop, text='支行名')
        label2.place(x=140, y=50)
        entry2 = tk.Entry(newTop, width=30)
        entry2.place(x=140, y=100)
        label3 = tk.Label(newTop, text='总金额')
        label3.place(x=290, y=50)
        entry3 = tk.Entry(newTop, width=10)
        entry3.place(x=290, y=100)
        label4 = tk.Label(newTop, text='客户')
        label4.place(x=340, y=50)
        entry4 = tk.Entry(newTop, width=20)
        entry4.place(x=340, y=100)
        label5 = tk.Label(newTop, text='银行负责人')
        label5.place(x=440, y=50)
        entry5 = tk.Entry(newTop, width=20)
        entry5.place(x=440, y=100)
        confirmBtn = tk.Button(newTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(newTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            loanID = entry1.get().strip()
            branchName = entry2.get().strip()
            balance = entry3.get().strip()
            client = entry4.get().strip()
            staff = entry5.get().strip()
            sql1 = "insert into bank.共有(`贷款号`,`客户身份证号`) values(%s,%s);"
            sql2 = "insert into bank.负责(`员工身份证号`,`客户身份证号`,`负责人类型`) values(%s,%s,%s);"
            sql3 = "insert into bank.贷款(`贷款号`,`支行名`,`总金额`) values(%s,%s,%s);"
            try:
                connLoan.execCommit(sql3, (loanID, branchName, balance))
                connLoan.execCommit(sql1, (loanID, client))
                connLoan.execCommit(sql2, (staff, client, "贷款负责人_"+loanID))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror(
                    "警告", "无法添加 %s,%s,%s！" % (loanID, branchName, balance))
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
            sql = "select * from bank.贷款;"
        else:
            sql = genSQL("贷款", rawCondition)
        alldata = connLoan.execSQL(sql, None)
        while True:
            item = alldata.fetchone()
            if not item:
                break
            print(item)
            tree.insert('', 'end', values=item)

    def removeCondition(*args):
        conditionList.delete(conditionList.curselection()[0])

    def removeData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        if(data[3] == '发放中'):
            tk.messagebox.showerror("警告", "发放中贷款无法删除！")
            return
        sql1 = 'delete from bank.贷款 where `贷款号`=%s'
        sql2 = 'delete from bank.共有 where `贷款号`=%s'
        sql3 = 'delete from bank.负责 where `客户身份证号`=%s and `负责人类型`=%s'
        sql2_1 = 'select `客户身份证号` from bank.共有 where `贷款号`=%s'
        try:
            clinets = connLoan.execSQL(sql2_1, data[0])
            while True:
                client = clinets.fetchone()
                if not client:
                    break
                connLoan.execCommit(sql3, (client, '贷款负责人_'+data[0]))
            connLoan.execCommit(sql2, data[0])
            connLoan.execCommit(sql1, data[0])
            tree.delete(tree.selection())
        except Exception as e:
            tk.messagebox.showerror("警告", "无法删除！")
            print("Fail", e)

    def editData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        editTop = tk.Toplevel(loanTop, width=660, height=300)
        editTop.resizable(False, False)
        editTop.overrideredirect(1)
        label1 = tk.Label(editTop, text='贷款号')
        label1.place(x=100, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(editTop, width=30, textvariable=text1)
        entry1.place(x=60, y=100)
        label2 = tk.Label(editTop, text='支行名')
        label2.place(x=350, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(editTop, width=18, textvariable=text2)
        entry2.place(x=300, y=100)
        label3 = tk.Label(editTop, text='总金额')
        label3.place(x=500, y=50)
        text3 = tk.StringVar()
        entry3 = tk.Entry(editTop, width=18, textvariable=text3)
        entry3.place(x=450, y=100)
        confirmBtn = tk.Button(editTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(editTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            loanID = entry1.get().strip()
            branchName = entry2.get().strip()
            balance = entry3.get().strip()
            sql = "update bank.贷款 set `贷款号`=%s,`支行名`=%s,`总金额`=%s where `贷款号`=%s and `支行名`=%s and `总金额`=%s;"
            try:
                connLoan.execCommit(sql, (loanID, branchName, balance,
                                          data[0], data[1], data[2]))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror("警告", "修改失败！")
                print("Fail", e)

        def closeWindow():
            editTop.destroy()

        text1.set(data[0])
        text2.set(data[1])
        text3.set(data[2])
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        editTop.mainloop()

    def issueLoan():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        issueTop = tk.Toplevel(loanTop, width=810, height=300)
        issueTop.resizable(False, False)
        issueTop.overrideredirect(1)
        label1 = tk.Label(issueTop, text='贷款号')
        label1.place(x=100, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(issueTop, width=30, textvariable=text1)
        entry1.place(x=60, y=100)
        label2 = tk.Label(issueTop, text='当前余额')
        label2.place(x=350, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(issueTop, width=18, textvariable=text2)
        entry2.place(x=300, y=100)
        label3 = tk.Label(issueTop, text='发放金额')
        label3.place(x=500, y=50)
        text3 = tk.StringVar()
        entry3 = tk.Entry(issueTop, width=18, textvariable=text3)
        entry3.place(x=450, y=100)
        label4 = tk.Label(issueTop, text='发放日期')
        label4.place(x=650, y=50)
        text4 = tk.StringVar()
        entry4 = tk.Entry(issueTop, width=18, textvariable=text4)
        entry4.place(x=600, y=100)
        confirmBtn = tk.Button(issueTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(issueTop, text='取消')
        cancelBtn.place(x=350, y=250)
        #########################################

        def confirmFunc():
            willIssue = float(entry3.get().strip())
            balance = float(data[2])
            issueDate = entry4.get().strip()
            if(willIssue > balance):
                tk.messagebox.showerror("警告", "余额不足！")
                return
            balance -= willIssue
            sql1 = "update bank.贷款 set `总金额`=%s,`当前状态`=%s where `贷款号`=%s;"
            sql2 = "insert into bank.支付情况(`支付日期`,`贷款号`,`支付金额`) values(%s,%s,%s);"
            sql3 = "update bank.支行 set `资产`=`资产`-%s where `支行名`=%s;"
            status = "发放中"
            if(balance == 0):
                status = "已全部发放"
            try:
                connLoan.execSQL(sql2, (issueDate, data[0], str(willIssue)))
                connLoan.execSQL(sql1, (str(balance), status, data[0]))
                connLoan.execCommit(sql3, (willIssue, data[1]))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror("警告", "发放失败！")
                print("Fail", e)

        def closeWindow():
            issueTop.destroy()

        text1.set(data[0])
        text2.set(data[2])
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        issueTop.mainloop()

    def addUser():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        adduserTop = tk.Toplevel(loanTop, width=810, height=300)
        adduserTop.resizable(False, False)
        adduserTop.overrideredirect(1)
        label1 = tk.Label(adduserTop, text='贷款号')
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
        confirmBtn = tk.Button(adduserTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(adduserTop, text='取消')
        cancelBtn.place(x=350, y=250)
        #########################################

        def confirmFunc():
            #loanID = entry1.get().strip()
            loanID = data[0]
            clientID = entry2.get().strip()
            staffID = entry3.get().strip()
            sql1 = "insert into bank.负责(`员工身份证号`,`客户身份证号`,`负责人类型`) values(%s,%s,%s);"
            sql2 = "insert into bank.共有(`贷款号`,`客户身份证号`) values(%s,%s);"
            try:
                connLoan.execSQL(sql1, (staffID, clientID, "贷款负责人_"+loanID))
                connLoan.execCommit(sql2, (loanID, clientID))
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
    rightMenu = tk.Menu(loanTop)
    rightMenu.add_command(label='编辑', command=editData)
    rightMenu.add_command(label='删除', command=removeData)
    rightMenu.add_command(label='发放贷款', command=issueLoan)
    rightMenu.add_command(label='添加贷款人', command=addUser)

    def popupmenu(event):
        try:
            rightMenu.post(event.x_root, event.y_root)
        except:
            pass

    def closePop(*args):
        rightMenu.unpost()
    connLoan = dbop.mysqlConn()
    conditionList.bind('<Button-3>', removeCondition)
    tree.bind('<Button-3>', popupmenu)
    tree.bind('<Button-1>', closePop)
    conditionList.bind('<Double-Button-1>', removeCondition)
    cacheBtn.config(command=saveCondition)
    addDataBtn.config(command=addData)
    searchBtn.config(command=seachData)
    loanTop.mainloop()
