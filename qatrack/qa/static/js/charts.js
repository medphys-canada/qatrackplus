"use strict";

var last_requested_data;

/*************************************************************************/
//return all checked checkboxes within container
function get_checked(container){
    var vals =  [];
    $(container+" input[type=checkbox]:checked").each(function(i,cb){
        vals.push(cb.value);
    });
    return vals;
}

/*************************************************************************/
//Clean up after Control Chart created
var waiting_timeout = null;
function check_cc_loaded(){

	if ($("#control-chart-container img").height()>100){
		$("#control-chart-container div.please-wait").remove();
		clearInterval(waiting_timeout);
		finished_chart_update()
	}
}
/*************************************************************************/
//generate a url to allow linking directly to chart
function set_chart_url(){
	$("#chart-url").val("not implemented yet");
	var filters = get_data_filters();
	filters.from_date = [filters.from_date];
	filters.to_date = [filters.to_date];

	var options = [];

	$.each(filters,function(key,values){
		$.each(values,function(idx,value){
			options.push(key+QAUtils.OPTION_DELIM+value)
		});
	});

	var loc = window.location.protocol + "//"+window.location.hostname+":"+window.location.port+window.location.pathname;

	$("#chart-url").val(loc+"#"+options.join(QAUtils.OPTION_SEP));
}

/**************************************************************************/
//set initial options based on url hash
function set_options_from_url(){
    var options = QAUtils.options_from_url_hash(document.location.hash);
	var f,o;
	var clear_if_option_exists = ["unit", "test"];
	for (f in clear_if_option_exists){
		for (o in options){
			if (clear_if_option_exists[f] == options[o][0]){
				$("#"+clear_if_option_exists[f]+"-filter input").attr("checked",false);
				break;
			}
		}
	}

	var key,value;
    $.each(options,function(idx,option){
		key = option[0];
		value = option[1];
        switch(key){
            case  "slug" :
                $("#test-filter input[value="+value+"]").attr("checked","checked");
            break;
            case "unit":
                $("#unit-filter input[value="+value+"]").attr("checked","checked");
                break;
            default:
                break;
        }

    });
    update();
}
/**************************************************************************/
function get_control_chart_url(){
	var filters = get_data_filters();

	var	props = [
		"width="+$("#chart-container").width(),
		"height="+$("#chart").height(),
		"timestamp="+ new Date().getTime()
	];

	$.each(filters,function(k,v){
		if(	$.isArray(v)){
			$.each(v,function(i,vv){
				props.push(encodeURI(k+"[]="+vv));
			});
		}else{
			props.push(encodeURI(k+"="+v));
		}
	});

	return QACharts.control_chart_url+"?"+props.join("&");
}



function toggle_instructions(){
	$("#instructions").toggle();

	var visible = $("#instructions").is(":visible");
	var icon = "icon-plus-sign";
	if (visible) {
		icon = "icon-minus-sign";
	}

	$("#toggle-instructions i").removeClass("icon-plus-sign icon-minus-sign").addClass(icon);

}


function initialize_charts(){
	create_stockchart([{name:"",data:[[new Date().getTime(),0]]}]);
}
function switch_chart_type(){
	$("#chart-container, #control-chart-container").toggle();
}

function hide_all_tests(){
	$("#test input").parent().hide();
}

function update_tests(){
	var frequencies = get_selected_option_vals("#frequency");
	filter_test_lists(frequencies);
	
	var test_lists = get_checked("#test-list-container");
	var tests = get_tests_for_lists(test_lists);
	var categories = get_selected_option_vals("#category");


	var to_show = filter_tests(tests,categories,frequencies);
	show_tests(to_show);
}
function filter_test_lists(frequencies){
	var test_lists = get_test_lists_for_frequencies(frequencies);

	$("#test-list-container input").each(function(i,option){
		var pk = $(this).val();
		if (test_lists.indexOf(pk)>=0){
			$(this).parent().show();
		}else{
			$(this).attr("checked",false)
			$(this).parent().hide();
		}
	});
}

function get_test_lists_for_frequencies(frequencies){
	
	var test_lists = [];

	var i;
	$.each(frequencies,function(i,frequency){
		$.each(QACharts.test_info.test_lists,function(pk,test_list){				
			if (test_list.frequencies.indexOf(frequency)>=0){
				test_lists.push(pk)
			}
		});
	});

	return test_lists;

}


function get_selected_option_vals(select_id){
	var selected = [];

	$(select_id).find(":selected").each(function(){
		selected.push(parseInt($(this).val()));
	});
	return selected;
}

function get_tests_for_lists(test_lists){
	var all_tests = [];
	var tests,test_list;
	var i;
	$.each(test_lists,function(i,pk){
		test_list =  QACharts.test_info.test_lists[pk];
		if (test_list){
			all_tests.push.apply(all_tests,test_list.tests);
		}
	});

	return all_tests;
}

function filter_tests(tests,categories,frequencies){
	var filtered = [];
	$.each(QACharts.test_info.tests,function(idx,test){
		if (
				(categories.indexOf(test.category)>=0) &&
				(tests.indexOf(test.pk) >= 0)
			){
			filtered.push(test.pk);
		}
	});
	return filtered;
}

function show_tests(visible_tests){
	$("#test input").each(function(i,option){
		var pk = parseInt($(this).val());
		if (visible_tests.indexOf(pk) >= 0){
			$(this).parent().show();
		}else{
			$(this).attr("checked",false);
			$(this).parent().hide();
		}
	});
}

function update_chart(){
	start_chart_update();
	set_chart_url();
	if (basic_chart_selected()){
		create_basic_chart();
	}else{
		create_control_chart();
	}
}

function basic_chart_selected(){
	return $("#chart-type").val() === "basic";
}

function retrieve_data(callback,error){
	var data_filters = get_data_filters();
	if (data_filters.tests.length === 0){
		initialize_charts();
		finished_chart_update();
		return;
	}

	$.ajax({
            type:"get",
            url:QACharts.data_url,
            data:data_filters,
            contentType:"application/json",
            dataType:"json",
            success: function(result,status,jqXHR){
				last_requested_data = result;
                finished_chart_update();
				callback(result);
            },
            error: function(error){
				last_requested_data = {};
                finished_chart_update();
                if (typeof console != "undefined") {console.log(error)};
            }
	});

}
function create_basic_chart(){
	retrieve_data(plot_data);
}

function plot_data(data){
	var data_to_plot = convert_data_to_highchart_series(data.data);
	create_stockchart(data_to_plot);
	update_data_table(data);
}

function create_stockchart(data){
	window.chart = new Highcharts.StockChart({
            chart : {
                renderTo : 'chart'
            },

            rangeSelector : get_range_options(),

			legend: get_legend_options(),

            plotOptions: {
                series: {
					lineWidth : get_line_width(),
					marker : {
						enabled : true,
						radius : 4
					}
                },
				line:{
					animation:false
				}
            },

            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change})<br/>',
                valueDecimals: 2
            },

            series : data
	});

}

function get_range_options(){
	return {
		buttons: [{
				type: 'week',
				count: 1,
				text: '1w'
			},{
				type: 'month',
				count: 1,
				text: '1m'
			},{
				type: 'month',
				count: 6,
				text: '6m'
			},{
				type: 'year',
				count: 1,
				text: '1y'
			},{
				type: 'all',
				text: 'All'
			}
		],
		selected: 1
	}
}

function get_legend_options(){
	var legend = {};
	if ($("#show-legend").is(":checked")){
		legend = {
			align: "right",
			layout: "vertical",
			enabled: true,
			verticalAlign: "middle"
		}
	}
	return legend;
}

function get_line_width(){
	if ($("#show-lines").is(":checked")){
		return 2;
	}else{
		return 0;
	}
}

function convert_data_to_highchart_series(data){
	var hc_series = [];

	$.each(data,function(idx,series){
		var series_data = []
		$.each(series.data,function(idx,values){
			var date = QAUtils.parse_iso8601_date(values[0]).getTime();
			series_data.push([date,values[1]]);
		});

		hc_series.push({
			name:series.unit.name+" " +series.test.name,
			data:series_data,
			showInLegend:true
		});
	});
	return hc_series;
}

function create_control_chart(){
	$("#control-chart-container img").remove();
	$("#control-chart-container").append("<img/>");

	$("#control-chart-container").append('<div class="please-wait"><em>Please wait for control chart to be generated...this could take a few minutes.</em></div>');

	waiting_timeout = setInterval("check_cc_loaded()",250);
	var chart_src_url = get_control_chart_url();
	$("#control-chart-container img").attr("src",chart_src_url);

	retrieve_data(update_data_table);

}

function start_chart_update(){
	$("#gen-chart").button("loading");
}

function finished_chart_update(){
	$("#gen-chart").button("reset");
}

function get_data_filters(){
	var filters = {
		units:get_selected_option_vals("#unit"),
		statuses:get_selected_option_vals("#status"),
		from_date:get_date("#from-date"),
		to_date:get_date("#to-date"),
		tests:get_selected_tests(),
		n_baseline_subgroups:$("#n-baseline-subgroups").val(),
		subgroup_size:$("#subgroup-size").val(),
		fit_data:$("#include-fit").is(":checked")
	};

	return filters;
}

function get_date(date_id){
	return $(date_id).val();


}
function get_selected_tests(){
	return get_checked("#test");
	var tests = [];
	$("input.test:checked").each(function(){
		tests.push($(this).val());
	});
	return tests;
}

function update_data_table(data){

	$("#data-table-wrapper").html(data.table);
}



/**************************************************************************/
$(document).ready(function(){
	$.when(QAUtils.init()).done(function(){
		initialize_charts();

		hide_all_tests();

		$("#control-chart-container, #instructions").hide();

		$("#chart-type").change(switch_chart_type);

		$("#test-list-filters select, #frequency input, #test-list-container input").change(update_tests);

		$("#gen-chart").click(update_chart);
		$("#display-options input").change(update_chart);

	    $("#toggle-instructions").click(toggle_instructions);

		update_tests();

	});
});
