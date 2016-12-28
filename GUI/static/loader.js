var channels = {
   html: {
      socket: null,

      start: function() {
         html.socket = new WebSocket("ws://" + location.host + "/html");
         html.socket.onmessage = function(event) {

         }
      }
   },

   data: {
      socket: null,

      start: function() {
         data.socket = new WebSocket("ws://" + location.host + "/data");
         data.socket.onmessage = function(event) {

         }
      }
   }
};
