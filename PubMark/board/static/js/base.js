function LoadCanvas(elementId, nome, valor, color){
	var canvas = document.getElementById(elementId);
	var ctx = canvas.getContext('2d');
	var x_size = 262;
	var y_size = 156;

	// Criando o retangulo
	ctx.fillStyle = color;
	ctx.fillRect(0, 0, x_size, y_size);

	// Criand o titulo
	ctx.font = 'bold 12px arial';
	ctx.textAlign = 'center';
	ctx.textBaseline =  "top";
	ctx.fillStyle = 'white';
	ctx.fillText( nome, x_size/2, 10);

	// Criando o Indicador
	ctx.font = '32px serif';
	ctx.textAlign = 'center';
	ctx.textBaseline =  "middle";
	ctx.fillStyle = 'white';
	ctx.fillText(valor , x_size/2, y_size/2);
	
	//ctx.restore();
}

		
