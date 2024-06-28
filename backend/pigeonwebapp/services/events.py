from pigeonwebapp.models import Event
from pigeonwebapp.serializers.event import EventFlatSerializer
import os


def generate_json(file_name):
    events = Event.objects.all()
    serializer = EventFlatSerializer(events, many=True)
    with open(file_name, 'w') as f:
        f.write(str(serializer.data).replace("'", '"'))

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

    