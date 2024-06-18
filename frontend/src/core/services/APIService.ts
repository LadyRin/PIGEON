import AxiosClient from '@/utils/AxiosClient'
import { APIResource, type Creatable, type Updatable } from '@/core/resources/APIResource'
import type { PaginationResponse } from '@/core/Common'
import { buildException } from '@/core/exceptions'
export class APIService {
  client: AxiosClient = new AxiosClient(import.meta.env.VITE_API_URL + '/api')
}

export class APIResourceService<T extends APIResource> extends APIService {
  type: new () => T
  apiRoute: string

  constructor(type: new () => T) {
    super()
    this.type = type
    this.apiRoute = new type().apiRoute
  }

  /**
   * GetAll
   */
  getAll(token: string): Promise<T[]> {
    return this.client
      .get(this.apiRoute, token)
      .then((result) => (result.data as any[]).map((item) => new this.type().fromJson(item)))
      .catch((err) => {
        throw buildException(err)
      })
  }

  /**
   * GetAll (with pagination)
   */
  getAllPaginated(
    token: string,
    per_page: number,
    current_page: number,
    sort_by: string,
    sort_desc: boolean,
    search: string,
    exact_search: boolean = false
  ): Promise<PaginationResponse> {
    const params: any = {
      per_page: per_page,
      current_page: current_page
    }
    if (sort_by != '') {
      params.order_by = sort_by
      params.order_type = sort_desc ? 'DESC' : 'ASC'
    }
    if (search != '') {
      params.search = search
      params.exact_search = exact_search
    }
    return this.client
      .get(this.apiRoute, token, params)
      .then((result) => {
        const response: Array<any> = result.data.results
        const array: Array<T> = response.map((item) => new this.type().fromJson(item))
        const out: PaginationResponse = {
          count: result.data.count,
          num_pages: result.data.num_pages,
          start_index: result.data.start_index,
          end_index: result.data.end_index,
          results: array
        }
        return out
      })
      .catch((err) => {
        throw buildException(err)
      })
  }

  /**
   * Get
   */
  get(id: any, token: string): Promise<T> {
    return this.client
      .get(this.apiRoute + '/' + id, token)
      .then((result) => {
        console.log(result)
        return result
      })
      .then((result) => new this.type().fromJson(result.data))
      .catch((err) => {
        throw buildException(err)
      })
  }

  /**
   * Create
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  create(item: Creatable<T>, token: string, _params?: any): Promise<T> {
    return this.client
      .post(this.apiRoute, item.toJsonRequest(), token)
      .then((result) => new this.type().fromJson(result.data))
      .catch((err) => {
        throw buildException(err)
      })
  }

  /**
   * Update
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  update(item: Updatable<T>, token: string, _params?: any): Promise<T> {
    return this.client
      .put(this.apiRoute + '/' + item.getIdentifier(), item.toJsonRequest(), token)
      .then((result) => new this.type().fromJson(result.data))
      .catch((err) => {
        throw buildException(err)
      })
  }

  /**
   * Delete
   */
  delete(item: T, token: string): Promise<boolean> {
    return this.client
      .delete(this.apiRoute + '/' + item.getIdentifier(), null, token)
      .then(() => true)
      .catch((err) => {
        throw buildException(err)
      })
  }

  /**
   * Delete many
   */
  deleteMany(items: T[], token: string): Promise<boolean> {
    const json = { ids: items.map((item) => item.getIdentifier()) }
    return this.client
      .delete(this.apiRoute + '/destroy_list', json, token)
      .then(() => true)
      .catch((err) => {
        throw buildException(err)
      })
  }
}
