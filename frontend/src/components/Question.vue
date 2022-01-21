<template>
  <div class="container ">
    <div class="card">
      <div class="form-group">
        <label>{{ question.text }}</label>
      </div>
      <div v-for="choice in question.choices" class="form-check">
        <input v-model="choice.isSelected" class="form-check-input" type="checkbox" :id="`flexCheckDefault-${choice.id}`">
        <label class="form-check-label" :for="`flexCheckDefault-${choice.id}`">
          {{ choice.text }}
        </label>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "Question",
  props: ['question'],
}
</script>

<style scoped>

</style>