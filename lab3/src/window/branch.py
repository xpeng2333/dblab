import tkinter as tk
from tkinter import ttk
from db import dbop
import tkinter.messagebox
from SQl.sql import *


def branchWindow():
    branchTop = tk.Toplevel(width=900, height=550)
    branchTop.title(string='branchTop')
    branchTop.resizable(False, False)
    addDataBtn = tk.Button(branchTop, text='新建', height=4, width=10)
    addDataBtn.place(x=40, y=40)
    attrCombo = ttk.Combobox(
        branchTop, width=12, state='readonly')
    attrCombo['values'] = ('支行名', '城市', '资产')
    attrCombo.place(x=220, y=20)
    attrCombo.current(0)
    conditionEntry = tk.Entry(branchTop, width=30)
    conditionEntry.place(x=380, y=20)
    cacheBtn = tk.Button(branchTop, text='添加', width=10)
    cacheBtn.place(x=650, y=20)
    searchBtn = tk.Button(branchTop, text='查找', width=10)
    searchBtn.place(x=750, y=20)
    conditionList = tk.Listbox(branchTop, width=52, height=5)
    conditionList.place(x=220, y=50)
    tree = ttk.Treeview(branchTop, height=13,
                        columns=('name', 'city', 'asset'))
    tree.column('name', width=400, anchor='center')
    tree.column('city', width=200, anchor='center')
    tree.column('asset', width=200, anchor='center')
    tree.heading('name', text='支行名')
    tree.heading('city', text='城市')
    tree.heading('asset', text='资产')
    tree["show"] = "headings"
    tree.place(x=40, y=200)

    ##########################################

    def addData():
        newTop = tk.Toplevel(branchTop, width=660, height=300)
        newTop.resizable(False, False)
        newTop.overrideredirect(1)
        label1 = tk.Label(newTop, text='支行名')
        label1.place(x=100, y=50)
        entry1 = tk.Entry(newTop, width=30)
        entry1.place(x=60, y=100)
        label2 = tk.Label(newTop, text='城市')
        label2.place(x=350, y=50)
        entry2 = tk.Entry(newTop, width=18)
        entry2.place(x=300, y=100)
        label3 = tk.Label(newTop, text='资产')
        label3.place(x=500, y=50)
        entry3 = tk.Entry(newTop, width=18)
        entry3.place(x=450, y=100)
        confirmBtn = tk.Button(newTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(newTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            branchName = entry1.get().strip()
            city = entry2.get().strip()
            asset = entry3.get().strip()
            sql = "insert into bank.支行(`支行名`,`城市`,`资产`) values(%s,%s,%s);"
            try:
                connBranch.execCommit(sql, (branchName, city, asset))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror(
                    "警告", "无法添加 %s,%s,%s！" % (branchName, city, asset))
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
            sql = "select * from bank.支行;"
        else:
            sql = genSQL("支行", rawCondition)
        alldata = connBranch.execSQL(sql, None)
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
        sql = 'delete from bank.支行 where `支行名`=%s and `城市`=%s and `资产`=%s;'
        try:
            connBranch.execCommit(sql, data)
            tree.delete(tree.selection())
        except Exception as e:
            tk.messagebox.showerror("警告", "无法删除！")
            print("Fail", e)

    def editData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        editTop = tk.Toplevel(branchTop, width=660, height=300)
        editTop.resizable(False, False)
        editTop.overrideredirect(1)
        label1 = tk.Label(editTop, text='支行名')
        label1.place(x=100, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(editTop, width=30, textvariable=text1)
        entry1.place(x=60, y=100)
        label2 = tk.Label(editTop, text='城市')
        label2.place(x=350, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(editTop, width=18, textvariable=text2)
        entry2.place(x=300, y=100)
        label3 = tk.Label(editTop, text='资产')
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
            branchName = entry1.get().strip()
            city = entry2.get().strip()
            asset = entry3.get().strip()
            sql = "update bank.支行 set `支行名`=%s,`城市`=%s,`资产`=%s where `支行名`=%s and `城市`=%s and `资产`=%s;"
            try:
                connBranch.execCommit(sql, (branchName, city, asset,
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

    rightMenu = tk.Menu(branchTop)
    rightMenu.add_command(label='编辑', command=editData)
    rightMenu.add_command(label='删除', command=removeData)

    def popupmenu(event):
        try:
            rightMenu.post(event.x_root, event.y_root)
        except:
            pass

    def closePop(*args):
        rightMenu.unpost()
    connBranch = dbop.mysqlConn()
    conditionList.bind('<Button-3>', removeCondition)
    tree.bind('<Button-3>', popupmenu)
    tree.bind('<Button-1>', closePop)
    conditionList.bind('<Double-Button-1>', removeCondition)
    cacheBtn.config(command=saveCondition)
    addDataBtn.config(command=addData)
    searchBtn.config(command=seachData)
    branchTop.mainloop()
