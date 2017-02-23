var link = {
   // WebSocket object
   socket: null,

   // max number of requests the link will take.  negative numbers are interpreted as infinity.
   request: -1,

   // start socket
   start: function() {
      var self = link;
      self.socket = new WebSocket('ws://' + location.host + '/data');
      self.socket.onmessage = function(event) {
         // if we have exceeded our max requests, do nothing
         if (self.requests > 0) {
            self.requests--;
         } else if (self.requests == 0) {
            return;
         }

         // parse the request and log it
         var data = JSON.parse(event.data);
         console.log(data);

         // update html
         // if !(data.html === '') {
         var global = document.getElementById('global')
         global.innerHTML = data.html;
         // }

         // execute code if present
         var codes = global.getElementsByTagName('script');
         for (var i=0; i<codes.length; i++) {
            eval(codes[i].text);
         }

         // update dispayable data
         update(data);
      }
   },

   // close socket
   end: function() {
      link.socket.close()
   }
};
