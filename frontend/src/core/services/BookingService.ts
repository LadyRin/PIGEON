import { APIService } from '@/core/services/APIService'
import type { BookableResource } from '@/core/resources/BookableResource'

export class BookingService extends APIService {
  getResources(token: string): Promise<BookableResource[]> {
    return this.client
      .get('booking/resources', token)
      .then((result) => result.data.resources as any[])
      .then((resources) =>
        resources.map((r) => ({
          id: r.resourceId,
          name: r.name
        }))
      )
  }
}
