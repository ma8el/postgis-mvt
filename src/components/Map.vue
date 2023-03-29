<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue'
  import 'ol/ol.css';
  import Map from 'ol/Map';
  import MVT from 'ol/format/MVT';
  import View from 'ol/View';
  import OSM from 'ol/source/OSM';
  import TileLayer from 'ol/layer/Tile';
  import VectorTileLayer from 'ol/layer/VectorTile';
  import VectorTileSource from 'ol/source/VectorTile';
  import {Stroke, Style, Fill} from 'ol/style.js';
  import { fromLonLat } from 'ol/proj';
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

  ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
  
  const props = defineProps<{
                  host: String;
                  port: Number;
                  table: String;
                }>();

  const host = ref(props.host);
  const port = ref(props.port);
  const table = ref(props.table);

  const buildingName = ref('Click on a building');
  const buildingType = ref('Click on a building');
  const numberOfBuildings = ref(50);
  const numberOfRetailBuildings = ref(0);
  const numberOfIndustrialBuildings = ref(0);

//  const chartData = ref(
//    [numberOfBuildings.value,
//    numberOfRetailBuildings.value,
//    numberOfIndustrialBuildings.value]
//  );

  const options = ref({
    responsive: true,
  })

  const data = computed(() => {
    return {
    labels: ['Buildings', 'Retail', 'Industry'],
    datasets: [{
      label: '# of Buildings',
      data: [numberOfBuildings.value, numberOfRetailBuildings.value, numberOfIndustrialBuildings.value],
      backgroundColor: [
        'rgba(176, 196, 222, 0.5)',
        'rgba(192, 255, 192, 0.5)',
        'rgba(255, 192, 192, 0.5)',
      ],
      borderColor: [
        'rgba(176, 196, 222, 1)',
        'rgba(192, 255, 192, 1)',
        'rgba(255, 192, 192, 1)',
      ],
      borderWidth: 1
    }]
    }
  });

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
        buildingType.value = feature.get('building');
        buildingName.value = feature.get('name');
      });
    });

    map.on('pointermove', function(evt) {
      if (evt.dragging) {
        return;
      }
      var pixel = map.getEventPixel(evt.originalEvent);
      var hit = map.hasFeatureAtPixel(pixel);
      map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    });

    map.on('moveend', function(evt) {
      numberOfBuildings.value = 0;
      numberOfIndustrialBuildings.value = 0;
      numberOfRetailBuildings.value = 0;
      let extent = map.getView().calculateExtent(map.getSize());
      const source = vtLayer.getSource();
      if (source) {
        const features = source.getFeaturesInExtent(extent);
        features.forEach((feature) => {
          if (feature.get('building') === 'retail') {
            numberOfRetailBuildings.value += 1;
          }
          else if (feature.get('building') === 'industrial') {
            numberOfIndustrialBuildings.value += 1;
          }
        });
        numberOfBuildings.value = features.length;
        data.value.datasets[0].data = [
          numberOfBuildings.value,
          numberOfRetailBuildings.value,
          numberOfIndustrialBuildings.value
        ]
        console.log(data.value.datasets[0])
      }
      })
    });
</script>

<template>
  <div id="map" ref="map"></div>
  <div class="metadata">
    <h2>Selected Building</h2>
    <li class="no-bullet">Building Name: {{ buildingName }}</li>
    <li class="no-bullet">Building Type: {{ buildingType }}</li>
    <hr>
    <h2>Buildings in View</h2>
    <li class="no-bullet">Number of Buildings: {{ numberOfBuildings }}</li>
    <li class="no-bullet">Number of Retail Buildings: {{ numberOfRetailBuildings }}</li>
    <li class="no-bullet">Number of Industrial Buildings: {{ numberOfIndustrialBuildings }}</li>
    <Bar
      id="my-chart-id"
      :options="options"
      :data="data"
    />
  </div>
</template>

<style scoped>

#map {
  position: absolute;
  height: 90%;
  width: 100%;
}
.no-bullet {
  list-style-type: none;
}

.metadata {
  position: absolute;
  right: 0;
  background-color: rgba(255, 255, 255, 0.8);
  font-size: 1.1em;
  font-weight: bold;
  width: 300px;
  height: 100vh;
}


</style>