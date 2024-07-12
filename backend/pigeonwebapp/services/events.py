from pigeonwebapp.models import Event, EventTheme, EventType
from pigeonwebapp.serializers.event import EventFlatSerializer
import json
import os
from pigeonwebapp.services.booking import Booker


def generate_json(file_name):
    events = Event.objects.all()
    serializer = EventFlatSerializer(events, many=True)
    theme_names = EventTheme.objects.values_list('name', flat=True)
    type_names = EventType.objects.values_list('name', flat=True)

    try:
        booker = Booker()
        booker.authenticate()
        locations = booker.get_all_resources()['resources']

        for event in serializer.data:
            for location in locations:
                if event['resource_id'] == int(location['resourceId']):
                    event['location'] = location['name']
                    break

    except Exception as e:
        print('Error while fetching locations:', e)

    data = {
        "events": serializer.data,
        "themes":  list(theme_names),
        "types": list(type_names)
    }

    with open(file_name, 'w') as f:
        f.write(json.dumps(data, indent=4))

def check_for_updates():
    # Generate JSON file and compare with the previous one
    new_path = 'events_new.json'
    old_path = 'events.json'

    if not os.path.exists(old_path):
        generate_json(old_path)
        return True

    generate_json(new_path)
    with open(new_path, 'r') as f:
        new_json = f.read()

    with open(old_path, 'r') as f:
        old_json = f.read()

    if new_json != old_json:
        os.remove(old_path)
        os.rename(new_path, old_path)
        return True
    else:
        os.remove(new_path)
        return False

    