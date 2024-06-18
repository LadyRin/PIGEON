import { flashMessage } from '@/utils/FlashMessages'

export const handleError = (err: Error) => {
  const message = err.message

  flashMessage.error('Error', message)
}
