from json import dumps, loads
from asyncio import get_event_loop, gather
from aiobotocore.session import get_session
from os import env

queue_url = env.get('consumerQueue')

def lambda_handler(event, context):
    print("Start Async Python Function")
    asyncio_event_loop = get_event_loop()
    queued_messages = asyncio_event_loop.run_until_complete(execute_lambda(event))
    
    return {
        'body': queued_messages
    }


async def execute_lambda(event):

    messages_count = event.get('messagesCount', 20)

    print(f"Number of messages: {messages_count}")
    
    message_ids = list(range(messages_count))
    
    session = get_session()

    async with session.create_client('sqs', region_name=env.get('region', 'us-east-1')) as sqs_client:
        queued_messages = await gather(*[sqs_client.send_message(QueueUrl=queue_url, MessageBody=dumps({'messageId': message_id})) for message_id in message_ids])
        
    print(f"len of queued_messages: {queued_messages}")
    
    return queued_messages