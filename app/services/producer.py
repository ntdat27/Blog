import pika
import json

rabbit_mq_conenction = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbit_mq_conenction.channel()
channel.queue_declare(queue='like_queue')
def send_like_event(post_id: str, user_email: str,action: str):
    message = json.dumps({
        "post_id": post_id,
        "user_email": user_email,
        "action": action
    })
    channel.basic_publish(exchange='', routing_key='like_queue', body=message)
    print(f"Sent like event: {message}")