<script setup lang="ts">
import Map from './components/Map.vue'
import Wrapper from './components/Wrapper.vue'

components: {
  Map
  Wrapper
}
</script>

<template>
    <v-app>
      <Wrapper>
        <Map />
      </Wrapper>
    </v-app>
</template>
