import json, time
import psycopg2
import pika
from worker.config import DATABASE_URL, RABBITMQ_URL

def process_load(conn, load_id):
    cur = conn.cursor()
    cur.execute("SELECT id, company_id, status FROM loads WHERE id=%s", (load_id,))
    load = cur.fetchone()
    if not load:
        print('load not found', load_id)
        return
    if load[2] != 'pending':
        print('load already processed or in progress:', load[2])
        return
    cur.execute("UPDATE loads SET status='processing' WHERE id=%s", (load_id,))
    conn.commit()
    cur.execute("SELECT id, employee_id, amount, status FROM load_items WHERE load_id=%s", (load_id,))
    items = cur.fetchall()
    for it in items:
        item_id, employee_id, amount, status = it
        if status != 'pending':
            continue
        cur.execute('''INSERT INTO balances (employee_id, benefit_type, amount)
                       VALUES (%s, %s, %s)
                       ON CONFLICT (employee_id, benefit_type) DO UPDATE
                         SET amount = balances.amount + EXCLUDED.amount,
                             updated_at = now()
                       RETURNING id, amount''',
                    (employee_id, 'alimentacao', amount))
        new = cur.fetchone()
        cur.execute("UPDATE load_items SET status='processed' WHERE id=%s", (item_id,))
        conn.commit()
        print(f"Processed item {item_id} -> employee {employee_id} +{amount} (balance id {new[0]})")
        time.sleep(0.02)
    cur.execute("UPDATE loads SET status='completed' WHERE id=%s", (load_id,))
    conn.commit()
    print("Load", load_id, "completed")

def on_message(ch, method, properties, body):
    try:
        payload = json.loads(body)
        load_id = payload.get('load_id')
        print("Received job for load", load_id)
        conn = psycopg2.connect(DATABASE_URL)
        try:
            process_load(conn, load_id)
        finally:
            conn.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error processing message:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main(retries=0, delay=2):
    """Connect to RabbitMQ

    Se o rabbitMQ ainda não estiver pronto, tenta novamente até obter sucesso.
    """
    params = pika.URLParameters(RABBITMQ_URL)
    attempt = 0
    while True:
        attempt += 1
        try:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue='benefit.load.request', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='benefit.load.request', on_message_callback=on_message)
            print("Worker listening for load requests...")
            channel.start_consuming()
            break
        except pika.exceptions.AMQPConnectionError:
            print(f"Worker: RabbitMQ not ready (attempt {attempt}), retrying in {delay}s...")
            time.sleep(delay)
            if retries and attempt >= retries:
                print("Worker: exceeded max retries connecting to RabbitMQ; exiting")
                raise

if __name__ == '__main__':
    main()
