
var margin = {top: 30, right: 50, bottom: 150, left: 90};
var svgWidth = 1000;
var svgHeight = 550;
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var activeScene = 0;

var graphData = JSON.parse(data[tableData[activeScene].name]);

$('#descr').text(tableData[activeScene].descr);


var select_bar = d3.select('#dropdown_bar')
    .append('select')
        .attr('class','select_bar')
        .on('change',onchange_bar);

function onchange_bar() {
    selectValue = d3.select('.select_bar').property('value')
    activeScene = parseInt(selectValue);
    graphData = JSON.parse(data[tableData[activeScene].name]);
    $('#descr').text(tableData[activeScene].descr);
    updateBarChart();
};

var options = select_bar
    .selectAll('option')
    .data(tableData).enter()
    .append('option')
      .text(function (d) { return d.display; })
      .attr('value', function(d) { return d.num;});

var y = d3.scaleLinear()
    .range([ height,0]);  


var x = d3.scaleBand()
    .padding(0.1)
    .range([0,width]);

var svg = d3.select(".svg_canvas").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class","xAxis");

// Add the Y Axis
svg.append("g")
    .attr("class","yAxis");


var tooltip = d3.select("#navbar")
 .append("div")
 .attr("class", "toolTip");

var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

updateBarChart = function() {

    var names = graphData.map(function(item) {
        return item.name;
    });
    
    var values = graphData.map(function(item) {
        return item.count;
    });
    

    x.domain(names);
    
    x.domain(graphData.map(function(d) { return d.name; }));
    y.domain([ d3.min(graphData, function(d) { return d.count; })*.9, d3.max(graphData, function(d) { return d.count; })*1.1]);


    var y_axis = svg.selectAll(".yAxis")
        .data(["dummy"]);
    var new_y_axis = y_axis.enter().append("g")
        .attr("class", "yAxis")

    y_axis.merge(new_y_axis).call(d3.axisLeft(y)) 

    d3.select(".xAxis").remove();
    d3.select(".yAxis").remove();
    d3.select(".xlabel").remove();
    d3.select(".ylabel").remove();

    svg.append("g")
        .attr("class", "xAxis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65)");

    svg.append("text")
        .attr("class", "xlabel")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text(tableData[activeScene].ylabel);

           
    // add y-axis
    svg.append("g")
        .attr("class", "yAxis")
        .call(d3.axisLeft(y))
            .append("text") // and text1
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .style("font-size", "16px");
            
    svg.append("text")
        .attr("class", "ylabel")           
        .attr("transform",
                "translate(" + (width/2) + " ," + 
                                (height + margin.top + 60) + ")")
        .style("text-anchor", "middle")
        .text(tableData[activeScene].xlabel);

    if (tableData[activeScene].type == 'bar') {
    var bars = svg.selectAll(".bar")
        .remove()
        .exit()
        .data(graphData)
    bars.enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.name); })
        .attr("width", 20)
        .attr("y", function(d) { return y(d.count); })
        .attr("height", function(d) { return height - y(d.count); })
        .attr('fill', tableData[activeScene].color)
        .on("mouseover", function(d) {
            div.transition()		
                .duration(200)		
                .style("opacity", .9);
            div.html("<strong>" +d.name+": "+d.count.toLocaleString('en', {useGrouping:true})+"</strong>")
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY-20) + "px")
                .style("display", "inline-block")
        })
        .on("mouseout", function(d) {		
            div.transition()		
                .duration(500)		
                .style("opacity", 0)	
        });
    }

    if (tableData[activeScene].type == 'point') {
    var bars = svg.selectAll(".bar")
        .remove()
        .exit()
        .data(graphData)
    bars.enter()
        .append('circle')
        .attr("class", "bar") 
        .attr("r", 10)
        .attr('fill', tableData[activeScene].color)         
        .attr("cx", function(d) { return x(d.name); })
        .attr("cy", function(d) { return y(d.count); })
        .on("mouseover", function(d) {
            div.transition()		
                .duration(200)		
                .style("opacity", .9);
            div.html("<strong>" +d.name+": "+d.count.toLocaleString('en', {useGrouping:true})+"</strong>")
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY-20) + "px")
                .style("display", "inline-block")
        })
        .on("mouseout", function(d) {		
            div.transition()		
                .duration(500)		
                .style("opacity", 0)	
        });
    }
}