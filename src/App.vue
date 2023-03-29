<script setup lang="ts">
import { ref } from 'vue'
import Map from './components/Map.vue'
import Wrapper from './components/Wrapper.vue'

const host = ref('localhost')
const table = ref('osm_buildings_distinct')

components: {
  Map
  Wrapper
}
</script>

<template>
    <v-app>
      <Wrapper>
        <Map :host="host" :port=8000 :table="table"/>
      </Wrapper>
    </v-app>
</template>