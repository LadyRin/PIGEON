export const formatTime = (time: string) => {
  return time.split(':').slice(0, 2).join(':')
}

export const formatDate = (date: string) => {
  const dateObj = new Date(date)
  return dateObj.toLocaleDateString()
}
