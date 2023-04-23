<script setup lang="ts">
  import { ref } from 'vue'
  import { Bar } from 'vue-chartjs'

  interface ChartData {
    buildings: number;
    retail: number;
    industry: number;
  }

  const chartData = ref<ChartData>({buildings: 0, retail: 0, industry: 0})

  const data = ref({
    labels: ['Buildings', 'Retail', 'Industry'],
    datasets: [{
      label: '# of Buildings',
      data: [chartData.value.buildings, chartData.value.retail, chartData.value.industry],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
      ],
      borderWidth: 1
    }]
  })

  const options = ref({
    responsive: true,
  })

  const props = defineProps<{
      chartData: ChartData;
  }>()
</script>

<template>
    <Bar
      id="bar-cahrt"
      :data="data"
      :options = "options"
    />
</template>