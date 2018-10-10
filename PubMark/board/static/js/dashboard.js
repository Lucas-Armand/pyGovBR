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

	d3.selectAll("p").style("color", "white");
	
	//ctx.restore();
}

function LoadDoughnutChart(elementId,Data){

	data = {
		datasets: [{
			data: Data['count'],
			backgroundColor: ["#f4c309","#fd8609","#e04408","#d4191f","#ee2151","#f33d87","#ca4eb0","#7c57b1","#2266af","#15a4d6","#1cdeed","#1fedc9","#1fedc9","#408f0d","#a3bb07"]

		}],

		// These labels appear in the legend and in the tooltips when hovering different arcs
		labels: Data['name']
	};


	var ctx = document.getElementById(elementId).getContext('2d');                  
	var myDoughnutChart = new Chart(ctx, {                                          
		type: 'doughnut',                                                           
		data: data,                                                                 
		options:{responsive: true,                                                  
				'onClick' : function (evt, item) {                                  
								console.log ('legend onClick', evt, item);          
						},} 

		}
	)
}

function LoadBarChart(elementId,data,key1,key2){
	
	svg = document.getElementById(elementId);

	var series = d3.stack()
	    .keys([key2])
	    .offset(d3.stackOffsetDiverging)
	    (data);

	var svg = d3.select("svg#"+elementId),
	    margin = {top: 20, right: 30, bottom: 30, left: 60},
	    width = +svg.attr("width"),
	    height = +svg.attr("height");

	var svg = d3.select("svg#"+elementId),
	    margin = {top: 20, right: 30, bottom: 30, left: 60},
	    width = +svg.attr("width"),
	    height = +svg.attr("height");

	var x = d3.scaleBand()
	    .domain(data.map(function(d) { return d[key1]; }))
	    .rangeRound([margin.left, width - margin.right])
	    .padding(0.1);

	var y = d3.scaleLinear()
	    .domain([d3.min(series, stackMin), d3.max(series, stackMax)])
	    .rangeRound([height - margin.bottom, margin.top]);

	var z = d3.scaleOrdinal(d3.schemeCategory10);

	svg.append("g")
	  .selectAll("g")
		.attr("class", "svg")
	  .data(series)
	  .enter().append("g")
	    .attr("fill", function(d) { return z(d.key); })
	  .selectAll("rect")
	  .data(function(d) { return d; })
	  .enter().append("rect")
		.attr("class", "rect")
	    .attr("width", x.bandwidth)
	    .attr("x", function(d) { return x(d.data[key1]); })
	    .attr("y", function(d) { return y(d[1]); })
	    .attr("height", function(d) { return y(d[0]) - y(d[1]); })


	svg.append("g")
	    .attr("transform", "translate(0," + y(0) + ")")
	    .call(d3.axisBottom(x))
	   .selectAll("text")
		.attr("transform", "rotate(-10)" );

	svg.append("g")
	    .attr("transform", "translate(" + margin.left + ",0)")
	    .call(d3.axisLeft(y));

	function stackMin(serie) {
	  return d3.min(serie, function(d) { return d[0]; });
	}

	function stackMax(serie) {
	  return d3.max(serie, function(d) { return d[1]; });
	}
}

