
#使用该方法不能指定_id
from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from elasticsearch_dsl import Document,Text,Integer,Keyword,Long,Boolean
from elasticsearch_dsl.connections import connections

connections.configure(default={'hosts':'192.168.59.129:9200'})

class TeacherType(Document):
    tno = Long(required=True)
    tname = Keyword()
    tsex = Keyword()
    tbirthday = Keyword()
    prof = Keyword()
    depart = Text(analyzer="ik_max_word")

    class Index():
        name = 'teacher'
        # doc_type = 'teacher'


class Mysql_Data_to_Es():
    def __init__(self):
        self.db = create_engine("mysql+pymysql://root:mysql@192.168.59.1:3306/sql_test",encoding='utf8')


    def get_mysql_date(self):
        resultProxy = self.db.execute('select * from teacher')
        data = resultProxy.fetchall()
        resultProxy.close()
        items = []
        for item in data:
            print(item.tname)
            items.append(item)
        return items

    def save_to_es(self,item):
        teacher = TeacherType()
        teacher.tno = item.tno
        teacher.tname = item.tname
        teacher.tbirthday = item.tbirthday
        teacher.prof = item.prof
        teacher.depart = item.depart
        teacher.save(id=item.tno)       #指定_id,如果不指定会自己生成。不方便查询。


if __name__ == '__main__':
    pass
