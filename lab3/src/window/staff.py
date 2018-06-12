import tkinter as tk
from tkinter import ttk
from db import dbop
import tkinter.messagebox
from SQl.sql import *


def staffWindow():
    staffTop = tk.Toplevel(width=900, height=550)
    staffTop.title(string='staffTop')
    staffTop.resizable(False, False)
    addDataBtn = tk.Button(staffTop, text='新建', height=4, width=10)
    addDataBtn.place(x=40, y=40)
    attrCombo = ttk.Combobox(
        staffTop, width=14, state='readonly')
    attrCombo['values'] = ('员工身份证号', '支行名', '部门经理身份证号',
                           '姓名', '电话', '家庭住址', '入职日期')
    attrCombo.place(x=220, y=20)
    attrCombo.current(0)
    conditionEntry = tk.Entry(staffTop, width=30)
    conditionEntry.place(x=380, y=20)
    cacheBtn = tk.Button(staffTop, text='添加', width=10)
    cacheBtn.place(x=650, y=20)
    searchBtn = tk.Button(staffTop, text='查找', width=10)
    searchBtn.place(x=750, y=20)
    conditionList = tk.Listbox(staffTop, width=52, height=5)
    conditionList.place(x=220, y=50)
    tree = ttk.Treeview(staffTop, height=13, columns=(
        'ID', 'branch', 'managerID', 'name', 'phone', 'address', 'joinDate'))
    tree.column('ID', width=150, anchor='center')
    tree.column('branch', width=150, anchor='center')
    tree.column('managerID', width=150, anchor='center')
    tree.column('name', width=50, anchor='center')
    tree.column('phone', width=100, anchor='center')
    tree.column('address', width=150, anchor='center')
    tree.column('joinDate', width=80, anchor='center')
    tree.heading('ID', text='员工身份证号')
    tree.heading('branch', text='支行名')
    tree.heading('managerID', text='部门经理身份证号')
    tree.heading('name', text='姓名')
    tree.heading('phone', text='电话')
    tree.heading('address', text='家庭住址')
    tree.heading('joinDate', text='入职日期')
    tree["show"] = "headings"
    tree.place(x=40, y=200)
    # staffTop.overrideredirect(1)

    def addData():
        newTop = tk.Toplevel(staffTop, width=900, height=300)
        newTop.resizable(False, False)
        newTop.overrideredirect(1)
        label1 = tk.Label(newTop, text='员工身份证号')
        label1.place(x=40, y=50)
        entry1 = tk.Entry(newTop, width=18)
        entry1.place(x=40, y=100)
        label2 = tk.Label(newTop, text='支行名')
        label2.place(x=190, y=50)
        entry2 = tk.Entry(newTop, width=18)
        entry2.place(x=190, y=100)
        label3 = tk.Label(newTop, text='部门经理身份证号')
        label3.place(x=340, y=50)
        entry3 = tk.Entry(newTop, width=18)
        entry3.place(x=340, y=100)
        label4 = tk.Label(newTop, text='姓名')
        label4.place(x=490, y=50)
        entry4 = tk.Entry(newTop, width=6)
        entry4.place(x=490, y=100)
        label5 = tk.Label(newTop, text='电话')
        label5.place(x=540, y=50)
        entry5 = tk.Entry(newTop, width=12)
        entry5.place(x=540, y=100)
        label6 = tk.Label(newTop, text='家庭住址')
        label6.place(x=640, y=50)
        entry6 = tk.Entry(newTop, width=18)
        entry6.place(x=640, y=100)
        label7 = tk.Label(newTop, text='入职日期')
        label7.place(x=790, y=50)
        entry7 = tk.Entry(newTop, width=12)
        entry7.place(x=790, y=100)
        confirmBtn = tk.Button(newTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(newTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            ID = entry1.get().strip()
            branch = entry2.get().strip()
            managerID = entry3.get().strip()
            name = entry4.get().strip()
            phone = entry5.get().strip()
            address = entry6.get().strip()
            joinDate = entry7.get().strip()
            sql = "insert into bank.员工(`员工身份证号`,`支行名`,`部门经理身份证号`,`姓名`,`电话`,`家庭住址`,`入职日期`) values(%s,%s,%s,%s,%s,%s,%s);"
            try:
                conn.execCommit(sql, (ID, branch, managerID,
                                      name, phone, address, joinDate))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror(
                    "警告", "无法添加 %s,%s,%s,%s,%s,%s,%s！" % (ID, branch, managerID, name, phone, address, joinDate))
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
            sql = "select * from bank.员工;"
        else:
            sql = genSQL("员工", rawCondition)
        alldata = conn.execSQL(sql, None)
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
        sql = "delete from bank.员工 where `员工身份证号`=%s and `支行名`=%s and `部门经理身份证号`=%s and `姓名`=%s and `电话`=%s and `家庭住址`=%s and `入职日期`=%s;"
        try:
            conn.execCommit(sql, data)
            tree.delete(tree.selection())
        except Exception as e:
            tk.messagebox.showerror("警告", "无法删除！")
            print("Fail", e)

    def editData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        editTop = tk.Toplevel(staffTop, width=900, height=300)
        editTop.resizable(False, False)
        editTop.overrideredirect(1)
        label1 = tk.Label(editTop, text='员工身份证号')
        label1.place(x=40, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(editTop, width=18, textvariable=text1)
        entry1.place(x=40, y=100)
        label2 = tk.Label(editTop, text='支行名')
        label2.place(x=190, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(editTop, width=18, textvariable=text2)
        entry2.place(x=190, y=100)
        label3 = tk.Label(editTop, text='部门经理身份证号')
        label3.place(x=340, y=50)
        text3 = tk.StringVar()
        entry3 = tk.Entry(editTop, width=18, textvariable=text3)
        entry3.place(x=340, y=100)
        label4 = tk.Label(editTop, text='姓名')
        label4.place(x=490, y=50)
        text4 = tk.StringVar()
        entry4 = tk.Entry(editTop, width=6, textvariable=text4)
        entry4.place(x=490, y=100)
        label5 = tk.Label(editTop, text='电话')
        label5.place(x=540, y=50)
        text5 = tk.StringVar()
        entry5 = tk.Entry(editTop, width=12, textvariable=text5)
        entry5.place(x=540, y=100)
        label6 = tk.Label(editTop, text='家庭住址')
        label6.place(x=640, y=50)
        text6 = tk.StringVar()
        entry6 = tk.Entry(editTop, width=18, textvariable=text6)
        entry6.place(x=640, y=100)
        label7 = tk.Label(editTop, text='入职日期')
        label7.place(x=790, y=50)
        text7 = tk.StringVar()
        entry7 = tk.Entry(editTop, width=12, textvariable=text7)
        entry7.place(x=790, y=100)
        confirmBtn = tk.Button(editTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(editTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            ID = entry1.get().strip()
            branch = entry2.get().strip()
            managerID = entry3.get().strip()
            name = entry4.get().strip()
            phone = entry5.get().strip()
            address = entry6.get().strip()
            joinDate = entry7.get().strip()
            sql = "update bank.员工 set `员工身份证号`=%s,`支行名`=%s,  `部门经理身份证号`=%s ,`姓名`=%s , `电话`=%s , `家庭住址`=%s , `入职日期`=%s where `员工身份证号`=%s and `支行名`=%s and `部门经理身份证号`=%s and `姓名`=%s and `电话`=%s and `家庭住址`=%s and `入职日期`=%s;"
            try:
                conn.execCommit(sql, (ID, branch, managerID, name, phone, address, joinDate,
                                      data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
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
        text6.set(data[5])
        text7.set(data[6])
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        editTop.mainloop()
    rightMenu = tk.Menu(staffTop)
    rightMenu.add_command(label='编辑', command=editData)
    rightMenu.add_command(label='删除', command=removeData)

    def popupmenu(event):
        try:
            rightMenu.post(event.x_root, event.y_root)
        except:
            pass

    def closePop(*args):
        rightMenu.unpost()
    conn = dbop.mysqlConn()
    conditionList.bind('<Button-3>', removeCondition)
    tree.bind('<Button-3>', popupmenu)
    tree.bind('<Button-1>', closePop)
    conditionList.bind('<Double-Button-1>', removeCondition)
    cacheBtn.config(command=saveCondition)
    addDataBtn.config(command=addData)
    searchBtn.config(command=seachData)
    staffTop.mainloop()
