class TokenExpirationUtil {
  private handler: () => void = () => {}

  public registerHandler(handler: () => void) {
    this.handler = handler
  }

  public warnTokenIsExpired() {
    this.handler()
  }
}

export const tokenExpirationUtil = new TokenExpirationUtil()
