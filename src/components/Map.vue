<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import 'ol/ol.css';
  import Map from 'ol/Map';
  import View from 'ol/View';
  import TileLayer from 'ol/layer/Tile';
  import OSM from 'ol/source/OSM';
  import MVT from 'ol/format/MVT';
  import VectorTileLayer from 'ol/layer/VectorTile';
  import VectorTileSource from 'ol/source/VectorTile';
  import {Stroke, Style, Fill} from 'ol/style.js';
  import { fromLonLat } from 'ol/proj';
  
  const props = defineProps<{
                  host: String;
                  port: Number;
                  table: String;
                }>();

  const host = ref(props.host);
  const port = ref(props.port);
  const table = ref(props.table);

  onMounted(() => {
    var vtLayer = new VectorTileLayer({
      declutter: false,
      source: new VectorTileSource({
        format: new MVT(),
        url: `http://${host.value}:${port.value}/mvt/${table.value}/{z}/{x}/{y}.mvt`,
      }),
      renderMode: 'vector',
      style: new Style({
          stroke: new Stroke({
            color: 'blue',
            width: 1
          }),
      fill: new Fill({
        color: 'rgba(176, 196, 222, 0.4)'
      })
      })
    });
  
    const map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
        vtLayer,
      ],
      view: new View({
        center: fromLonLat([8.6821, 50.1109]),
        zoom: 13,
      }),
    })
  });
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