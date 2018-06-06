
def genSQL(table, rawCondition):

    sql = "select * from bank."+table+" where "
    for item in rawCondition:
        atom = item.strip().split(':')
        attr = atom[0]
        value = atom[1].split(',')
        if(len(value) != 1):
            if atom[1][0] == "(":
                sql += attr+">"+value[0][1:]+" and "
            elif atom[1][0] == "[":
                sql += attr+">="+value[0][1:]+" and "
            if atom[1][-1] == ")":
                sql += attr+"<"+value[1][:-1]+" and "
            elif atom[1][-1] == "]":
                sql += attr+"<="+value[1][:-1]+" and "
        else:
            sql += attr+"='"+value[0]+"' and "
    sql = sql[:-5]+";"
    return sql


'''
haha = ("支行名:[1,2)",)
sql = genSQL("支行", haha)
print(sql)
'''
