from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
cluster = MongoClient("mongodb+srv://engwissam:ZUVLXokrDHs6M2Mm@cluster0.jsugl.mongodb.net/?retryWrites=true&w=majority")

db = cluster["bakery"]
users = db["users"]
orders = db["orders"]
app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    content = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    user = users.find_one({"number": number})
    response = MessagingResponse()
    # msg = response.message("You are most Welcome")
    # msg2.media("https://th.bing.com/th/id/OIP.SAyOSwMmTThro3NyleyGrQHaE9?w=289&h=193&c=7&r=0&o=5&dpr=1.56&pid=1.7")
    # msg.media("http://africau.edu/images/default/sample.pdf")
    if bool(user) == False:
        response.message("عزيزنا المتعامل ، أهلاً بك في خدمة المجيب الآلي لبلدية البطائح، يرجى التفضل بالإختيار من القائمة أدناه:")
        response.message("1️⃣ بيانات الإتصال \n2️⃣ تقديم الطلبات \n3️⃣ تحميل تطبيق خدمات قسم رقابة المباني ( لأجهزة أندرويد)\n4️⃣ الإطلاع على دليل الخدمات لإدارة الهندسة")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(content)
        except:
            response.message("المعذرة، لم أفهم ما تريد، فضلاً اختر رقماً من القائمة أعلاه")
            return str(response)
        if option == 1:
               response.message("للإستفسار عن خدمات قسم رقابة المباني التواصل من خلال قنوات الإتصال التالية:")
               response.message("البريد الالكتروني\n wissam.safa@batmun.shj.ae\n هاتف : 065073630")
        elif option == 2:
                response.message("تسرنا خدمتكم ، يرجى التفضل بإختيار نوع الطلب من القائمة أدناه:")
                response.message("1️⃣ طلب تدقيق إنشائي\n2️⃣ طلب شهادة نسبة إنجاز\n3️⃣ طلب شهادة إنجاز\n4️⃣ طلب شهادة توصيل خدمات\n5️⃣ طلب تقرير موقع للمشاريع قيد الإنشاء\n6️⃣ العودة إلى القائمة الرئيسية")
                users.update_one(
                    {"number": number}, {"$set": {"status": "ordering"}})
        elif option == 3:
                response.message("https://play.google.com/store/apps/details?id=com.batmun.android.engdept")

        elif option == 4:
                 response.message("https://gofile.io/d/spgQVi")
        else:
            response.message("المعذرة، لم أفهم ما تريد، فضلاً اختر رقماً من القائمة أعلاه")
            users.update_one({"number":number},{"$push":{"messages":{"content":content,"date":datetime.now()}}})
        return str(response)
    elif user["status"] == "ordering":
        try:
            option = int(content)
        except:
            response.message("المعذرة، لم أفهم ما تريد، فضلاً اختر رقماً من القائمة أعلاه")
            return str(response)
        if option == 6:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            response.message(
                "عزيزنا المتعامل ، أهلاً بك في خدمة المجيب الآلي لبلدية البطائح، يرجى التفضل بالإختيار من القائمة أدناه:")
            response.message(
                "1️⃣ بيانات الإتصال \n2️⃣ تقديم الطلبات \n3️⃣ تحميل تطبيق خدمات قسم رقابة المباني ( لأجهزة أندرويد)\n4️⃣ الإطلاع على دليل الخدمات لإدارة الهندسة")
        elif option == 1:
            response.message("https://docs.google.com/forms/d/1UoOdVDdMeh-6in1XbUY22nGOILGfHyYCfBOkmeUVXNQ/edit?usp=sharing")
        elif option == 2:
            response.message("https://docs.google.com/forms/d/1AI9fVB6t3oZqvpjA28CtQJqP_iPrDh9J6bBpRfS1FMo/edit?usp=sharing")
        elif option == 3:
            response.message("https://docs.google.com/forms/d/1Kwwn6YURr4p8TMO57deGLqjeg7bsBlJHsxfVwX_SEak/edit?usp=sharing")
        elif option == 4:
            response.message("https://docs.google.com/forms/d/1-jXwWZF6CDo6mwgvKhfdgjJAH2Pi8OQNs1Za7WSvM4M/edit?usp=sharing")
        elif option == 5:
            response.message("https://docs.google.com/forms/d/e/1FAIpQLSdM7lW3YeSvp99_EOGfxEzGSuQRCJbE4VIIFIQszflAzwPHCQ/viewform")
        else:
            response.message("المعذرة، لم أفهم ما تريد، فضلاً اختر رقماً من اقائمة أعلاه")

    return str(response)
if __name__ == "__main__":
    app.run()
