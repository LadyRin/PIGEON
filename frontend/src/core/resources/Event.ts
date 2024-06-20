import { APIResource, type Creatable, type Updatable } from '@/core/resources/APIResource'
import { EventTheme } from '@/core/resources/EventTheme'
import { EventType } from '@/core/resources/EventType'
import { MailingList } from '@/core/resources/MailingList'
import { User } from '@/core/resources/User'

export class Event extends APIResource implements Creatable<Event>, Updatable<Event> {
  get apiRoute(): string {
    return 'events'
  }

  id: number = 0
  title: string = ''
  event_type: EventType | null = null
  theme: EventTheme | null = null
  mailing_list: MailingList | null = null
  speaker_first_name: string = ''
  speaker_last_name: string = ''
  speaker_from: string = ''
  speaker_comment: string = ''
  date: string = ''
  start_time: string = ''
  end_time: string = ''
  description: string = ''
  attachment: string = ''
  owner: User | null = null

  getIdentifier() {
    return this.id
  }

  fromJson(json: any) {
    this.id = json.id
    this.title = json.title
    this.event_type = new EventType().fromJson(json.event_type)
    this.theme = new EventTheme().fromJson(json.theme)
    this.mailing_list = new MailingList().fromJson(json.mailing_list)
    this.speaker_first_name = json.speaker_first_name
    this.speaker_last_name = json.speaker_last_name
    this.speaker_from = json.speaker_from
    this.speaker_comment = json.speaker_comment
    this.date = json.date
    this.start_time = json.start_time
    this.end_time = json.end_time
    this.description = json.description
    this.attachment = json.attachment
    this.owner = json.owner ? new User().fromJson(json.owner) : null
    return this
  }

  toJsonRequest() {
    return {
      title: this.title,
      event_type: this.event_type ? this.event_type.getIdentifier() : null,
      theme: this.theme ? this.theme.getIdentifier() : null,
      mailing_list: this.mailing_list ? this.mailing_list.getIdentifier() : null,
      speaker_first_name: this.speaker_first_name,
      speaker_last_name: this.speaker_last_name,
      speaker_from: this.speaker_from,
      speaker_comment: this.speaker_comment,
      date: this.date,
      start_time: this.start_time,
      end_time: this.end_time,
      description: this.description
    }
  }
}
