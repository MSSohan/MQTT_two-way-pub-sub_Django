import json
from django.http import JsonResponse
from mqtt_test.mqtt import client as mqtt_client

def publish_message(request):
    try:
        # Parse the JSON body of the request
        request_data = json.loads(request.body)

        # Publish the message to the specified topic
        returnCode, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])

        # Check if the publish was successful
        if returnCode == 0:
            response_data = {
                'status': 'success',
                'code': returnCode,
                'message_id': mid,
                'message': 'Message published successfully'
            }
        else:
            response_data = {
                'status': 'error',
                'code': returnCode,
                'message': 'Failed to publish message'
            }

        # Return the result as a JSON response
        return JsonResponse(response_data)

    except Exception as e:
        # Handle any exceptions that may occur
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
