<template>
  <div class="home">

    <div class="features">
      <br>
      <h2>Выберите тест</h2>
      <br>
        <div v-for="quiz in quizes">
          <div class="alert alert-warning">
            <h3>{{ quiz.title }}</h3>
            <h5>Количество вопросов: {{ quiz.questions_count }}</h5>
            <a @click="startQuiz(quiz.id)" class="btn btn-warning">Пройти тестирование</a>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      quizes: [],
    }
  },
  methods:{
    refreshData(){
      axios.get('/quiz/')
      .then((response)=>{
        console.log(response.data);
        this.quizes = response.data;
      })
    },

    startQuiz(quizId) {
      axios.post(`quiz/${quizId}/start/`)
        .then(resp => {
          let quizPassId = resp.data.quiz_pass_id;
          this.$router.push(`/quiz/${quizPassId}/`)
        })

    }
  },
  mounted: function(){
    this.refreshData();
  }
}
</script>
