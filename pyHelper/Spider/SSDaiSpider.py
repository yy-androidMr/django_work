import http.cookiejar
import json

import os
import requests
import shutil
import urllib

info_dir = "info/"
csv = ".csv"


def order_line(key, value=None):
    if value:
        return key + ",\t" + str(value) + "\n"
    return key + ",\t空\n"


def create_dirs(file_path, is_dir=False, delete_exist=False):
    if is_dir:
        target_dir = file_path
    else:
        target_dir = os.path.dirname(file_path)

    if target_dir:
        if os.path.exists(target_dir):
            if delete_exist:
                shutil.rmtree(target_dir)
            else:
                return
        os.makedirs(target_dir)


def load_url(session, url):
    content = session.get("http://app.ssdai8.com:8080" + url)
    info = json.loads(content.text)
    return info


def request_selecct_loan_order(session, page):
    return load_url(session,
                    "/api/loanOrder/userSelectLoanOrder?limitPayTime=&name=&phone=&currentPage=" + str(
                        page) + "&status=-2")


# orderNumber userName  phone   逾期天数    贷款期限    借款金额    打款金额    应还金额        打款时间    应还款时间       贷款单号
# 贷款单号     姓名       电话  overdueDays limitDays   borrowMoney realMoney   needPayMoney    giveTime    limitPayTime    orderNumber
def write_main_info(folder, usr_info):
    main_file = folder + "概括信息_" + usr_info["user"]["userName"] + csv
    if os.path.exists(main_file):
        os.remove(main_file)
    content = order_line("贷款单号", usr_info["orderNumber"]) + order_line("姓名", usr_info["user"]["userName"]) \
              + order_line("电话", usr_info["user"]["phone"]) + order_line("逾期天数", usr_info["overdueDays"]) \
              + order_line("贷款期限", usr_info["limitDays"]) + order_line("借款金额", usr_info["borrowMoney"]) \
              + order_line("打款金额", usr_info["realMoney"]) + order_line("应还金额", usr_info["needPayMoney"]) \
              + order_line("打款时间", usr_info["giveTime"]) + order_line("应还款时间", usr_info["limitPayTime"]) \
              + order_line("贷款单号", usr_info["orderNumber"]) + order_line("银行卡号", usr_info["bankCardNum"]) \
              + order_line("银行名字", usr_info["bankName"])
    with open(main_file, "w+", encoding='utf-8') as f:
        f.write(content)


# 查询认证信息
# userId
# /api/userBasicMsg/selectOneDetailsByUserId?id=36071
# print(session.get("http://app.ssdai8.com:8080/api/userBasicMsg/selectOneDetailsByUserId?id=36071").text)
# 申请时间      联系人一姓名      联系人一电话          婚姻    联系人一关系            联系人二姓名         联系人二电话       联系人二关系              工作地址  公司名称    工资        工作电话    学历      详细地址
# gmtDatetime   linkPersonNameOne linkPersonPhoneOne    marry   linkPersonRelationOne   linkPersonNameTwo    linkPersonPhoneTwo linkPersonRelationTwo     workPlace workCompany workMoney   workPhone   study   addressDetails
# 省         城市  county
# province  city    区
def write_friend_info(folder, f_info):
    main_file = folder + "联系人认证_" + f_info["user"]["userName"] + csv
    content = order_line("申请时间", f_info["gmtDatetime"]) + order_line("联系人一姓名", f_info["linkPersonNameOne"]) \
              + order_line("联系人一电话", f_info["linkPersonPhoneOne"]) + order_line("婚姻", f_info["marry"]) \
              + order_line("联系人一关系", f_info["linkPersonRelationOne"]) + order_line("联系人二姓名",
                                                                                   f_info["linkPersonNameTwo"]) \
              + order_line("联系人二电话", f_info["linkPersonPhoneTwo"]) + order_line("联系人二关系",
                                                                                f_info["linkPersonRelationTwo"]) \
              + order_line("工作地址", f_info["workPlace"]) + order_line("公司名称", f_info["workCompany"]) \
              + order_line("工资", f_info["workMoney"]) + order_line("省", f_info["province"]) \
              + order_line("城市", f_info["county"]) + order_line("公司电话", f_info["workPhone"]) \
              + order_line("学历", f_info["study"])
    with open(main_file, "w+", encoding='utf-8') as f:
        f.write(content)


# 认证信息中的身份信息
# userId
# /api/userIdentity/selectOneDetailsByUserId?id=
# 身份证号码     认证状态            qq号     省市区 详细地址            身份证正面照   身份证反面照    人脸照片
# identityNum   status:1代表认证    qqNum   address  addressDetails     identityFront   identityBack    faceUrl
def write_idc_info(folder, id_info):
    main_file = folder + "联系人认证_" + id_info["userName"] + csv
    content = order_line("身份证号码", id_info["identityNum"]) + order_line("认证状态", str(id_info["status"]) + ",1代表已认证!") \
              + order_line("qq号", id_info["qqNum"]) + order_line("详细地址", id_info["addressDetails"])
    with open(main_file, "w+", encoding='utf-8') as f:
        f.write(content)
    r = requests.get(id_info["identityFront"])
    with open(folder + id_info["userName"] + "_身份证正面.jpg", "wb") as f:
        f.write(r.content)
    r = requests.get(id_info["identityBack"])
    with open(folder + id_info["userName"] + "_身份证反面.jpg", "wb") as f:
        f.write(r.content)
    r = requests.get(id_info["faceUrl"])
    with open(folder + id_info["userName"] + "_人脸照.jpg", "wb") as f:
        f.write(r.content)


# 银行卡认证
# userId
# /api/userBank/selectByUserId?id=
# 银行名字  卡的名字    卡类型     卡号          身份证号    生日      地址      银行手机号   名称
# bankName  cardname    cardtype    bankcardno   idcardno   birthday   address   bankPhone    name

# 手机运营商认证
# userId
# /api/userPhone/selectOne?id=
# 手机绑定真实姓名  绑定的身份证号  手机余额                   入网时间    网龄
# realName          identityCode    accountBalance(需要*0.01)  netTime    netAgeo
def write_bank_info(folder, b_info, m_info):
    main_file = folder + "银行卡认证_手机运营商认证_" + b_info["name"] + csv
    content = order_line("银行名字", b_info["bankName"]) + order_line("卡的名字", b_info["cardname"]) \
              + order_line("卡类型", b_info["cardtype"]) + order_line("卡号", b_info["bankcardno"]) \
              + order_line("身份证号", b_info["idcardno"]) + order_line("生日", b_info["birthday"]) \
              + order_line("地址", b_info["address"]) + order_line("银行手机号", b_info["bankPhone"]) \
              + order_line("名称", b_info["name"]) + order_line("手机归属地", b_info["mobileCity"]) \
              + order_line("以下是手机运营商信息", "-----------") + order_line("手机绑定真实姓名", m_info["realName"]) \
              + order_line("绑定的身份证号", m_info["identityCode"]) + order_line("手机余额", "0" if m_info[
                                                                                              "accountBalance"] == None else  float(
        m_info["accountBalance"]) * 0.01) \
              + order_line("入网时间", m_info["netTime"]) + order_line("网龄", m_info["netAgeo"])
    with open(main_file, "w+", encoding='utf-8') as f:
        f.write(content)


# 手机通讯录
# userId
# /api/userPhoneList/findByUserPage?userId=" + id + "&pageNo=" + pageNo + "&pageSize=" + pageSize
# http://app.ssdai8.com:8080/api/userPhoneList/findByUserPage?userId=36071&pageNo=1
# 需要加入关系:link
def write_phone_list(folder, session, usr_id):
    def get_phone_info(info_list):
        content = ""
        for item in info_list:
            content += ",".join(
                [str(item["userId"]), str(item["name"]), "\t" + str(item["phone"]), str(item["link"])]) + "\n"
        return content

    main_file = folder + "联系人信息" + csv

    load_info = load_url(session, "/api/userPhoneList/findByUserPage?userId=" + usr_id + "&pageNo=1")["data"]
    content = "用户id,名字,电话,关系\n"
    content += get_phone_info(load_info["list"])
    page_count = load_info["pages"] + 1
    for i in range(2, page_count):
        load_info = load_url(session, "/api/userPhoneList/findByUserPage?userId=" + usr_id + "&pageNo=" + str(i))[
            "data"]
        content += get_phone_info(load_info["list"])

    with open(main_file, "w+", encoding='utf-8') as f:
        f.write(content)


# 通话记录
# "/api/userPhoneRecord/findByUserIdPage?userId=" + id + "&pageNo=" + pageNo + "&pageSize=" + pageSize,
# http://app.ssdai8.com:8080/api/userPhoneRecord/findByUserIdPage?userId=36071&pageNo=1
# commFee 费用,归属地 commPlac,通话日期startTime,主被叫callType,通话时长connTimes,手机号码phoneNo,通话类型commMode
def write_my_essay(folder, session, usr_id):
    def get_phone_info(info_list):
        content = ""
        for item in info_list:
            content += ",".join(
                ["\t" + str(item["phoneNo"]), str(item["commPlac"]), "\t" + str(item["connTimes"]),
                 str(item["commFee"]),
                 str(item["commMode"]), str(item["callType"]), "\t" + str(item["startTime"])]) + "\n"
        return content

    load_info = load_url(session, "/api/userPhoneRecord/findByUserIdPage?userId=" + usr_id + "&pageNo=1")["data"]
    content = "手机号,归属地,通话时长,通话费用,通话类型,主被叫,通话日期\n"
    content += get_phone_info(load_info["list"])
    page_count = load_info["pages"] + 1
    for i in range(2, page_count):
        load_info = load_url(session, "/api/userPhoneRecord/findByUserIdPage?userId=" + usr_id + "&pageNo=" + str(i))[
            "data"]
        content += get_phone_info(load_info["list"])

    main_file = folder + "通话记录" + csv
    with open(main_file, "w+") as f:
        f.write(content)


def write_infos(folder, usr):
    error_info = ""
    print("开始写入:" + str(usr["user"]["userName"]))
    try:
        # 1 概括信息
        write_main_info(folder, usr)

        # 2  联系人信息
        write_friend_info(folder, load_url(session, "/api/userBasicMsg/selectOneDetailsByUserId?id=" + str(
            usr["userId"]))["data"])

        # 3 身份证信息
        write_idc_info(folder,
                       load_url(session, "/api/userIdentity/selectOneDetailsByUserId?id=" + str(usr["userId"]))[
                           "data"])

        # 4 银行卡认证
        write_bank_info(folder,
                        load_url(session, "/api/userBank/selectByUserId?id=" + str(usr["userId"]))["data"],
                        load_url(session, "/api/userPhone/selectOne?id=" + str(usr["userId"]))["data"])

        # 5  联系人
        write_phone_list(folder, session, str(usr["userId"]))
    except:
        error_info += "名字:" + str(usr["user"]["userName"]) + " id:" + str(usr["userId"]) + "\n"
        print("写入错误!用户信息:" + str(usr["userId"]))
    print("写入完成!")
    return error_info
    # 6 通话记录
    # write_my_essay(folder, session, str(usr["userId"]))


def rang_total_info_list(list):
    err_inf = ""
    for item in list:
        usr_info = item
        # 0
        folder_path = info_dir + "_".join(
            [str(usr_info["limitPayTime"]).split(" ")[0],
             str(usr_info["user"]["userName"]),
             str(usr_info["user"]["phone"])]) + "/"
        create_dirs(folder_path, True)

        err_inf += write_infos(folder_path, usr_info)
    return err_inf


session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='SSDai')

try:
    # 加载Cookies文件
    session.cookies.load(ignore_discard=True)
except:
    session.get("http://app.ssdai8.com:8080/api/admin/login?userName=催收B&password=383838")
    session.cookies.save()
# content = session.get("http://app.ssdai8.com:8080/admin/index.html")#主页

page_info = request_selecct_loan_order(session, 25)
total_info_count = page_info["data"]["pageDto"]["total"]
page_count = (int)(total_info_count / 10) + 1
print(total_info_count, "page_count:", page_count)
e_info = rang_total_info_list(page_info["data"]["pageDto"]["list"])
for i in range(26, page_count):
    page_info = request_selecct_loan_order(session, i)
    e_info += rang_total_info_list(page_info["data"]["pageDto"]["list"])
    pass
with open(info_dir + "错误信息.txt", encoding='utf-8') as f:
    f.write(e_info)

# 支付宝认证
# http://app.ssdai8.com:8080/api/userZhifubao/selectOne?id=36071
# huabeiQuota花呗额度,aliNumber阿里手机号


# 详情页 id=userBasicMsg的id
# /api/loanOrder/selectOneDetail?id=126725
# id,姓名user.userName,电话:.user.phone,贷款单号:orderNumber,银行名称:bankName,银行卡号:bankCardNum,贷款期限limitDays,借款金额:borrowMoney,到账金额:realMoney,利息:interestMoney,平台服费:placeServeMoney,短信认证费:msgAuthMoney,风控服务费:riskServeMoney,风控准备金:riskPlanMoney,综合费用:wateMoney,优惠券节省金额:saveMoney,
# 借款协议agreementUrl
# 借款服务协议agreementTwoUrl
