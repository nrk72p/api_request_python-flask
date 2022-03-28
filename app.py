from flask import Flask
from flask_restful import Api ,Resource,abort ,reqparse ,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy, Model
from numpy import require 
app = Flask(__name__)

#database connection
db = SQLAlchemy(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"

class CityModel(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    temp=db.Column(db.String(100), nullable=False)
    weather=db.Column(db.String(100), nullable=False)
    people=db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"City(name={name}),temp={temp},weather={weather},people={people})"
        
db.create_all()

#request parser 
#add
city_add_args  = reqparse.RequestParser()
city_add_args.add_argument("name",type=str,required=True,help="กรุณาป้อนชื่อจังหวัด")
city_add_args.add_argument("temp",type=str,required=True,help="กรุณาป้อนอุณหภูมิ")
city_add_args.add_argument("weather",type=str,required=True,help="กรุณาป้อนสภาพอากาศ")
city_add_args.add_argument("people",type=str,required=True,help="กรุณาป้อนจำนวนประชากร")

#update agrs
city_update_args=reqparse.RequestParser()
city_update_args.add_argument("name",type=str,help="กรุณาป้อนชื่อจังหวัดที่ต้องการแก้ไข")
city_update_args.add_argument("temp",type=str,help="กรุณาป้อนอุณหภูมิที่ต้องการแก้ไข")
city_update_args.add_argument("weather",type=str,help="กรุณาป้อนสภาพอากาศที่ต้องการแก้ไข")
city_update_args.add_argument("people",type=str,help="กรุณาป้อนจำนวนประชากรที่ต้องการแก้ไข")

resource_field = {
    "id":fields.Integer , 
    "name":fields.String , 
    "temp":fields.String , 
    "weather":fields.String ,
    "people":fields.String
}

mycity={
    "chonburi":{"name":"ชลบุรี","weather":"อากาศร้อนอบอ้าว","people":1500},
    "rayong":{"name":"ระยอง","weather":"ฝนตก","people":500},
    "bangkok":{"name":"กรุงเทพ","weather":"ร้อนแบบมีฝุ่น","people":5000}
}



#design
class weatherCity(Resource):
    
    @marshal_with(resource_field)
    def get(self,city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(401,message="ไม่พบข้อมูลในระบบ")
        return result

    
    @marshal_with(resource_field)
    def post(self,city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409,message="รหัสนี้ถูกบันทึกก่อนหน้านี้แล้ว")               
        args = city_add_args.parse_args()
        city=CityModel(
            id=city_id,
            name=args["name"],
            temp=args["temp"],
            weather=args["weather"],
            people=args["people"])
        db.session.add(city)
        db.session.commit()
        return city,201
    
    @marshal_with(resource_field)
    def patch(self,city_id):
        args=city_update_args.parse_args()
        result = CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404,"ไม่พบข้อมูลจังหวัด")
        if args["name"]:
            result.name=args["name"] 
        if args["temp"]:
            result.temp=args["temp"]
        if args['weather']:
            result.weather=args["weather"]
        if args['people']:
            result.people=args["people"]
            
        db.session.commit()
        return result

#call 
api.add_resource(weatherCity,"/weather/<int:city_id>")

if __name__ == '__main__':
    app.run(debug=True)