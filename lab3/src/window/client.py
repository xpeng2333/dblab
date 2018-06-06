import tkinter as tk
from tkinter import ttk
from db import dbop
import tkinter.messagebox
from SQl.sql import *


def clientWindow():
    clientTop = tk.Toplevel(width=900, height=550)
    clientTop.title(string='clientTop')
    clientTop.resizable(False, False)
    addDataBtn = tk.Button(clientTop, text='新建', height=4, width=10)
    addDataBtn.place(x=40, y=40)
    attrCombo = ttk.Combobox(
        clientTop, width=12, state='readonly')
    attrCombo['values'] = ('客户身份证号', '姓名', '联系电话', '家庭住址',
                           '联系人姓名', '联系人手机号', '联系人email', '关系')
    attrCombo.place(x=220, y=20)
    attrCombo.current(0)
    conditionEntry = tk.Entry(clientTop, width=30)
    conditionEntry.place(x=380, y=20)
    cacheBtn = tk.Button(clientTop, text='添加', width=10)
    cacheBtn.place(x=650, y=20)
    searchBtn = tk.Button(clientTop, text='查找', width=10)
    searchBtn.place(x=750, y=20)
    conditionList = tk.Listbox(clientTop, width=52, height=5)
    conditionList.place(x=220, y=50)
    tree = ttk.Treeview(clientTop, height=13, columns=(
        'ID', 'name', 'phone', 'address', 'contacts', 'phone_c', 'email', 'relation'))
    tree.column('ID', width=150, anchor='center')
    tree.column('name', width=50, anchor='center')
    tree.column('phone', width=100, anchor='center')
    tree.column('address', width=150, anchor='center')
    tree.column('contacts', width=100, anchor='center')
    tree.column('phone_c', width=100, anchor='center')
    tree.column('email', width=100, anchor='center')
    tree.column('relation', width=50, anchor='center')
    tree.heading('ID', text='客户身份证号')
    tree.heading('name', text='姓名')
    tree.heading('phone', text='联系电话')
    tree.heading('address', text='家庭住址')
    tree.heading('contacts', text='联系人姓名')
    tree.heading('phone_c', text='联系人手机号')
    tree.heading('email', text='联系人email')
    tree.heading('relation', text='关系')
    tree["show"] = "headings"
    tree.place(x=40, y=200)
    # clientTop.overrideredirect(1)
    ############################################

    def addData():
        newTop = tk.Toplevel(clientTop, width=900, height=300)
        newTop.resizable(False, False)
        newTop.overrideredirect(1)
        label1 = tk.Label(newTop, text='客户身份证号')
        label1.place(x=40, y=50)
        entry1 = tk.Entry(newTop, width=18)
        entry1.place(x=40, y=100)
        label2 = tk.Label(newTop, text='姓名')
        label2.place(x=190, y=50)
        entry2 = tk.Entry(newTop, width=6)
        entry2.place(x=190, y=100)
        label3 = tk.Label(newTop, text='联系电话')
        label3.place(x=240, y=50)
        entry3 = tk.Entry(newTop, width=12)
        entry3.place(x=240, y=100)
        label4 = tk.Label(newTop, text='家庭住址')
        label4.place(x=340, y=50)
        entry4 = tk.Entry(newTop, width=18)
        entry4.place(x=340, y=100)
        label5 = tk.Label(newTop, text='联系人姓名')
        label5.place(x=490, y=50)
        entry5 = tk.Entry(newTop, width=12)
        entry5.place(x=490, y=100)
        label6 = tk.Label(newTop, text='联系人手机号')
        label6.place(x=590, y=50)
        entry6 = tk.Entry(newTop, width=12)
        entry6.place(x=590, y=100)
        label7 = tk.Label(newTop, text='联系人email')
        label7.place(x=690, y=50)
        entry7 = tk.Entry(newTop, width=13)
        entry7.place(x=690, y=100)
        label8 = tk.Label(newTop, text='关系')
        label8.place(x=800, y=50)
        entry8 = tk.Entry(newTop, width=5)
        entry8.place(x=800, y=100)
        confirmBtn = tk.Button(newTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(newTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            ID = entry1.get().strip()
            name = entry2.get().strip()
            phone = entry3.get().strip()
            address = entry4.get().strip()
            contacts = entry5.get().strip()
            phone_c = entry6.get().strip()
            email = entry7.get().strip()
            relation = entry8.get().strip()
            sql = "insert into bank.客户(`客户身份证号`,`姓名`,`联系电话`,`家庭住址`,`联系人姓名`,`联系人手机号`,`联系人email`,`关系`) values(%s,%s,%s,%s,%s,%s,%s,%s);"
            try:
                connClient.execCommit(sql, (ID, name, phone, address,
                                            contacts, phone_c, email, relation))
                closeWindow()
            except Exception as e:
                tk.messagebox.showerror(
                    "警告", "无法添加 %s,%s,%s,%s,%s,%s,%s,%s！" % (ID, name, phone, address, contacts, phone_c, email, relation))
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
            sql = "select * from bank.客户;"
        else:
            sql = genSQL("客户", rawCondition)
        alldata = connClient.execSQL(sql, None)
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
        sql = "delete from bank.客户 where `客户身份证号`=%s and `姓名`=%s and `联系电话`=%s and `家庭住址`=%s and `联系人姓名`=%s and `联系人手机号`=%s and `联系人email`=%s and `关系`=%s;"
        try:
            connClient.execCommit(sql, data)
            tree.delete(tree.selection())
        except Exception as e:
            tk.messagebox.showerror("警告", "无法删除！")
            print("Fail", e)

    def editData():
        item = tree.selection()[0]
        data = tree.item(item, "values")
        editTop = tk.Toplevel(clientTop, width=900, height=300)
        editTop.resizable(False, False)
        editTop.overrideredirect(1)
        label1 = tk.Label(editTop, text='客户身份证号')
        label1.place(x=40, y=50)
        text1 = tk.StringVar()
        entry1 = tk.Entry(editTop, width=18, textvariable=text1)
        entry1.place(x=40, y=100)
        label2 = tk.Label(editTop, text='姓名')
        label2.place(x=190, y=50)
        text2 = tk.StringVar()
        entry2 = tk.Entry(editTop, width=6, textvariable=text2)
        entry2.place(x=190, y=100)
        label3 = tk.Label(editTop, text='联系电话')
        label3.place(x=240, y=50)
        text3 = tk.StringVar()
        entry3 = tk.Entry(editTop, width=12, textvariable=text3)
        entry3.place(x=240, y=100)
        label4 = tk.Label(editTop, text='家庭住址')
        label4.place(x=340, y=50)
        text4 = tk.StringVar()
        entry4 = tk.Entry(editTop, width=18, textvariable=text4)
        entry4.place(x=340, y=100)
        label5 = tk.Label(editTop, text='联系人姓名')
        label5.place(x=490, y=50)
        text5 = tk.StringVar()
        entry5 = tk.Entry(editTop, width=12, textvariable=text5)
        entry5.place(x=490, y=100)
        label6 = tk.Label(editTop, text='联系人手机号')
        label6.place(x=590, y=50)
        text6 = tk.StringVar()
        entry6 = tk.Entry(editTop, width=12, textvariable=text6)
        entry6.place(x=590, y=100)
        label7 = tk.Label(editTop, text='联系人email')
        label7.place(x=690, y=50)
        text7 = tk.StringVar()
        entry7 = tk.Entry(editTop, width=13, textvariable=text7)
        entry7.place(x=690, y=100)
        label8 = tk.Label(editTop, text='关系')
        label8.place(x=800, y=50)
        text8 = tk.StringVar()
        entry8 = tk.Entry(editTop, width=5, textvariable=text8)
        entry8.place(x=800, y=100)
        confirmBtn = tk.Button(editTop, text='确认')
        confirmBtn.place(x=250, y=250)
        cancelBtn = tk.Button(editTop, text='取消')
        cancelBtn.place(x=350, y=250)
        ########################

        def confirmFunc():
            ID = entry1.get().strip()
            name = entry2.get().strip()
            phone = entry3.get().strip()
            address = entry4.get().strip()
            contacts = entry5.get().strip()
            phone_c = entry6.get().strip()
            email = entry7.get().strip()
            relation = entry8.get().strip()
            sql = "update bank.客户 set `客户身份证号`=%s , `姓名`=%s , `联系电话`=%s , `家庭住址`=%s , `联系人姓名`=%s , `联系人手机号`=%s , `联系人email`=%s , `关系`=%s where `客户身份证号`=%s and `姓名`=%s and `联系电话`=%s and `家庭住址`=%s and `联系人姓名`=%s and `联系人手机号`=%s and `联系人email`=%s and `关系`=%s;"
            try:
                connClient.execCommit(sql, (ID, name, phone, address, contacts, phone_c, email, relation,
                                            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
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
        text8.set(data[7])
        confirmBtn.config(command=confirmFunc)
        cancelBtn.config(command=closeWindow)
        editTop.mainloop()

    rightMenu = tk.Menu(clientTop)
    rightMenu.add_command(label='编辑', command=editData)
    rightMenu.add_command(label='删除', command=removeData)

    def popupmenu(event):
        try:
            rightMenu.post(event.x_root, event.y_root)
        except:
            pass

    def closePop(*args):
        rightMenu.unpost()
    connClient = dbop.mysqlConn()
    conditionList.bind('<Button-3>', removeCondition)
    tree.bind('<Button-3>', popupmenu)
    tree.bind('<Button-1>', closePop)
    conditionList.bind('<Double-Button-1>', removeCondition)
    cacheBtn.config(command=saveCondition)
    addDataBtn.config(command=addData)
    searchBtn.config(command=seachData)
    clientTop.mainloop()
