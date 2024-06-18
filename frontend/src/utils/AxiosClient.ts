import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { tokenExpirationUtil } from './TokenExpirationUtil'

/**
 * Représente un client Axios pour envoyer et recevoir des requêtes HTTP avec
 * les méthodes POST et GET avec ou sans authentification
 */
class AxiosClient {
  client: AxiosInstance

  constructor(url: string) {
    this.client = axios.create({
      baseURL: url
    })
  }

  async verifyToken(token: string): Promise<boolean> {
    return await this.client
      .post('/token/verify', {
        token: token
      })
      .then(() => true)
      .catch(() => {
        tokenExpirationUtil.warnTokenIsExpired()
        return false
      })
  }

  async execIfTokenValid(token: string, promise: () => Promise<AxiosResponse>): Promise<AxiosResponse> {
    const isTokenValid = await this.verifyToken(token)

    if (isTokenValid) return promise()

    return Promise.reject(new Error('Token is not valid'))
  }

  /**
   * Appel HTTP POST
   * @param url URL de la requête HTTP
   * @param data Body de la requête HTTP
   * @param token Token Bearer à ajouter à l'entête
   */
  post(url: string, data: any, token?: string): Promise<AxiosResponse> {
    const config: any = {
      timeout: 1000 * 30
    }

    if (!token) return this.client.post(url, data, config)

    config.headers = {
      Authorization: 'Bearer ' + token
    }

    return this.execIfTokenValid(token, () => this.client.post(url, data, config))
  }

  /**
   * Appel HTTP PUT
   * @param url URL de la requête HTTP
   * @param data Body de la requête HTTP
   * @param token Token Bearer à ajouter à l'entête
   */
  put(url: string, data: any, token: string, param?: any): Promise<AxiosResponse> {
    const config: any = {
      timeout: 1000 * 30,
      params: param,
      headers: {
        Authorization: 'Bearer ' + token
      }
    }

    return this.execIfTokenValid(token, () => this.client.put(url, data, config))
  }

  /**
   * Appel HTTP GET
   * @param url URL de la requête HTTP
   * @param token Token Bearer à ajouter à l'entête
   */
  get(url: string, token: string, param?: any, responseType?: string): Promise<AxiosResponse> {
    const config: any = {
      timeout: 1000 * 100,
      params: param,
      headers: {
        Authorization: 'Bearer ' + token
      },
      responseType: responseType
    }

    return this.execIfTokenValid(token, () => this.client.get(url, config))
  }

  /**
   * Appel HTTP DELETE
   * @param url URL de la requête HTTP
   * @param data Body de la requête HTTP
   * @param token Token Bearer à ajouter à l'entête
   */
  delete(url: string, data: any, token: string, param?: any): Promise<AxiosResponse> {
    const config: any = {
      timeout: 1000 * 30,
      params: param,
      data: data,
      headers: {
        Authorization: 'Bearer ' + token
      }
    }

    return this.execIfTokenValid(token, () => this.client.delete(url, config))
  }
}

export default AxiosClient
