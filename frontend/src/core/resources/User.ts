import { APIResource } from '@/core/resources/APIResource'

export class User extends APIResource {
  get apiRoute(): string {
    return 'users'
  }

  id: number = 0
  username: string = ''
  email: string = ''
  first_name: string = ''
  last_name: string = ''
  is_superuser: boolean = false

  getIdentifier() {
    return this.id
  }

  fromJson(json: any) {
    this.id = json.id
    this.username = json.username
    this.email = json.email
    this.first_name = json.first_name
    this.last_name = json.last_name
    this.is_superuser = json.is_superuser

    if (this.first_name == '' && this.last_name == '') {
      this.first_name = this.username
    }

    return this
  }
}
