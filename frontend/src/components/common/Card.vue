<template>
  <div class="bg-white dark:bg-[#16213e] rounded-lg shadow-md p-6 border border-gray-100 dark:border-[#2d3748] transition-colors duration-300">
    <div v-if="title" class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">{{ title }}</h3>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string;
}

defineProps<Props>();
</script>
