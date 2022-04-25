from django.http import HttpResponse


class StripeWHookHandler:
    """
    Class to handle Stripe Webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        This method handles a generic/unknown/
        unexpected webhook event.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
