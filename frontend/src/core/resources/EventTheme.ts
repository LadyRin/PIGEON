import { APIResource, type Creatable, type Updatable } from '@/core/resources/APIResource'

export class EventTheme extends APIResource implements Creatable<EventTheme>, Updatable<EventTheme> {
  get apiRoute(): string {
    return 'event_themes'
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
