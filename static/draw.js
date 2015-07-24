var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var rect = canvas.getBoundingClientRect();

var socket = io.connect('http://localhost:5000/draw_data');

var lastMoves = {};
var drawing = false;
var isNew = true;

canvas.onmousedown = function(){drawing = true};
canvas.onmouseup = function(){drawing = false; isNew = true};
canvas.onmousemove = function(e){
	if (drawing == false) return;
	socket.emit('client_to_server_move', {point: mouseToPoint(e), isNew: isNew});
	isNew = false;
}

socket.on('server_to_client_move', function(move) {
	if (typeof lastMoves[move.artist] !== 'undefined' && !move.isNew) {
		var prev = lastMoves[move.artist];
		var curr = move.point;

		ctx.beginPath();
		ctx.moveTo(prev.x, prev.y);
		ctx.lineTo(curr.x, curr.y);
		ctx.stroke();
	}
	lastMoves[move.artist] = move.point;
});

function mouseToPoint(e) {
	return {x: e.clientX - rect.left, y: e.clientY - rect.top};
}