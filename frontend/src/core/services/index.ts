import { APIResourceService } from '@/core/services/APIService'
import { Event } from '@/core/resources/Event'
import { EventType } from '@/core/resources/EventType'
import { EventTheme } from '@/core/resources/EventTheme'
import { MailingList } from '@/core/resources/MailingList'
import { User } from '@/core/resources/User'

export const eventService = new APIResourceService(Event)
export const eventTypeService = new APIResourceService(EventType)
export const eventThemeService = new APIResourceService(EventTheme)
export const mailingListService = new APIResourceService(MailingList)
export const userService = new APIResourceService(User)
