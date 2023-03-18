<script setup lang="ts">
import { onMounted } from 'vue'
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

onMounted(() => {
  const map = L.map('map').setView([51.505, -0.09], 13);
  L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

})
</script>

<template>
  <div id="map"></div>
</template>

<style scoped>

#map {
  position: absolute;
  height: 90%;
  width: 100%;
}

</style>