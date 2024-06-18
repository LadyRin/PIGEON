export class PopupUtil {
  private openConfirm: ((message: string) => Promise<boolean>) | null = null
  private openPrompt: ((message: string) => Promise<string | null>) | null = null
  private openAlert: ((message: string) => Promise<void>) | null = null

  async confirm(message: string): Promise<boolean> {
    if (!this.openConfirm) {
      throw new Error('confirm popup not registered')
    }

    return this.openConfirm(message)
  }

  registerConfirmPopup(open: (message: string) => Promise<boolean>) {
    if (this.openConfirm) {
      throw new Error('confirm popup already registered')
    }

    this.openConfirm = open
  }

  async prompt(message: string): Promise<string | null> {
    if (!this.openPrompt) {
      throw new Error('prompt popup not registered')
    }

    return this.openPrompt(message)
  }

  registerPromptPopup(open: (message: string) => Promise<string | null>) {
    if (this.openPrompt) {
      throw new Error('prompt popup already registered')
    }

    this.openPrompt = open
  }

  async alert(message: string): Promise<void> {
    if (!this.openAlert) {
      throw new Error('alert popup not registered')
    }

    return this.openAlert(message)
  }

  registerAlertPopup(open: (message: string) => Promise<void>) {
    if (this.openAlert) {
      throw new Error('alert popup already registered')
    }

    this.openAlert = open
  }
}

export const popupUtil = new PopupUtil()
