import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', () => {
  const openAiApiKey = ref('')
  const tavilyApiKey = ref('')
  function updateOpenAiApiKey(newKey: string) {
    openAiApiKey.value = newKey
  }
  function updateTavilyApiKey(newKey: string) {
    tavilyApiKey.value = newKey
  }

  return { openAiApiKey, tavilyApiKey, updateOpenAiApiKey, updateTavilyApiKey }
})
