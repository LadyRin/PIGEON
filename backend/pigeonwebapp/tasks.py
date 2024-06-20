from celery import shared_task

@shared_task
def add(x, y):
    print(f'Adding {x} and {y}')
    print(f'The result is {x + y}')
    return x + y