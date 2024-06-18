class FlashMessages {
  private flashHandler: (message: FlashMessage) => void = () => {}

  public registerHandler(handler: (message: FlashMessage) => void) {
    this.flashHandler = handler
  }

  public show({ type, title, text }: FlashMessage) {
    this.flashHandler({ type, title, text })
  }

  public success(text: string, title: string = 'Success') {
    this.show({ type: 'success', title, text })
  }

  public warning(text: string, title: string = 'Warning') {
    this.show({ type: 'warning', title, text })
  }

  public error(text: string, title: string = 'Error') {
    this.show({ type: 'error', title, text })
  }

  public info(text: string, title: string = 'Info') {
    this.show({ type: 'info', title, text })
  }
}

export interface FlashMessage {
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  text: string
}

export const flashMessage = new FlashMessages()
