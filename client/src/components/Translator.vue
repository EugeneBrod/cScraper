<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>craigslist scraper</h1>
        <hr><br><br>
        <alert :message="finishedMessage" v-if="finished"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>settings</button>
        <br><br>
        <div class="btn-group" role="group">
          <button type="button" class="btn btn-warning btn-sm" @click="startSubscription()">
            subscribe</button>
          <button type="button" class="btn btn-danger btn-sm" @click="startCancel()">cancel</button>
        </div>
        <br><br>
        <!-- <table class="table table-hover">
          <tbody>
            <tr v-for="(listing, index) in listings" :key="index">{{ listing }}></tr>
          </tbody>
        </table> -->
      </div>
    </div>
    <div v-text="progress" id="app"></div>
    <div v-text="plainText" id="app"></div>
    <div v-text="encryptedText" id="app"></div>
    <b-modal ref="addBookModal"
         id="book-modal"
         title="scraper settings:"
         hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                label="email addresses for sending listings of new posts."
                label-for="form-title-input">
          <b-form-input id="form-title-input"
                    type="text"
                    v-model="setStringsForm.emails"
                    required
                    placeholder="enter space separated email addresses.">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                  label="searches to scrape"
                  label-for="form-author-input">
          <b-form-input id="form-author-input"
                      type="text"
                      v-model="setStringsForm.urls"
                      required
                      placeholder="enter space separated urls of search queries">
          </b-form-input>
        </b-form-group>
        <br><br>
        <b-button type="submit" variant="primary">submit</b-button>
        <b-button type="reset" variant="danger">reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      setStringsForm: {
        string: '',
        transformationString: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    start() {
      const path = 'http://localhost:5000/start';
      axios.get(path)
        .then((res) => {
          console.log(res.data.success);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    stop() {
      const path = 'http://localhost:5000/stop';
      this.occupied = false;
      axios.get(path)
        .then((res) => {
          console.log(res.data.success);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    setSettings(payload) {
      const path = 'http://localhost:5000/setSettings';
      axios.post(path, payload)
        .then((res) => {
          console.log(res.data.success);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    initForm() {
      this.setStringsForm.emails = '';
      this.setStringsForm.urls = '';
    },
    startSubscription() {
      this.start();
    },
    startCancel() {
      this.stop();
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        recipient_emails: this.setStringsForm.emails.split(' '),
        urls: this.setStringsForm.urls.split(' '),
      };
      console.log(payload);
      this.setSettings(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
  },
  created() {
  },
};
</script>
