// var optionData = {
// 	State: 0,
// 	Data:	[["x01", "BattleShip"],
// 		  	["Option 1", "Option 2", "Option 3"],
// 	  	  ["301", "501", "701"]]
// };
//
// var battlefieldData = {
// 	State: 1,
// 	Data: {
// 		Heading: ["Battlefield", "Round", "Throw"],
// 		PlayerNames: ["Scott", "Trent", "Ryan"],
// 		PlayerScores: ["ScottScore", "TrentScore", "RyanScore"]
// 	}
// };
//
// var x01Data = {
// 	State: 2,
// 	Data: {
// 		Heading: ["X01", "Round", "Throw"],
// 		PlayerNames: ["Scott", "Trent", "Ryan"],
// 		PlayerScores: ["ScottScore", "TrentScore", "RyanScore"]
// 	}
// };
//
// var winnerData = {
// 	State: 3,
// 	Data: ["Scott"]
// };
//
// var all=[optionData, battlefieldData, x01Data, winnerData]
var begin = '{"State": 0, "Data": [["X01", "Battleship"], ["Players", "Score", "Start"], ["2", "3", "4", "1"]]}';

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/chatsocket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function(data) {
        generate(data);
    }
};

function generate(data) {
	console.log(data)
	switch (data.State) {
		case(0):
			generateOptions(data.Data);
			break;
		case(1):
			switch(data.Data.Name) {
				case('X01'):
					generatex01(data.Data);
					break;
				case('Battleship'):
					generateBattleship(data.Data);
					break;
				}
			break;
		case(2):
			generateWinner(data.Data);
			break;
	}
}

function clear(id) {
	document.getElementById(id).innerHTML="";
}

function generateOptions(list) {
	generateTitle("title", ["Welcome to Dartboard", "Options"]);
	generateParagraph("game", list[0]);
	generateParagraph("option", list[1]);
	generateParagraph("selection", list[2]);
}

function generateBattleship(list) {
	generateTitle("title", [list.Name, "Round: " + list.Round, "Throw: " + list.Throw]);
	generateParagraph("game", list.Players);
	generateParagraph("option", list.Scores);
	generateBeer("selection", 1);
}

function generatex01(list) {
	generateTitle("title", [list.Name, "Round: " + list.Round, "Throw: " + list.Throw]);
	generateParagraph("game", list.Players);
	generateParagraph("option", list.Scores);
	generateBeer("selection", 1);
}

function generateWinner(list) {
	generateTitle("title", ["Congratulations!", list[0], "You are the Winner!"]);
	hellaBeer(1);
}

function hellaBeer(num) {
	generateBeer("game", num);
	generateBeer("option", num);
	generateBeer("selection", num);
}

function generateParagraph(id, list) {
	clear(id);
	generateDarts(id, 17);
	list.forEach(function(item) {
		var node = document.createElement("p");
		var textnode = document.createTextNode(item);
		node.appendChild(textnode);
		document.getElementById(id).appendChild(node);
	})
}

function generateTitle(id, list) {
	clear(id);
	list.forEach(function(item) {
		var node = document.createElement("h2");
		var textnode = document.createTextNode(item);
		node.appendChild(textnode);
		document.getElementById(id).appendChild(node);
	})
}

function generateBeer(id, num) {
	clear(id);
	for (i = 0; i < num; i++) {
		var node = document.createElement("i");
		node.className = " em em-beer";
		document.getElementById(id).appendChild(node);
	}
}

function generateDarts(id, num) {
	clear(id);
	for (i = 0; i < num; i++) {
		var node = document.createElement("i");
		node.className = " em em-dart";
		document.getElementById(id).appendChild(node);
	}
}
