import { APIResource, type Creatable, type Updatable } from '@/core/resources/APIResource'

export class MailingList extends APIResource implements Creatable<MailingList>, Updatable<MailingList> {
  get apiRoute(): string {
    return 'mailing_lists'
  }

  id: number = 0
  name: string = ''
  address: string = ''

  getIdentifier() {
    return this.id
  }

  fromJson(json: any) {
    this.id = json.id
    this.name = json.name
    this.address = json.address

    return this
  }

  toJsonRequest() {
    return {
      name: this.name,
      address: this.address
    }
  }
}
