import { APIService } from '@/core/services/APIService'

export class SSHService extends APIService {
  getPublicKey(token: string): Promise<string> {
    return this.client
      .get('ssh/public_key', token)
      .then((result) => result.data.public_key)
      .catch((err) => {
        throw err
      })
  }

  generateKeyPair(token: string): Promise<string> {
    return this.client
      .post('ssh/generate_key_pair', {}, token)
      .then((result) => result.data.public_key)
      .catch((err) => {
        throw err
      })
  }

  forceUpdate(token: string): Promise<void> {
    return this.client
      .post('ssh/update_servers', {}, token)
      .then(() => {})
      .catch((err) => {
        throw err
      })
  }
}
