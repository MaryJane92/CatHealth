/**
 * Общие типы для API.
 */

export interface HealthResponse {
  status: string;
  app: string;
  version: string;
}

export interface HealthDbResponse {
  status: string;
  database: string;
}

/** Формат даты, используемый в приложении: ДД.ММ.ГГГГ */
export const DATE_FORMAT = "DD.MM.YYYY";

/** Формат даты для API (ISO): ГГГГ-ММ-ДД */
export const DATE_FORMAT_API = "YYYY-MM-DD";
