import { flashMessage } from '@/utils/FlashMessages'

export const handleError = (err: any) => {
  const response = err.response ?? null
  const data = response?.data ?? null
  const status = response?.status ?? null
  const statusText = response?.statusText ?? null
  const url = data?.url ?? null
  const message = data?.message ?? null

  if (data && status && statusText && url && message) {
    flashMessage.error(message, `${status} - ${statusText} on ${url}`)
  } else if (response && status && statusText) {
    flashMessage.error(`${status} - ${statusText}`)
  } else {
    flashMessage.error('Unknown error')
    console.error(err)
  }
}
