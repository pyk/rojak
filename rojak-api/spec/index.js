var express = require('express');
var app = express();

// Serving static files from "public" folder
app.use(express.static('public'));

app.get('/pairings', function(req, res) {
  
});
app.get('/pairings/:pairingId', function(req, res) {
  
});
app.get('/pairings/:pairingId/media-sentiments', function(req, res) {
  
});
app.get('/candidates', function(req, res) {

});
app.get('/candidates/:candidateId', function(req, res) {

});
app.get('/candidates/:candidateId/media-sentiments', function(req, res) {

});
app.get('/news', function(req, res) {

});
app.get('/news/:newsId', function(req, res) {

});
app.get('/media', function(req, res) {

});
app.get('/media/:mediaId', function(req, res) {

});
app.get('/media/:mediaId/sentiments', function(req, res) {

});

app.listen(3000, function() {
  console.log('Task api up and running...');
});
