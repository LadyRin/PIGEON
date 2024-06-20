/**
 * Représente une ressource de l'API, avec des méthodes pour la sérialisation et la désérialisation, ainsi qu'une route d'API
 */
export abstract class APIResource {
  abstract get apiRoute(): string

  abstract getIdentifier(): any
  abstract fromJson(json: any): this
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export interface Creatable<T extends APIResource> {
  toJsonRequest(): any
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export interface Updatable<T extends APIResource> {
  getIdentifier(): any
  toJsonRequest(): any
}
