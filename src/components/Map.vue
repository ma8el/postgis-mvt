<script setup lang="ts">
import { onMounted } from 'vue'
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.vectorgrid';

onMounted(() => {
  const map = L.map('map').setView([50.110924, 8.682127], 13);
  L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  const vectorTileOptions = {
    vectorTileLayerStyles: {
      layerName: (properties: any, zoom: any) => ({
        color: "#3388ff",
        weight: 2,
        fillColor: "#3388ff",
        fillOpacity: 0.5,
      }),
    },
    interactive: true,
    crossOrigin: 'anonymous',
    getFeatureId: (feature: any) => feature.properties.id,
  };

  const url = `http://localhost:8000/mvt/postgis_mvt_source_mercator/{z}/{x}/{y}.mvt`;
  L.vectorGrid.protobuf(url, vectorTileOptions).addTo(map);
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