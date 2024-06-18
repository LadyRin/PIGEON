export const buildException = (error: any): Error => {
  const response = error.response ?? null
  const data = response?.data ?? null
  const status = response?.status ?? null
  const statusText = response?.statusText ?? null
  const url = data?.url ?? null
  const message = data?.message ?? null

  if (data && status && statusText && url && message) {
    return new Error(`${status} - ${statusText} on ${url} - ${message}`)
  } else if (response && status && statusText) {
    return new Error(`${status} - ${statusText}`)
  } else {
    return new Error('Unknown error')
  }
}
