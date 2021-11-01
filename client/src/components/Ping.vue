<template>
  <div class = "container">
    <button type = "button" class = "btn btn-primary">{{ msg }} </button>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
      counter: 0,
    };
  },
  methods: {
    incrementcounter() {
      this.counter = '0';
    },
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
    this.incrementcounter();
  },
};
</script>
