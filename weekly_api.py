"""Bunker 1 Church Weekly API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'Weekly'

class Weekly(messages.Message):
    """Weekly that stores a message."""
    message = messages.StringField(1)


class WeeklyCollection(messages.Message):
    """Collection of Weeklies."""
    items = messages.MessageField(Weekly, 1, repeated=True)


STORED_GREETINGS = WeeklyCollection(items=[
    Weekly(message='hello world!'),
    Weekly(message='goodbye world!'),
])

@endpoints.api(name='b1cweekly', version='v1')
class B1CWeeklyApi(remote.Service):
    """Bunker 1 Church Weekly API v1."""

    @endpoints.method(message_types.VoidMessage, WeeklyCollection,
                      path='weekly', http_method='GET',
                      name='weeklies.listWeekly')
    def weeklies_list(self, unused_request):
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Weekly,
                      path='weekly/{id}', http_method='GET',
                      name='weeklies.getWeekly')
    def weeklies_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Weekly %s not found.' %
                                              (request.id,))

APPLICATION = endpoints.api_server([B1CWeeklyApi])