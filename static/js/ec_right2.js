var ec_right2 = echarts.init(document.getElementById("r2"), "dark");

var datamessage = [];
var option_right2 = {
	title: {
		text: "今日微博热搜",
		textStyle: {
			color: 'white'
		},
		left: 'center'
	},
	tooltip: {
		show: false
	},
	series: [{
		type: 'wordCloud',
		gridSize: 10,
		sizeRange: [10, 60], //文字范围
		//文本旋转范围，文本将通过rotationStep45在[-90,90]范围内随机旋转
		rotationRange: [-45, 0, 45, 90],
		// rotationStep: 45,
		// textRotation: [0, 45, 90, -45],
		// //形状
		// shape: 'circle',
		textStyle: {
			normal: {
				color: function() { //文字颜色的随机色
					// return 'rgb(' + [
					// 	Math.round(Math.random() * 250),
					// 	Math.round(Math.random() * 250),
					// 	Math.round(Math.random() * 250)
					// ].join(',') + ')';
					return 'rgb(' +
						Math.round(Math.random() * 255) +
						',' + Math.round(Math.random() * 255) +
						',' + Math.round(Math.random() * 255) + ')'
				}
			}
		},

		data: datamessage
	}]
};
//使用制定的配置项和数据显示图表
ec_right2.setOption(option_right2);
