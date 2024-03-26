
# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('20240205103958-3fd42d09-7deb-4dfe-8ee6-2da1063b4aad')
pro._DataApi__http_url = 'http://tsapi.majors.ltd:7000'

def test_mjs():
    # df = pro.jinse(start_date='2024-02-10 22:00:00', end_date='2024-02-15 22:15:00', \
    #             fields='title, type, datetime')
    # print(df)
    df =pro.twitter_kol(start_date='2024-02-10 22:00:00', end_date='2024-02-15 22:15:00', fields="id,account,nickname,content,retweet_content,media,str_posted_at")
    print(df)