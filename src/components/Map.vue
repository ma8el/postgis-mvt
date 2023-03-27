<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import 'ol/ol.css';
  import Map from 'ol/Map';
  import View from 'ol/View';
  import MVT from 'ol/format/MVT';
  import OSM from 'ol/source/OSM';
  import TileLayer from 'ol/layer/Tile';
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

  const accessToken = import.meta.env.VITE_MAPBOX_TOKEN

  onMounted(() => {
    var vtLayer = new VectorTileLayer({
      declutter: false,
      source: new VectorTileSource({
        format: new MVT(),
        url: `http://${host.value}:${port.value}/api/v1/mvt/${table.value}/{z}/{x}/{y}.mvt`,
      }),
      renderMode: 'vector',
      style: (feature) => {
        const building = feature.get('building');
        let color = 'rgba(176, 196, 222, 0.4)';
        let width = 1;
        let strokeColor = 'blue';

        if (building === 'industrial') {
          color = 'rgba(255, 192, 192, 0.4)';
          width = 1;
          strokeColor = 'red';
        }
        else if (building === 'commercial' || building === 'retail') {
          color = 'rgba(192, 255, 192, 0.4)';
          width = 1;
          strokeColor = 'green';
        }
        return new Style({
          stroke: new Stroke({
            color: strokeColor,
            width: width
          }),
          fill: new Fill({
            color: color
          })
        });
      }
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
    });

    map.on('click', function(evt) {
      map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
        console.log(feature.getProperties());
      });
    });
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