import {createI18n} from 'vue-i18n';
import en from '@/locales/en.json';
import ru from '@/locales/ru.json';
import {LocalStorageService} from "@/shared/api/services/local-storage-service.ts";

const localLanguage = new LocalStorageService<{ name: string, short: string, icon: string }>('language');

const messages = {
  en: en,
  ru: ru
};

export const i18n = createI18n({
  legacy: false,
  locale: localLanguage.getItem()?.short || 'en',
  fallbackLocale: localLanguage.getItem()?.short || 'en',
  messages
});