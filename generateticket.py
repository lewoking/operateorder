import sqlite3

#定义操作票生成方法
def transaction(args1,args2):

#连接本地sqlite3数据库
    conn = sqlite3.connect('breaklist.db',check_same_thread = False)

#为两种操作方式设置固定的匹配语句

    list_bzh = ["核对调度指令，确认与操作任务相符",
			    "合上××变××线××断路器",
                "检查××变××线××断路器监控指示为合位",
                "检查××变××线××断路器电流指示正常",
                "检查××变××线功率正常"]
    list_bzf = ["核对调度指令，确认与操作任务相符",
			    "断开××变××线××断路器",
                "检查××变××线××断路器监控指示为分位",
                "检查××变××线××断路器电流指示为零",
                "检查××变××线功率为零"]

#定义设备名称中含有以下字符的变量
 
    flag1 = '主变'
    flag2 = '#1站用变'
    flag3 = '#2站用变'
    flag4 = '#3站用变'

#传入查询的开关编号
    bh = str(args1).strip()

#查询数据库
    cur = conn.cursor()
    sql = ''.join(["select 站名||开关电压||名称,开关电压,名称,站名,编号 from 荆门开关表 ",
    "where 所属调度 in ('地调','省调','省调许可') and 编号 = ?"])
    cur.execute(sql,[bh])
    info = cur.fetchall()

#关闭数据库连接

    cur.close()
    conn.close()

#如果查询结果不为空，则执行以下语句
    
    if info:

        temp = str(info[0][0])
        temp1 = str(info[0][1])
        temp2 = str(info[0][2])
        temp3 = str(info[0][3])
        temp4 = str(info[0][4])

#如果编号中含有普云和马良则按如下方式处理

        if temp4[0:2] == '普云' or temp4[0:2] == '马良':
            temp5 = temp4[0:2]
        else:
            temp5 = temp4[0]

#如果名称中含有以下电压等级则按如下方式处理
  
        if '220kV' in temp3:
            temp6 = '220kV'
        elif '110kV' in temp3:
            temp6 = '110kV'
        else:
            temp6 = '35kV'

#如果名称中如上述定义的字符则按如下方式处理
        
        if flag1 in temp:
            temp2 = temp2 + '*'
            substring1 = temp2[4:]
            temp2 = temp2.replace(substring1,temp1+'侧')
            temper = temp3 + temp6 + temp5 + temp2
        elif flag2 in temp:
            temp2 = temp2 + '*'
            substring4 = temp2[5:]
            temp2 = temp2.replace(substring4,'')
            temper = temp3 + temp5 + temp1 + temp2
        elif flag3 in temp:
            temp2 = temp2 + '*'
            substring5 = temp2[5:]
            temp2 = temp2.replace(substring5,'')
            temper = temp3 + temp5 + temp1 + temp2
        elif flag4 in temp:
            temp2 = temp2 + '*'
            substring6 = temp2[5:]
            temp2 = temp2.replace(substring6,'')
            temper = temp3 + temp5 + temp1 + temp2
        else:
            temper = str(info[0][0])

#按照操作方式进行字符串替换，若操作方式不存在则给出错误提示

        if args2 == '合上':
            list_cz = [c.replace("××变××线", temper) for c in list_bzh]
            list_cz = [c.replace('××', bh) for c in list_cz]
            list_num = [1,2,3,4,5]
            d1 = {}
            for i in range(len(list_num)):
                d1[list_num[i]] = list_cz[i]
            return d1
        elif args2 == '断开':
            list_cz = [c.replace("××变××线",temper) for c in list_bzf]
            list_cz = [c.replace('××', bh) for c in list_cz]
            list_num = [1,2,3,4,5]
            d2 = {}
            for i in range(len(list_num)):
                d2[list_num[i]] = list_cz[i]
            return d2  
        else:
            d3 = {'错误提示':'错误的操作方式'}
            return d3
     
#若输入的编号在数据库中不存在则给出错误提示并关闭数据库连接

    else:
        d4 = {'错误提示':'数据库中无此设备'}
        return d4   