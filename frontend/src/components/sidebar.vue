<template>
        <v-navigation-drawer
          class="bg-grey-darken-4"
          theme="dark"
          permanent
        >
        <template v-slot:prepend>
            <div class="d-flex justify-center align-center">
                <img src="@/assets/logo.webp" :width="100" ></img>
                <h2>SciGen</h2>
            </div>
          </template>
          <v-container>
            <v-row>
                <v-col>
                    <v-text-field
                        v-model="openAiApiKey"
                        :label="t('open-ai-api-key')"
                        :append-icon="showOpenAiApiKey ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="showOpenAiApiKey ? 'text' : 'password'"
                        name="input-10-1"
                        hide-details
                        @click:append="showOpenAiApiKey = !showOpenAiApiKey"
                        @update:modelValue="updateOpenAiApiKey"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-text-field
                        v-model="tavilyApiKey"
                        :label="t('tavily-api-key')"
                        :append-icon="showTavilyApiKey ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="showTavilyApiKey ? 'text' : 'password'"
                        name="input-10-1"
                        hide-details
                        @click:append="showTavilyApiKey = !showTavilyApiKey"
                        @update:modelValue="updateTavilyApiKey"
                    ></v-text-field>
                </v-col>
            </v-row>

          </v-container>
          
  
          <template v-slot:append>
                      </template>
        </v-navigation-drawer>
</template>
<script setup lang="ts">
import { useSettingsStore } from '@/stores/settings';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
const {t} = useI18n();

const settingsStore = useSettingsStore();


const openAiApiKey = ref('');
const tavilyApiKey = ref('');
const showOpenAiApiKey = ref(false);
const showTavilyApiKey = ref(false);


const updateOpenAiApiKey = (value: string) => {
    settingsStore.updateOpenAiApiKey(value);
};

const updateTavilyApiKey = (value: string) => {
    settingsStore.updateTavilyApiKey(value);
};

</script>