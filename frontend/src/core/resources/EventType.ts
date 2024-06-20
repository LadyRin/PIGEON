import { APIResource, type Creatable, type Updatable } from '@/core/resources/APIResource'

export class EventType extends APIResource implements Creatable<EventType>, Updatable<EventType> {
  get apiRoute(): string {
    return 'event_types'
  }

  id: number = 0
  name: string = ''

  getIdentifier() {
    return this.id
  }

  fromJson(json: any) {
    this.id = json.id
    this.name = json.name

    return this
  }

  toJsonRequest() {
    return {
      name: this.name
    }
  }
}
