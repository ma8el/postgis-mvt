<template>
    <header>
      <v-toolbar class="bg-teal" density="compact">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title>Postgis MVT</v-toolbar-title>

        <v-spacer></v-spacer>
      </v-toolbar>
    </header>
    <div class="content">
      <slot></slot>
    </div>
    <v-footer class="d-flex flex-column ma-0 pa-0 w-100" app>
      <div class="bg-teal d-flex w-100 align-center px-4">
        <strong>Checkout my Map!</strong>
        <v-spacer></v-spacer>
      </div>
  
      <div class="px-4 py-2 bg-black text-center w-100">
        {{ new Date().getFullYear() }} — <strong>Map</strong>
      </div>
    </v-footer>
</template>
<style>
.content {
  width: 100%;
}
</style>