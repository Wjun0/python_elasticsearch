from elasticsearch import Elasticsearch
from flask import Flask, jsonify


es = Elasticsearch("192.168.59.129:9200")

app = Flask(__name__)



@app.route('/',methods=['get','post'])
def index():
    # 1,#查看所有的index
    # indexs = es.indices.get("*")
    # print(indexs)
    # print(indexs.keys())

    # 2,添加index
    body = {
        "settings":{
            "number_of_shards":3,
            "number_of_replicas":1
        },
        "mappings":{
            "_doc":{
                'properties':{
                    'tno':{'type':'keyword'},
                    'tname':{'type':"keyword"},
                    'tsex':{'type':"keyword"},
                    "tbirthday":{'type':"keyword"},
                    "prof":{'type':"keyword"},
                    "depart":{
                        "type":'text',
                        'analyzer':'ik_max_word',
                        'search_analyzer':'ik_max_word'
                    }
                }
            }
        }
    }

    # create(self, index, body=None, params=None, headers=None)
    # result = es.indices.create(index='teacher',body=body,ignore=[400]) #忽略index存在了不能新建的错误
    # print(result)


    # 3.向index中添加数据
    from apps.import_data_to_es import Mysql_Data_to_Es
    # Mysql_Data_to_Es().get_mysql_date()   #使用自己定义的方法添加数据，也可以使用下面的方法es.index一条一条添加

    # items = Mysql_Data_to_Es().get_mysql_date()
    # for item in items:
    #     body = {}
    #     body['tno'] = item.tno
    #     body['tname'] = item.tname
    #     body['tbirthday'] = item.tbirthday
    #     body['prof'] = item.prof
    #     body['depart'] = item.depart
    #     res = es.index(index='teacher',id=item.tno,doc_type='_doc',body=body)  #添加数据
    #     print(res)

    # create(self, index, id, body, doc_type=None, params=None, headers=None):
    # res = es.create(index='student',type='')


    # es.index()  也可以添加数据，id会自动生成，如果数据存在会更新，不存在就添加
    # es.delete(index='student',doc_type='politices',id=1) #删除数据


    # 分词搜索
    body = {
        'query':{
            'match':{
                # 'depart':'计算'   #根据depart字段搜索，模糊匹配
                'prof':"副教授"      #根据prof字段搜索，必须完全匹配，
            }
        }
    }

    # 逻辑运算 or
    body = {
        'query': {
            'match': {
                'depart':'计算 电子'   #根据depart字段搜索，模糊匹配
            }
        }
    }

    # 逻辑运算 and 必须使用bool,must
    body = {
        'query': {
            'bool':{
                'must': [
                    {'match':{'depart':'电子'} },  #根据depart字段搜索，模糊匹配
                    {'match':{'depart':'系'} }
                ]
            }
        }
    }

    res = es.search(index='teacher',doc_type='_doc',body=body)
    print(res)
    return jsonify(res)




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)




