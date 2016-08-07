
# Instructions
## models.py:
### Class:Query():
数据库查询结果时用  
存放一条记录的相关信息  
uid:ctid  
similar_score:score  
codes:两条代码的地址

### Class:Cheat():
定义数据库表
#### method:addRecord:
添加记录到antiCheat表，主要从Submissions那里得到记录，需要调用Submissions类的submissionList方法
#### method:getCheatList:
获得作弊涉嫌名单
#### method:antiCheat:
整个反作弊算法的入口函数

## views.py:
### method:addRecord:
调用models的addRecord方法
### method:showResult:
调用models的getCheatList方法  
返回一个嵌套list的list。内层的每个list格式为user1,user2,problem,similarscore。


