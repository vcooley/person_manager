var defaultPerson = {
  id: null,
  firstName: '',
  lastName: '',
  birthDate: '',
  zipCode: null
};

var defaultMessage = {className: '', message: ''};

var vm = new Vue({
  el: '#app',
  data: {
    person: Object.assign({}, defaultPerson),
    showPerson: null,
    removePerson: null,
    retrievedPersons: [],
    message: Object.assign({}, defaultMessage)
  },
  methods: {
    handleCreate: function(e){
      this.$http.post('/person/', this.person)
        .then(function(data) {
          this.$set('message', {className: 'alert-success', message: 'Successfully added person.'});
        })
    },
    handleRetrieve: function(){
      var id = this.person.id === null ? '' : this.person.id;
      this.$http.get('/person/' + id)
        .then(function(data) {
          var persons = JSON.parse(data.body).persons;
          console.log(persons)
          this.$set('retrievedPersons', Array.isArray(persons) ? persons : [persons])
        })
    },
    handleUpdate: function(e){
      if (this.person.id === null) {
        this.message = {className: 'alert-danger', message: 'You must enter an id.'};
        return;
      }
      this.$http.put('/person/' + this.person.id, this.person)
        .then(function(data) {
          this.$set('message', {className: 'alert-success', message: 'Successfully added person.'});
        });
    },
    handleDelete: function(){
      if (this.person.id === null) {
        this.message = {className: 'alert-danger', message: 'You must enter an id.'};
        return;
      }
      this.$http.delete('/person/' + this.person.id)
        .then(function(data) {
          this.$set('message', {className: 'alert-success', message: 'Person deleted.'})
        })
    },
    clearMessage: function() {
      this.message = Object.assign({}, defaultMessage);
    },
    clearPerson: function() {
      this.person = Object.assign({}, defaultPerson);
    },
    clearAll: function() {
      this.clearMessage();
      this.clearPerson();
    }
  }
});