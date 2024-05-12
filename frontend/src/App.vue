<template>
  <v-card>
    <v-layout>
      <Sidebar />
      <v-main>
        <v-card>
          test
        </v-card>
      </v-main>
    </v-layout>
  </v-card>
 
 
</template>
<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import Sidebar from './components/sidebar.vue';

const {t} = useI18n();
</script>