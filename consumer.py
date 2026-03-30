import pika
import json
from bson import ObjectId
from app.db.session import post_collection

def callback(ch, method, properties, body):
    data = json.loads(body)
    post_id = data['post_id']
    action = data['action']

    print(f"Yeu cau {action} like cho bai viet {post_id}")

    try:
        if action == "increase":
            post_collection.update_one(
                {"_id": ObjectId(post_id)}, 
                {"$inc": {"like": 1}}
            )
        elif action == "decrease":
            post_collection.update_one(
                {"_id": ObjectId(post_id)}, 
                {"$inc": {"like": -1}}
            )
        print("cap nhat db \n")
    except Exception as e:
        print("Lỗi :", e)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='like_queue')

channel.basic_consume(
    queue='like_queue', 
    on_message_callback=callback, 
    auto_ack=True 
)

print('dang cho tin...')
channel.start_consuming()