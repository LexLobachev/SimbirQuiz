<template>
  <div class="container ">

    <h2>{{ quiz.title }}</h2>

    <div v-if="!hasResult && curQuestion">
      <Question :question="curQuestion"></Question>
      <br>
      <div>
        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item" :disabled="isFirstQuestion" @click="onPrev"><a class="page-link">Previous</a></li>
            <li class="page-item" v-for="quest in quiz.questions">
              <a class="page-link" :class="{'bg-info': (quest === curQuestion)}" href="#"
                 @click="goToQuestion(quest.idx)">{{ quest.idx + 1 }}</a>
            </li>
            <li class="page-item" :disabled="isLastQuestion" @click="onNext"><a class="page-link">Next</a></li>
          </ul>
        </nav>
      </div>

      <div>
        <button @click="submitQuiz">Отправить на проверку</button>
      </div>
    </div>


    <div class="container" v-if="hasResult">
      <h2>Тест завершен</h2>
      <div class="row justify-content-center">
        <div class="col-4">
          Ваш показатель: {{ testResult }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Question from "./Question";

export default {
  name: "Quiz",
  components: {Question},
  props: ['quizPassId'],
  data() {
    return {
      quiz: {
        title: '',
        questions: [],
      },
      testResult: null,
      curQuestion: null
    }
  },

  mounted: function () {
    this.refreshData();
    console.log(this.hasResult)
  },

  computed: {
    isLastQuestion() {
      return this.curQuestion.idx === this.quiz.questions.length - 1;
    },

    isFirstQuestion() {
      return this.curQuestion.idx === 0;
    },

    hasResult() {
      return typeof this.testResult === 'number' && isFinite(this.testResult);
    }
  },

  methods: {
    refreshData() {
      axios.get(`/quiz/${this.quizPassId}/`)
          .then((response) => {
            this.quiz = response.data;
            this.quiz.questions.forEach((el, idx) => el.idx = idx)
            this.curQuestion = this.quiz.questions[0]
          })
    },

    onPrev() {
      if (!this.isFirstQuestion) {
        this.curQuestion = this.quiz.questions[this.curQuestion.idx - 1]
      }
    },

    onNext() {
      if (!this.isLastQuestion) {
        this.curQuestion = this.quiz.questions[this.curQuestion.idx + 1]
      }
    },

    goToQuestion(idx) {
      this.curQuestion = this.quiz.questions[idx];
    },

    submitQuiz() {
      axios.post(`/quiz/${this.quizPassId}/submit/`,
          this.quiz.questions.map(q => {
                return {
                  question_id: q.id,
                  choice_ids: q.choices.filter(c => c.isSelected).map(c => c.id)
                }
              }
          )
      )
          .then(resp => {
            this.curQuestion = null;
            this.testResult = resp.data.result;
            console.log(this.testResult, this.hasResult)
          })
    }
  }
}
</script>
