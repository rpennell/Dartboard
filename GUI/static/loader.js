var channels = {
   html: {
      socket: null,

      start: function() {
         channels.html.socket = new WebSocket("ws://" + location.host + "/html");
         channels.html.socket.onmessage = function(event) {

         }
      }
   },

   data: {
      socket: null,

      start: function() {
         channels.socket = new WebSocket("ws://" + location.host + "/data");
         channels.socket.onmessage = function(event) {

         }
      }
   }
};
