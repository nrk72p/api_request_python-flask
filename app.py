from flask import Flask
from flask_restful import Api ,Resource

app = Flask(__name__)
api = Api(app)

mycity={
    1:{"name":"ชลบุรี","weather":"อากาศร้อนอบอ้าว","people":1500},
    2:{"name":"ระยอง","weather":"ฝนตก","people":500},
    3:{"name":"กรุงเทพ","weather":"ร้อนแบบมีฝุ่น","people":5000}
        }


#design
class weatherCity(Resource):
    def get(self,city_id):
        return mycity[city_id]
    def post(self):
        return{"data":"Create Resource = "+name}

#call 
api.add_resource(weatherCity,"/weather/<int:city_id>")

if __name__ == '__main__':
    app.run(debug=True)