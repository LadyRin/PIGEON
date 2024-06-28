import { APIResource, type Creatable, type Updatable } from '@/core/resources/APIResource'

export class Server extends APIResource implements Creatable<Server>, Updatable<Server> {
  get apiRoute(): string {
    return 'servers'
  }

  id: number = 0
  name: string = ''
  hostname: string = ''
  username: string = ''
  upload_directory: string = ''
  port: number = 22

  getIdentifier() {
    return this.id
  }

  fromJson(json: any) {
    this.id = json.id
    this.name = json.name
    this.hostname = json.hostname
    this.username = json.username
    this.upload_directory = json.upload_directory
    this.port = json.port

    return this
  }

  toJsonRequest() {
    return {
      name: this.name,
      hostname: this.hostname,
      username: this.username,
      upload_directory: this.upload_directory,
      port: this.port
    }
  }
}
